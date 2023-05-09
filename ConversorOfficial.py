# importe as classes e funções necessárias das etapas anteriores
from tokenizer import Tokenizer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from codeGenerator import CodeGenerator

def convert(input_code):
    # etapa 1: tokenização
    tokenizer = Tokenizer(input_code)
    tokens = tokenizer.tokenize()

    # etapa 2: análise sintática
    parser = Parser(tokens)
    ast = parser.parse()

    # etapa 3: análise semântica
    semantic_analyzer = SemanticAnalyzer(ast)
    semantic_analyzer.analyze()

    # etapa 4: geração de código
    codeGenerator = CodeGenerator(ast)
    output_code = codeGenerator.generate()

    return output_code

# exemplo de uso
python_code = "x = 1 + 2 * 3 \n print ( x )"
js_code = convert(python_code)
print(js_code)
