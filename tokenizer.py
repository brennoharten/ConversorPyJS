import re
from enum import Enum

class TokenType(Enum):
    NEWLINE = 1
    WHITESPACE = 2
    COMMA = 3
    LOGICAL_OPERATOR = 4
    LBRACE = 5
    RBRACE = 6
    RBRACKET = 7
    LBRACKET = 8
    RPAREN = 9
    LPAREN = 10
    RELATIONAL = 11
    ASSIGNMENT = 12
    EQUALITY = 13
    OPERATOR = 14
    IDENTIFIER = 15
    FUNCTION = 16
    KEYWORD = 17
    STRING = 18
    NUMBER = 19
    BOOLEAN = 20
    COLON = 21

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.code):
            current_char = self.code[self.position]

            # Verifica se é um dígito
            if current_char.isdigit():
                value = current_char
                next_char_index = self.position + 1
                while next_char_index < len(self.code) and self.code[next_char_index].isdigit():
                    value += self.code[next_char_index]
                    next_char_index += 1
                self.tokens.append(Token(TokenType.NUMBER, value))
                self.position = next_char_index

            # Verifica se é uma string
            elif current_char == '"':
                value = ''
                next_char_index = self.position + 1
                while next_char_index < len(self.code) and self.code[next_char_index] != '"':
                    value += self.code[next_char_index]
                    next_char_index += 1
                if next_char_index < len(self.code) and self.code[next_char_index] == '"':
                    self.tokens.append(Token(TokenType.STRING, value))
                    self.position = next_char_index + 1
                else:
                    raise ValueError("Unterminated string")

            # Verifica se é um identificador
            elif current_char.isalpha() or current_char == '_':
                value = current_char
                next_char_index = self.position + 1
                while next_char_index < len(self.code) and (self.code[next_char_index].isalnum() or self.code[next_char_index] == '_'):
                    value += self.code[next_char_index]
                    next_char_index += 1

                # Verifica se é uma palavra-chave
                if value in ('if', 'else', 'while', 'for', 'break', 'continue', 'return', 'print'):
                    self.tokens.append(Token(TokenType.KEYWORD, value))
                # Verifica se é uma função
                elif value in ('abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'):
                    self.tokens.append(Token(TokenType.FUNCTION, value))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, value))
                self.position = next_char_index

            # Verifica se é um operador
            elif current_char in '+-*/%':
                self.tokens.append(Token(TokenType.OPERATOR, current_char))
                self.position += 1

            # Verifica se é uma expressão de atribuição
            elif current_char == '=':
                if self.position + 1 < len(self.code) and self.code[self.position + 1] == '=':
                    self.tokens.append(Token(TokenType.EQUALITY, '=='))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenType.ASSIGNMENT, '='))
                    self.position += 1

            # Verifica se é um operador relacional
            elif current_char in '<>!':
                value = current_char
                next_char_index = self.position + 1
                if next_char_index < len(self.code) and self.code[next_char_index] == '=':
                    self.tokens.append(Token(TokenType.RELATIONAL, value + '='))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenType.RELATIONAL, value))
                    self.position += 1

            # Verifica se é um parêntese esquerdo
            elif current_char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '('))
                self.position += 1

            # Verifica se é um parêntese direito
            elif current_char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')'))
                self.position += 1

            # Verifica se é um colchete esquerdo
            elif current_char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '['))
                self.position += 1

            # Verifica se é um colchete direito
            elif current_char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']'))
                self.position += 1

            # Verifica se é uma chave direita
            elif current_char in '}':
                self.tokens.append(Token(TokenType.RBRACE, '}'))
                self.position += 1

            # Verifica se é uma chave esquerda
            elif current_char in '}':
                self.tokens.append(Token(TokenType.LBRACE, '{'))
                self.position += 1

            elif current_char == '!':
                self.tokens.append(Token(TokenType.BOOLEAN, 'not'))
                self.position += 1
            
            elif current_char in 'TF':
                if current_char == 'T':
                    if self.code[self.position:self.position + 4] == 'True':
                        self.tokens.append(Token(TokenType.BOOLEAN, True))
                        self.position += 4
                    else:
                        raise ValueError("Invalid token: True")
                elif current_char == 'F':
                    if self.code[self.position:self.position + 5] == 'False':
                        self.tokens.append(Token(TokenType.BOOLEAN, False))
                        self.position += 5
                    else:
                        raise ValueError("Invalid token: False")
            
            elif current_char == 'n':
                if self.code[self.position:self.position + 3] == 'not':
                    self.tokens.append(Token(TokenType.LOGICAL_OPERATOR, 'not'))
                    self.position += 3
                else:
                    raise ValueError("Invalid token: 'not'")

            elif current_char == 'a':
                if self.code[self.position:self.position + 3] == 'and':
                    self.tokens.append(Token(TokenType.LOGICAL_OPERATOR, 'and'))
                    self.position += 3
                else:
                    raise ValueError("Invalid token: 'and'")
            
            elif current_char == 'o':
                if self.code[self.position:self.position + 2] == 'or':
                    self.tokens.append(Token(TokenType.LOGICAL_OPERATOR, 'or'))
                    self.position += 2
                else:
                    raise ValueError("Invalid token: 'or'")

            # Verifica se é um operador lógico
            elif current_char in '&|':
                value = current_char
                next_char_index = self.position + 1
                if next_char_index < len(self.code) and self.code[next_char_index] == current_char:
                    value += current_char
                    self.tokens.append(Token(TokenType.LOGICAL_OPERATOR, value))
                    self.position += 2
                else:
                    raise ValueError(f"Invalid token: {value}")
                
            # Verifica se é uma vírgula
            elif current_char == ',':
                self.tokens.append(Token(TokenType.COMMA, ','))
                self.position += 1

            elif current_char == ' ':
                ##self.tokens.append(Token(TokenType.WHITESPACE, ' '))
                self.position += 1

            elif current_char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, ' '))
                self.position += 1
            
            elif current_char == ':':
                self.tokens.append(Token(TokenType.COLON, current_char))
                self.position += 1

            # Se nenhum dos casos anteriores for satisfeito, verifica se é uma função
            else:
                match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\(', self.code[self.position:])
                if match:
                    function_name = match.group(1)
                    self.tokens.append(Token(TokenType.FUNCTION, function_name))
                    self.position += len(function_name)
                else:
                    raise ValueError(f"Bad character: {current_char}")
        
        return self.tokens
            
