import math
import socket

def send_file(file_name, buffer_size = 1024):
    fin = open(file_name, 'r')

    lines = fin.readlines()
    #print(f"Initial lines: {lines}")
    
    split_data = split_into_chunks(buffer_size, lines)
    #print(f"Split lines: {split_data}")

    return split_data

def split_into_chunks(buffer_size, lines):
    new_lines = []

    for line in lines:
        if len(line) < buffer_size:
            new_lines.append(line)
            #print("Line is less than buffer_size")
        else:
            rng = int(math.ceil(len(line) / buffer_size))
            #print("Range = " + str(rng))

            for i in range(1, rng + 1):
                index = ((i - 1) * buffer_size, i * buffer_size)
                
                #print(f"Index = {index}")

                if index[1] >= len(line):
                    index = (index[0], len(line))
                    print(f"Index is out of bounds \n New index = {index}") 

                new_line = line[index[0]:index[1]]
                #print(f"\t Line: {new_line}")
                new_lines.append(new_line)

    return new_lines




