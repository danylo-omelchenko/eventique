from typing import Any
from typing import Union
from typing import List
from dataclasses import dataclass

from tokenizer import Tokenizer
"""

on Start -> ( 
    Print{text: "Hello world"},
    Prompt{text: "Your name: "}
)

on Input{text: x} -> Print{text: x}

////////

program = [ws], {on_statement, [ws]};

on_statement = on, [ws], then, [ws], emit;

then = "->";

on = "on", ws, message;

emit = message
     | "(", [ws], (message | messages), [ws], ")";

messages = message, {[ws], ",", [ws], message};

ws = {" ", "\t", "\n"};

message = identifier
        | identifier, [ws], message_body;

message_body = "{", [ws], (field | fields), [ws], "}";

field = identifier, [ws], ":", [ws], (literal|identifier);

fields = field, {[ws], ",", [ws], field};

identifier = r"[a-zA-Z]+";

literal = str_literal
        | int_literal;

int_literal = r"\d+";

str_literal = r"\".*\"";

"""




@dataclass
class StrLiteral:
    value: str


@dataclass
class IntLiteral:
    value: int


@dataclass
class Identifier:
    name: str


@dataclass
class Variable:
    name: str


@dataclass 
class Field:
    name: Identifier
    value: Union[Identifier, IntLiteral, StrLiteral]


@dataclass
class Message:
    name: Identifier
    fields: List[Field]


@dataclass
class OnStatement:
    left: Message 
    right: List[Message]


@dataclass
class Program:
    statements: List[OnStatement]


class Parser:
    def parse(self, string: str) -> Program:
        self._string = string
        self._tokenizer = Tokenizer(self._string)
        
        self._lookahead = self._tokenizer.get_next_token()

        return self.program()

    def program(self) -> Program:
        return Program(self.on_statement_list())
    
    def on_statement_list(self) -> List[OnStatement]:
        statements = [self.on_statement()]

        while self._lookahead is not None:
            statements.append(self.on_statement())

        return statements

    def on_statement(self) -> OnStatement:
        self._eat("on")
        left = self.message()
        self._eat("->")
        
        if self._lookahead.type == "(":
            self._eat("(")
            right = self.message_list()
            self._eat(")")
        else:
            right = [self.message()]
        return OnStatement(left=left, right=right)
    
    def message(self) -> Message:
        name = self.identifier()
        self._eat("{")
        if self._lookahead.type != "}":
            fields = self.fields_list()
        else:
            fields = []
        self._eat("}")
        return Message(name, fields)
    
    def fields_list(self) -> List[Field]:
        fields = [self.field()]
        while self._lookahead.type != "}":
            self._eat(",")
            fields.append(self.field())

        return fields

    def field(self) -> Field:
        name = self.identifier()
        self._eat(":")
        value = self.literal()
        return Field(name, value)

    def message_list(self) -> List[Message]:
        messages = [self.message()]

        while self._lookahead.type != ")":
            self._eat(",")
            messages.append(self.message())
        
        return messages

    def literal(self):
        match self._lookahead.type:
            case "INT": 
                return self.int_literal()
            case "STR":
                return self.str_literal()
            case "ID":
                return self.variable()
            case _:
                raise SyntaxError("unexpected literal")

    def str_literal(self) -> StrLiteral:
        token = self._eat("STR")
        return StrLiteral(token.value[1:-1])
    
    def variable(self) -> Variable:
        token = self._eat("ID")
        return Variable(token.value)

    def identifier(self) -> Identifier:
        token = self._eat("ID")
        return Identifier(token.value)
    
    def int_literal(self) -> IntLiteral:
        token = self._eat("INT")
        return IntLiteral(int(token.value))

    def _eat(self, type):
        token = self._lookahead

        if token is None:
            raise SyntaxError(f"unexpected end of input, expected token of type {type}")
        
        if token.type != type:
            raise SyntaxError(f"unexpected token {token.value}")
        
        self._lookahead = self._tokenizer.get_next_token()

        return token

