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
from math import floor as floor

###############################################################################
###############################################################################
###############################################################################

class RSA_Key ( object ):
    """
    Key object for RSA cryptography. Self generates if called with no args or if only sizeModulus is given.
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
        
        # The following variables are for testing purposes
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

    def make_blocks(self, data, data_len=None, shift=None, blocks=None):
        """ (recursive function) Brakes data into chunks small enough to be encrypted and recovered by the key. Takes int, returns list """
        if blocks == None:       
            blocks = []
        if shift == None:
            shift = 0
        if data_len == None:
            data_len = data.bit_length()

        target = self.modulus.bit_length()
        tag = int(floor( data_len / ( target / 2 ) ) * ( target / 2 ))
        overhead = target - tag.bit_length()

        WorkingShift = int(floor(data.bit_length()/2))
        first = data >> WorkingShift
        second = first << WorkingShift
        second = data ^ second
        
        if first.bit_length() >= overhead or second.bit_length() >= overhead:
            for i in self.make_blocks(first, data_len, WorkingShift + shift):
                blocks.append(i)
            for i in self.make_blocks(second, data_len, shift):
                blocks.append(i)
        else:
            first = first << tag.bit_length()
            first = first ^ (shift + WorkingShift)
            blocks.append(first)
            second = second << tag.bit_length()
            second = second ^ shift
            blocks.append(second)

        return blocks

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def assemble_blocks(self, data):
        """ Assembles chunks of data back into the original data. Takes list returns int """
        assembled_message = 0
        tag_size = self.modulus.bit_length()/2 * len(data)
        proto_tag = tag_size.bit_length()

        for block in data:
            clean_block = block >> proto_tag
            mask = clean_block << proto_tag
            tag = block ^ mask
            block = clean_block << tag
            assembled_message |= block

        return assembled_message

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def hash(self, data):
        """ 
        Adds at least 88 bits (11 bytes) of random data and removal tage to data then encrypts it. 
        Takes int. returns int or list.
        """

        if len(str(data)) > len(str(self.modulus)):
            block = self.make_blocks(data)
            for i in block:
                self.hash(i)
            return block

        else:
            #try:
            pad_len = self.modulus.bit_length() - data.bit_length()
            data <<= pad_len
            if self.modulus < data:
                data >>= 1
                pad_len -= 1
            padding = int(os.urandom( (pad_len/8) - 2).encode('hex'),16)
            tag_len = self.modulus.bit_length()
            tag_len = tag_len.bit_length()
            padding <<= tag_len 
            padding = padding | pad_len
            package = data | padding

            return pow(package,self.pubEx,self.modulus)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def unhash(self, data):
        """
        decrypt message
        calculate length of padding removal tag based on the size of modulus.
        data_1 = data >> tag length, data_2 = data << tag length, data_1 ^ data_2 = tag.
        data >> tag = message!

        Takes int or list and returns int.
        """
        if type(data) == list:
            for i in data:
                i = self.unhash(i)
            package = self.assemble_blocks(data)
        else:
            package = pow(data, self.secretEx, self.modulus)
            tag_size = self.modulus.bit_length().bit_length()
            cancel = package >> tag_size
            cancel <<= tag_size
            tag = package ^ cancel
            package >>= tag
            
        return package