import unittest
import numpy as np
from mensajes.hola.saludos import generar_array

class pruebashola(unittest.TestCase):
    def test_generararray(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))

