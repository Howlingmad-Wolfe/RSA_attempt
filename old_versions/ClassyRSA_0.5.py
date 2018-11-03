#!/bin/python

# python version:	python 2.7.x
# Auther:			Jesse Wolfe, jessewolfe7c6@gmail.com

### An attempt at implanting the RSA algorithm ###

# 	________________________	Warning	________________________

###			Not for use in real cryptographic aplications!	 	###
###		The auther will take no responsability for compromized	###
###		security due to the use of this script! This script  	###
###		is intended only to be an academic exercise for the 	###
###		auther!													###


# ------------------ Imported Modules ------------------

import random # change all instances of random.randint() to random.SystemRandom() or os.urandom()?
import json
import os

# The following are imported for multithreading purposes.
#from multiprocessing import pool, cpu_count


# imported items below this line are for testing please remove when finished 
# from timeit import Timer as timer

###############################################################################
###############################################################################
###############################################################################

def coprime( number_1, number_2 ):
	"""
	Uses the Euclidean algorithm to find if two numbers have a
	common divisor. The order the numbers are placed in doesn't 
	matter. The function will use the smaller number as the 
	initial divisor.
	

	--------------------------------------------------------
	Parameters
	--------------------------------------------------------
		number_1:	int

		number_2:	int


	--------------------------------------------------------
	Returns
	--------------------------------------------------------
		boolean

	"""
	if number_1 < number_2:
		a = number_2
		b = number_1
	else:
		a = number_1
		b = number_2

	while b != 0:
		t = b
		b = pow( a, 1, b )
		a = t

	if a != 1:
		return False
	else:
		return True
	
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fermat_prime( number, pass_no = 1 ):
	"""
	Preforms a Fermat primality test on a given "number"
	a "pass_no" number of times. pass_no defalts to 1 if left blank.

	
	--------------------------------------------------------
	Parameters
	--------------------------------------------------------
		number:		int
			The number to be tested for primeality.


		Pass_no:	int
			The number of times to run the test for a given "number" 
	
	
	--------------------------------------------------------
	Returns
	--------------------------------------------------------
		Boolean (True or False)

	"""
	if number < 2 or pow( number, 1, 2 ) == 0:
		return False
	
	count = 0
	while count <= pass_no:
		x = random.randint( 3, number - 1 ) # this may not be a problem in this use case?
		
		if coprime( number, x ) == False:
			return False

		elif pow( x, number-1, number ) != 1:
			return False
		
		else:
			count += 1
	return True

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def miller_rabin( number , pass_no = 1 ):
	"""
	Runs a Probabilistic Miller-Rabin Primeality test. returns a boolean.
	
	Performs a Miller-Rabin (Rabin-Miller) test on a given number (number).
	The test is performed as many times as the value given for the Pass_no.
	argument. If pass_no is left blank the funtion will defalt to 1.
	Every time the test is run the "Witness" (a) value should be different.


	--------------------------------------------------------
	Parameters
	--------------------------------------------------------
		number:		int
			The number to be tested for primeality.


		Pass_no:	int
			The number of times to run the test for a given number "number".


	--------------------------------------------------------
	Returns
	--------------------------------------------------------
		Boolean (True or False)
		
	"""
	# odd_Filtering out any values that are even or equal to 1.
	if number <= 2:
		return False
	elif pow( number, 1, 2 ) == 0:
		return False
	
	k = 0
	while pow ( number-1, 1, pow( 2, k + 1 ) ) == 0:
		k += 1
	
	for i in range( pass_no ):
		
		# test primer
		m = ( number - 1) / pow( 2, k )
		a = random.randint( 2, number - 1 ) # this may not be a problem in this use case?
		test = pow( a, m, number )
		
		# main body of test
		loop_stop = 0
		while test != number - 1:
			
			if 100 < loop_stop:
				return False

			elif test == 1 and 0 < loop_stop:
				return False

			elif loop_stop == 0 and test == 1:
				break

			else:
				# setting up for next stage of the test.
				a = test
				m = 2
				loop_stop += 1
				
				test = pow( a, m, number )
	return True

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

###############################################################################
###############################################################################
###############################################################################

