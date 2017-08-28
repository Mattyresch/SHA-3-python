
from utils import *

def main():
##    print("0101001101010011010100110101001101010011010100110101001101010011 This is the original")

    rightShift('1100101000110101', 8)
    newShift('1100101000110101', 8)
    rightShiftNew('1100101000110101', 8)
##    leftShift('0101001101010011010100110101001101010011010100110101001101010011', 15)
##    rightShift('0101001101010011001101011100111000110101110011100101001101010011', 15)
##    newShift('0101001101010011001101011100111000110101110011100101001101010011', 15)
##    for x in range(0, 24):
##        triangleNumber(x)
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
    Keccac(input_list, capacity, state, A)

    remainder = len(binrep)%rate
    print("Remainder for %d bit blocks: %d"%(rate, remainder))
    return

if __name__ == '__main__':
    main()
