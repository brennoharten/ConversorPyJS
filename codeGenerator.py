class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.output = ""

    def generate(self):
        self.generate_program(self.ast)
        return self.output

    def generate_program(self, node):
        for statement in node.statements:
            self.generate_statement(statement)

    def generate_statement(self, node):
        if isinstance(node, AssignmentNode):
            self.generate_assignment(node)
        elif isinstance(node, ExpressionNode):
            self.generate_expression(node)

    def generate_assignment(self, node):
        variable_name = node.identifier.name
        expression = self.generate_expression(node.expression)
        self.output += f"let {variable_name} = {expression};\n"

    def generate_expression(self, node):
        if isinstance(node, BinaryOperatorNode):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            operator = self._convert_operator(node.operator)
            return f"({left} {operator} {right})"
        elif isinstance(node, UnaryOperatorNode):
            expression = self.generate_expression(node.expression)
            operator = self._convert_operator(node.operator)
            return f"({operator}{expression})"
        elif isinstance(node, NumberNode):
            return str(node.value)
        elif isinstance(node, IdentifierNode):
            return node.name
        elif isinstance(node, FunctionCallNode):
            function_name = node.identifier.name
            arguments = ", ".join(self.generate_expression(arg) for arg in node.arguments)
            return f"{function_name}({arguments})"

    def _convert_operator(self, operator):
        if operator == "+":
            return "+"
        elif operator == "-":
            return "-"
        elif operator == "*":
            return "*"
        elif operator == "/":
            return "/"
        elif operator == "%":
            return "%"
        elif operator == "==":
            return "=="
        elif operator == "!=":
            return "!="
        elif operator == "<":
            return "<"
        elif operator == ">":
            return ">"
        elif operator == "<=":
            return "<="
        elif operator == ">=":
            return ">="
        elif operator == "and":
            return "&&"
        elif operator == "or":
            return "||"
        elif operator == "not":
            return "!"
        else:
            raise CodeGenerationError(f"Unknown operator: {operator}")
