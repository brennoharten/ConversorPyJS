from enum import Enum

class NodeType(Enum):
    LITERAL = 0
    IDENTIFIER = 1
    UNARY_OPERATION = 2
    BINARY_OPERATION = 3
    TERNARY_OPERATION = 4
    FUNCTION_CALL = 5
    IF = 6
    WHILE = 7
    FOR = 8
    OPERATOR = 9



class TokenType:
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMA = ","
    LOGICAL_OPERATOR = "LOGICAL_OPERATOR"
    LBRACE = "{"
    RBRACE = "}"
    RBRACKET = "]"
    LBRACKET = "["
    RPAREN = ")"
    LPAREN = "("
    RELATIONAL = "RELATIONAL"
    ASSIGNMENT = "ASSIGNMENT"
    EQUALITY = "EQUALITY"
    OPERATOR = "OPERATOR"
    IDENTIFIER = "IDENTIFIER"
    FUNCTION = "FUNCTION"
    KEYWORD = "KEYWORD"
    STRING = "STRING"
    NUMBER = "NUMBER"
    
    
class ASTNode:
    def __init__(self, node_type, value=None, left_child=None, right_child=None):
        self.type = node_type
        self.value = value
        self.left_child = left_child
        self.right_child = right_child



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse_expression(self):
        tokens = self.tokens
        # Identificação de operadores e operandos
        precedence = {
            "**": 4,
            "*": 3,
            "/": 3,
            "+": 2,
            "-": 2,
            "<": 1,
            ">": 1,
            "<=": 1,
            ">=": 1,
            "==": 0,
            "!=": 0,
            "and": -1,
            "or": -2
        }
        
        # Construção da árvore de sintaxe usando uma pilha
        output_queue = []
        operator_stack = []
        for token in tokens:
            if token[0] == TokenType.WHITESPACE or token[0] == TokenType.NEWLINE:
                continue
            elif token[0] == TokenType.NUMBER or token[0] == TokenType.STRING or token[0] == TokenType.IDENTIFIER:
                output_queue.append(token)
            elif token[0] == TokenType.FUNCTION or token[0] == TokenType.KEYWORD:
                operator_stack.append(token)
            elif token[0] == TokenType.OPERATOR or token[0] == TokenType.LOGICAL_OPERATOR or token[0] == TokenType.RELATIONAL or token[0] == TokenType.ASSIGNMENT or token[0] == TokenType.EQUALITY:
                while len(operator_stack) > 0 and operator_stack[-1][0] in [TokenType.OPERATOR, TokenType.LOGICAL_OPERATOR, TokenType.RELATIONAL, TokenType.ASSIGNMENT, TokenType.EQUALITY]:
                    if precedence[token[1]] < precedence[operator_stack[-1][1]]:
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token[0] == TokenType.LPAREN or token[0] == TokenType.LBRACKET or token[0] == TokenType.LBRACE:
                operator_stack.append(token)
            elif token[0] == TokenType.RPAREN or token[0] == TokenType.RBRACKET or token[0] == TokenType.RBRACE:
                while len(operator_stack) > 0 and operator_stack[-1][0] != TokenType.LPAREN and operator_stack[-1][0] != TokenType.LBRACKET and operator_stack[-1][0] != TokenType.LBRACE:
                    output_queue.append(operator_stack.pop())
                if len(operator_stack) == 0:
                    raise SyntaxError("Mismatched parentheses/brackets/braces")
                operator_stack.pop()
                if len(operator_stack) > 0 and operator_stack[-1][0] == TokenType.FUNCTION:
                    output_queue.append(operator_stack.pop())

        while len(operator_stack) > 0:
            if operator_stack[-1][0] == TokenType.LPAREN or operator_stack[-1][0] == TokenType.RPAREN or operator_stack[-1][0] == TokenType.LBRACKET or operator_stack[-1][0] == TokenType.RBRACKET or operator_stack[-1][0] == TokenType.LBRACE or operator_stack[-1][0] == TokenType.RBRACE:
                raise SyntaxError("Mismatched parentheses/brackets/braces")
            output_queue.append(operator_stack.pop())

        # Adição dos nós de operador e operando à árvore de sintaxe
        node_stack = []
        for token in output_queue:
            if token[0] == TokenType.NUMBER or token[0] == TokenType.STRING:
                node_stack.append(ASTNode(NodeType.LITERAL, token[1]))
            elif token[0] == TokenType.IDENTIFIER:
                node_stack.append(ASTNode(NodeType.IDENTIFIER, token[1]))
            elif token[0] == TokenType.OPERATOR or token[0] == TokenType.LOGICAL_OPERATOR or token[0] == TokenType.RELATIONAL or token[0] == TokenType.ASSIGNMENT or token[0] ==TokenType.EQUALITY:
                right = node_stack.pop()
                left = node_stack.pop()
                node_stack.append(ASTNode(NodeType.OPERATOR, token[1], left, right))

            elif token[0] == TokenType.FUNCTION:
                args = []
                while len(node_stack) > 0 and node_stack[-1].type != NodeType.FUNCTION_CALL:
                    args.insert(0, node_stack.pop())
                    if len(node_stack) == 0:
                        raise SyntaxError("Function call without function name")
                    function_name = node_stack.pop().value
                    node_stack.append(ASTNode(NodeType.FUNCTION_CALL, function_name, *args))

            elif token[0] == TokenType.KEYWORD:
                if token[1] == "if":
                    condition = node_stack.pop()
                    if_body = node_stack.pop()
                    else_body = None
                if len(node_stack) > 0 and node_stack[-1].type == NodeType.KEYWORD and node_stack[-1].value == "else":
                    node_stack.pop()
                    else_body = node_stack.pop()
                    node_stack.append(ASTNode(NodeType.IF, condition, if_body, else_body))
                elif token[1] == "while":
                    condition = node_stack.pop()
                    body = node_stack.pop()
                    node_stack.append(ASTNode(NodeType.WHILE, condition, body))
                elif token[1] == "for":
                    step = None
                    stop = node_stack.pop()
                    start = node_stack.pop()
                if len(node_stack) > 0 and node_stack[-1].type == NodeType.LITERAL:
                    step = node_stack.pop()
                    body = node_stack.pop()
                    node_stack.append(ASTNode(NodeType.FOR, start, stop, step, body))

            if len(node_stack) != 1:
                raise SyntaxError("Invalid expression")

            return node_stack.pop()

