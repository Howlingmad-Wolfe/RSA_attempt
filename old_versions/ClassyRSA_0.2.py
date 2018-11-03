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
###############################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def coprime( number_1, number_2 ):
	"""


	Parameters
	--------------------------------------------------------


	Returnes
	--------------------------------------------------------
	list:


	"""

	if number_1 < number_2:
		a = number_2
		b = number_1
	else:
		a = number_1
		b = number_2

	while b != 0:
		t = b
		b = pow( a, 1, b)
		a = t
		#print a, " a"

	if a != 1:
		return False
	else:
		return True
	
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def fermat_prime( p, pass_no = 1 ):
	"""
	Preforms a Fermat primality test on a given number "p"
	a "pass_no" number of times. pass_no defalts to 1 if left blank.

	Parameters
	--------------------------------------------------------
	p:			int
		The number to be tested for primeality.

	Pass_no:	int
		The number of times to run the test for a given number "p"
	Returnes
	--------------------------------------------------------
	Boolean (True or False)

	"""
	if p < 2 or pow( p, 1, 2 ) == 0:
		return False
	
	count = 0
	while count < pass_no:
		x = random.randint( 3,p - 1 )
		
		if coprime( p, x ) == False:
			return False
		
		else:		
			return pow( x, p-1, p ) == 1

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def miller_rabin( n , pass_no = 1 ):
	"""
	Runes a Probabilistic Miller-Rabin Primeality test. returns a boolean.
	
	Preformes a Miller-Rabin (Rabin-Miller) test on a given number (n).
	The test is preformed as many times as the value given for the Pass_no.
	argument. If pass_no is left blank the funtion will defalt to 1.
	Every time the test is run the "Witness" (a) value should be different.

	Parameters
	--------------------------------------------------------
	n:		int
		The number to be tested for primeality.

	Pass_no:	int
		The number of times to run the test for a given number "n".

	Returnes
	--------------------------------------------------------
	Boolean (True or False)
		
	"""
	# Filtering out any values that are even or equil to 1.
	if n <= 2:
		return False
	elif pow( n, 1, 2 ) == 0:
		return False
	
	# finding the 
	k = 0
	while pow ( n-1, 1, pow( 2, k + 1 ) ) == 0:
		k += 1
	
	for i in range( pass_no ):
		
		# first part of test
		m = ( n - 1) / pow( 2, k )
		a = random.randint( 2, n - 1 )
		test = pow( a, m, n )
		
		loop_stop = 0
		while test != n - 1:
			
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
				
				test = pow( a, m, n )
	return True

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def find_prime( bit_size = 1024 ):
	"""
	Returns a probable prime number of length "bit_size".

	Generates a random number of length "bit_size". and runs a series of tests 
	(a simple sieve, the 'fermat_prime' test, and the 'miller_rabin' test) to 
	determine if the number is a prime number. if the number is determined to 
	be composit the function decrements the number to the closest odd number 
	and repeats the tests until a number passes the tests.

	Parameters
	--------------------------------------------------------
	bit_size:	int
		
		desired length, in bits, of prime.

	Returnes
	--------------------------------------------------------
	int:
		Probable prime number within the bounds of the function.
	
	"""
	sieve = [ i for i in range( 3, 100, 2 ) ]
	test_passes = 0
	prime = int( os.urandom( bit_size / 8 ).encode( 'hex' ), 16)
	
	if pow( prime, 1, 2 ) == 0:
		prime -= 1
		
	is_prime = False
	while is_prime == False:

		sieve_pass = False
		while sieve_pass == False:
			#print "Start sieve"
			for i in sieve:
				if pow( prime, 1, i ) == 0:
					prime -= 2
					test_passes += 1
					break
			sieve_pass = True

		if fermat_prime( prime, 1 ) == False:
			#print "passed sieve test but is composite"
			prime -= 2
			test_passes += 1

		elif miller_rabin( prime, 10 ) == False:
			#print "is probably a Carmichael number"
			prime -= 2
			test_passes += 1

		else:
			#print prime, "Is Probably Prime"
			is_prime = True

	return prime

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

