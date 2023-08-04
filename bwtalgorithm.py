__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"

MINIMUM_ASCII = 36

import copy

class BWTCode:
    def __init__(self, word='', encoded_string=''):
        self.word = word
        self.cyclic_word = []
        self.encoded_string = encoded_string
        self.rank = [-1] * (126 - 36 + 1)
        self.decoded_string = ""
        self.occurrence = [[0] * (126 - 36 + 1)]

    def create_cyclic(self):
        word = self.word
        for i in range(len(word)):
            string = "".join([word[i:], word[:i]])
            self.cyclic_word.append(string)
        self.cyclic_word.sort()

    def rank_and_occurrence(self):
        temp_word = self.word
        temp_word = "".join(sorted(temp_word))
        rank = 0
        for i in temp_word:
            # put the rank to the list during the first encounter of that letter
            if self.rank[ord(i) - MINIMUM_ASCII] == -1:
                self.rank[ord(i) - MINIMUM_ASCII] = rank
            # add one each time in order to get the rank for different letter
            rank += 1

    def rank_occurrence_decode(self):
        temp_word = self.encoded_string
        temp_word = "".join(sorted(temp_word))
        rank = 0
        for i in temp_word:
            if self.rank[ord(i) - MINIMUM_ASCII] == -1:
                self.rank[ord(i) - MINIMUM_ASCII] = rank
            rank += 1

    def bwt_encoding(self):
        self.create_cyclic()
        self.rank_and_occurrence()
        temp_list = []
        # get the last letter for each cyclic order
        for i in self.cyclic_word:
            temp_list.append(i[-1])
        self.encoded_string = "".join(temp_list)
        return self.encoded_string

    # p.s. complexity = O(n*(126-36+1)) since the list is copied each time but when processing large string,
    # it will be more efficient that using count() to specific index (since it requires O(n^2) time)
    def bwt_occurrence(self):
        # 2D list where each row represent each index and each column represent the letter
        occurrence_bwt_pos = self.occurrence[0]
        encoded_str = self.encoded_string
        # the occurrence is count up to i - 1, so last letter is not counted, hence loop for n-1 times
        for i in range(1, len(encoded_str)):
            alphabet = encoded_str[i - 1]
            updated_occurrence_bwt_pos = copy.deepcopy(occurrence_bwt_pos)
            updated_occurrence_bwt_pos[ord(alphabet) - MINIMUM_ASCII] += 1
            occurrence_bwt_pos = updated_occurrence_bwt_pos
            self.occurrence.append(occurrence_bwt_pos)
        return self.occurrence

    def bwt_decoding(self):
        self.rank_occurrence_decode()  # find rank
        self.bwt_occurrence()  # find position
        encoded_string = self.encoded_string
        self.decoded_string = []  # since '$' will be removed later, I don't include it rather than stripping it later
        # start from the first letter of the encoded string
        current_position = encoded_string[0]
        position_index = 0
        while current_position != "$":  # condition to stop is when '$' encountered
            self.decoded_string.append(current_position)
            current_alpha_ord = ord(current_position) - MINIMUM_ASCII
            # rank + occurrence up till current index
            next_position = self.rank[current_alpha_ord] + self.occurrence[position_index][current_alpha_ord]
            # change letter to the next letter
            current_position = encoded_string[next_position]
            position_index = next_position
        # join then reverse the decoded string
        self.decoded_string = "".join(self.decoded_string)
        return self.decoded_string[::-1]

