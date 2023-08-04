__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"

import sys
from binarybuffer import BinaryBuffer
from eliascode import EliasCode
from huffmancode import HuffmanCode
from bwtalgorithm import BWTCode


def string_decoding(filename):
    # read file
    bin_buf_obj = BinaryBuffer(filename)
    bin_buf_obj.read_file()

    huffman_obj = HuffmanCode()
    bwt_string = ""

    # decoding elias (start from 1 string first then expand within the elias code, hence obj is needed in param)
    # elias_decoding(self, binary_string, buffer_object):
    bwt_length = EliasCode().elias_decoding(bin_buf_obj.take_bits(1), bin_buf_obj)
    bwt_unique = EliasCode().elias_decoding(bin_buf_obj.take_bits(1), bin_buf_obj)

    for i in range(bwt_unique):
        ascii_alpha = chr(int(bin_buf_obj.take_bits(7), 2))
        elias_decode = EliasCode().elias_decoding(bin_buf_obj.take_bits(1), bin_buf_obj)
        huffman_length = bin_buf_obj.take_bits(elias_decode)
        huffman_obj.huffman_decoding_tree(ascii_alpha, elias_decode, huffman_length)

    # CHECK UNTIL THE END (USING WHILE)
    # in this case for huffman, only move 1 each time
    total_run_length = 0
    while total_run_length < bwt_length:
        bwt_alpha, binary_fail_check = huffman_obj.huffman_decoding(huffman_obj.root, bin_buf_obj.take_bits(1), bin_buf_obj)
        run_length = EliasCode().elias_decoding(binary_fail_check, bin_buf_obj)
        total_run_length += run_length
        bwt_string = ''.join([bwt_string, bwt_alpha * run_length])

    bwt_obj = BWTCode(encoded_string=bwt_string)
    real_string = bwt_obj.bwt_decoding()

    # close file
    bin_buf_obj.close_file()

    return real_string


if __name__ == "__main__":
    file_name = sys.argv[1]

    output_string = string_decoding(file_name)
    with open('recovered.txt', 'w') as f:
        f.write(output_string)


