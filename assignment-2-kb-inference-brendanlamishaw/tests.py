import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase

class KBMoreTests(unittest.TestCase):
    def setUp(self):
        # Li Kim Tests
        file = 'statements_kb5.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    def test6(self):
        """this student generated test ensures retract only removes facts and rules that are supported by
        1 or less fact-rule pairs
        """
        r1 = read.parse_input("fact: (dresslike profHammond TonyStark)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (isliterally ?X TonyStark)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : profHammond")
        ask2 = read.parse_input("fact: (resembles profHammond ?Y)")
        print(' Asking if', ask2)
        answer = self.KB.kb_ask(ask2)
        self.assertFalse(answer)

    def test7(self):
        """this student generated test ensures retracting the 2nd fact in the lhs of a rule
        successfully retracts the final inferred fact but re-assertion re-infers the fact
        """
        r1 = read.parse_input("fact: (lookslike profHammond TonyStark)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (resembles profHammond ?Y)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertFalse(answer)
        a1 = read.parse_input("fact: (lookslike profHammond TonyStark)")
        print(' Reasserting', a1)
        self.KB.kb_assert(a1)
        ask2 = read.parse_input("fact: (resembles profHammond ?Y)")
        print(' Asking if', ask2)
        answer = self.KB.kb_ask(ask2)
        self.assertEqual(str(answer[0]), "?Y : TonyStark")

    def test8(self):
        """this student generated test ensures retracting a fact that supports inferences 2 links away
        also retracts all facts down that chain
        """
        r1 = read.parse_input("fact: (techgenius profHammond)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        r2 = read.parse_input("fact: (talkslike profHammond TonyStark)")
        print(' Retracting', r2)
        self.KB.kb_retract(r2)
        ask1 = read.parse_input("fact: (isliterally ?X TonyStark)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertFalse(answer)
        ask2 = read.parse_input("fact: (IronMan ?X)")
        print(' Asking if', ask2)
        answer = self.KB.kb_ask(ask2)
        self.assertFalse(answer)
        ask3 = read.parse_input("fact: (Avenger ?X)")
        print(' Asking if', ask3)
        answer = self.KB.kb_ask(ask3)
        self.assertFalse(answer)


    def test9(self):
        """this student generated test ensures retracting a fact that supports two or more facts or rules
        successfully retracts all inferred facts and rules
        """
        r1 = read.parse_input("fact: (techgenius profHammond)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (employable ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertFalse(answer)
        ask2 = read.parse_input("fact: (smart ?X)")
        print(' Asking if', ask2)
        answer = self.KB.kb_ask(ask2)
        self.assertFalse(answer)

    def test10(self):
        """this student generated test ensures the inference engine is working at a basic level"""
        ask1 = read.parse_input("fact: (Avenger ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : profHammond")
        ask2 = read.parse_input("fact: (smart ?X)")
        print(' Asking if', ask2)
        answer = self.KB.kb_ask(ask2)
        self.assertEqual(str(answer[0]), "?X : profHammond")
        ask3 = read.parse_input("fact: (employable ?X)")
        print(' Asking if', ask3)
        answer = self.KB.kb_ask(ask3)
        self.assertEqual(str(answer[0]), "?X : profHammond")

