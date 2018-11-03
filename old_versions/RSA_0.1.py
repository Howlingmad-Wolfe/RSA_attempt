#!/bin/python

### Attempt at implanting RSA ###

###		Warning!!! Don't user for real cryptographic purposes!!!!!!		###

# ------------------ Imported Modules ------------------

import random
import json


# imported items below tjos line are for testing please remove when finished 
from timeit import default_timer as timer

###############################################################################

def coprime(integer,pass_no = None): 
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
	if pass_no is None:
		pass_no = 1
	while len(coprimes) < pass_no:
		if integer <= int_co_p:
			break
		for i in coprimes:
			if int_co_p % i == 0:
				int_co_p += 1
		if pow(integer,1,int_co_p) == 0:
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

def miller_rabin(n , pass_no = None):
	"""
	Runes a Probablilistic Miller-Rabin Primeality test. returns a boolean.
	
	Preformes a Miller-Rabin (Rabin-Miller) test on a given number (n).
	The test is preformed as many times as the value given for the Pass_no.
	argument. If pass_no is left blank the funtion will defalt to 1.
	Every time the test is run the "Witness" (a) value should be different.

	Parameters
	--------------------------------------------------------
	n:			int
		The number to be tested for primeality.

	Pass_no:	int
		The number of times to run the test for a given number "n".

	Returnes
	--------------------------------------------------------
	Boolean (True or False)
		
	"""
	
	if pass_no == None:
		pass_no = 1
	
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
	using randomly selected large Fibonacci numbers (unsure might look into it). 
	However, I suspect that doing so my reduce the pool of prime numbers this 
	script can access thereby makeing the prime factors of a RSA key generated 
	by this script easier to find (even if only slightly).

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
	sieve = [i for i in range(3,100)]
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

def keys(bit_size=None):
	"""
	Returns a RSA public and privet key pair. If no input is given for the 
	bit_size argument, the function defalts to a bit length of 2048 for the 
	large number n component of the key and lock.

	Parameters
	--------------------------------------------------------
	bit_size:	int
		Length of key to be generated.

	Returnes
	--------------------------------------------------------
	dictionary
		contains: 		
		pub_n (product of two large primes)
		phi_n (prime1 - 1 multiplied by prime2 - 1)
		Lock (coprime of pub_n and phi n)
		key (coprime of pub_n and phi n, and the mathmatical complement of the lock)

	"""
	if bit_size is None:
		bit_size = 2048
	
	# In order for the public composit number to be equal to bit_size 
	# the prime numbers must be half the size?
	bit_size = bit_size / 2 
	
	lower = pow(10,len(str(pow(2,bit_size)))- 1)
	pa = find_prime(lower, pow(2,bit_size)) 
	pb = find_prime(lower, pow(2,bit_size)) 
	n = pa * pb
	phi_n = (pa - 1) * (pb - 1)
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
	k = 1
	while pow(k*phi_n+1, 1, e) != 0: #(k*phi_n + 1) % e
		k += 1
	
	d = (k*phi_n + 1)/e
	test = pow(e*d,1,phi_n)
	if test != 1:
		print "There is a problem with your decyption exponent"
	
	return {"pub_n" : n, "phi_n" : phi_n, "lock" : e, "key" : d}

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def keys2(identifier, bit_size=None):
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
	if bit_size is None:
		bit_size = 2048
	
	# In order for the public composit number to be equal to bit_size 
	# the prime numbers must be half the size?
	bit_size = bit_size / 2
	
	lower = pow(10,len(str(pow(2,bit_size)))- 1)
	pa = find_prime(lower, pow(2,bit_size)) 
	pb = find_prime(lower, pow(2,bit_size)) 
	n = pa * pb
	phi_n = (pa - 1) * (pb - 1)
	
	
	# Generating public coprime
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
	
	#Generating Private coprime
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
	
	# (remove when resolved) The below line may be a slightly bloated way of doing things.
	key_file = open('RSA_keys.json', 'r')
	h = json.load(key_file)
	key_file.close()
	h['RSA'].update({str(identifier) : {"pub_n" : n, "phi_n" : phi_n, "lock" : e, "key" : d}})

	key_holder = open('RSA_keys.json', 'w')
	json.dump(h, key_holder, ensure_ascii=False, encoding ='UTF-8', indent=4)
	key_holder.close()
	
	return None

