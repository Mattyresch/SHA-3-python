import sys
import numpy

def toBit(string):
    result = []
    for c in string:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):]+bits
        result.extend([int(b) for b in bits])
    return result

def fromBit(bits):
    chars = []
    for b in range(len(bits)//8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

#Padding function: for a given message M, pad so that it has blocks of size R, with no empty positions.
def pad(message, rate):
    string = toBit(message)
    remainder = len(string)%rate
    padding = rate - remainder
    a=''
    if(remainder==(rate-1)):
        print("Worst case; one spot left in block. Must create new block")
        to_be_appended = '1' + ('0' * (rate-1)) + '1'
        ##print(to_be_appended)
        #a=''
##        for i in string:
##            a += str(i)
##        newstring = a+to_be_appended
    elif(remainder==0):
        print("Second worst case; block is full, must create new block of size R")
        to_be_appended = '1' + ('0' * (rate-2)) + '1'
        #a = ''
##        for i in string:
##            a+=str(i)
##        newstring = a + to_be_appended
        #print("Old string: " + a + "\nNew String: " + newstring+ " " + str(len(newstring)))
    else:
        print("Standard case; fill this block")
        to_be_appended = '1' + ('0' * (padding - 2)) + '1'
        #a = ''
    for i in string:
            a+=str(i)
    newstring = a + to_be_appended    
    print("Old string: " + a + "\nNew String: " + newstring + " " + str(len(newstring)))
    return(newstring)

def xor(x, y):
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))


def permutation(A):
    count = 0
    colcount=0
    for z in range(0,64):
        for y in range(0,5):
            for x in range(0,5):
                if(A[x, y, z] == 1.0):
                    count+=1
                print(A[x, y, z])
            if(count%2==0):
                print("Even Parity for column")
                for x in range(0,5):
                    
            else:
                print("Odd parity for column")
            colcount+=1
            print("Column " + str(colcount))    
##    for x in range(0,5):
##        for y in range(0,5):
##            count += 1
##            print(str(count))
##            print(A[x,y])

def main():
    string = input("Please enter a string \n")
    binrep = toBit(string)
    A = numpy.zeros((5,5,64))
    print(binrep)
    print("Binary value of " + string)
    print("Rate in bits: " + str(len(binrep)))
    rate = int(input("Please enter a rate \n"))
    block_size = int(input("Please enter the size of a block in bits: \n"))
    state = '0' * 1600
    print("State: " + state)
    capacity = block_size - rate
    if(rate<=1):
        exit()
    padded_input = pad(string, rate)
    ##create a list from padded input, broken into blocks of size R
    input_list = [padded_input[i:i+rate] for i in range(0, len(padded_input), rate)]
 
##    for i in A:
##        print(i)
    #for each Block P, pad to be size of capacity
    for i in input_list:
        #extend P so that is same length as block_size
        to_be_appended = '0' * capacity
        newstr = i + to_be_appended
        #xor with state S
        result = xor(state, newstr)
        for x in range (0,5):
            for y in range(0, 5):
                for z in range(0, 64):
                    A[x,y,z] = result[64*((5*y)+x) + z]
##        print("State: " + state)
##        print("Current chunk: " + newstr)
##        print("XOR'd string: " + result)
        state = permutation(A)
       # state = result
    remainder = len(binrep)%rate
    print("Remainder for %d bit blocks: %d"%(rate, remainder))
    return

if __name__ == '__main__':
    main()
