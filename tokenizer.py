import re
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


t_spec = [
    [r"on", "on"],
    [r"\s+", None],
    [r"\/\/.*", None],
    [r"\d+", "INT"],
    [r"[a-zA-Z][a-zA-Z0-9]*", "ID"],
    [r'"[^"]*"', "STR"],
    [r"->", "->"],
    [r",", ","],
    [r"\(", "("],
    [r"\)", ")"],
    [r"\{", "{"],
    [r"\}", "}"],
    [r"\:", ":"],
    ]


class Tokenizer:
    def __init__(self, string: str):
        self._string = string
        self._cursor = 0
    
    def has_more_tokens(self) -> bool:
        return self._cursor < len(self._string) 
    
    def get_next_token(self):
        if not self.has_more_tokens():
            return
        
        buffer = self._string[self._cursor:]

        for regex, token_type in t_spec:
            m = re.match(regex, buffer)
            
            if m is None:
                continue
            
            self._cursor += len(m[0])

            if token_type is None:
                return self.get_next_token()

            return Token(type=token_type, value=m[0])

