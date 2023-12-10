from typing import Union
from typing import List
from typing import Dict
from typing import Callable
from typing import Optional
from collections import deque
from dataclasses import dataclass, field


q = deque()
handlers = list()

@dataclass
class Field:
    name: str
    value: str = ""


@dataclass
class Variable:
    name: str
    value: str 

@dataclass
class Message:
    type: str
    fields: Dict[str, Union[Field, Variable]] = field(default_factory=dict)

    def replace_variables(self, vars: Dict[str, str]):
        for f_name in self.fields.keys():
            if type(self.fields[f_name]) is Variable:
                self.fields[f_name] = Field(f_name, vars[f_name])
    

@dataclass
class EventHandler:
    on: Message
    emit: List[Message] = field(default_factory=list)
    act: Optional[Callable[[Message], None]] = None

    def variables_for_message(self, m: Message):
        return {var.name: m.fields.get(param_name) for param_name, var in self.on.fields.items() if type(var) is Variable}
        


def on(trigger: Message, sequence: List[Message]):
    h.append(EventHandler(trigger, sequence or []))


def startup():
    q.append(Message("Start", { "file": Field("file", "main.py")}))


def find_handler(e: Message):
    for h in handlers:
        if h.on.type == e.type:
            return h

def loop():
    while True:
        if len(q) > 0:
            e = q.popleft()
            h = find_handler(e)
            if h:
                h.act and h.act(e)
                context = e
                for ne in h.emit:
                    
                    vars = h.variables_for_message(e)

                    ne.replace_variables(vars)
                    q.append(ne)
            else:
                q.append(e)
"""
on Start -> ( 
    Print{text: "Hello world"},
    Prompt{text: "Your name: "}
)

on Input{text: x} -> Print{text: x}

"""

handlers = [
        EventHandler(on=Message("Start"), emit=[
            Message("Print", { "text": Field("text", "Hello world")}),
            Message("Prompt"),
            ]),
        
        EventHandler(on=Message("Input", {"text": Variable("text", "x")}), emit=[
            Message("Print", {"text": Variable("text", "x")}),
            Message("Exit"),
            ]),

        # standart
        EventHandler(on=Message("Prompt"), act=lambda e: q.append(Message("Input", {"text": input(e.fields.get("text", "> "))}))),
        EventHandler(on=Message("Print"), act=lambda e: print(e.fields.get("text").value)),
        EventHandler(on=Message("Exit"), act=lambda e: exit())
        ]

startup()
loop()

