__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"

import heapq

"""
Note:
In order to operate the heapq well, I use the same function overwriting the __lt__ following GeeksForGeeks
https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/
"""

MINIMUM_ASCII = 36


class Node:
    def __init__(self, count=0, letter=""):
        # the letter of node
        self.letter = letter
        self.right = None
        self.left = None
        # count the occurrence
        self.count = count

    # done in order to do heapq
    def __lt__(self, next):
        return self.count < next.count


class HuffmanCode:
    def __init__(self, input_word="", binary=None):
        # the input word to be translated
        self.input_word = input_word
        # the binary code to be passed
        self.binary = binary
        # the leftover binary that is not code
        self.leftover_binary = ""
        # store the occurrence of string together with the letter
        self.alphabet_and_occurrence = [0] * (126 - 26 + 1)
        # store the heapq
        self.nodes_priority_queue = []
        # the encoded tree (nodes_p_q[0])
        self.encoded_tree = []
        # store the binary encoding
        self.encoding_list = [None] * (126 - 26 + 1)
        # create a decoded tree
        self.root = Node()

    # get the occurrence of string
    def get_alpha_with_occur(self):
        for i in range(len(self.input_word)):
            self.alphabet_and_occurrence[ord(self.input_word[i]) - MINIMUM_ASCII] += 1

        # collect the existing ascii and put in a heapq
        for j in range(len(self.alphabet_and_occurrence)):
            if self.alphabet_and_occurrence[j] != 0:
                count = self.alphabet_and_occurrence[j]
                node = Node(count, chr(j + MINIMUM_ASCII))
                self.nodes_priority_queue.append(node)

        heapq.heapify(self.nodes_priority_queue)

        return self.nodes_priority_queue

    def huffman_tree(self):
        self.get_alpha_with_occur()
        # create a tree until length is 1 (all has been combined)
        while len(self.nodes_priority_queue) > 1:
            new_node = Node()
            comparison_1 = heapq.heappop(self.nodes_priority_queue)
            comparison_2 = heapq.heappop(self.nodes_priority_queue)
            # put the position where lesser count is put on left side of tree and bigger on right
            if comparison_1.count <= comparison_2.count:
                new_node.left = comparison_1
                new_node.right = comparison_2
            else:
                new_node.left = comparison_2
                new_node.right = comparison_1
            # modify the node as the total count and merge the ascii
            new_node.count = comparison_1.count + comparison_2.count
            new_node.letter = "".join([comparison_1.letter, comparison_2.letter])
            # replace the 2 nodes to the 1 node created
            heapq.heappush(self.nodes_priority_queue, new_node)

    def huffman_codeword(self):
        self.huffman_tree()
        self.huffman_codeword_util(self.nodes_priority_queue[0])
        return self.encoding_list

    def huffman_codeword_util(self, node, string=""):
        # go down the tree and put it to the lookup list when a leaf is found
        if node.left is not None:
            new_string = string + "0"
            self.huffman_codeword_util(node.left, new_string)
        if node.right is not None:
            new_string = string + "1"
            self.huffman_codeword_util(node.right, new_string)
        if node.left is None and node.right is None:
            index = ord(node.letter) - MINIMUM_ASCII
            self.encoding_list[index] = string

    def huffman_encoding(self, string):
        return self.encoding_list[ord(string) - MINIMUM_ASCII]

    def huffman_decoding_tree(self, alpha, elias, binary_string):
        current_node = self.root
        for i in range(elias):
            if binary_string[i] == "0":
                # create node if it is not yet created
                if current_node.left is None:
                    current_node.left = Node()
                current_node = current_node.left
            elif binary_string[i] == "1":
                if current_node.right is None:
                    current_node.right = Node()
                current_node = current_node.right
        # put the location
        current_node.letter = alpha

    def huffman_decoding(self, current_node, binary_string, binary_buffer_object):
        # decoding when tree has been created and number of bits needed is unsure
        # stops only when it reaches the node with no child node
        while current_node.left is not None and current_node.right is not None:
            if binary_string == "0":
                current_node = current_node.left
                # take 1 bit
                binary_string = binary_buffer_object.take_bits(1)
            elif binary_string == "1":
                current_node = current_node.right
                binary_string = binary_buffer_object.take_bits(1)
        return current_node.letter, binary_string

