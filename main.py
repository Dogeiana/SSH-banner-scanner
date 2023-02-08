import socket
import sys
import signal

ipadder = []

failed = 0
passed = 0
total = 0

debian = 0
ubuntu = 0
dropbear = 0
cisco = 0
ross = 0
raspbian = 0
fbsd = 0
other = 0

def results():
    print(f"""
Info:
Ubuntu = [{ubuntu}]
Debian = [{debian}]
DropBear = [{dropbear}]
Cisco = [{cisco}]
ROSSSH = [{ross}]
Raspberry = [{raspbian}]
FreeBSD = [{fbsd}]
Other = [{other}]

Status:
Failed = [{failed}]
Success = [{passed}]
Total = [{total}]
    """)

def signal_handler():
    results()
    sys.exit(0)

def getbanner(host, port):
    global ubuntu, debian, other, dropbear, cisco, ross, raspbian ,fbsd, total, failed, passed

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    success = False
    total += 1
    try:
        s.connect((host, port))
        banner = s.recv(1024).decode()
        s.shutdown(socket.SHUT_RD)
        success = True
    except Exception:
        failed +=1

    if success == True:
        s.close()
        if "SSH-2.0" in banner:
            passed += 1
            banner = banner.replace('\n', '')
            print(f"\x1b[38;5;85m{host} \x1b[38;5;190m---> \x1b[96m{banner}\033[0m")
            if "Ubuntu" in banner:
                ubuntu += 1
            elif "Debian"in banner:
                debian += 1
            elif "ROSSSH" in banner:
                ross += 1
            elif "Cisco" in banner:
                cisco += 1
            elif "FreeBSD" in banner:
                fbsd += 1
            elif "dropbear" in banner:
                dropbear += 1
            elif "raspbian" in banner:
                raspbian += 1
            else:
                other += 1
            with open("sshb", 'a') as w:
                w.write(f"{host}\n")
        else:
            failed += 1

if len(sys.argv) < 3:
    print(f"Usage: python3 {sys.argv[0]} <list> <port>")
    sys.exit()

try:
    client = open(sys.argv[1], "r").readlines()
except FileNotFoundError:
    print("File not found")
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

for host in client:
    if not str(host) == '\n':
        host = host.replace('\n', '')
        #getban(host)
        ipadder.append(host)

port =  int(sys.argv[2])

for host in ipadder:
    getbanner(host, port)

results()
