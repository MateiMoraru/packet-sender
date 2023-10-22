import sys
import string

chars = ' ' + string.printable
chars = chars.replace(string.whitespace, '')# + ' '
#chars += ' '
def write_to_file(file_name, data, mode=' '):
    ext = ""
    if mode == '-d' :
        ext = '.dec'
    else:
        ext = '.enc'

    fout_name = file_name.split('.')[0] + ext
    if mode == ' ':
        #print("File: " + file_name)
        fout_name = file_name
    fout = open(fout_name, 'w')
    fout.write(data)
    fout.close()

def encrypt(data, key, save, file_name):
    new_data = ""

    #for i in range(0, len(data)):
    for j in range(0, len(data)):
        for k in range(0, len(chars)):
            if data[j] == chars[k]:
                index = k + key // (len(chars) + 1)

                while index >= len(chars):
                    index -= len(chars) - 1

                new_data += chars[index]

    #print("\n" in chars)
    #print(new_data)
    if save:
        #print(new_data)
        write_to_file(file_name, new_data)
    else:
        write_to_file(file_name, new_data, '-e')
    #print("Finished encrypting " + file_name)

    return new_data


def decrypt(data, key, save, file_name):
    new_data = ""

    #for i in range(0, len(data)):
    for j in range(0, len(data)):
        for k in range(0, len(chars)):
            if data[j] == chars[k]:
                index = abs(k - key // (len(chars) + 1))# - 0 

                while index >= len(chars):
                    index -= len(chars) - 1
                        #print(index)
                new_data += chars[index]

    if save:
        write_to_file(file_name, new_data)
    else:
        write_to_file(file_name, new_data, '-d')
    #print("Finished decrypting " + file_name)

    return new_data


mode = ""
file_name = ""
key = ""
fin = ""
new_data = ""
data = ""

def run():
    print('-' * 100)

    if len(sys.argv) < 4:
        print("WRONG USAGE")
        print("Correct Syntax: python ecrypt.py < -d/-e > < file_name > < key >")
        print('-' * 100)
        sys.exit()

    mode = sys.argv[1]
    file_name = sys.argv[2]
    key = int(sys.argv[len(sys.argv) - 1])
    fin = open(file_name, 'r')
    new_data = ""
    data = ""

    if "," in file_name:
        file_name = file_name.split(",")
        print(file_name)

        for i in range(0, len(file_name)):
            #if file_name[i][len(file_name[i])] == ',':

            fin = open(file_name[i], 'r')
            data = fin.readlines()
            if mode == '-d':
                decrypt()
            else:
                encrypt()
    else:
        data = fin.readlines()

        if mode == '-d':
            decrypt(data, key, True, file_name)
        else:
            encrypt(data, key, True, file_name)
    
    #if mode == '-d':
    #    decrypt()
    #else:
    #    encrypt(data, key, True)

    print("Listening for commands...")
    print("Type -h for help")

    while True:
        command = input('> ')
        argv = command.split(' ')

        if command == '-h':
            print()
            msg = ["Type -d <file_name> <key> for decryption", "Type -e <file_name> <key> for encryption", "Type -k to kill program", 'For multiple files, restart the program and separate them by using " | "']
            print('*' * (len(msg[3]) + 3))
    
            for message in msg:
                print('*' + message, end='')
                print(' ' * (len(msg[3]) - len(message)), '*')

            print('*' * (len(msg[3]) + 3))
            print()
        elif command == '-k':
            print("Quitting Program")
            print('-' * 100)
            sys.exit()
        elif '-d' in command or '-e' in command:
            if len(argv) > 2:
                file_name = argv[1]
                key = int(argv[2])
                if '-d' in command:
                    decrypt()
                else:
                    encrypt()
            else:
                print("Missing arguments")

    print('-' * 100)

if __name__ == "__main__":
    run()
