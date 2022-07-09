import unittest
from main import crearTipoAtomico,crearTipoStruct,empaquetado,noEmpaquetado,optimo,tipos,tiposAtomicos, crearTipoUnion

class Testing(unittest.TestCase):
	def test(self):
		crearTipoAtomico("int","4","4")
		crearTipoAtomico("bool","1","2")
		crearTipoAtomico("char","1","2")
		crearTipoAtomico("double","8","8")
		crearTipoStruct("struct",["int","char","int","double","bool"],0)
		noEmpaquetado("struct",["int","char","int","double","bool"],0)
		self.assertEqual(tipos["struct"][0], [[0, 3, 0], [4, 4, 1], [8, 11, 0], [16, 23, 0], [24, 24, 1]])
		empaquetado("struct",["int","char","int","double","bool"],0)
		self.assertEqual(tipos["struct"][0], [[0, 3, 0], [4, 4, 0], [5, 8, 0], [9, 16, 0], [17, 17, 0]])
		optimo("struct",["int","char","int","double","bool"],0)      
		self.assertEqual(tipos["struct"][0], [[0, 3, 0], [4, 4, 0], [16, 19, 0], [8, 15, 0], [5, 5, 1]])
		crearTipoUnion("union", ["int","char","int"], 0)
		self.assertTrue("union" in tiposAtomicos)
		self.assertEqual(tiposAtomicos["union"][1],4)
		
if __name__ == '__main__':
    unittest.main()
