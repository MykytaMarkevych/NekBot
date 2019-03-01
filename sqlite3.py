# -*- coding: utf-8
import sqlite3

class SQlighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """получаем номер строки"""
        with self.connection:
                return self.cursor.execute('SELECT * FROM questions').fetchall()

    def select_single(self, rownum):
