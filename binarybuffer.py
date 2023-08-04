__student_name__ = "Klarissa Jutivannadevi"
__student_id__ = "32266014"


BIT_TO_BYTE = 8

class BinaryBuffer:
    def __init__(self, input_file):
        self.binary_string = ""
        self.input_file = input_file
        self.open_file = None

    def read_file(self):
        input_file = self.input_file
        f = open(input_file, 'rb')

        self.open_file = f

    def close_file(self):
        self.open_file.close()

    # take 1 byte each time called
    def take_byte(self):
        f = self.open_file
        return f.read(1)

    # return the number of bits (length of binary) based on the request of the parameter
    def take_bits(self, bits):
        # take immediately if the binary_string (usually only store 8 bits at most) suffice the length requested
        if bits <= len(self.binary_string):
            binary_taken, self.binary_string = self.binary_string[:bits], self.binary_string[bits:]
        else:
            # if the requested bits is larger than the currently read binary string
            while bits > len(self.binary_string):
                byte = self.take_byte()
                # stop running if there is no more byte to take
                if byte == b'':
                    break
                if byte != b'':
                    # take the binary representation of the byte
                    binary_representation = bin(int.from_bytes(byte, byteorder='big'))[2:]
                    # ensure that the binary taken is 8 bits for every byte
                    if len(binary_representation) < BIT_TO_BYTE:
                        padding = BIT_TO_BYTE - len(binary_representation)
                        # add the leading zeros
                        binary_representation = ''.join(["0" * padding, binary_representation])
                    self.binary_string = ''.join([self.binary_string, binary_representation])
            # once looping is finished, do the same thing as the previous one
            binary_taken, self.binary_string = self.binary_string[:bits], self.binary_string[bits:]

        return binary_taken
