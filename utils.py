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

def rightShiftNew(bit, shift, wordsize):
    new = [0]*wordsize
    for x in range(0, wordsize):
        temp = x + shift
        if(temp>=wordsize):
            temp = (temp%wordsize)
            new[temp] = bit[x]
            temp = 0
        elif(temp < wordsize):
            new[temp] = bit[x]
            temp = 0
    result=''
    for i in new:
        result += i
    print(result)
            
#change 16 to desired word size
def rightShift(bits, seq_no):
    new = [0]*16
    check = 16 - seq_no
    shift = seq_no
    for x in range(0, 16):
        if(x == check):
            new[0] = bits[x]
        elif(x > check):
            shift = 0
            shift = (x+shift) - 16
            new[abs(shift)] = bits[x]
        elif(x < check):
            new[x+shift] = bits[x]
    result =''
    for i in new:
        result+=str(i)
    print(result + " right shift 8 bits")

def newShift(bits, seq_no):
    temp = 16 - seq_no
    slice1 = bits[temp:]
    slice2 = bits[0:temp]
    #print("bits in order: " + bits)
    #print("end slice: " + slice1)
    #print("start slice: " + slice2)
    print(slice1 + slice2 + " shifted: 8 bits")

def leftShift(bits, seq_no):
    new_word = [0]*64
    if(seq_no > 64):
        shift = (seq_no % 64)
    else:
        shift = seq_no
    
    for x in range(0, 64):
        if(x < shift):
              remainder=shift-x
              new_word[64-remainder] = bits[x]
        else:
            new_word[x-shift] = bits[x]
    result = ''
    for i in new_word:
        result += i
    print(result + " left shift")
    return(result)

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

def triangleNumber(x):
    temp = 0
    if(x==0):
        return
    elif(x>=0):
        temp = (x*(x+1))/2
        print(str(temp))
        return(temp)

def Keccac(item_list, capacity, state, A):
    for i in item_list:
        #extend P so that is same length as block_size
        to_be_appended = '0' * capacity
        newstr = i + to_be_appended
        #xor with state S
        result = xor(state, newstr)
        ##construct 3d array form 2d array
        for x in range (0,5):
            for y in range(0, 5):
                for z in range(0, 64):
                    A[x,y,z] = result[64*((5*y)+x) + z]
##        print("State: " + state)
        print("Current chunk: " + newstr)
##        print("XOR'd string: " + result)
        state = permutation(A)

def computeParity(A):
    p_a = numpy.zeros((5,64))
    
    for y in range(0,5):
        for x in range(0,5):
            for z in range(0,64):
                if(A[x, y, z] ==1.0):
                    p_a[x,z] = p_a[x,z] + 1

    return p_a

def applyParity(A, p_a):
    for y in range(0, 5):
        for x in range(0, 5):
            for z in range(0, 64):
                print("3d Array Value at : (" + str(x) + "," + str(y) + "," + str(z) + ") = " + str(A[x, y, z]))
                print("Parity Array Value: " + str(p_a[x-1, z]))
                print(str(int(A[x, y, z])))
                A[x, y, z] = xor(str(int(A[x, y, z])), str(int(p_a[x-1, z])))
                try:
                    A[x, y, z] = xor(str(int(A[x, y, z])), str(int(p_a[x+1, z-1])))
                except IndexError as e:
                    A[x, y, z] = xor(str(int(A[x, y, z])), str(int(p_a[x-1, z-1])))
                print("New 3d Array Value: " + str(A[x, y, z]))

def bitwiseCombine(A):
    for x in range(0, 5):
        for y in range(0, 5):
            for z in range(0, 64):
                temp = A[x, y, z]
                temp2 = bitwiseAnd(A[x, y+1, z], A[x, y+2, z])
                A[x, y, z] = xor(temp, temp2)
                
def bitwiseAnd(x, y):
    if(x==1.0):
        x == 0.0
    elif(x==0.0):
        x == 1.0
    if(x == y):
        if(x == 1.0):
            return 1.0
        else:
            return 0.0
    else:
        return 0.0

def permutation(A):
    count = 0
    colcount=0
    p_a = computeParity(A)
    applyParity(A, p_a)
##
##    for x in range(0,5):
##        for z in range(0,64):
##            if(p_a[x,z]%2==0):
##                print(p_a[x,z])
##                print("Coumn at (" + str(x) + ", " + str(z) + ") has even parity")
##                p_a[x,z] = 1.0
##            else:
##                print(p_a[x,z])
##                print("Coumn at (" + str(x) + ", " + str(z) + ") has odd parity")
##                p_a[x,z] = 0.0
##    
##    for z in range(0,64):
##        for y in range(0,5):
##            for x in range(0,5):
##                if(A[x, y, z] == 1.0):
##                    count+=1
##                print(A[x, y, z])
##            if(count%2==0):
##                print("Even Parity for column")
##                #for x in range(0,5):
##                    
##            else:
##                print("Odd parity for column")
##            colcount+=1
##            print("Column " + str(colcount))    
##    for x in range(0,5):
##        for y in range(0,5):
##            count += 1
##            print(str(count))
##            print(A[x, y])
