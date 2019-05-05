import unittest
from prime_tools import *

class TestTools(unittest.TestCase):
    def test_coprime(self):
       self.assertEqual( coprime( 2583476, 7 ), False )
       self.assertEqual( coprime( 4, 2583476 ), False )
       self.assertEqual( coprime( 2583476, 9 ), True )
       self.assertEqual( coprime( 2583476, -9 ), False )
       self.assertEqual( coprime( 1229480, 43 ), True )
       self.assertEqual( coprime( 1229480, 72), False )
       self.assertEqual( coprime( 97, 13221360 ), True )
       self.assertEqual( coprime( 21, 13221360 ), False )
       self.assertEqual( coprime(17685743, 19), True )
       self.assertEqual( coprime(17685743, 1), False )


    #def test_preFilter(self):
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )
    #    self.assertEqual( preFilter(), )

    def test_fermat_prime(self):
        self.assertEqual( fermat_prime( -499 ), False )
        self.assertEqual( fermat_prime( 0 ), False )
        self.assertEqual( fermat_prime( 1 ), False )
        self.assertEqual( fermat_prime( 2 ), True )
        self.assertEqual( fermat_prime( 499 ), True )
        self.assertEqual( fermat_prime( 2579 ), True )
        #self.assertEqual( fermat_prime( 561 ), True) # This is a carmichael number and, therefor, not prime
        self.assertEqual( fermat_prime( 2136 ), False )
        self.assertEqual( fermat_prime( 13415 ), False )
        self.assertEqual( fermat_prime( 29341 ), True) # This is a carmichael number and, therefor, not prime

    def test_miller_rabin(self):
        self.assertEqual( miller_rabin(-499), False )
        self.assertEqual( miller_rabin(0), False )
        self.assertEqual( miller_rabin(1), False )
        self.assertEqual( miller_rabin(2), True )
        self.assertEqual( miller_rabin(499), True )
        self.assertEqual( miller_rabin( 2579 ), True )
        self.assertEqual( miller_rabin( 561 ), False )
        self.assertEqual( miller_rabin( 2136 ), False )
        self.assertEqual( miller_rabin( 13415 ), False )
        self.assertEqual( miller_rabin( 29341 ), False )

    #def test_prime(self):
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )
    #    self.assertEqual( prime(), )


if __name__ == '__main__':
    unittest.main()