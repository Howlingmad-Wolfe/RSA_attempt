#!/bin/python

# python version:	python 2.7.x
# Auther:			Howlingmad-Wolfe

### Functions for finding prime numbers and coprime numbers ###

# 	________________________ Warning and Disclaimer ________________________

###			Not for use in real cryptographic aplications!	 	###
###		The auther will take no responsability for compromized	###
###		security due to the use of this script! This script  	###
###		is intended only to be an academic exercise for the 	###
###		auther!													###


# ------------------ Imported Modules ------------------

import random # change all instances of random.randint() to random.SystemRandom() or os.urandom()?
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
	if number_1 <= 1 or number_2 <= 1:
		return False
	elif number_1 < number_2:
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
def preFilter(seed, filter=None):
    """ Simple devision test to filter"""
    if pow(seed,1,2) == 0:
        seed += 1
    
    if filter == None:
        filter = [ i for i in range( 3, 100, 2 ) ]
    
    for divisor in filter:
        if pow(seed,1,divisor) == 0:
            
            seed = preFilter(seed + 2, filter)
            break
    return seed

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
	if number == 2:
		return True
	
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
	if number <= 1:
		return False
	elif number == 2:
		return True
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
			
			if 100 < loop_stop: # 100 is kind of a magic number here. I wonder if there's a better way of doing this.
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

def prime(size, primeCandidate=None):
    """ Returns a prime number"""
    if primeCandidate == None:
        primeCandidate = int(os.urandom(size).encode( 'hex' ), 16)

    if pow(primeCandidate,1,2) == 0: # pre-filtering even numbers.
        primeCandidate += 1
    
    while True:
        primeCandidate = preFilter(primeCandidate)
        if miller_rabin(primeCandidate, 10)==True:
            break
        else:
            primeCandidate += 2

    return primeCandidate