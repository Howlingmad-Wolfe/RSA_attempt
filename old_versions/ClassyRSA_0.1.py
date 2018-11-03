#!/bin/python

# python version:	python 2.7.x
# Auther:			Jesse Wolfe, jessewolfe7c6@gmail.com

### An attempt at implanting the RSA algorithm ###

# 	________________________	Warning	________________________

###			Not for use in real cryptographic aplications!	 	###
###		The auther will take no responsability for compromized	###
###		security do to the use of this script! This script  	###
###		is intended only to be an academic exercise for the 	###
###		auther!													###


# ------------------ Imported Modules ------------------

import random # change all instances of random.randint() to random.SystemRandom()?
import json
#import os

# The following are imported for multithreading purposes.
#from multiprocessing import pool, cpu_count


# imported items below this line are for testing please remove when finished 
#from timeit import default_timer as timer

###############################################################################


###############################################################################
###############################################################################
###############################################################################


def coprime(number ,pass_no = 1): # review
	"""
	Returns a list (with lengthe equal to pass_no.
	if blank, pass_no = 1) of coprimes for a given integer.

	Parameters
	--------------------------------------------------------
	Interger:	int
		Number to get coprimes of.

	Pass_no:	int
		Number of coprimes to list.

	Returnes
	--------------------------------------------------------
	list:
		list of coprimes with "interger".

	"""
	coprimes = []
	int_co_p = 2
	while len(coprimes) < pass_no:
		if number <= int_co_p:
			break
		for i in coprimes:
			if int_co_p % i == 0:
				int_co_p += 1
		if pow(number,1,int_co_p) == 0:
			int_co_p += 1
		else:
			coprimes.append(int_co_p)
			int_co_p += 1
	return coprimes
	
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def fermat_prime(p, pass_no = None):   
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
	if p < 2:
		return False
	if pass_no == None:
		pass_no = 1
	x = coprime(p,pass_no)
	for i in x:	
		if pow(p,1,2) == 0: # p % 2 == 0
			return False
		else:		
			return pow(i,p-1,p) == 1 # i**(p-1) % p == 1

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def miller_rabin(n , pass_no = 1):
	"""
	Runes a Probablilistic Miller-Rabin Primeality test. returns a boolean.
	
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
	
	#if pass_no == None:
		#pass_no = 1
	
	# Filtering out any values that are even or equil to 1
	
	if n < 2:
		return False
	elif n == 2:
		return True
	elif pow(n,1,2)==0:
		return False
	
	k = 1
	while pow(n-1, 1, pow(2,k)) == 0: # (n-1) % (2**k) == 0:
		k += 1
	k -= 1

	m = (n-1) / (2**k)
	a = random.randint(2,n-1)
	prob_prime = False
	ground_hog_day = 0
	
	for i in range(0,pass_no):
		while prob_prime == False:
			""" 
			The if statement below prevents an infinite loop
			that will ocure when a whitness number 'a' has a
			relationship with the number being tested such 
			that the test will never return a value equil 
			to 1 or -1. In which case, the number will not be
			prime anyway.
			"""
			if 100 <= ground_hog_day:
				return False
				break
			
			test = pow(a,m,n)	#a**m % n
			if test == 1 or test == n-1:
				if ground_hog_day == 0:
					prob_prime = True
				else:
					if test == 1:
						return False
						break
					else:
						prob_prime = True	
			else:
				a = test
				m = 2
				ground_hog_day += 1
	
	return prob_prime

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def find_prime(low,high):
	"""
	Returns a probable prime number in range 'low' to 'high'.

	Generates a random number within the range of arguments 'low' and 'high'
	and runs a series of tests (a simple sieve, the 'fermat_prime' test,
	and the 'miller_rabin' test) to determine if the number is a prime number.
	if the number is determined to be composit the function decrements the 
	number to the closest odd number and repeats the tests until a number 
	passes the tests.

	It's posable that a large prime number may be found/generated faster 
	using randomly selected large Fibonacci numbers (unsure, might look into it). 
	However, doing so will reduce the pool of prime numbers this script can 
	access, since not every prime number is with in the Fibonacci sequince. 
	I suspect that this will make the prime factors of a RSA key generated 
	by this script easier to find (even if only slightly). The computational
	benifits may outweigh the security hit.

	Parameters
	--------------------------------------------------------
	low:	int
		lower bounds for the output of the function.
	
	high:	int
		upper bounds for the output of the function.

	Returnes
	--------------------------------------------------------
	int:
		Probable prime number within the bounds of the function.
	
	"""
	sieve = [i for i in range(3,100,2)]
	test_passes = 0
	prime = random.randint(low, high)
	
	if pow(prime,1,2) == 0:
		prime -= 1
		
	is_prime = False
	while is_prime == False:
		if prime < low:
			prime = random.randint(low, high)
		else:
			sieve_pass = False
			while sieve_pass == False:
				#print "Start sieve"
				for i in sieve:
					if pow(prime,1,i) == 0:
						prime -= 2
						test_passes +=1
						break
				sieve_pass = True

			if fermat_prime(prime,1) == False:
				#print "passed sieve test but is composite"
				prime -= 2
				test_passes +=1

			elif miller_rabin(prime,10) == False:
				#print "is probably a Carmichael number"
				prime -= 2
				test_passes +=1

			else:
				#print prime, "Is Probably Prime"
				is_prime = True
	return prime		


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------ under construction ------------------

def find_prime_multi(low,high):
	"""
	Returns a probable prime number in range 'low' to 'high'.

	Generates a random number within the range of arguments 'low' and 'high'
	and runs a series of tests (a simple sieve, the 'fermat_prime' test,
	and the 'miller_rabin' test) to determine if the number is a prime number.
	if the number is determined to be composit the function decrements the 
	number to the closest odd number and repeats the tests until a number 
	passes the tests.

	It's posable that a large prime number may be found/generated faster 
	using randomly selected large Fibonacci numbers (unsure, might look into it). 
	However, doing so will reduce the pool of prime numbers this script can 
	access, since not every prime number is with in the Fibonacci sequince. 
	I suspect that this will make the prime factors of a RSA key generated 
	by this script easier to find (even if only slightly). The computational
	benifits may outweigh the security hit.

	Parameters
	--------------------------------------------------------
	low:	int
		lower bounds for the output of the function.
	
	high:	int
		upper bounds for the output of the function.

	Returnes
	--------------------------------------------------------
	int:
		Probable prime number within the bounds of the function.
	
	"""
	
	sieve = [i for i in range(3,100,2)] # range cannot start at one for obvious reasons.
	prime = random.randint(low, high)
	
	if pow(prime,1,2) == 0: # filtering even numbers
		prime -= 1
	is_prime = False
	while is_prime == False:
		if __name__ == '__main__':
			egg_hunt = pool()
			p_test = egg_hunt.map(miller_rabin(prime,10),range(prime,prime - 2*cpu_count(),-2)) # line too long.
			
###############################################################################
###############################################################################
###############################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def keys(identifier, bit_size=2048):
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
	#if bit_size is None:
		#bit_size = 2048
	
	# In order for the public composit number to be equal to bit_size 
	# the prime numbers must be half the size?
	bit_size = bit_size / 2
	
	lower = pow(10,len(str(pow(2,bit_size)))- 1)
	pa = find_prime(lower, pow(2,bit_size)) 
	pb = find_prime(lower, pow(2,bit_size)) 
	n = pa * pb
	phi_n = (pa - 1) * (pb - 1)
	
	
	# Generating public coprime ! may need to adjust to get random int for a range.
	"""
	n_coprimes = coprime(n,9000)
	phi_n_coprimes = coprime(phi_n, 9000)
	e = 0
	for i in n_coprimes:
		if 0 < e:
			break
		for x in phi_n_coprimes:
			if i == x:
				e = i
				break
	"""



	# This seems to be a standard practice for defending against the low public exponent vulnerability.
	e = 65537 
	
	# Generating Private: coprime e*d is conguent to 1 (mod phi_n)
	k = 1
	while pow(k * phi_n + 1, 1, e) != 0:
		k += 1
	d = (k * phi_n + 1) / e
	
	# Testing that the private coprime was generated correctly a problem here may indicate 
	# an issue with the prime/primality test funtions(This part can probably be removed)

	test_d = pow(e * d, 1, phi_n)
	if test_d != 1:
		print "There is a problem with your decyption exponent"
		
	# Placing keys in a file so that they don't have to be generated every time the program is run.
	key_file = open('RSA_keys.json', 'r')
	h = json.load(key_file)
	key_file.close()
	h['RSA'].update({str(identifier) : {"modulus" : n, "phi_n" : phi_n, "lock" : e, "key" : d}})

	key_holder = open('RSA_keys.json', 'w')
	json.dump(h, key_holder, ensure_ascii=False, encoding ='UTF-8', indent=4)
	key_holder.close()
	
	return None

#test = keys("00x")


#a_key_ring = open('RSA_keys.json', 'r')
#a_key_ring_dict = json.load(a_key_ring)
#print a_key_ring_dict['RSA']['00x']
#a_key_ring.close()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def send_pub_key(identifyer):
	"""

	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	master_keys = open('RSA_keys.json', 'r')
	pub_key = json.load(master_keys)
	master_keys.close()
	
	modulus = pub_key['RSA'][str(identifyer)]['modulus']
	lock = pub_key['RSA'][str(identifyer)]['lock']

	return {'modulus' : modulus, 'lock' : lock}

