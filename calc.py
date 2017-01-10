import re
import sys
import math

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

ans = 0

functions = {
    "ans": lambda p: ans,
    "exit": lambda p: sys.exit(0),
    "mean": lambda numbers: float(sum(numbers)) / max(len(numbers), 1),
    "sum": lambda numbers: math.fsum(numbers)
}

tokenDefinitions = [
    Token("number", r"\d+(\.\d+)?"),
    Token("op_add", r"\+"),
    Token("op_sub", r"\-"),
    Token("op_mul", r"\*"),
    Token("op_div", r"\/"),
    Token("op_mod", r"\%"),
    Token("function", r"[a-zA-Z]+"),
    Token("paren_open", r"\("),
    Token("paren_close", r"\)"),
    Token("comma", r"\,"),
    Token("whitespace", r"\s+")
]

grammar = [
    [
        "function",
        "paren_open",
        "expr",
        "paren_close",
        lambda tokens: [
            tokens[0],
            tokens[1],
            Token("params", [tokens[2].value]),
            tokens[3]
        ]
    ],
    [
        "number",
        lambda tokens: [
            Token("expr", float(tokens[0].value))
        ]
    ],
    [
        "expr",
        "paren_open",
        "expr",
        "paren_close",
        lambda tokens: [
            Token("expr", tokens[0].value * tokens[2].value)
        ]
    ],
    [
        "paren_open",
        "expr",
        "paren_close",
        lambda tokens: [
            Token("expr", tokens[1].value)
        ]
    ],
    [
        "expr",
        "op_div",
        "expr",
        lambda tokens: [
            Token("expr", tokens[0].value / tokens[2].value)
        ]
    ],
    [
        "expr",
        "op_mul",
        "expr",
        lambda tokens: [
            Token("expr", tokens[0].value * tokens[2].value)
        ]
    ],
    [
        "expr",
        "op_mod",
        "expr",
        lambda tokens: [
            Token("expr", tokens[0].value % tokens[2].value)
        ]
    ],
    [
        "expr",
        "op_add",
        "expr",
        lambda tokens: [
            Token("expr", tokens[0].value + tokens[2].value)
        ]
    ],
    [
        "expr",
        "op_sub",
        "expr",
        lambda tokens: [
            Token("expr", tokens[0].value - tokens[2].value)
        ]
    ],
    [
        "expr",
        "comma",
        "expr",
        lambda tokens: [
            Token("params", [tokens[0].value, tokens[2].value])
        ]
    ],
    [
        "params",
        "comma",
        "expr",
        lambda tokens: [
            Token("params", tokens[0].value + [tokens[2].value])
        ]
    ],
    [
        "function",
        "paren_open",
        "paren_close",
        lambda tokens: [
            tokens[0],
            tokens[1],
            Token("params", []),
            tokens[2]
        ]
    ],
    [
        "function",
        "paren_open",
        "params",
        "paren_close",
        lambda tokens: [
            Token("expr", functions[tokens[0].value](tokens[2].value))
        ]
    ]
]

def lex (source):

    pointer = 0

    result = []

    while pointer < len(source):
        foundMatch = False
        for token in tokenDefinitions:
            match = re.search(token.value, source[pointer:])
            if match and match.start() == 0:
                if not token.type == "whitespace":
                    result.append(Token(token.type, match.group(0)))
                pointer = pointer + match.end()
                foundMatch = True
                break
        if not foundMatch:
            print source
            print ' ' * pointer + "^"
            print "Unexpected character {0}".format(source[pointer])
            sys.exit(1)
        
    return result

def parse (program):
    while len(program) > 1:
        for node in grammar:
            pointerLen = len(node) - 2
            pointer = 0
            match = False
            while pointer + pointerLen < len(program):
                match = True
                for i in range(0, pointerLen + 1):
                    if not program[pointer + i].type == node[i]:
                        match = False
                if match:
                    newTokens = node[len(node) - 1](program[pointer: pointer + pointerLen + 1])
                    program = program[:pointer] + newTokens + program[pointer + pointerLen + 1:]
                    break
                else:
                    pointer += 1
            if match:
                break
            
    
    if program[0].type == "expr":
        return float(program[0].value)

    return False

if (len(sys.argv) > 1):
    for i in range(1, len(sys.argv)):
        program = lex(sys.argv[i])
        ans = parse(program)
        print ans
else:
    while True:
        source = raw_input("> ")
        program = lex(source)
        ans = parse(program)
        print ans