###############################################################################
###############################################################################
###############################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def keys( identifier, bit_size=2048 ):
	"""
	Generates a RSA public and privet key pair and places it in a .json file. 
	If no input is given for the bit_size argument, the function defalts to a 
	bit length of 2048 for the large composite number component of the public 
	and private key sets.

	Parameters
	--------------------------------------------------------
	identifyer: str
		Used as the dict. key for the RSA key generated by the function
	
	bit_size:	int
		Length of key to be generated.

	Returnes
	--------------------------------------------------------
	None

	"""
	# In order for the public composit number to be equal to bit_size 
	# the prime numbers must be half the size?
	
	pa = find_prime( bit_size / 2 )
	pb = find_prime( bit_size / 2 )
	
	modulus = pa * pb
	phi_modulus = ( pa - 1 ) * ( pb - 1 )
	
	# Generating public exponent aka "the lock"
#	lock = random.randint( 65537, 100000 )
#	while coprime( phi_modulus, lock ) != True:
#		lock += 1

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
		
	components = {  "bit_size" : bit_size, 
					"modulus" : modulus, 
					"phi_modulus" : phi_modulus, 
					"lock" : lock, 
					"key" : key
					}

	# Placing keys in a file so that they don't have to be generated every time the program is run.
	try:
		key_file = open( 'RSA_keys.json', 'r' )
		h = json.load( key_file )
		key_file.close()
	
	except IOError: # if this script is moved to python 3.x this will need to be changed to FileNotFoundError.
		key_file = open( 'RSA_keys.json', 'w+' )
		key_file.close()
		h = {}
		h.update({'RSA' : { str( identifier ) : components } } )
	
	h[ 'RSA' ].update({ str( identifier ) : components } )
	key_holder = open( 'RSA_keys.json', 'w' )
	json.dump( h, key_holder, ensure_ascii = False, encoding = 'UTF-8', indent = 4 )
	key_holder.close()
	
	return components