#print send_pub_key('005')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


###############################################################################
###############################################################################
###############################################################################
# ------------------ under construction ------------------
class RSA(object):
	"""

	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	
	blocks = []
	
	def __init__(self, message, key_ring):
		self.message = message
		self.key_ring = key_ring

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def __repr__(self):
		return "(s%, s%, s%)" %(self.message, self.key_ring, self.message_blocks)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------	
	
	def block(self):
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

		Returnes
		--------------------------------------------------------
		list/array
			
		"""
		# Turning message into ascii values.
		ascii_message = ""
		for i in self.message:
			i = str(ord(i))
			while len(i) < 3:
				i = "0" + i
			ascii_message += i

		key_len = len(str(self.key_ring['modulus']))

		# Sets the length of blocks to a random number < 'modulus'
		#block_len = random.randint(key_len / 8 , key_len - 11)
		
		block_len = random.randint(256 , key_len - 11) 

		message_count = 0
		
		# Breaking message into blocks
		while message_count < len(ascii_message):
			block_x = ''
			
			# Insuring that the last block doesn't go out of range.
			if len(ascii_message) - message_count < block_len:
				block_len = len(ascii_message) - message_count
			
			# Assembling blocks
			for l in range(message_count, message_count + block_len):
				block_x += ascii_message[l]
			
			self.blocks.append(block_x)

			# Next block
			message_count += block_len
		
		return self.blocks

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def ublock(self):
		"""

		
		Parameters
		--------------------------------------------------------
		
		Returnes
		--------------------------------------------------------

		"""
		unascii = ""
		unblock = ""
		for b in self.blocks:
			for i in b:
				unblock += i

		while pow(len(unblock),1,3) != 0:
		#	print pow(len(unblock),1,3), ' is 0?'
		#	print ''
		#	print unblock
			unblock = '0' + unblock
		print len(str(unblock)), " unblock 2"
		print ''
		
		for i in range(2, len(unblock), 3):
