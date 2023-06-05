from tokenizer import TokenType
from codeGenerator import CodeGenerator

class Parser:
    def __init__(self, tokens):
        self.code_generator = CodeGenerator()
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = None
        self.indent_level = 0
        self.js_code = ""
        self.next = False

    def parse(self):
        self.advance()
        while self.current_token and self.current_token != None :
            if self.current_token.type == TokenType.NEWLINE:
                self.consume(TokenType.NEWLINE)
                self.js_code += "\n"
            elif self.current_token.type == TokenType.WHITESPACE:
                self.js_code += self.consume(TokenType.WHITESPACE)
            elif self.current_token.type == TokenType.IDENTIFIER:
                self.js_code += self.parse_assignment_statement()
            elif self.current_token.type == TokenType.KEYWORD:
                if self.current_token.value == 'if':
                    self.parse_if_statement()
                elif self.current_token.value == 'while':
                    self.js_code += self.parse_while_loop()
                elif self.current_token.value == 'for':
                    self.js_code += self.parse_for_loop()
                elif self.current_token.value == 'print':
                    self.js_code += self.parse_print_statement()
                elif self.current_token.value == 'return':
                    self.js_code += self.parse_return_statement()
                else:
                    self.error(f"Invalid keyword: {self.current_token.value}")
            elif self.current_token.value == 'def':
                self.js_code += self.parse_function_definition()
            elif self.current_token.type == TokenType.FUNCTION:
                self.js_code += self.parse_function_call()
            else:
                self.error(f"Unexpected token: {self.current_token.type}")
        return self.js_code

    #_________________________________________________________

    def error(self, message):
        raise SyntaxError(message)

    def advance(self):
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
            self.current_token_index += 1
        else:
            self.current_token = None

    def consume(self, expected_type):
        if self.current_token.type == expected_type and self.current_token.type != None:
            self.advance()
        else:
            self.error(f"Expected token type {expected_type}, but found {self.current_token.type}")

    def parse_block(self):
        self.consume(TokenType.COLON)  # Consumir o token ':'
        
        self.indent_level += 1  # Aumentar o nível de indentação
        self.parse()
        self.indent_level -= 1  # Reduzir o nível de indentação

    def parse_print_statement(self):
        self.consume(TokenType.KEYWORD)
        expression = self.parse_expression()
        # Generate JavaScript code for print statement using 'expression'
        return self.code_generator.generate_js_code_for_print(expression)
    
    def parse_function_call(self):
        function_name = self.current_token.value
        self.consume(TokenType.FUNCTION)
        self.consume(TokenType.LPAREN)

        # Parse os argumentos da função
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            argument = self.parse_expression()
            arguments.append(argument)
            while self.current_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
                argument = self.parse_expression()
                arguments.append(argument)

        self.consume(TokenType.RPAREN)

        # Gerar código JavaScript para a chamada da função
        return self.code_generator.generate_js_code_for_function_call(function_name, arguments)


    def parse_return_statement(self):
        self.consume(TokenType.KEYWORD)
        expression = self.parse_expression()
        # Generate JavaScript code for return statement using 'expression'
        return self.code_generator.generate_js_code_for_return(expression)


    def parse_assignment_statement(self):
        identifier = self.current_token.value
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGNMENT)
        expression = self.parse_expression()
        # Gerar código de atribuição em JavaScript usando 'identifier' e 'expression'
        return self.code_generator.generate_js_code_for_assignment(identifier, expression)

    def parse_if_statement(self):
        self.consume(TokenType.KEYWORD)
        condition = self.parse_expression()
        #self.consume(TokenType.COLON)
        # Generate JavaScript code for 'if' structure using 'condition'
        self.js_code += self.code_generator.generate_js_code_for_if_structure(condition)
        #self.consume(TokenType.NEWLINE)

        # Parse the 'if' block
        self.parse_block()

        # Check for 'else' statement
        if self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'else':
            self.consume(TokenType.KEYWORD)
            self.consume(TokenType.COLON)

            # Generate JavaScript code for 'else' block
            self.js_code += self.code_generator.generate_js_code_for_else_block()
            self.consume(TokenType.NEWLINE)

            self.parse_block()

        # Close the 'if' structure
        self.js_code += self.code_generator.generate_js_code_for_close_if_structure()

    def parse_while_loop(self):
        self.consume(TokenType.KEYWORD)
        condition = self.parse_expression()
        self.consume(TokenType.COLON)
        self.js_code += f"while ({condition}) "  # Gerar código JavaScript para o loop 'while'
        self.parse_block()

    def parse_for_loop(self):
        self.consume(TokenType.KEYWORD)
        identifier = self.current_token.value
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.IN)
        iterable = self.parse_expression()
        self.consume(TokenType.COLON)
        self.js_code += f"for (let {identifier} of {iterable}) "  # Gerar código JavaScript para o loop 'for'
        self.parse_block()


    def parse_expression(self):
        return self.parse_logical_expression()

    def parse_logical_expression(self):
        left = self.parse_equality_expression()
        if self.current_token and self.current_token.type != TokenType.LOGICAL_OPERATOR or self.next == True or self.current_token == None:
            return self.code_generator.generate_js_code_for_number(left)
        else:
            while self.current_token and self.current_token.type == TokenType.LOGICAL_OPERATOR:
                operator = self.current_token.value
                self.consume(TokenType.LOGICAL_OPERATOR)
                right = self.parse_equality_expression()
                # Gerar código JavaScript para a expressão lógica usando 'left', 'operator' e 'right'
                # Atualizar 'left' com o resultado da expressão lógica para análise posterior
                return self.code_generator.generate_js_code_for_expression(left, operator, right)

    def parse_equality_expression(self):
        left = self.parse_relational_expression()
        if self.current_token and self.current_token.type != TokenType.EQUALITY or self.next == True or self.current_token == None:
            return self.code_generator.generate_js_code_for_number(left)
        else:
            while self.current_token and self.current_token.type == TokenType.EQUALITY:
                operator = self.current_token.value
                self.consume(TokenType.EQUALITY)
                right = self.parse_relational_expression()
                # Gerar código JavaScript para a expressão de igualdade usando 'left', 'operator' e 'right'
                # Atualizar 'left' com o resultado da expressão de igualdade para análise posterior
                return self.code_generator.generate_js_code_for_expression(left, operator, right)

    def parse_relational_expression(self):
        left = self.parse_additive_expression()
        if self.current_token and self.current_token.type != TokenType.RELATIONAL or self.next == True or self.current_token == None:
            return self.code_generator.generate_js_code_for_number(left)
        else:
            while self.current_token and self.current_token.type == TokenType.RELATIONAL:
                operator = self.current_token.value
                self.consume(TokenType.RELATIONAL)
                right = self.parse_additive_expression()
                # Gerar código JavaScript para a expressão relacional usando 'left', 'operator' e 'right'
                # Atualizar 'left' com o resultado da expressão relacional para análise posterior
                return self.code_generator.generate_js_code_for_expression(left, operator, right)

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        if self.current_token and self.current_token.type != TokenType.OPERATOR or self.next == True or self.current_token == None:
            return self.code_generator.generate_js_code_for_number(left)
        else:
            while self.current_token and self.current_token.type == TokenType.OPERATOR:
                operator = self.current_token.value
                self.consume(TokenType.OPERATOR)
                right = self.parse_multiplicative_expression()
                # Gerar código JavaScript para a expressão aditiva usando 'left', 'operator' e 'right'
                # Atualizar 'left' com o resultado da expressão aditiva para análise posterior
                return self.code_generator.generate_js_code_for_expression(left, operator, right)

    def parse_multiplicative_expression(self):
        left = self.parse_primary_expression()
        if self.current_token and self.current_token.type != TokenType.OPERATOR or self.next == True or self.current_token == None:
            return self.code_generator.generate_js_code_for_number(left)
        else:
            while self.current_token and self.current_token.type == TokenType.OPERATOR:
                operator = self.current_token.value
                self.consume(TokenType.OPERATOR)
                right = self.parse_primary_expression()
                # Gerar código JavaScript para a expressão multiplicativa usando 'left', 'operator' e 'right'
                # Atualizar 'left' com o resultado da expressão multiplicativa para análise posterior
                return self.code_generator.generate_js_code_for_expression(left, operator, right)

    def parse_primary_expression(self):
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.consume(TokenType.NUMBER)
            # Gerar código JavaScript para um número
            return self.code_generator.generate_js_code_for_number(value)
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.consume(TokenType.STRING)
            # Gerar código JavaScript para uma string
            return self.code_generator.generate_js_code_for_string(value)
        elif self.current_token.type == TokenType.BOOLEAN:
            value = self.current_token.value
            self.consume(TokenType.BOOLEAN)
            # Gerar código JavaScript para um booleano
            return self.code_generator.generate_js_code_for_boolean(value)
        elif self.current_token.type == TokenType.IDENTIFIER:
            identifier = self.current_token.value
            self.consume(TokenType.IDENTIFIER)
            # Gerar código JavaScript para um identificador
            return self.code_generator.generate_js_code_for_identifier(identifier)
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expression = self.parse_expression()
            self.consume(TokenType.RPAREN)
            # Gerar código JavaScript para uma expressão entre parênteses
            self.next = True
            return self.code_generator.generate_js_code_for_parenthesized_expression(expression)
        elif self.current_token.type == TokenType.FUNCTION:
            return self.parse_function_call()


        else:
            raise SyntaxError(f"Invalid expression: {self.current_token.value}")
        
    def parse_function_definition(self):
        self.consume(TokenType.FUNCTION)
        function_name = self.current_token.value
        self.consume(TokenType.FUNCTION)
        self.consume(TokenType.LPAREN)

        # Parse os parâmetros da função
        parameters = []
        if self.current_token.type == TokenType.IDENTIFIER:
            parameters.append(self.current_token.value)
            self.consume(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
                if self.current_token.type == TokenType.IDENTIFIER:
                    parameters.append(self.current_token.value)
                    self.consume(TokenType.IDENTIFIER)
                else:
                    self.error("Invalid parameter")
        self.consume(TokenType.RPAREN)
        self.parse_block()
        # Gerar código JavaScript para a definição da função
        return self.code_generator.generate_js_code_for_function_declaration(function_name, parameters, self.js_code)
    