test = keys2("003", 128)

a_key_ring = open('RSA_keys.json', 'r')
a_key_ring_dict = json.load(a_key_ring)
print a_key_ring_dict['RSA']['002']
a_key_ring.close()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------ under construction ------------------

def block(message,size=None):
	"""
	Takes a "message" input and brakes it down into blocks of a given "size".
	If the "size" argument is left blank it defaults to 128 bits.
	
	Returns a list consisting of the origenal message devided into string-blocks 
	of length = "size"

	Parameters
	--------------------------------------------------------
	message:
		type = str
		default = no default (if left blank, will throw error)

		The data that will be devided into blocks.

	size:
		type = int
		default = 128

		The size of the block into which the data will be devided.

	Returnes
	--------------------------------------------------------
	list/array
		
	"""
	if size == None:
		size = 128
	size = len(str(pow(2,size)))
	platter = []
	start = 0
	while start < len(str(message)):
		cooked = ""
		if len(str(message)) < start + size:
			size = len(str(message)) - start
		for i in range(start,start + size):
			cooked += message[i]
		print""
		print cooked
		platter.append(cooked)
		start += size
	return platter

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def standard_pad(message_block,key_size):
	"""

	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	message_block = str(message_block)
	key_size = len(str(pow(2,key_size)))
	block_size = len(message_block)
	diff = str(key_size - block_size)
	
	if key_size < block_size:
		return "Error! block must be smaller than key"
	else:	
		while block_size < key_size - len(diff):
			message_block = message_block + '0'
			block_size = len(message_block)
		message_block = message_block + diff
		print len(message_block)
		return message_block

#print standard_pad("hello world", 128)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def xor (message_block, init):
	"""

	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	pass
#	message_block = ''.join(format(ord(x), 'b') for x in message_block)
#	init = bin(init)
#	count = len(init) - 1
#	print message_block
#	# exclusive or (There's got to be a better way of doing this!!!!)
#	output = ""
#	for s in range(len(message_block)-1,0,-1):
#		l = message_block[s]
#		i = init[count]
#		if l == '1' and i == '1':
#			output = '0'+ output
#		elif l == '0' and i == '0':
#			output = '0'+ output
#		elif l =='1' or i == '1':
#			output = '1'+ output
#		else:
#			output = '1'+ output
#		count -= 1
#	return output

#xor funtion test

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


def RSA_encrypt(message_block, key_ring):
	pass
	"""

	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	int_message = [str(ord(x)) for x in message_block]
	message_as_ints = ""
	for i in int_message:
		if len(i) < 3:
			while len(i) < 3:
				i = '0' + i
		message_as_ints += i
	message_as_ints = int(message_as_ints)
	return pow(message_as_ints, key_ring['lock'], key_ring['pub_n'])

#test = keys(1028)
#text = "hello world"
#secret = RSA_encrypt(text, test)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def RSA_decrypt(message_block, key_ring):
	"""
	
	
	Parameters
	--------------------------------------------------------
	
	Returnes
	--------------------------------------------------------

	"""
	raw_message = str(pow(message_block, key_ring['key'], key_ring['pub_n']))
	processing = []
	output = ""
	for i in range(2,len(raw_message),3):
		processing.append(int(raw_message[i-2] + raw_message[i-1] + raw_message[i]))
	for s in processing:
		output += chr(s)
	return output

print ''
#print RSA_decrypt(secret, test)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------




###############################################################################

# ------------------ Testing Area------------------


# ------------------ encyption & decyption test ------------------



# --------------------------------------------------------