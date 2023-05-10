from parser2 import NodeType
class SemanticAnalyzer:
    def __init__(self, root):
        self.root = root
    
    def analyze(self):
        symbol_table = {}

        def traverse(node):
            if node is None:
                return

            if node.type == NodeType.IDENTIFIER:
                if node.value not in symbol_table:
                    raise NameError(f"Name '{node.value}' is not defined")
            elif node.type == NodeType.OPERATOR:
                if node.left.type != NodeType.IDENTIFIER:
                    raise SyntaxError("Can only assign to variable")
                symbol_table[node.left.value] = True
            elif node.type == NodeType.FUNCTION_CALL:
                if node.func.type == NodeType.IDENTIFIER:
                    if node.func.value == "print":
                        if len(node.args) != 1:
                            raise TypeError("print() takes exactly 1 argument")
                    else:
                        raise NameError(f"Name '{node.func.value}' is not defined")
            elif node.type == NodeType.BINARY_OPERATION:
                traverse(node.left)
                traverse(node.right)
            elif node.type == NodeType.UNARY_OPERATION:
                traverse(node.expr)
            elif node.type == NodeType.FUNCTION_CALL:
                symbol_table[node.name] = True
                for arg in node.args:
                    symbol_table[arg] = True
                traverse(node.body)
            elif node.type == NodeType.IF:
                traverse(node.cond)
                traverse(node.if_body)
                if node.else_body:
                    traverse(node.else_body)
            elif node.type == NodeType.WHILE or node.type == NodeType.FOR:
                traverse(node.cond)
                traverse(node.body)

        traverse(self.root)
