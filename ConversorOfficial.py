# importe as classes e funções necessárias das etapas anteriores
from tokenizer import Tokenizer
from sintatic_analyzer import Parser
from semantic_analyzer import SemanticAnalyzer
from codeGenerator import CodeGenerator

def convert(input_code):
    # etapa 1: tokenização
    tokenizer = Tokenizer(input_code)
    tokens = tokenizer.tokenize()

    # etapa 2: análise sintática
    parser = Parser(tokens)
    code = parser.parse()

    # etapa 3: análise semântica
    """ semantic_analyzer = SemanticAnalyzer(ast)
    code = semantic_analyzer.analyze() """

    print(code)

    # etapa 4: geração de código
    """ codeGenerator = CodeGenerator()
    output_code = codeGenerator.generate(ast) """

    return code

# exemplo de uso
python_code = "x = 2 + 3 * 4 \n print(x)"
js_code = convert(python_code)
print(js_code)