class RSA_Keys ( object ):
	"""
	
	--------------------------------------------------------
	Parameters: (bit_size, identifier, key_ring, public_key_ring, primes, path)
	--------------------------------------------------------
	
		bit_size:			int
		------------------------
			Defaults to 2048.
			
			Size of modulus in bits.


		identifier:			str
		------------------------
			Defaults to an empty string.
			
			Session identifier/key_ring idenifier used 
			to save keys.


		key_ring: 			dict
		------------------------
			Defaults to empty dictionary.

			This is the RSA key.
			dictionary keys are:

				'bit_size'		(Is size of modulus in bits)
				
				'modulus'		(Is the devisor to be used in 
								the hash and unhash functions)
				
				'phi_modulus'	(Is the number used to create 
								the public and private exponent. 
								Not used in this class)
				
				'lock'			(Is the public exponent)
				
				'key'			(Is the private exponent)


		public_key_ring:	dict
		------------------------
			Defaults to empty dictionary.
			
			Stores the fallowing:
				
				'modulus'		(Is the devisor to be used in 
								the hash and unhash functions)
				
				'lock'			(Is the public exponent)


		primes:				list/array
		------------------------
			Defaults to empty list.
			
			stores primes used to create the modulus 
			and phi_modulus.


		path:				str
		------------------------
			Defaults to empty string.
			
			Path to the file used to store RSA keys.


	--------------------------------------------------------
	Class Variables
	--------------------------------------------------------
	

	--------------------------------------------------------
	Functions: (get_primes, key_gen, lock_key, save_keys, public_key)
	--------------------------------------------------------
	
		__get_primes__:
			self.primes

		__key_gen__:
			self.key_ring

		__lock_key__:
			self.key_ring

		__save_keys__:
			file

		__public_key__:
			self.public_key_ring

	--------------------------------------------------------
	Returns
	--------------------------------------------------------

	"""
	def __init__( self, bit_size=2048, identifier=None, key_ring=None, public_key_ring=None, primes=None, path=None):
		
		self.bit_size = bit_size
		
		if identifier == None:
			self.identifier = ""
		else:
			self.identifier = identifier
		
		if key_ring == None:
			self.key_ring = {}
		else:
			self.key_ring = key_ring
		
		if primes == None:
			self.primes = []
		else:
			self.primes = primes
		
		if path == None:
			self.path = ""
		else:
			self.path = path
		
		if public_key_ring == None:
			self.public_key_ring ={}
		else:
			self.public_key_ring = public_key_ring

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def __repr__( self ):
		return "(s%, s%, s%, s% )" % ( self.bit_size, self.identifier, self.key_ring, self.primes )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def get_primes( self ):
		"""
		Returns a probable prime number of length ~ 1/2 "bit_size".

		Generates a random number of length ~ 1/2 "bit_size". and runs a series of tests 
		(a simple odd_filter, the 'fermat_prime' test, and the 'miller_rabin' test) to 
		determine if the number is a prime number. if the number is determined to 
		be composite the function decrements the number to the closest odd number 
		and repeats the tests until a number passes the tests.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			bit_size:	int
				
				desired length, in bits, of prime.


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.primes:	list/array
				
				adds a Probable prime number within the bounds of the 
				function to self.primes.
		
		"""
		prime_bit_size = self.bit_size / 2
		prime = int( os.urandom( prime_bit_size / 8 ).encode( 'hex' ), 16 )
		
		odd_filter = [ i for i in range( 3, 100, 2 ) ]
		
		if pow( prime, 1, 2 ) == 0:
			prime -= 1
			
		is_prime = False
		while is_prime == False:

			odd_filter_pass = False
			while odd_filter_pass == False:
				
				for i in odd_filter:
					
					if pow( prime, 1, i ) == 0:
						prime -= 2
						break
				
				odd_filter_pass = True

			if fermat_prime( prime, 20 ) == False:
				prime -= 2

			elif miller_rabin( prime, 40 ) == False:
				prime -= 2

			else:
				is_prime = True
		
		self.primes.append(prime)
		return prime

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def key_gen(self):
		"""
		Generates a RSA public and privet key pair and places it in a .json file. 
		If no input is given for the bit_size argument, the function defalts to a 
		bit length of 2048 for the large composite number component of the public 
		and private key sets.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			identifyer: str
				Used as the dict. key for the RSA key generated by the function
			

			bit_size:	int
				Length of key to be generated.


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.key_ring

		"""
		modulus = self.primes[0] * self.primes[1]
		phi_modulus = ( self.primes[0] - 1 ) * ( self.primes[1] - 1 )
		
		# Generating public exponent aka "the lock"
		#lock = random.randint( 65537, 100000 )
		#while coprime( phi_modulus, lock ) != True:
		#	lock += 1

		# This seems to be a standard practice for defending 
		# against the low public exponent vulnerability.
		lock = 65537 
		
		# Generating private exponent using extended euclidean algorithm? 
		k = 1
		while pow( k * phi_modulus + 1, 1, lock ) != 0:
			k += 1
		key = ( k * phi_modulus + 1 ) / lock
		
		# Testing that the private coprime was generated correctly. 
		# requirement: e * d (mod phi_modulus) must == 1
		test_d = pow( lock * key, 1, phi_modulus )
		if test_d != 1:
			raise Exception ( "There is a problem with the private exponent" )
			
		self.key_ring = {	"bit_size" : self.bit_size, 
							 "modulus" : modulus, 
						 "phi_modulus" : phi_modulus, 
								"lock" : lock, 
								 "key" : key
							}
		
		return self.key_ring

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def lock_key( self ):
		"""
		Creats a random public exponent and a corasponding
		private exponent for a given "key_ring".


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.key_ring[ 'phi_modulus' ]


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.key_ring
		"""
		phi_modulus = self.key_ring[ "phi_modulus" ]

		# Generating public exponent aka "the lock"
		lock = random.randint( 65537, 4294967296 ) # Max value == 32 bits
		while coprime( phi_modulus, lock ) != True:
			lock += 1

		# Generating private exponent using extended euclidean algorithm? 
		k = 1
		while pow( k * phi_modulus + 1, 1, lock ) != 0:
			k += 1
		key = ( k * phi_modulus + 1 ) / lock

		# Testing that the private coprime was generated correctly. 
		# requirement: e * d (mod phi_modulus) must == 1
		test_d = pow( lock * key, 1, phi_modulus )
		if test_d != 1:
			raise Exception ( "There is a problem with the private exponent" )
		
		self.key_ring[ 'lock' ] = lock
		self.key_ring[ 'key' ] = key

		return self.key_ring

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def save_keys( self ):
		"""
		Saves generated RSA "key_ring" to a file. Creats a file
		if none exists.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.key_ring


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			file

		"""
		# Change "RSA_keys.json" to self.path so that file location can be specified instead of preset.
		try:
			key_file = open( 'RSA_keys.json', 'r' )
			h = json.load( key_file )
			key_file.close()
		
		except IOError: # if this script is moved to python 3.x this will need to be changed to FileNotFoundError.
			key_file = open( 'RSA_keys.json', 'w+' )
			key_file.close()
			h = {}
			h.update({'RSA' : { str( self.identifier ) : self.key_ring } } )
		
		h[ 'RSA' ].update({ str( self.identifier ) : self.key_ring } )
		key_holder = open( 'RSA_keys.json', 'w' )
		json.dump( h, key_holder, ensure_ascii = False, encoding = 'UTF-8', indent = 4 )
		key_holder.close()

		return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def public_key( self ):
		"""
		Retrieves the "modulus" and "lock" from self.key_ring and
		places them in a new directory.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.key_ring


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.public_key_ring

		"""
		self.public_key_ring["modulus"] = self.key_ring["modulus"]
		self.public_key_ring["lock"] = self.key_ring["lock"]

		return self.public_key_ring

