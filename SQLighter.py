# -*- coding: utf-8
import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """получаем номер строки"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM questions').fetchall()

    def select_single(self, rownum):
        """получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM questions WHERE id = ?', (rownum,)).fetchall()

    def count_rows(self):
        """считаем количество строк"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM questions').fetchall()
            return len(result)


    def close(self):
        self.connection.close()
        
