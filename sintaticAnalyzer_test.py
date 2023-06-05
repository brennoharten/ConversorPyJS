from tokenizer import Tokenizer
from sintatic_analyzer import Parser
from ConversorOfficial import convert


""" resultado = convert(code) """

def test_parseQuebraDeLinha():
    #Incializar o token
    code = "x = 2 * 6 * 4 \n print(x)"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "var x = 2 * 6 * 4;\nconsole.log(x);" == resultado

def test_parseValorUnico():
    #Incializar o token
    code = "x = 2"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "var x = 2;" == resultado

def test_parseString():
    #Incializar o token
    code = "x = wesker"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "var x = wesker;" == resultado

def test_parseVariasVar():
    #Incializar o token
    code = "x = 2 \n z = a"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "var x = 2\nvar z = a;" == resultado

""" def test_parseErroDeCodigo():
    #Incializar o token
    code = "x = 2 * 6 * , 4 \n print(x)"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()
 """
    
def test_parseVariasVar():
    #Incializar o token
    code = "x = 2 \n z = a"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "var x = 2;\nvar z = a;" == resultado

def test_parseCondicionalIf():
    #Incializar o token
    code = """x = 2  
    z = 3 
    if x == z :
    print(x)"""
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    

    assert "var x = 2;\nvar z = 3;\nif (x == z) {console.log(x);}" == resultado

def test_parseFunção():
    #Incializar o token
    code = """def somar(a, b):
    return a + b 

    def main():
    num1 = 2
    num2 = 3 
    resultado = somar(num1, num2) 
    print(resultado) 

    main()"""
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "function somar(a, b) {\nreturn a + b;\n}\n\nfunction main() {\nvar num1 = 2;\nvar num2 = 3;\nvar resultado = somar(num1, num2);\nconsole.log(resultado);\n}\n\nmain()" == resultado


""" def test_parseIf_Else_While():
    #Incializar o token
    code = x = 2  
    z = 3 
    if x == z :
    print(x)
    else :
    print(z)
    while x > z :
    print(x)
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()
    
    assert "var x = 2;\nvar z = 3;\nif (x == z) {console.log(x);}\nelse {\nconsole.log(z)}\nwhile(x > z) {\nconsole.log(x)}" == resultado
 """