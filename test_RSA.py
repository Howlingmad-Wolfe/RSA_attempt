import unittest
from prime_tools import *
from RSA import *

class TestRSA(unittest.TestCase):
    
    test_RSA_key = RSA_Key(sizeModulus = 2048)

    
    def test_validate_key_components(self):
        
        modulus = self.test_RSA_key.prime_a * self.test_RSA_key.prime_b
        self.assertEqual( self.test_RSA_key.modulus, modulus )

        phi = ( self.test_RSA_key.prime_a - 1 ) * ( self.test_RSA_key.prime_b - 1 )
        self.assertEqual( self.test_RSA_key.phiModulus, phi )

        # public exponent
        self.assertEqual(coprime( self.test_RSA_key.modulus, self.test_RSA_key.pubEx ), True)
        self.assertEqual( coprime( self.test_RSA_key.phiModulus, self.test_RSA_key.pubEx ), True )

        # private exponent
        self.assertEqual( coprime( self.test_RSA_key.modulus, self.test_RSA_key.secretEx ), True)
        self.assertEqual( coprime( self.test_RSA_key.phiModulus, self.test_RSA_key.secretEx ), True)


    def test_Hash_Unhash(self):
        
        pass


if __name__ == '__main__':
    unittest.main()