#a_key_ring = open('RSA_keys.json', 'r')
#a_key_ring_dict = json.load(a_key_ring)
#print a_key_ring_dict['RSA']['00x']
#a_key_ring.close()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def send_pub_key( identifyer ):
	"""

	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	master_keys = open( 'RSA_keys.json', 'r' )
	pub_key = json.load( master_keys )
	master_keys.close()
	
	modulus = pub_key[ 'RSA' ][ str( identifyer ) ][ 'modulus' ]
	lock = pub_key[ 'RSA' ][ str( identifyer ) ][ 'lock' ]

	return { 'modulus' : modulus,
				'lock' : lock 
				}

#print send_pub_key('005')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


###############################################################################
###############################################################################
###############################################################################


class RSA( object ):
	"""
	Takes a message and an RSA key (as a dictionary) and encrypts
	or decrypts the message.
	
	Parameters
	--------------------------------------------------------
	message: str

		the message to be encrypted

	key_ring: dict

		This is the RSA key.
		dictionary keys should be:

			'bit_size'		(Is size of modulus in bits)
			'modulus'		(Is the devisor to be used in the hash and unhash functions)
			'phi_modulus'	(Is the number used to create the public and private exponent. Not used in this class)
			'lock'			(Is the public exponent)
			'key'			(Is the private exponent)
	
	Class Variables
	--------------------------------------------------------
	blocks:	list/array
		Stores the message as a list of blocks
	
	self.bit_block_len: int
		length, in bits, of a given block in blocks. This is 
		determined by the key_ring[ 'bit_size' ]

	self.self.deci_block_len:
		length, in decimal, of a given block in blocks. This is 
		determined by using self.bit_block_len


	Functions
	--------------------------------------------------------
	ublock

	v1_5_like_padding

	strip_pad

	hash

	uhash


	Returnes
	--------------------------------------------------------

	"""
	
	def __init__( self, message, key_ring ):
		
		self.message = message
		
		self.key_ring = key_ring
		
		self.bit_block_len = self.key_ring[ 'bit_size'] / 8 - 42
		
		self.deci_block_len = len( str( pow( 2, self.bit_block_len ) ) )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def __repr__( self ):
		return "(s%, s%, s%)" % ( self.message, self.key_ring, self.message_blocks )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------	
	
	def block( self ):
		"""
		Takes a "message" input and brakes it down into blocks of a given "size".
		If the "size" argument is left blank it defaults to 128 bits.
		
		Returns a list consisting of the origenal message devided into string-blocks 
		of length = "size"


		Parameters
		--------------------------------------------------------
		self.message:
			
			type = str
			default = no default (if left blank, will throw error)

			The data that will be devided into blocks.

		self.key_ring:
			
			type = dict

			Usees the modulus ('modulus') to set The size of the blocks into which
			the data will be devided.


		Modifies:
		--------------------------------------------------------
		self.blocks: list/array
			
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
			unpadded = self.deci_block_len - 4
			block_data = random.randint( unpadded / 2, unpadded )
			
			# Insuring that the last block doesn't go out of range.
			if len( ascii_message ) - message_count < block_data:
				block_data = len( ascii_message ) - message_count
			
			# Assembling blocks.
			for l in range ( message_count, message_count + block_data ):
				block_x += ascii_message[ l ]
			
			blocks.append( block_x )
			self.message = blocks
			# Next block.
			message_count += block_data
		
		return self.message


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def ublock( self ):
		"""
		Takes blocks in self.blocks and fuses them together into a string of integers. 
		It then converts the message into ascii characters.
		
		Parameters
		--------------------------------------------------------
		self.blocks:	list/array


		Modifies:
		--------------------------------------------------------
		self.blocks:	list/array

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


		Parameters
		--------------------------------------------------------
		self.blocks:			list/array

		self.deci_block_len:	int


		Modifies:
		--------------------------------------------------------
		self.blocks:	list/array

		"""

		padded_blocks = []
		
		# Decimal digit length of padding
		for b in self.message:
			y = self.deci_block_len - len( b ) - len( str( self.bit_block_len ) )
		#	y = self.bit_block_len - len( b ) - len( str( self.bit_block_len ) )
			padding = random.randint( 1, pow( 2, y ) )

		#	padding = int( os.urandom( y ).encode('hex'), 16)		

			# Making sure that padding fills lenght of y
			while len(str ( padding ) ) < y: 
				padding = str( padding ) + "0"
			
			# Making sure that y is three integers long for accurate reading and removal later
			while len(str(y)) < 3:
				y = "0" + str( y )

			# Attaching padding.
			padded_blocks.append( str( padding ) + b + str( y ) )
		
		self.message = padded_blocks
			
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def strip_pad( self ):
		"""
		Removes v1_5_like_padding from blocks in self.blocks
		
		Parameters
		--------------------------------------------------------
		self.blocks:	list/array


		Modifies:
		--------------------------------------------------------
		self.blocks:	list/array

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
		Runs blocks in self.blocks though a oneway hash function.

		
		Parameters
		--------------------------------------------------------
		self.blocks:	list/array
		
		self.key_ring:	dict


		Modifies:
		--------------------------------------------------------
		self.blocks: list/array

		"""	
		secrets = []
		
		for b in self.message:
			do = pow( int( b ), self.key_ring[ 'lock' ], self.key_ring[ 'modulus' ] )
			secrets.append( do )
		
		self.message = secrets

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def uhash( self ):
		"""
		Runs blocks in self.blocks though a oneway hash function
		that unhashes blocks hashed by 'RSA.hash'
		
		Parameters
		--------------------------------------------------------
		self.blocks:	list/array
		
		self.key_ring:	dict
		
		
		Modifies:
		--------------------------------------------------------
		self.blocks: list/array

		"""	
		secrets = []
		
		for b in self.message:
			undo = pow( b, self.key_ring[ 'key' ], self.key_ring[ 'modulus' ] )
			secrets.append( str( undo ) )
		
		self.message = secrets

###############################################################################
###############################################################################
###############################################################################


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------




###############################################################################

# ------------------ Testing Area ------------------


# block() test
#"""
access = open( 'RSA_keys.json', 'r' )
access_dict = json.load( access )
access.close()

inigo = "Hello, my name is Inigo Montoya! You killed my father. Prepare to die!"

hello = RSA( message=inigo, key_ring=access_dict[ 'RSA' ][ '00x' ] )
print hello.key_ring[ 'bit_size' ]

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

#keys( '001', 128 )
#keys( '002', 256 )
#keys( '003', 512 )
#keys( '004', 1024 )
#keys( '005', 2048 )
#keys( '006', 4096 )
#keys( "007", 8192 )

#print keys("00x", 2048)





"""
access = open('RSA_keys.json', 'r')

access_dict = json.load(access)

#print len(str(access_dict['RSA']['001']['key']))
#print len(str(pow(2,256)))
access.close()



test =  zip_up_pad("Hello, my name is Inigo Montoya! You killed my father. Prepare to die", access_dict['RSA']['003']['modulus'])

print test

ex = unzip_pad(test)
print ""
print ex

#print RSA_string_encrypt("Hello, my name is Inigo Montoya! You killed my father. Prepare to die",access_dict['RSA']['003'])

#print len(str(pow(2,2)))

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

