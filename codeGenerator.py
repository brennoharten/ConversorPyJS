from parser2 import NodeType

class CodeGenerator:
    def __init__(self):
        self.output = ""
        self.indentation = 0

    def generate(self, node):
        if node.type == NodeType.LITERAL:
            self.output += node.value
        elif node.type == NodeType.IDENTIFIER:
            self.output += node.value
        elif node.type == NodeType.OPERATOR:
            self.generate(node.left)
            self.output += " " + node.value + " "
            self.generate(node.right)
        elif node.type == NodeType.FUNCTION_CALL:
            self.output += node.value + "("
            for i, arg in enumerate(node.children):
                self.generate(arg)
                if i < len(node.children) - 1:
                    self.output += ", "
            self.output += ")"
        elif node.type == NodeType.IF:
            self.output += "if ("
            self.generate(node.condition)
            self.output += ") {\n"
            self.indentation += 1
            self.generate(node.if_body)
            self.indentation -= 1
            self.output += self._indent() + "}"
            if node.else_body:
                self.output += " else {\n"
                self.indentation += 1
                self.generate(node.else_body)
                self.indentation -= 1
                self.output += self._indent() + "}"
        elif node.type == NodeType.WHILE:
            self.output += "while ("
            self.generate(node.condition)
            self.output += ") {\n"
            self.indentation += 1
            self.generate(node.body)
            self.indentation -= 1
            self.output += self._indent() + "}"
        elif node.type == NodeType.FOR:
            self.output += "for (var " + node.children[0].value + " = "
            self.generate(node.children[1])
            self.output += "; " + node.children[0].value + " <= "
            self.generate(node.children[2])
            self.output += "; " + node.children[0].value + " += "
            self.generate(node.children[3])
            self.output += ") {\n"
            self.indentation += 1
            self.generate(node.children[4])
            self.indentation -= 1
            self.output += self._indent() + "}"
        else:
            raise ValueError("Unknown node type: " + str(node.type))

    def _indent(self):
        return "  " * self.indentation

