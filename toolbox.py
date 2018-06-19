""" The Toolbox module is written by Peter Hecht Glad and contains the following tools: """

import socket, subprocess, os, sys

##########################################################################################################################
# Optional modules from requirements.txt are ignored if non-existent
##########################################################################################################################
optional_modules = ['paramiko']
for module in optional_modules:
    try:
        import paramiko
    except ImportError:
        pass

##########################################################################################################################
# Command Executor
# Example: toolbox.run_command('ls /', True) """
##########################################################################################################################
def run_command(command, verbose):
    try:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        if verbose:
            print('[+] Showing result of command: ' + command)
            print(CMD.stdout.read())
        return CMD.stdout.read()
    except Exception as e:
        sys.stderr.write('[-] ' + e)

##########################################################################################################################
# Port Check
# Example: toolbox.check_tcp_port('10.10.10.1', 80)
##########################################################################################################################
def check_tcp_port(ip, port, verbose):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip,port))
        if verbose:
            if not result:
                print('[+] TCP port: ' + str(port) + ' is open on ' + str(ip))
            else:
                print('[-] TCP port: ' + str(port) + ' is closed on ' + str(ip))
        return not result
    except Exception as e:
        sys.stderr.write('[-] ' + e)
        return False

##########################################################################################################################
# IP Syntax Validator
# Example: toolbox.check_ipv4_syntax('8.8.8.8')
##########################################################################################################################
def check_ipv4_syntax(address, verbose):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            if verbose:
                print('[-] ' + address + ' is not a valid IPv4 address')
            return False
        return address.count('.') == 3
    except socket.error:
        if verbose:
            print('[-] ' + address + ' is not a valid IPv4 address')
        return False
    if verbose:
        print('[+] ' + address + ' is a valid IPv4 address')
    return True

##########################################################################################################################
# Loops through given file and comments lines in and appends a provided string or replaces strings depending on mode
# Example: toolbox.file_editor('comment', '/etc/ntp.conf', 'pool ', 'pool myserver', False)
##########################################################################################################################
def file_editor(mode, filepath, line_startswith, text_to_add, verbose):
    if verbose and mode == 'replace':
        print('[+] Writing to file: ' + filepath + ', looking to replace lines starting with: ' + line_startswith + ' with: ' + text_to_add)
    elif verbose and mode == 'comment':
        print('[+] Writing to file: ' + filepath + ', looking to comment in lines starting with: ' + line_startswith + ' and appending this: ' + text_to_add)
    try:
        with open(filepath) as infile:
            with open(filepath + '.new', 'w') as outfile:
                for line in infile:
                   if line.startswith(line_startswith):
                        line = line.strip('\n')
                        if mode == 'comment':
                            outfile.write('#' + line + '\n')
                            if verbose:
                                print('[#] Commented in this line: ' + line)
                        if mode == 'replace':
                            outfile.write(text_to_add + '\n')
                            if verbose:
                                print('[R] Replaced this line: ' + line)
                   else:
                       outfile.write(line + '\n')
                #Appending text to end of file if comment mode
                if mode == 'comment':
                    outfile.write(text_to_add + '\n')
                    if verbose:
                        print('[+] Appended this to file: ' + text_to_add)
                run_command('mv ' + filepath + ' ' + filepath + '.old', False)
                run_command('mv ' + filepath + '.new ' + filepath, False)
                if verbose:
                    print('[+] Backed up original config file to ' + filepath + '.old')
    except Exception as e:
        sys.stderr.write('[-] ' + e)

##########################################################################################################################
# Writes a new file
# Example: toolbox.file_writer('/etc/ntp.conf', 'text', False)
##########################################################################################################################
def file_writer(filepath, text_to_add, verbose):
    if verbose:
        print('[+] Writing to file: ' + filepath)
    if os.path.exists(filepath):
        outfile_name = filepath + '.new'
        if verbose:
            print('[!] File already exists. Backing up to: ' + filepath + '.old')
    else:
        outfile_name = filepath
    try:
        with open(outfile_name, 'w') as outfile:
            for line in text_to_add.split('\n'):
                outfile.write(line + '\n')
            if outfile_name.endswith('.new'):
                run_command('mv ' + filepath + ' ' + filepath + '.old', False)
                run_command('mv ' + filepath + '.new ' + filepath, False)
    except Exception as e:
        sys.stderr.write('[-] ' + e)


##########################################################################################################################
# Reads contents of a file into object
# Example: data = toolbox.file_reader('/etc/ntp.conf')
##########################################################################################################################
def file_reader(filepath):
    try:
        with open(filepath) as file:
            data = file.read()
            if verbose:
                print('[+] Read file: ' + filepath)
            return data
    except Exception as e:
         sys.stderr.write('[-] ' + e)

##########################################################################################################################
# Takes a list object and checks if apt package is installed and returns two list objects
# Example: list = ['mlocate', 'telnet']; toolbox.apt_check_packages(list, True)
##########################################################################################################################
def apt_check_packages(packages, verbose):
    packages_installed = []
    packages_not_installed = []
    try:
        for package in packages:
            if '[installed]' in run_command('apt list ' + package, False):
                if verbose:
                    print('[+] ' + package + ' is installed')
                packages_installed.append(package)
            else:
                packages_not_installed.append(package)
                if verbose:
                    print('[-] ' + package + ' is not installed')
        return packages_installed, packages_not_installed
    except Exception as e:
        sys.stderr.write('[-] ' + e)

##########################################################################################################################
# Takes a list object and installs apt packages one by one
# Example: list = ['mlocate', 'telnet']; toolbox.apt_install_packages(list, True)
##########################################################################################################################
def apt_install_packages(packages, verbose):
    packages_installed, packages_not_installed = apt_check_packages(packages, verbose)
    try:
        for package in packages_not_installed:
            if verbose:
                print('[+] Installing ' + package)
            run_command('apt install -y -qq -o=Dpkg::Use-Pty=0 ' + package, False)
    except Exception as e:
        sys.stderr.write('[-] ' + e)

##########################################################################################################################
# Takes a list object and runs the provided action against systemctl
# Example: list = ['apache2', 'networking']; toolbox.service(list, 'restart', False)
##########################################################################################################################
def service(services, action, verbose):
    try:
        for service in services:
            run_command('systemctl {} {}'.format(action, service), False)
            if verbose:
                print('[+] {} service: {}'.format(action.capitalize(), service))
    except Exception as e:
        sys.stderr.write('[-] ' + e)

##########################################################################################################################
# Execute remote SSH command and sudo (requires paramiko module installed)
# Example: run_ssh_command('10.10.10.1', 22, 'username', 'password', 'systemctl start apache2', True)
##########################################################################################################################
def run_ssh_command(server, port, user, password, command, verbose):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port, user, password)
        transport = ssh.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command("sudo -k " + command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(password +'\n')
        stdin.flush()
        if verbose:
            print('Host: ' + server)
            for line in stdout.read().splitlines():
                print(line)
    except Exception as e:
        sys.stderr.write('[-] ' + e)  
