# importe as classes e funções necessárias das etapas anteriores
from tokenizer import Tokenizer
from sintatic_analyzer import Parser

def gerar_arquivo_js(codigo_js, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(codigo_js)

def ler_arquivo_python(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()

    return conteudo

def convert(input_code):
    # etapa 1: tokenização
    tokenizer = Tokenizer(input_code)
    tokens = tokenizer.tokenize()

    # etapa 2: análise sintática
    parser = Parser(tokens)
    return parser.parse()

js_code = convert(ler_arquivo_python('entrada.py'))

print(js_code)

gerar_arquivo_js(js_code, 'arquivo.js')

