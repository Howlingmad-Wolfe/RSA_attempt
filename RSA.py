#!/bin/python

# python version:	python 2.7.x
# Auther:			Howlingmad-Wolfe

### An attempt at implanting the RSA algorithm ###

# 	________________________ Warning and Disclaimer ________________________

###			Not for use in real cryptographic aplications!	 	###
###		The auther will take no responsability for compromized	###
###		security due to the use of this script! This script  	###
###		is intended only to be an academic exercise for the 	###
###		auther!													###


# ------------------ Imported Modules ------------------
import os
from prime_tools import *

###############################################################################
###############################################################################
###############################################################################

class RSA_Key ( object ):
    """
    """
    PRIME1 = 0
    PRIME2 = 0

    def __init__(self, sizeModulus=None, modulus=None, phiModulus=None, pubEx=None, secretEx=None):
        
        if sizeModulus == None:
            self.sizeModulus = 4096 # This number should be the set to whatever is considered secure by the industry.
        else:
            self.sizeModulus = sizeModulus
        
        if modulus == None:
            sizePrime = (self.sizeModulus / 2 ) / 8
            PRIME1 = prime(sizePrime)
            PRIME2 = prime(sizePrime)
            self.modulus = PRIME1 * PRIME2
            self.phiModulus = (PRIME1 - 1)*(PRIME2 - 1)
            self.pubEx = int(os.urandom(3).encode("hex"),16)
            
            while coprime(self.phiModulus, self.pubEx) != True:
                self.pubEx += 1 
            k = 1
            
            while pow( k * self.phiModulus + 1, 1, self.pubEx ) != 0:
                k += 1
            
            self.secretEx = ( k * self.phiModulus + 1 ) / self.pubEx

        else:
            self.modulus = modulus
            self.phiModulus = phiModulus
            self.pubEx = pubEx
            self.secretEx = secretEx

        self.prime_a = PRIME1
        self.prime_b = PRIME2

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def refresh(self):
        """New public and private exponents"""
        self.pubEx = int(os.urandom(3).encode("hex"),16)           
        
        while coprime(self.phiModulus, self.pubEx) != True:
            self.pubEx += 1 
        k = 1
            
        while pow( k * self.phiModulus + 1, 1, self.pubEx ) != 0:
            k += 1
            
        self.secretEx = ( k * self.phiModulus + 1 ) / self.pubEx

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def hash(self, data):

        if len(str(data)) > len(str(self.modulus)):
            print "error | block is too big. Cannot hash without data loss."
        else:
            try:
                pad_len = self.modulus.bit_length() - data.bit_length()
                data = data << pad_len
                if self.modulus < data:
                    data = data >> 1
                    pad_len -= 1
                padding = int(os.urandom( (pad_len/8) - 2).encode('hex'),16)
                padding = padding << 16 #This and the 2 in the preceding line are "magic numbers". Need to make non-arbatrary! Was pad_len.bit_length()
                padding = padding | pad_len
                package = data | padding

                return pow(package,self.pubEx,self.modulus)

            except TypeError:
                print "error | NULL data or bad data type!"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def unhash(self, data):

        try:
            package = pow(data,self.secretEx,self.modulus)
            binary = str(bin(package))
            pad_len = ""
            for bit in range(len(binary)-1, len(binary)-16, -1):
                pad_len = binary[bit] + pad_len
            
            pad_len = int(pad_len, 2)
            package = package >> pad_len
            
            return package

        except TypeError:
            print "error | NULL data or bad data type!"

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------        
