__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"


class EliasCode:
    def __init__(self, number=None):
        self.number = number
        self.number_to_binary = []
        self.number_to_binary_string = ""
        self.decoded_integer = 0

    def elias_encoding(self):
        if self.number == 1:
            return str(self.number)
        else:
            num_in_bin = bin(self.number)[2:]
            self.number_to_binary.append(num_in_bin)
            # length of binary
            digit_count = len(num_in_bin)
            # get the binary of the length - 1 and change the leftmost bit to 0 and repeat the steps
            while digit_count > 1:
                new_binary = bin(digit_count - 1)
                remove_b = new_binary[2:]
                change_zero = "0" + remove_b[1:]
                self.number_to_binary.append(change_zero)
                digit_count = len(change_zero)

        # joining in reverse to get the right encoding
        for i in self.number_to_binary:
            self.number_to_binary_string = "".join([i, self.number_to_binary_string])
        return self.number_to_binary_string

    def elias_decoding(self, binary_string, buffer_object):
        # add the length of binary recursively each time until encounter the actual binary (check zero as leftmost)
        if binary_string[0] == "0":
            binary_string = "".join(["1", binary_string[1:]])
            integer_representation = int(binary_string, 2)
            self.elias_decoding(buffer_object.take_bits(integer_representation + 1), buffer_object)
        # condition if it reaches the real number (starts with 1)
        else:
            self.decoded_integer = int(binary_string, 2)
        return self.decoded_integer