###############################################################################
###############################################################################
###############################################################################

class RSA( RSA_Keys ):
	"""
	Takes a message and an RSA key (as a dictionary) and encrypts
	or decrypts the message.
	
	--------------------------------------------------------
	Parameters
	--------------------------------------------------------
	
		message: str
		------------------------
			the message to be encrypted.

		
		All parameters from the "RSA_Keys" class.
	
	--------------------------------------------------------
	Class Variables: (self.byte_block_len, self.deci_block_len)
	--------------------------------------------------------
	
		self.byte_block_len: 	int
		---------------------------
			length, in bits, of a given block in blocks. This is 
			determined by the key_ring[ 'bit_size' ]


		self.deci_block_len:	int
		---------------------------
			length, in decimal, of a given block in blocks. This is 
			determined by using self.byte_block_len


	--------------------------------------------------------
	Functions: (block, ublock, v1_5_like_padding, strip_pad, hash, uhash)
	--------------------------------------------------------
		__block__:
			self.message:	list/array

		__ublock__:
			self.message:	str

		__v1_5_like_padding__:
			self.message:	list/array

		__strip_pad__:
			self.message:	list/array

		__hash__:
			self.message:	list/array

		__uhash__:
			self.message:	list/array

	--------------------------------------------------------
	Returns
	--------------------------------------------------------

	"""
	def __init__( self, message, bit_size=2048, identifier=None, key_ring=None,\
				 public_key_ring=None, primes=None, path=None ):
		super( RSA, self ).__init__( bit_size, identifier, key_ring, public_key_ring, primes, path  )
		
		self.message = message
		
		if key_ring == None:
			self.get_primes()
			self.get_primes()
			self.key_gen()
			self.byte_block_len = self.key_ring[ 'modulus' ].bit_length() / 8 #- 42
			
			print self.byte_block_len, " byte_block_len"
			
			self.deci_block_len = len( str( pow( 2, self.byte_block_len ) ) )
		else:
			self.byte_block_len = self.key_ring[ 'modulus'].bit_length() / 8 #- 42
			
			print self.byte_block_len, " byte_block_len"
			
			self.deci_block_len = len( str( pow( 2, self.byte_block_len ) ) )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def __repr__( self ):
		return "(s%, s%, s%)" % ( self.message, self.key_ring, self.message_blocks )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------	
	
	def block( self ):
		"""
		Takes a "message" input and breaks it down into blocks of a given "size".
		If the "size" argument is left blank it defaults to 128 bits.
		
		Returns a list consisting of the original message divided into string-blocks 
		of length = "size"


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			
			self.message:	str
			---------------------------
				default = no default (if left blank, will throw error)
				The data that will be divided into blocks.


			self.key_ring:	dict
			---------------------------
				Uses the modulus ('modulus') to set The size of the 
				blocks into which the data will be divided.


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.message: list/array
			
		"""
		# Turning message into ascii values.
		ascii_message = ""
		for i in self.message:
			i = str( ord( i ) )
			
			while len( i ) < 3:
				i = "0" + i
			ascii_message += i

		# Breaking message into blocks.
		blocks = []
		message_count = 0
		
		while message_count < len( ascii_message ):
			block_x = ''
			
			# Sets the length of blocks to a random number < modulus.
			block_data = self.byte_block_len - 11

			# Insuring that the last block doesn't go out of range.
			if len( ascii_message ) - message_count < block_data:
				block_data = len( ascii_message ) - message_count
			
			# Assembling blocks.
			for l in range ( message_count, message_count + block_data ):
				block_x += ascii_message[ l ]
			
			blocks.append( block_x )

			message_count += block_data
	
		self.message = blocks
		return self.message

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def ublock( self ):
		"""
		Takes blocks in self.blocks and fuses them together into a string of 
		integers. It then converts the message into ascii characters.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			
			self.message:	list/array
			---------------------------


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.message:	str

		"""
		unascii = ""
		unblock = ""
		
		# Fuseing the blocks
		for b in self.message:
			for i in b:
				unblock += i

		# Converting message back into text.
		for i in range( 2, len( unblock ), 3 ):
			ascii_val = int( unblock[ i - 2 ] + unblock[ i - 1 ] + unblock[ i ] )
			unascii += chr( ascii_val )
		
		self.message = unascii

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------		
	
	def v1_5_like_padding(self):
		"""
		Modifies the blocks in self.blocks to have a length equal to
		the value of self.deci_block_len.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.message:			list/array


			self.deci_block_len:	int


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.message:	list/array

		"""

		padded_blocks = []
		
		# Decimal digit length of padding
		for b in self.message:
			print int(b).bit_length() / 8, " b bytes 1"
			#pad_len = self.deci_block_len - len( b ) - len( str( self.byte_block_len ) )
			#padding = random.randint( 1, pow( 2, pad_len ) )

			# bug: pad_len / 8 can cause a float.
			pad_len = self.byte_block_len - ( int( b ).bit_length() / 8 ) - 11
			padding = int( os.urandom( pad_len / 8 ).encode( 'hex' ), 16 )
			
			print int( b ).bit_length() / 8, " byte block"
			print pad_len, " pad len"
			print padding.bit_length() / 8, " padding byts"

			# Making sure that padding fills lenght of y
			while len(str ( padding ) ) < pad_len: 
				padding = str( padding ) + "0"
			
			# Making sure that y is three integers long for accurate reading and removal later
			while len( str( pad_len ) ) < 3:
				pad_len = "0" + str( pad_len )
			
			# Attaching padding.
			padded_blocks.append( str( padding ) + b + str( pad_len ) )
		
		self.message = padded_blocks
			
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def strip_pad( self ):
		"""
		Removes v1_5_like_padding from blocks in self.blocks
		

		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.message:	list/array


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.message:	list/array

		"""
		clean_blocks = []
		
		for b in self.message:
			pad_len = ""

			#  Extracting padding indicator from the block
			for o in range( len( b ) - 3, len( b ) ):
				pad_len += b[ o ]
			
			# Getting length of data
			dat = len( b ) - int( pad_len ) - 3
			
			# Extracting data from padded block
			new_b = ""
			for i in range( int(pad_len), len( b ) - 3 ):
				new_b += b[ i ]
			
			# Data with padding removed
			clean_blocks.append( new_b )

		self.message = clean_blocks

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def hash( self ):
		"""
		Runs blocks in self.blocks though a one-way hash function.


		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.blocks:	list/array
		

			self.key_ring:	dict


		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.message: list/array

		"""	
		secrets = []
		
		for b in self.message:
			do = pow( int( b ), self.key_ring[ 'lock' ], self.key_ring[ 'modulus' ] )
			secrets.append( do )
		
		self.message = secrets

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def uhash( self ):
		"""
		Runs blocks in self.blocks though a one-way hash function
		that unhashes blocks hashed by 'RSA.hash'
		

		--------------------------------------------------------
		Parameters
		--------------------------------------------------------
			self.blocks:	list/array
		

			self.key_ring:	dict
		

		--------------------------------------------------------
		Modifies:
		--------------------------------------------------------
			self.message: list/array

		"""	
		secrets = []
		
		for b in self.message:
			undo = pow( b, self.key_ring[ 'key' ], self.key_ring[ 'modulus' ] )
			secrets.append( str( undo ) )
		
		self.message = secrets

