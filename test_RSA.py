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


    def test_refresh(self):
        previouse_public_key = self.test_RSA_key.pubEx
        previouse_private_key = self.test_RSA_key.secretEx
        
        self.test_RSA_key.refresh() # getting new public and private exponents
        
        # Proving new public exponent
        self.assertEqual(previouse_public_key == self.test_RSA_key.pubEx, False)
        self.assertEqual(coprime( self.test_RSA_key.modulus, self.test_RSA_key.pubEx ), True)
        self.assertEqual( coprime( self.test_RSA_key.phiModulus, self.test_RSA_key.pubEx ), True )
        
        # Proving new private exponent
        self.assertEqual(previouse_private_key == self.test_RSA_key.secretEx, False) 
        self.assertEqual( coprime( self.test_RSA_key.modulus, self.test_RSA_key.secretEx ), True)
        self.assertEqual( coprime( self.test_RSA_key.phiModulus, self.test_RSA_key.secretEx ), True)


    def test_small_Hash_Unhash(self):
        # test for messages shorter than lenght(modulus - 11 bytes) simulatedt AES 256 key.
        sim_AES256_key = int(os.urandom(32).encode("hex"), 16)
        #self.test_RSA_key.make_blocks(sim_AES256_key)
        hashed_sim_AES256_key = self.test_RSA_key.hash( sim_AES256_key )
        self.assertEqual( hashed_sim_AES256_key == sim_AES256_key, False ) # hashed message should not equal the cleartext message.
        #self.assertEqual(len( str( hashed_sim_AES256_key ) ), len( str ( self.test_RSA_key.modulus ) ) ) # checking if hashed message is approx. the length of modulus
        self.assertEqual( self.test_RSA_key.unhash( hashed_sim_AES256_key ), sim_AES256_key ) # unhashed message should be the same as cleartext message.

    def test_large_Hash_Unhash(self):

        data_larger_than_modulus = int(os.urandom(1024).encode("hex"), 16)
        data_into_blocks = self.test_RSA_key.make_blocks(data_larger_than_modulus)

        hashed_blocks = []
        for block in data_into_blocks:
            hashed_block = self.test_RSA_key.hash(block)
            self.assertEqual( hashed_block == block, False )
            hashed_blocks.append(hashed_block)
        
        index = 0
        unhashed_blocks = []
        for block in hashed_blocks:
            unhashed_block = self.test_RSA_key.unhash(block)
            self.assertEqual(unhashed_block, data_into_blocks[index])
            unhashed_blocks.append(unhashed_block)
            index += 1

        assembled_large_data = self.test_RSA_key.assemble_blocks(unhashed_blocks)
        self.assertEqual(assembled_large_data, data_larger_than_modulus)


        



if __name__ == '__main__':
    unittest.main()