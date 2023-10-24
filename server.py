import socket, sys, os, datetime, encrypt
import send_file as sf

def recv(conn):
    message = conn.recv(BUFFER_SIZE).decode(ENCODING)
    return encrypt.decrypt(message, KEY, False, '')


def send(conn, msg): #TODO: Maybe '+R4' in just specific cases
    message = encrypt.encrypt(msg + '+R4', KEY, False, '')
    conn.send(message.encode(ENCODING))

    print("SENDING TO CONN: " + msg)


def get_time():
    return datetime.datetime.now()


def log(msg):
    LOG.write(msg + '\n')
    print(msg + '\n')


def login(conn):
    global USER
    user_info = recv(conn)

    for data in ADMINS:
        if data == user_info:
            send(conn, f"{len(USER)} Logged In")
            USER.append(user_info.split('|||')[0])
            user_paths.append('')
            log(f"> {USER[len(USER)-1]} Has Logged In")
            return

    if user_info not in data: 
        send(conn, "Wrong credentials")

        while user_info not in data:
            login(conn)


def write_to_file(msg, file):
    fout = open(file, "w")
    fout.write(msg)
    fout.close()


def get_file(conn, file_name, current_path): #TODO: Multiple Files
    if isinstance(file_name, str):
        data = sf.send_file(current_path + '/' +  file_name, BUFFER_SIZE)

        for chunk in data:
            send(conn, chunk)

        log("> {USER[len(USER)-1]} Downloaded A File Saved as {file_name}") 
    else:
        for file in file_name:
            data = sf.send_file(current_path + '/' +  file, BUFFER_SIZE)

            for chunk in data:
                send(conn, chunk)
            
            #send(conn, "DONE")
        
            log(f"> {USER[len(USER)-1]} Downloaded A File Saved As {file}")
    
    send(conn, "DONE!")

def send_file(file_name, current_path, save): #TODO: Multiple Files
    print(isinstance(file_name, str))
    if isinstance(file_name, str):
        print(0)
        raw_file = ""
        data = recv(conn)
        print(1)
        
        try:
            while data != "DONE!":
                print("!!!SEX: " + data)
                raw_file += data
                
                data = recv(conn)

                if "DONE!" in data:
                    break
        except:
            print("eroare")

        if save:
            fout = open(current_path + '/' + file_name, 'w')
            fout.write(raw_file)
            fout.close()

def process_commands(conn, command):
    try:
        global path
        ID = int(command[0])
        current_path = PATH + user_paths[ID]
        
        if command[1] == 'add_admin':
            fout = open("login", 'a')
            fout.write(command[2]+'|||'+command[3] + '\n')
            log(f">{USER[ID]} Added A New Admin ({command[1]})")
            fout.close()
            send(conn, "Successfully Added Admin\n-w")

        elif command[1] == 'get_file':
            file_name = command[2]
            
            if len(command) > 3:
                file_name = command[2:len(command)]
               
            get_file(conn, file_name, current_path)

        elif command[1] == 'send_file':
            log("SA MOARA MA SA")
            save = False
            file_name = command[2:len(command)]
            print("PULA n PIZDA")
            if file_name[len(file_name) - 1] == '-s':
                file_name = file_name.pop()
                save = True

            print("SEX")
            if len(command) > 3:
                pass
            print("SALUT COAIE")
            send_file(file_name, current_path, save)

        elif command[1] == 'mkdir':
            temp_path = current_path + command[2]
            os.mkdir(temp_path)

            log(f">{USER[ID]} Created A New Directory ({temp_path})")
            send(conn, f"Successfully Created Directory +B3{command[2]}\n-w")

        elif command[1] == 'rmdir':
            #print(command[2])
            os.rmdir(current_path + '/' + command[2])
            log(f">{USER[ID]} Removed directory {user_paths[ID] + '/' + command[2]}")
            send(conn, f"Successfully Removed +R2{command[2]}-w")

        elif command[1] == 'rmfile':
            #temp_path = curre
            os.remove(current_path + '/' + command[2])

        elif command[1] == 'cd':
            if len(command) == 2:
                user_paths[ID] = ''

            elif os.path.exists(PATH + '/' + command[2]):
                user_paths[ID] += '/' + command[2]
                send(conn, user_paths[ID])
            else:
                pass   
            #send(conn, user_paths[ID])

        elif command[1] == 'ls':
            data = os.listdir(PATH + user_paths[ID])
            files = ""

            for i in range(0, len(data)):
                file = data[i]
                if os.path.isdir(PATH + user_paths[ID] + '/' + file):
                    files += '+B3' + file + ' '
                else:
                    files += '+P5' + file + ' '

            #files += '+R4'
            send(conn, files + '-w')
            #print(f"Files: {files}")

        elif command[1] == 'send':
            msg = ''
            tmsg = command[2:len(command)]
           
            print(command[len(command) - 2])

            if command[len(command) - 2] == ">>":
                
                file_name = PATH + user_paths[ID] + '/' + command[len(command) - 1]
                
                tmsg = tmsg[:len(tmsg)-2]

                for text in tmsg:
                    msg += text + ' '
                
                write_to_file(msg, file_name)
                log(f"> {USER[ID]} Wrote To File ({file_name})")
                send(conn, f'+TABSuccessfully Wrote To File +B3"{file_name}"-w')

            else:
                for text in tmsg:
                    msg += text + ' '

                send(conn, f"You: {msg}-w")
           
            log(f"{USER[ID]}> {msg}")

        elif command[1] == 'QUITTING':
            log(f"> {USER[ID]} Quit The Session")
        else:
            send(conn, "Unknown command, try running +P5help-w")
    except Exception as e:
        print(e)
        send(conn, f"\nWrong command arguments, try running +P5help+NEWLINE+TAB+R2ERROR: {e}-w")


IP_ADDR = "192.168.0.199"
PORT = 8080
BUFFER_SIZE = 1024 * 10
ENCODING = "UTF-8"
LOG = open("server-log.log", 'a')
ADMINS = open("login", 'r').readlines()
KEY = 256
USER = []
PATH = 'server/files'

user_paths = [PATH]

for i in range(0, len(ADMINS)):
    ADMINS[i] = ADMINS[i][:-1]

if len(sys.argv) > 2:
    IP_ADDR = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    print(f"No ip and port provided, running on default {IP_ADDR}:{PORT}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP_ADDR, PORT))
s.listen()

log(f"\n \t\t\t NEW INSTANCE \n")
log(f"> Server is up and running on {IP_ADDR}:{PORT} at {get_time()}")

conn, addr = s.accept()

with conn:
    log(f"Connected by {addr}\n")
    login(conn)

    while True:
        try:
            command = recv(conn).split(' ')
            process_commands(conn, command)

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            sys.exit()

