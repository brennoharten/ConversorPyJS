from typing import List, Tuple

# Define as constantes para representar cada tipo de nó na árvore de sintaxe
class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class BinaryOperatorNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

# Define a classe Parser para fazer a análise sintática
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def parse(self):
        statements = []
        while self.posicao < len(self.tokens):
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            else:
                print(f"Erro de sintaxe na posição {self.posicao}")
                break
        return ProgramNode(statements)

    def parse_statement(self):
        # Tenta analisar a instrução como uma atribuição
        assignment = self.parse_assignment()
        if assignment:
            return assignment

        # Tenta analisar a instrução como uma expressão
        expression = self.parse_expression()
        if expression:
            return expression

        # Se não houver correspondência, retorna None
        return None

    def parse_assignment(self):
        identifier = self.parse_identifier()
        if identifier and self.current_token_type() == "ASSIGN":
            self.advance()
            expression = self.parse_expression()
            if expression:
                return AssignmentNode(identifier, expression)
        self.rollback()
        return None

    def parse_expression(self):
        left = self.parse_term()
        if left:
            while True:
                operator = self.parse_operator()
                if not operator:
                    break
                right = self.parse_term()
                if not right:
                    break
                left = BinaryOperatorNode(left, operator, right)
            return left
        self.rollback()
        return None

    def parse_term(self):
        number = self.parse_number()
        if number:
            return number

        identifier = self.parse_identifier()
        if identifier:
            return IdentifierNode(identifier)

        if self.current_token_type() == "LPAREN":
            self.advance()
            expression = self.parse_expression()
            if expression and self.current_token_type() == "RPAREN":
                self.advance()
                return expression
        self.rollback()
        return None

    def parse_identifier(self):
        if self.current_token_type() == "IDENTIFIER":
            self.advance()
            return self.current_token_value()
        return None

    def parse_number(self):
        if self.current_token_type() == "NUMBER":
            self.advance()
            return NumberNode(self.current_token_value())
        return None

    def parse_operator(self):
        if self.current_token_type() in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE"]:
            operator = self.current_token_value()
            self.advance()
            return operator
        return None

    def current_token_type(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao][0]
        return None

    def current_token_value(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao][1]
        return None

    def advance(self):
        self.posicao += 1

    def rollback(self):
        self.posicao -= 1

