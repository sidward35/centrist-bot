import sys
import sqlite3
import codecs
import re
from random import randint

SENTENCE_SEPARATOR = '.'
WORD_SEPARATOR = ' '

def parseGen(args):
	usage = 'Usage: %s (parse <name> <depth> <path to txt file>|gen <name> <count>)' % (args[0], )

	if (len(args) < 3):
		raise ValueError(usage)

	mode  = args[1]
	name  = args[2]
	
	if mode == 'parse':
		if (len(args) != 5):
			raise ValueError(usage)
		
		depth = int(args[3])
		file_name = args[4]
		
		db = Db(sqlite3.connect(name + '.db'), Sql())
		db.setup(depth)
		
		txt = codecs.open(file_name, 'r', 'utf-8').read()
		Parser(name, db, SENTENCE_SEPARATOR, WORD_SEPARATOR).parse(txt)
	
	elif mode == 'gen':
		output = []
		count = int(args[3])
		db = Db(sqlite3.connect(name + '.db'), Sql())
		generator = Generator(name, db, Rnd())
		for i in range(0, count):
			output.append(generator.generate(WORD_SEPARATOR))
		return output
	
	else:
		raise ValueError(usage)


class Db:
	DEPTH_PARAM_NAME = 'depth'
	
	def __init__(self, conn, sql):
		self.conn   = conn 
		self.cursor = conn.cursor()
		self.sql    = sql
		self.depth  = None

	def setup(self, depth):
		self.depth = depth
		self.cursor.execute(self.sql.create_word_table_sql(depth))
		self.cursor.execute(self.sql.create_index_sql(depth))
		self.cursor.execute(self.sql.create_param_table_sql())
		self.cursor.execute(self.sql.set_param_sql(), (self.DEPTH_PARAM_NAME, depth))

	def _get_word_list_count(self, word_list):
		if len(word_list) != self.get_depth():
			raise ValueError('Expected %s words in list but found %s' % (self.get_depth(), len(word_list)))

		self.cursor.execute(self.sql.select_count_for_words_sql(self.get_depth()), word_list)
		r = self.cursor.fetchone()
		if r:
			return r[0]
		else:
			return 0

	def get_depth(self):
		if self.depth == None:
			self.cursor.execute(self.sql.get_param_sql(), (self.DEPTH_PARAM_NAME,))
			r = self.cursor.fetchone()
			if r:
				self.depth = int(r[0])
			else:
				raise ValueError('No depth value found in database, db does not seem to have been created by this utility')
			
		return self.depth
		
	def add_word(self, word_list):
		count = self._get_word_list_count(word_list)
		if count:
			self.cursor.execute(self.sql.update_count_for_words_sql(self.get_depth()), [count + 1] + word_list)
		else:
			self.cursor.execute(self.sql.insert_row_for_words_sql(self.get_depth()), word_list + [1])

	def commit(self):
		self.conn.commit()

	def get_word_count(self, word_list):
		counts = {}
		sql = self.sql.select_words_and_counts_sql(self.get_depth())
		for row in self.cursor.execute(sql, word_list):
			counts[row[0]] = row[1]

		return counts


class Generator:
	def __init__(self, name, db, rnd):
		self.name = name
		self.db   = db
		self.rnd  = rnd

	def _get_next_word(self, word_list):
		candidate_words = self.db.get_word_count(word_list)
		total_next_words = sum(candidate_words.values())
		i = self.rnd.randint(total_next_words)
		t=0
		for w in candidate_words.keys():
			t += candidate_words[w]
			if (i <= t):
				return w
		assert False

	def generate(self, word_separator):
		depth = self.db.get_depth()
		sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1)
		end_symbol = [Parser.SENTENCE_END_SYMBOL] * (depth - 1)

		while True:
			tail = sentence[(-depth+1):]
			if tail == end_symbol:
				break
			word = self._get_next_word(tail)
			sentence.append(word)
		
		return word_separator.join(sentence[depth-1:][:1-depth])


