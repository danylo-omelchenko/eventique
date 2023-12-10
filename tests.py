import unittest

from parser import Parser
from parser import Program, OnStatement, Message, Identifier, Field, StrLiteral, IntLiteral, Variable


class TestParser(unittest.TestCase):
    def test_single_statement(self):
        p = Parser()
        input = """
        on Start{} -> Exit{}
        """
        ast = p.parse(input)
        expected_ast = Program(
            [
                OnStatement(
                    left=Message(Identifier('Start'), fields=[]),
                    right=[Message(Identifier("Exit"), fields=[])])
            ]
        )
        self.assertEqual(expected_ast, ast)

    def test_single_statement_multiple_emits(self):
        p = Parser()
        input = """
        on Start{} -> (
            Print{text: "Hello World"},
            Exit{}
        )
        """
        ast = p.parse(input)
        expected_ast = Program(
            [
                OnStatement(
                    left=Message(Identifier('Start'), fields=[]),
                    right=[
                        Message(
                            Identifier("Print"),
                            fields=[
                               Field(name=Identifier("text"), value=StrLiteral("Hello World"))
                            ]),
                        Message(Identifier("Exit"), fields=[]),
                    ])
            ]
        )
        self.assertEqual(expected_ast, ast)


    def test_multiple_statements(self):
        p = Parser()
        input = """
        on Start{} -> Prompt{text: "Say your name: "}

        on Input{text: name} -> (
            Print{text: "Hello"},
            Print{text: name},
            Exit{}
        )
        """
        ast = p.parse(input)
        expected_ast = Program(
            [
                OnStatement(
                    left=Message(Identifier('Start'), fields=[]),
                    right=[
                        Message(
                            Identifier("Prompt"),
                            fields=[
                               Field(name=Identifier("text"), value=StrLiteral("Say your name: "))
                            ])
                    ]),
                OnStatement(
                    left=Message(Identifier('Input'), fields=[Field(name=Identifier("text"), value=Variable("name"))]),
                    right=[
                        Message(
                            Identifier("Print"),
                            fields=[
                               Field(name=Identifier("text"), value=StrLiteral("Hello"))
                            ]),
                        Message(
                            Identifier("Print"),
                            fields=[
                               Field(name=Identifier("text"), value=Variable("name"))
                            ]),
                        Message(Identifier("Exit"), fields=[]),
                    ])

            ]
        )
        self.assertEqual(expected_ast, ast)


if __name__ == '__main__':
    unittest.main()
