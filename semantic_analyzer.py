# Step 3: Semantic Analysis
# ...
# ...

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def analyze(self):
        self.traverse(self.ast)

    def traverse(self, node):
        if isinstance(node, AssignNode):
            var_name = node.left.value
            if var_name in self.variables:
                raise Exception(f"Variable '{var_name}' already defined")
            self.variables[var_name] = self.get_type(node.right)

        elif isinstance(node, PrintNode):
            self.get_type(node.expr)

        elif isinstance(node, IfNode):
            self.get_type(node.condition)
            for child_node in node.true_body:
                self.traverse(child_node)
            for child_node in node.false_body:
                self.traverse(child_node)

        elif isinstance(node, WhileNode):
            self.get_type(node.condition)
            for child_node in node.body:
                self.traverse(child_node)

        elif isinstance(node, BinaryOpNode):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)
            op = node.op.type
            if op in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE"]:
                if left_type != "int" or right_type != "int":
                    raise Exception("Operands must be of type 'int'")

        elif isinstance(node, VarAccessNode):
            var_name = node.value
            if var_name not in self.variables:
                raise Exception(f"Variable '{var_name}' is not defined")

    def get_type(self, node):
        if isinstance(node, IntNode):
            return "int"
        elif isinstance(node, BoolNode):
            return "bool"
        elif isinstance(node, VarAccessNode):
            var_name = node.value
            if var_name not in self.variables:
                raise Exception(f"Variable '{var_name}' is not defined")
            return self.variables[var_name]
        elif isinstance(node, BinaryOpNode):
            return "int"
        else:
            raise Exception("Unsupported type")
