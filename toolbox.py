""" The Toolbox module is written by Peter Hecht Glad and contains the following tools: """

import socket, subprocess

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
    CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    if verbose:
        print(CMD.stdout.read())
    return CMD.stdout.read()

##########################################################################################################################
# Port Check
# Example: toolbox.check_tcp_port('10.10.10.1', 80)
##########################################################################################################################
def check_tcp_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip,port))
        return not result
    except Exception as e:
        return False

##########################################################################################################################
# IP Syntax Validator
# Example: toolbox.check_ipv4_syntax('8.8.8.8')
##########################################################################################################################
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

##########################################################################################################################
# Loops through given file and comments lines in and appends a provided string or replaces strings depending on mode
# Example: toolbox.file_editor('/etc/ntp.conf', 'pool ', 'pool myserver', False)
##########################################################################################################################
def file_editor(mode, filepath, line_startswith, text_to_add, verbose):
    with open(filepath) as infile:
        with open(filepath + '.new', 'w') as outfile:
            for line in infile:
               if line.rstrip().startswith(line_startswith):
                    if mode = 'comment':
                        outfile.write('#' + line + '\n')
                    if mode = 'replace':
                        outfile.write(text_to_add + '\n')
                    if verbose:
                        print('[V] Edited line: ' + line)
               else:
                   outfile.write(line + '\n')
            if mode = 'comment':
                outfile.write(text_to_add + "\n")
            if verbose:
                print('[V] Appendended: ' + text_to_add)
            run_command('mv ' + filepath + ' ' + filepath + '.old', False)
            run_command('mv ' + filepath + '.new ' + filepath, False)
            if verbose:
                print('[V] Backed up original config file to ' + filepath + '.old')

##########################################################################################################################
# Takes a list object and checks if apt package is installed and returns two list objects
# Example: list = ['mlocate', 'telnet']; toolbox.apt_check_packages(list, True)
##########################################################################################################################
def apt_check_packages(packages, verbose):
    packages_installed = []
    packages_not_installed = []
    for package in packages:
        if '[installed]' in run_command('apt list ' + package, False):
            if verbose:
                print('[V] ' + package + ' is installed')
            packages_installed.append(package)
        else:
            packages_not_installed.append(package)
            if verbose:
                print('[V] ' + package + ' is not installed')
    return packages_installed, packages_not_installed

##########################################################################################################################
# Takes a list object and installs apt packages one by one
# Example: list = ['mlocate', 'telnet']; toolbox.apt_install_packages(list, True)
##########################################################################################################################
def apt_install_packages(packages, verbose):
    packages_installed, packages_not_installed = apt_check_packages(packages, verbose)
    for package in packages_not_installed:
        if verbose:
            print('[V] Installing ' + package)
        run_command('apt install -y -qq -o=Dpkg::Use-Pty=0 ' + package, False)

##########################################################################################################################
# Takes a list object and runs the provided action against systemctl
# Example: list = ['apache2', 'networking']; toolbox.service(list, 'restart', False)
##########################################################################################################################
def service(services, action, verbose):
    for service in services:
        run_command('systemctl {} {}'.format(action, service), False)
        if verbose:
            print('[V] {} service: {}'.format(action.capitalize(), service))

##########################################################################################################################
# Execute remote SSH command and sudo (requires paramiko module installed)
# Example: run_ssh_command('10.10.10.1', 22, 'username', 'password', 'systemctl start apache2', True)
##########################################################################################################################
def run_ssh_command(server, port, user, password, command, verbose):
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
