The goal of this project is to practice programming in python and to gain an understanding of RSA encryption. Towards that end, objectives should be achieved using as few imported modules as reasonably possible.

This program should be able to:

1:) Create a fully functioning RSA public and private key pair.
    
    A:) Find 2 prime numbers of a given size.
            (bonus objective: find a way to make this process able to use multiple processor cores)
    
    B:) Multiply those numbers and their respective phi functions (prime - 1) together to get 
        a key and the number of numbers that are coprime to the key. 
            (prime_number - 1) = phi function of the prime number/all numbers coprime with prime.
            ([prime_a - 1] * [prime_b - 1] = phi_of_key).

    C:) Use the key and its phi function to generate a public and private exponent 
            (these two number must be coprime to key and phi_of_key and be complementary to each other.)


2:) Store the key as a dictionary in a .json file for use at a later time.
        (it should be noted that, in a real world application this file should probably 
        be password encrypted or safeguarded in some similar manner. For the now, this
        will be considered outside the scope of this project.)

    A:) Each RSA_key dictionary should be appended to a larger RSA dictionary within the .json file.


3:) Use the key and public exponent to encrypt a message (str or int).
        (asymmetric cryptography [such as RSA] is usually used to exchange a symmetric cryptography key.
        At this time RSA is the focus of this exercise. Therefor, symmetric key generation will be considered
        outside the scope of this exercise.)
    
    A:) Messages that are to be encrypted should be divided into "blocks" smaller than the RSA key size but not so small
        that it creates a vulnerability. (Just because it’s an exercise doesn't mean one shouldn't care.)

    B:) It would be a good idea to attempt to apply a cryptographic salt to the message before hashing it with the key.


4:) Use the key and private exponent to decrypt a message that was encrypted by its corresponding public key pair.