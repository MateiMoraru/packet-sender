import socket, sys, encrypt, getpass
import send_file as sf

def send(msg):
    message = encrypt.encrypt(msg, KEY, False, '')
    s.send(message.encode(ENCODING))


def recv():
    recieved = s.recv(BUFFER_SIZE).decode(ENCODING)
    message = encrypt.decrypt(recieved, KEY, False, '')
    
    if '-w' in message:
        message = response(message.replace('-w', ''))
        print(message)

    message = response(message)

    return message


def login(count):
    user = input("Username: ")
    pwd = getpass.getpass("Password: ")

    send(f"{user}|||{pwd}")
    response = recv().split(' ')
    
    if response[1] == "Logged":#isinstance(response[0], int):# "Logged":
        admin = True
        USER = user
        print("CONNECTED")
        ID = response[0]
        return

    elif count <= 3 :
        print("Wrong Credentials")
        login(count + 1)
    
    if count == 3:
        send("No User Account")
        print("No User Account")
        sys.exit()
        return
        


def help_prompt():
    msg = ['',
           'mkdir+R4 <dir> - Create A Directory',
           'cd+R4 <location> - Change Directory',
           'rmdir+R4 <dir> - Remove a Directory',
           'rmfile+R4 <file> - Remove a File',
           'send+R4 <message> - Send a message to the console\n\t Use -s To Save It In The Server Log File',
           'ls+R4 - List The Directories/Files in the current location',
           'add-admin+R4 <username> <password> - Add A New Admin',
           'send-file+R4 <file|files> - Sends The File To The Server'
           'get-file+R4 <file|files> - Downlaods The Selected Files From The Server '
           '+R4+R2kill+R4 - Kill The Program',
           '']
    print('_' * len(msg[6]))

    for i in range(0, len(msg)):
        print(response('+B3' + msg[i] + '+R4'))


def download_file(last_recv, file_name):
    file_name = file_name.split(' ')[1:len(file_name) - 1]
    current_file = 0
    file = ""

    while "DONE!" not in last_recv:
        file += last_recv
        last_recv = recv()

        if "DONE" in last_recv and not "DONE!" in last_recv:
            try:
                fout = open(file_name[current_file], 'w')
            except:
                print(f"{file_name} Doesn't Exist")

            fout.write(file)
            fout.close()

            file = ""
            last_recv = ""
            current_file += 1
        
    print(f"{COLORS[3][1]}{file}{COLORS[5][1]}")


def send_file(file_name): #TODO: Multiple Files
    if isinstance(file_name, str):
        try:
            data = sf.send_file(file_name, BUFFER_SIZE)
        except:
            print(f"{file_name} Doesn't Exist")
        
        for chunk in data:
            send(chunk)

    else:
        for file in file_name:
            try:
                data = sf.send_file(file, BUFFER_SIZE)
            except:
                print(f"{file} Doesn't Exist")
            
            for chunk in data:
                send(chunk)
            send("DONE")

    send("DONE!")


def response(data):
    for color in COLORS:
        if color[0] in data:
            
            data = data.replace(color[0], color[1])
    
    return data


IP_ADDR = "192.168.0.199"
PORT = 8080
BUFFER_SIZE = 1024 * 10
ENCODING = "UTF-8"
KEY = 256
USER = ""
ID = -1
path = ''

COLORS = [["+NEWLINE", '\n'], ["+TAB", '\t'], ['+R2', '\033[91m'], ['+B3', '\033[34m'], ['+P5', '\033[35m'], ['+R4', '\033[0m']]

if len(sys.argv) > 2:
    IP_ADDR = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    print(f"No ip and port provided, running on default {IP_ADDR}:{PORT}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDR, PORT))

admin = False
login(1)

if admin:
    print("Logged in successfully")

while True:
    print(f"\n{path}> ", end='')
    command = input()
    
    if command.split(' ')[0] == 'kill':
        send("QUITTING")
        s.close()
        sys.exit()
    
    elif command.split(' ')[0] == 'help': 
        help_prompt()

    elif command.split(' ')[0] == 'send-file':
        send(str(ID) + ' ' + command)
        file_name = command.split(' ')[1]
        send_file(file_name)
        data = recv()
    
    else:
        send(str(ID) + ' ' + command)

        data = recv()#response(recv())

        if command.split(' ')[0] == "cd":
            path = data

        elif command.split(' ')[0] == 'get-file':
            download_file(data, command)
