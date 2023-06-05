class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.indentation = '    '  # 4 spaces for each level of indentation

    def generate_js_code_for_print(self, expression):
        return f'console.log{expression};'

    def generate_js_code_for_return(self, expression):
        return f'return {expression};'

    def generate_js_code_for_assignment(self, identifier, expression):
        return f'var {identifier} = {expression};'

    def generate_js_code_for_if_structure(self, condition):
        return f'if ({condition}) {{'

    def generate_js_code_for_else_block(self):
        return 'else {'

    def generate_js_code_for_close_if_structure(self):
        return '}'

    def generate_js_code_for_expression(self, left, operator, right):
        return f'{left} {operator} {right}'

    def generate_js_code_for_number(self, value):
        return value

    def generate_js_code_for_string(self, value):
        return f'"{value}"'

    def generate_js_code_for_boolean(self, value):
        return value.lower()

    def generate_js_code_for_identifier(self, identifier):
        return identifier

    def generate_js_code_for_parenthesized_expression(self, expression):
        return f'({expression})'
    
    def generate_js_code_for_function_declaration(self, function_name, parameters, block_code):
        parameters_str = ', '.join(parameters)
        function_declaration = f"function {function_name}({parameters_str}) {{\n"
        function_declaration += block_code
        function_declaration += "}\n\n"
        return function_declaration
    
    def generate_js_code_for_while_loop(self, condition):
        return f'while ({condition}) {{'

    def generate_js_code_for_for_loop(self, identifier, iterable):
        return f'for (let {identifier} of {iterable}) {{'

    def generate_js_code_for_function_call(self, function_name, arguments):
        arguments_code = ', '.join(arguments)
        return f'{function_name}({arguments_code});'

