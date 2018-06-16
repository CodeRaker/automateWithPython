""" The Toolbox module is written by Peter Hecht Glad and contains the following tools: """

import socket

# Command Executor
def run_command(command):
    CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return CMD.stdout.read()

# Port Check
def check_tcp_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip,port))
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

# IP Syntax Validator
def check_ipv4_syntax(address):
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

# Loops through given file and comments lines in and appends a provided string
def file_comment_and_append(filepath, line_startswith, text_to_append):
    with open(path) as infile:
        with open(path + '.new', 'w') as outfile:
            for line in infile:
               if line.rstrip().startswith(line_startswith):
                   outfile.write('#' + line + '\n')
               else:
                   outfile.write(line + '\n')
            outfile.write(text_to_append + "\n")
            run_command('mv ' + path + ' ' + path + '.old')
            run_command('mv ' + path + '.new ' + path)

# Takes a list object and checks if apt package is installed and returns two list objects with installed and not installed packages
def apt_check_packages(packages, verbose):
    packages_installed = []
    packages_not_installed = []
    for package in packages:
        if '[installed]' in run_command('apt list ' + package):
            if verbose == True:
                print('[+] ' + package + ' is installed')
            packages_installed.append(package)
        else:
            packages_not_installed.append(package)
            if verbose == True:
                print('[-] ' + package + ' is not installed')
    return packages_installed, packages_not_installed

# Takes a list object and installs apt packages one by one
def apt_install_packages(packages, verbose):
    for package in packages:
        if verbose == True:
            print('[+] Installing ' + package)
        run_command('apt install -y -qq -o=Dpkg::Use-Pty=0 ' + package)
