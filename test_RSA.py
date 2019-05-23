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
        # test for messages shorter than lenght(modulus - 11 bytes) simulatedt AES 256 key.
        sim_AES256_key = int(os.urandom(32).encode("hex"), 16)
        hashed_sim_AES256_key = self.test_RSA_key.hash( sim_AES256_key )
        hashed_sim_AES256_key = self.test_RSA_key.hash( sim_AES256_key )
        self.assertEqual( hashed_sim_AES256_key == sim_AES256_key, False ) # hashed message should not equal the cleartext message.
        self.assertEqual(len( str( hashed_sim_AES256_key ) ), len( str ( self.test_RSA_key.modulus ) ) ) # checking if hashed message is approx. the length of modulus
        self.assertEqual( self.test_RSA_key.unhash( hashed_sim_AES256_key ), sim_AES256_key ) # unhashed message should be the same as cleartext message.


if __name__ == '__main__':
    unittest.main()