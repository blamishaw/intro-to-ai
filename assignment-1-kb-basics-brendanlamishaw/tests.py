import unittest
import platform
import read, copy
from logical_classes import *
from student_code import KnowledgeBase

class KB2Tests(unittest.TestCase):
    def setUp(self):
        # Assert starter facts
        file = 'statements_kb2.txt'
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact):
                self.KB.kb_assert(item)

    def test1(self):
        ask1 = read.parse_input("fact: (attacked Ai Nosliw)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(answer[0].bindings, [])

    def test2(self):
        ask1 = read.parse_input("fact: (diamonds ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : Loot")

    def test3(self):
        ask1 = read.parse_input("fact: (rubies gem)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertFalse(answer)










