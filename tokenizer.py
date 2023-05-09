import re

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
                self.tokens.append(('INTEGER', value))
                self.position = next_char_index

            # Verifica se é uma string
            elif current_char == '"':
                value = ''
                next_char_index = self.position + 1
                while next_char_index < len(self.code) and self.code[next_char_index] != '"':
                    value += self.code[next_char_index]
                    next_char_index += 1
                if next_char_index < len(self.code) and self.code[next_char_index] == '"':
                    self.tokens.append(('STRING', value))
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
                    self.tokens.append(('KEYWORD', value))
                # Verifica se é uma função
                elif value in ('abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'):
                    self.tokens.append(('FUNCTION', value))
                else:
                    self.tokens.append(('IDENTIFIER', value))
                self.position = next_char_index

            # Verifica se é um operador
            elif current_char in '+-*/%':
                self.tokens.append(('OPERATOR', current_char))
                self.position += 1

            # Verifica se é uma expressão de atribuição
            elif current_char == '=':
                if self.position + 1 < len(self.code) and self.code[self.position + 1] == '=':
                    self.tokens.append(('EQUALITY', '=='))
                    self.position += 2
                else:
                    self.tokens.append(('ASSIGNMENT', '='))
                    self.position += 1

            # Verifica se é um operador relacional
            elif current_char in '<>!':
                value = current_char
                next_char_index = self.position + 1
                if next_char_index < len(self.code) and self.code[next_char_index] == '=':
                    self.tokens.append(('RELATIONAL', value + '='))
                    self.position += 2
                else:
                    self.tokens.append(('RELATIONAL', value))
                    self.position += 1

            # Verifica se é um parêntese esquerdo
            elif current_char == '(':
                self.tokens.append(('LPAREN', '('))
                self.position += 1

            # Verifica se é um parêntese direito
            elif current_char == ')':
                self.tokens.append(('RPAREN', ')'))
                self.position += 1

            # Verifica se é um colchete esquerdo
            elif current_char == '[':
                self.tokens.append(('LBRACKET', '['))
                self.position += 1

            # Verifica se é um colchete direito
            elif current_char == ']':
                self.tokens.append(('RBRACKET', ']'))
                self.position += 1

            # Verifica se é uma chave direita
            elif current_char in '}':
                self.tokens.append(('RBRACE', '}'))
                self.position += 1

            # Verifica se é uma chave esquerda
            elif current_char in '}':
                self.tokens.append(('LBRACE', '{'))
                self.position += 1

            # Verifica se é um operador lógico
            elif current_char in '&|':
                value = current_char
                next_char_index = self.position + 1
                if next_char_index < len(self.code) and self.code[next_char_index] == current_char:
                    value += current_char
                    self.tokens.append(('LOGICAL_OPERATOR', value))
                    self.position += 2
                else:
                    raise ValueError(f"Invalid token: {value}")
                
            # Verifica se é uma vírgula
            elif current_char == ',':
                self.tokens.append(('COMMA', ','))
                self.position += 1

            elif current_char == ' ':
                self.tokens.append(('WHITESPACE', ' '))
                self.position += 1

            elif current_char == '\n':
                self.tokens.append(('NEWLINE', ' '))
                self.position += 1

            # Se nenhum dos casos anteriores for satisfeito, verifica se é uma função
            else:
                match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\(', self.code[self.position:])
                if match:
                    function_name = match.group(1)
                    self.tokens.append(('FUNCTION', function_name))
                    self.position += len(function_name)
                else:
                    raise ValueError(f"Bad character: {current_char}")
        
        return self.tokens
            