class Parser:
	SENTENCE_START_SYMBOL = '^'
	SENTENCE_END_SYMBOL = '$'

	def __init__(self, name, db, sentence_split_char = '\n', word_split_char = ''):
		self.name = name
		self.db   = db
		self.sentence_split_char = sentence_split_char
		self.word_split_char = word_split_char
		self.whitespace_regex = re.compile('\s+')

	def parse(self, txt):
		depth = self.db.get_depth()
		sentences = txt.split(self.sentence_split_char)
		i = 0

		for sentence in sentences:
			sentence = self.whitespace_regex.sub(" ", sentence).strip()

			list_of_words = None
			if self.word_split_char:
				list_of_words = sentence.split(self.word_split_char)
			else:
				list_of_words = list(sentence.lower())

			words = [Parser.SENTENCE_START_SYMBOL] * (depth - 1) + list_of_words + [Parser.SENTENCE_END_SYMBOL] * (depth - 1)
			
			for n in range(0, len(words) - depth + 1):
				self.db.add_word(words[n:n+depth])

			i += 1
			if i % 1000 == 0:
				print(i)
				sys.stdout.flush()

		self.db.commit()


class Rnd:
    def randint(self, maxint):
        return randint(1, maxint)


class Sql:
    WORD_COL_NAME_PREFIX = 'word'
    COUNT_COL_NAME       = 'count'
    WORD_TABLE_NAME      = 'word'
    INDEX_NAME           = 'i_word'
    PARAM_TABLE_NAME     = 'param'
    KEY_COL_NAME         = 'name'
    VAL_COL_NAME         = 'value'
    
    def _check_column_count(self, count):
        if count < 2:
            raise ValueError('Invalid column_count value, must be >= 2')
        
    def _make_column_name_list(self, column_count):
        return ', '.join([self.WORD_COL_NAME_PREFIX + str(n) for n in range(1, column_count + 1)])
        
    def _make_column_names_and_placeholders(self, column_count):
        return ' AND '.join(['%s%s=?' % (self.WORD_COL_NAME_PREFIX, n) for n in range(1, column_count + 1)])

    def create_word_table_sql(self, column_count):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.WORD_TABLE_NAME, self._make_column_name_list(column_count), self.COUNT_COL_NAME)
    
    def create_param_table_sql(self):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.PARAM_TABLE_NAME, self.KEY_COL_NAME, self.VAL_COL_NAME)
    
    def set_param_sql(self):
        return 'INSERT INTO %s (%s, %s) VALUES (?, ?)' % (self.PARAM_TABLE_NAME, self.KEY_COL_NAME, self.VAL_COL_NAME)
    
    def get_param_sql(self):
        return 'SELECT %s FROM %s WHERE %s=?' % (self.VAL_COL_NAME, self.PARAM_TABLE_NAME, self.KEY_COL_NAME)

    def create_index_sql(self, column_count):
        return 'CREATE INDEX IF NOT EXISTS %s ON %s (%s)' % (self.INDEX_NAME, self.WORD_TABLE_NAME, self._make_column_name_list(column_count))
    
    def select_count_for_words_sql(self, column_count):
        return 'SELECT %s FROM %s WHERE %s' % (self.COUNT_COL_NAME, self.WORD_TABLE_NAME, self._make_column_names_and_placeholders(column_count)) 
    
    def update_count_for_words_sql(self, column_count):
        return 'UPDATE %s SET %s=? WHERE %s' % (self.WORD_TABLE_NAME, self.COUNT_COL_NAME, self._make_column_names_and_placeholders(column_count)) 
    
    def insert_row_for_words_sql(self, column_count):
        columns = self._make_column_name_list(column_count) + ', ' + self.COUNT_COL_NAME
        values  = ', '.join(['?'] * (column_count + 1))
        
        return 'INSERT INTO %s (%s) VALUES (%s)' % (self.WORD_TABLE_NAME, columns, values) 
    
    def select_words_and_counts_sql(self, column_count):
        last_word_col_name = self.WORD_COL_NAME_PREFIX + str(column_count)
        
        return 'SELECT %s, %s FROM %s WHERE %s' % (last_word_col_name, self.COUNT_COL_NAME, self.WORD_TABLE_NAME, self._make_column_names_and_placeholders(column_count - 1))
    
    def delete_words_sql(self):
        return 'DELETE FROM ' + self.WORD_TABLE_NAME