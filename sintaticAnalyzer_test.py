from tokenizer import Tokenizer
from sintatic_analyzer import Parser
from ConversorOfficial import convert
import pytest

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

def test_parseErroDeCodigo():
    #Incializar o token
    code = "x = 2 * 6 * , 4 \n print(x)"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    
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
    code = "x = 2 \n z = 3 \n if x == z : \n print(x)"
    
    entrada = Tokenizer(code)

    #Tokenizar o codigo
    token = entrada.tokenize()

    #Incializar a analise
    analise = Parser(token) 
    resultado = analise.parse()

    assert "var x = 2;\nvar z = 3;\nif(x==z)\nconsole.log(x)" == resultado

""" 
 : 

 """

