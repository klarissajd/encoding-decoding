__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"

import sys

from bwtalgorithm import BWTCode
from eliascode import EliasCode
from huffmancode import HuffmanCode



def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line


INPUT_WORD = read_file(sys.argv[1])[0] + '$'
MINIMUM_ASCII = 36
BIT_TO_BYTE = 8
BIN_ASCII_LENGTH = 7


def objects_needed(word):
    # 1. Huffman tree
    huffman_obj = HuffmanCode(word)
    # huffman encoding essentially get the
    huffman_codeword = huffman_obj.huffman_codeword()

    # 2. BWT
    BWT_obj = BWTCode(word)
    bwt_encoding_string = BWT_obj.bwt_encoding()
    bwt_length = len(bwt_encoding_string)
    bwt_unique_char = []
    for i in range(len(BWT_obj.rank)):
        if BWT_obj.rank[i] != -1:
            # store as index instead of letter
            bwt_unique_char.append(i)

    huffman_tree = huffman_obj.nodes_priority_queue[0]

    return huffman_codeword, bwt_encoding_string, bwt_length, bwt_unique_char, huffman_tree


# Used to translate binary to byte every time a length of 8 is accumulated
def binary_to_bytes(binary, f):
    while len(binary) >= BIT_TO_BYTE:
        bin_convert, binary = binary[:BIT_TO_BYTE], binary[BIT_TO_BYTE:]
        int_from_bin = int(bin_convert, 2)
        f.write(int_from_bin.to_bytes(1, byteorder='big'))
    return binary


def string_encoding(word):
    f = open('bwtencoded.bin', 'wb')
    # retrieve the required attributes to run the program
    huffman_codeword, bwt_encoding_string, bwt_length, bwt_unique_char, huffman_tree = objects_needed(word)

    # length of string
    binary_string = EliasCode(number=bwt_length).elias_encoding()
    binary_string = binary_to_bytes(binary_string, f)

    # length of unique character
    binary_string = "".join([binary_string, EliasCode(number=len(bwt_unique_char)).elias_encoding()])
    binary_string = binary_to_bytes(binary_string, f)

    # loop through the unique string
    for i in bwt_unique_char:
        alpha = i + MINIMUM_ASCII
        ascii_binary = bin(alpha)[2:]

        # get the ascii in binary and do padding in order to get a length of 7
        ascii_padding = BIN_ASCII_LENGTH - len(ascii_binary)
        ascii_binary = "".join(["0" * ascii_padding, ascii_binary])

        binary_string = "".join([binary_string, ascii_binary])
        binary_string = binary_to_bytes(binary_string, f)

        # use elias encoding to get the binary representation of the integer
        binary_string = "".join([binary_string, EliasCode(len(huffman_codeword[i])).elias_encoding()])
        binary_string = binary_to_bytes(binary_string, f)

        # uses huffman encoding and retrieve from th created list instead of going down the tree each time
        binary_string = "".join([binary_string, huffman_codeword[i]])
        binary_string = binary_to_bytes(binary_string, f)

    bwt_tuple = [[bwt_encoding_string[0], 1]]
    # create a tuple based on the appearance of same letter in bwt side-by-side
    for i in range(1, len(bwt_encoding_string)):
        if bwt_encoding_string[i] == bwt_encoding_string[i-1]:
            bwt_tuple[-1][1] += 1
        else:
            bwt_tuple.append([bwt_encoding_string[i], 1])

    # get the elias and huffman encoding based on the tuple created
    for runlength in bwt_tuple:
        binary_string = "".join([binary_string, huffman_codeword[ord(runlength[0]) - MINIMUM_ASCII]])
        binary_string = binary_to_bytes(binary_string, f)

        binary_string = "".join([binary_string, EliasCode(runlength[1]).elias_encoding()])
        binary_string = binary_to_bytes(binary_string, f)

    return binary_string, f


if __name__ == '__main__':
    input_word = read_file(sys.argv[1])[0] + '$'
    binary_leftover, f = string_encoding(input_word)
    len_leftover = BIT_TO_BYTE - len(binary_leftover)
    # padding for the last set of bit (0-8) to be filled as the last byte
    if len(binary_leftover) != 0:
        binary_to_int = int(binary_leftover, 2) << len_leftover
        f.write(binary_to_int.to_bytes(1, byteorder='big'))
    f.close()