#			print int(unblock[i-2] + unblock[i-1] + unblock[i])
			unascii += chr(int(unblock[i-2] + unblock[i-1] + unblock[i]))
		
		self.message = unascii

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------		
	
	def v1_5_like_padding(self):
		"""
		Modifies the blocks in self.blocks to have a length equal to the
		modulus component of the RSA key. 


		Parameters
		--------------------------------------------------------
		self.blocks:	list/array

		self.key_ring:	dict


		Returnes
		--------------------------------------------------------
		None
		

		specifications:
		--------------------------------------------------------
		Padding should be a random value with a decimal digit length
		of the difference of length the modulus and the length of the
		message block.
		"""
		# decimal digit length of key
		x = len(str(self.key_ring['modulus']))
		print x, " x"
		#x -= 30
		padded_blocks = []
		
		# decimal digit length of padding
		for b in self.blocks:
			y = x - len(b) - len(str(x)) 
		
			padding = random.randint(1, pow(2,y))

			# making sure that padding fills lenght of y
			while len(str(padding)) < y: 
				padding = "0" + str(padding)
			
			# making sure that y fits 2 ** 8
			while len(str(y)) < 3:
				y = "0" + str(y)

			# Attaching padding.
			padded_blocks.append(b + str(padding) + str(y))
		
		self.blocks = padded_blocks
			
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def strip_pad(self):
		"""

		
		Parameters
		--------------------------------------------------------
		
		Returnes
		--------------------------------------------------------

		"""
		clean_blocks = []
		
		for b in self.blocks:
			pad_len = ""

			# Getting length of padding
			for o in range(len(b) - 3, len(b)):
				pad_len += b[o]
			
			# Getting length of data
			dat = len(b) - int(pad_len) - 3 
			
			
			# Extracting data from padded block
			new_b = ""
			for i in range(0, dat):
				new_b += b[i]
			
			# Data with padding removed
			clean_blocks.append(new_b)
		#	print ''
		#	print clean_blocks

		self.blocks = clean_blocks

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def hash(self):
		"""

		
		Parameters
		--------------------------------------------------------
		
		Returnes
		--------------------------------------------------------

		"""	
		secrets = []
		
		for b in self.blocks:
			do = pow(int(b),self.key_ring['lock'],self.key_ring['modulus'])
			secrets.append(do)
		self.blocks = secrets

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def uhash(self):
		"""

		
		Parameters
		--------------------------------------------------------
		
		Returnes
		--------------------------------------------------------

		"""	
		secrets = []
		
		for b in self.blocks:
			undo = pow(b, self.key_ring['key'], self.key_ring['modulus'])
			secrets.append(str(undo))
		self.blocks = secrets

###############################################################################
###############################################################################
###############################################################################


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------




###############################################################################

# ------------------ Testing Area ------------------




# block() test

access = open('RSA_keys.json', 'r')
access_dict = json.load(access)
access.close()

inigo = "Hello, my name is Inigo Montoya! You killed my father. Prepare to die!"

hello = RSA(message=inigo, key_ring=access_dict['RSA']['005'])

hello.block()
#print ''
#print hello.blocks

hello.v1_5_like_padding()
#print ''
#print hello.blocks
for i in hello.blocks:
	print len(str(i)), " padded"

hello.hash()
#print ''
for i in hello.blocks:
	print len(str(i)), " hashed"

hello.uhash()
#print ''
#print hello.blocks
for i in hello.blocks:
	print len(str(i)), " un-hashed"

hello.strip_pad()
#print ''
#print hello.blocks

hello.ublock()
#print ''
print hello.message

# ------------------ encyption & decyption test ------------------

#keys('001', 128)
#keys('002', 256)
#keys('003', 512)
#keys('004', 1024)
#keys('005', 2048)
#keys('006', 4096)





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
"""