###############################################################################
###############################################################################
###############################################################################

###############################################################################

# ------------------ Testing Area ------------------

# ------------------ RSA_Keys Testing ------------------

"""
p_test = RSA_Keys(identifier="p_testing")

p_test.get_primes()
p_test.get_primes()
#print p_test.primes
#print ''

p_test.key_gen()
print''
print p_test.key_ring
print''

p_test.save_keys()

print p_test.public_key()


#"""
# ------------------------------------------------------
# block() test

#"""
access = open( 'RSA_keys.json', 'r' )
access_dict = json.load( access )
access.close()

inigo = "Hello, my name is Inigo Montoya! You killed my father. Prepare to die!"

hello = RSA( message=inigo, key_ring=access_dict[ 'RSA' ][ '00x' ] )
#hello = RSA(message=inigo, identifier="hello")

hello.save_keys()
#print hello.public_key()
#print''

#print hello.key_ring[ 'bit_size' ]

hello.block()
print ''
print hello.message
print ''

hello.v1_5_like_padding()
print ''
print hello.message
print ''

hello.hash()
print ''
print hello.message
print ''

hello.uhash()
print ''
print hello.message
print ''

hello.strip_pad()
print ''
print hello.message
print ''

hello.ublock()
print ''
print hello.message
print ''

#"""
# ------------------ encyption & decyption test ------------------

"""
access = open('RSA_keys.json', 'r')

access_dict = json.load(access)

#print len(str(access_dict['RSA']['001']['key']))
#print len(str(pow(2,256)))
access.close()


#    4 bit len ==    2
#    8 bit len ==    3
#   16 bit len ==    5
#   32 bit len ==   10
#   64 bit len ==   20
#  128 bit len ==   39
#  256 bit len ==   78
#  512 bit len ==  155
# 1024 bit len ==  309
# 2048 bit len ==  617
# 4096 bit len == 1234
# --------------------------------------------------------


rand = os.urandom( 256 ).encode( 'hex' )

rand = int(rand, 16 )
print rand
print miller_rabin(rand, 65)

#"""