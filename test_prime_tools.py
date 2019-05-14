import unittest
import os
import json

from prime_tools import *
from search import *

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


    def test_preFilter(self):
        for iterations in range(10):
            primer = int(os.urandom(3).encode("hex"), 16)
            testnumber = preFilter(primer)
            
            for i in range(2,100):
                self.assertEqual( pow( testnumber, 1, i ) == 0 , False )


    def test_fermat_prime(self):
        passes = 30 # certen functions in prime_tools.py will conduct a test specified number of times.
        self.assertEqual( fermat_prime( -499, passes ), False )
        self.assertEqual( fermat_prime( 0, passes ), False )
        self.assertEqual( fermat_prime( 1, passes ), False )
        self.assertEqual( fermat_prime( 2, passes ), True )
        self.assertEqual( fermat_prime( 499, passes ), True )
        self.assertEqual( fermat_prime( 2579, passes ), True )
        #self.assertEqual( fermat_prime( 561, passes ), True) # 561 is a carmichael number and a not prime but it should fool the fermat test. 
        self.assertEqual( fermat_prime( 2136, passes ), False )
        self.assertEqual( fermat_prime( 13415, passes ), False )
        #self.assertEqual( fermat_prime( 29341, passes ), True) # 29341 is a carmichael number and a not prime but it should fool the fermat test.


    def test_miller_rabin(self):
        passes = 30 # certain functions in prime_tools.py will conduct a test a specified number of times.
        self.assertEqual( miller_rabin(-499, passes), False )
        self.assertEqual( miller_rabin(0, passes), False )
        self.assertEqual( miller_rabin(1, passes), False )
        self.assertEqual( miller_rabin(2, passes), True )
        self.assertEqual( miller_rabin(499, passes), True )
        self.assertEqual( miller_rabin( 2579, passes ), True )
        self.assertEqual( miller_rabin( 561, passes ), False )# 561 is a carmichael number and not a prime. It shouldn't fool the miller_rabin test
        self.assertEqual( miller_rabin( 2136, passes ), False )
        self.assertEqual( miller_rabin( 13415, passes ), False )
        self.assertEqual( miller_rabin( 29341, passes ), False )# 29341 is a carmichael number and not a prime. It shouldn't fool the miller_rabin test


    def test_prime(self):
        
        for i in range(10): # Demonstrating using a seen integer
            primer = int(os.urandom(3).encode("hex"), 16)   # seed int
            testNumb = prime(0,primer) # no size given only seed int
            
            primeFile = open("%s\prime_pool\%s" %(os.getcwd(),findFile(testNumb)), 'r')
            numbRange = json.load(primeFile)
            primes = SearchTree(numbRange)
            primeFile.close()
            self.assertEqual(testNumb, primes.search(testNumb))

        for i in range(10): # Getting a random prime number with a size of up to X bytes long.
            testNumb = prime(3) # No seed int given only size.
            
            primeFile = open("%s\prime_pool\%s" %(os.getcwd(),findFile(testNumb)), 'r')
            numbRange = json.load(primeFile)
            primes = SearchTree(numbRange)
            primeFile.close()
            self.assertEqual(testNumb, primes.search(testNumb))



if __name__ == '__main__':
    unittest.main()