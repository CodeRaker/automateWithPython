""" The Toolbox module is written by Peter Hecht Glad and contains the following tools to assist with scripting Linux infrastructure: """

# Command Executor
def runcmd(command):
    CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return CMD.stdout.read()

# Port Check
def checkport(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip,port))
    return result

# IP Syntax Validator
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True

# Commentor and appender
def comment_and_append(path, start_identifier, text_to_append):
    with open(path) as infile:
        with open(path + '.new', 'w') as outfile:
            for line in infile:
               if line.rstrip().startswith(start_identifier):
                   outfile.write('#' + line + '\n')
               else:
                   outfile.write(line + '\n')
            outfile.write(text_to_append + "\n")
            runcmd('mv ' + path + ' ' + path + '.old')
            runcmd('mv ' + path + '.new ' + path)

def are_packages_installed(packages):
    packages = packages.split(' ')
    packages_not_installed = []
    for package in packages:
        if '[installed]' in runcmd('apt list ' + package):
            print('[+] ' + package + ' is installed')
        else:
            print('[-] ' + package + ' is not installed')
            packages_not_installed.append(package)
    return packages_not_installed
