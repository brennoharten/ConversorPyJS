# importe as classes e funções necessárias das etapas anteriores
from tokenizer import Tokenizer
from sintatic_analyzer import Parser

def convert(input_code):
    # etapa 1: tokenização
    tokenizer = Tokenizer(input_code)
    tokens = tokenizer.tokenize()

    # etapa 2: análise sintática
    parser = Parser(tokens)
    return parser.parse()

# exemplo de uso
python_code = "x = 2 + 3 * 4 \n print(x)"
js_code = convert(python_code)
print(js_code)
