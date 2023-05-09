import pyjs
import unittest

# converter a função Python para JavaScript usando Pyjs
js_code = pyjs.compile_python_to_js("""
def soma(a, b):
    return a + b
""")

# definir a função JavaScript equivalente
exec(js_code)
js_soma = soma

class TestSoma(unittest.TestCase):
    def test_soma_1(self):
        self.assertEqual(soma(2, 3), js_soma(2, 3))

    def test_soma_2(self):
        self.assertEqual(soma(0, 0), js_soma(0, 0))

    def test_soma_3(self):
        self.assertEqual(soma(-1, 1), js_soma(-1, 1))

if __name__ == '__main__':
    unittest.main()