""" The Toolbox module is written by Peter Hecht Glad and contains the following tools: """

import socket, subprocess, os, sys, time, getpass

##########################################################################################################################
# Optional modules from requirements.txt are ignored if non-existent
##########################################################################################################################
optional_modules = ['paramiko','requests']
for module in optional_modules:
    try:
        import paramiko
    except ImportError:
        pass

##########################################################################################################################
# Decorator function to take and print run time
# Example on function created within script (not module):
#           @toolbox.stopwatch
#           def helloworld():
#              pass
# Example on function from module:
# toolbox.network.check_tcp_port = toolbox.stopwatch(toolbox.network.check_tcp_port)
# toolbox.network.check_tcp_port('8.8.8.8', 80, True)
##########################################################################################################################
def stopwatch(function):
    def wrapper(*arg, **kw):
        t1 = time.time()
        result = function(*arg, **kw)
        t2 = time.time()
        print('[+] ' + function.__name__ + ' took ' + str(t2 - t1) + ' seconds')
        return result
    return wrapper

class network(object):
    ##########################################################################################################################
    # Port Check
    # Example: toolbox.network.check_tcp_port('10.10.10.1', 80)
    ##########################################################################################################################
    @staticmethod
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
            sys.stderr.write('[-] ' + str(e))
            return False

    ##########################################################################################################################
    # IP Syntax Validator
    # Example: toolbox.network.check_ipv4_syntax('8.8.8.8')
    ##########################################################################################################################
    @staticmethod
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
    # Execute remote SSH command and sudo (requires paramiko module installed)
    # Example: toolbox.network.ssh_command('10.10.10.1', 22, 'username', 'password', 'systemctl start apache2', True)
    ##########################################################################################################################
    @staticmethod
    def ssh_command(server, port, user, password, command, verbose):
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
            sys.stderr.write('[-] ' + str(e))

    ##########################################################################################################################
    # Get data from webpage (requires requests module installed)
    # Example: toolbox.network.get_url('http://icanhazip.com', verbose=False)
    ##########################################################################################################################
    @staticmethod
    def get_url(url, verbose):
        r = requests.get(url)
        if verbose:
            print('[+] Showing result for: ' + url)
            for line in r:
                print(line)
        return r

class file(object):
    ##########################################################################################################################
    # Loops through given file and comments lines in and appends a provided string or replaces strings depending on mode
    # Example: toolbox.file.editor('comment', '/etc/ntp.conf', 'pool ', 'pool myserver', False)
    ##########################################################################################################################
    @staticmethod
    def editor(mode, filepath, line_startswith, text_to_add, verbose):
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
            sys.stderr.write('[-] ' + str(e))

    ##########################################################################################################################
    # Writes a new file
    # Example: toolbox.file.writer('/etc/ntp.conf', 'text', False)
    ##########################################################################################################################
    @staticmethod
    def writer(filepath, text_to_add, verbose):
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
            sys.stderr.write('[-] ' + str(e))

    ##########################################################################################################################
    # Reads contents of a file into object
    # Example: data = toolbox.file.reader('/etc/ntp.conf')
    ##########################################################################################################################
    @staticmethod
    def reader(filepath, verbose):
        try:
            with open(filepath) as file:
                data = file.read()
                if verbose:
                    print('[+] Read file: ' + filepath)
                return data
        except Exception as e:
             sys.stderr.write('[-] ' + str(e))

class apt(object):
    ##########################################################################################################################
    # Takes a list object and checks if apt package is installed and returns two list objects
    # Example: list = ['mlocate', 'telnet']; toolbox.apt.check_packages(list, True)
    ##########################################################################################################################
    @staticmethod
    def check_packages(packages, verbose):
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
            sys.stderr.write('[-] ' + str(e))

    ##########################################################################################################################
    # Takes a list object and installs apt packages one by one
    # Example: list = ['mlocate', 'telnet']; toolbox.apt.install_packages(list, True)
    ##########################################################################################################################
    @staticmethod
    def install_packages(packages, verbose):
        packages_installed, packages_not_installed = apt_check_packages(packages, verbose)
        try:
            if packages_not_installed:
                for package in packages_not_installed:
                    if verbose:
                        print('[+] Installing ' + package)
                    run_command('apt install -y -qq -o=Dpkg::Use-Pty=0 ' + package, False)
            else:
                if verbose:
                    print('[+] Nothing to install')
        except Exception as e:
            sys.stderr.write('[-] ' + str(e))

class system(object):
    ##########################################################################################################################
    # Command Executor
    # Example: toolbox.system.command(command='ls /', show_output=False, verbose=True) """
    ##########################################################################################################################
    @staticmethod
    def command(command, show_output, verbose):
        try:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            if verbose:
                print('[+] Command executed: ' + command)
            if show_output:
                if CMD.stdout.readline():
                    print('[+] Showing output:\n')
                    for line in CMD.stdout:
                        print(line.strip('\n'))
                    print('\n')
                else:
                    print('[!] Command did not produce an output')
            return CMD.stdout.read()
        except Exception as e:
            sys.stderr.write('[-] ' + str(e))

    ##########################################################################################################################
    # Takes a list object and runs the provided action against systemctl
    # Example: list = ['apache2', 'networking']; toolbox.system.service(list, 'restart', False)
    ##########################################################################################################################
    @staticmethod
    def service(services, action, verbose):
        try:
            for service in services:
                run_command('systemctl {} {}'.format(action, service), False)
                if verbose:
                    print('[+] {} service: {}'.format(action.capitalize(), service))
        except Exception as e:
            sys.stderr.write('[-] ' + str(e))

    ##########################################################################################################################
    # Get user input
    # Example: toolbox.system.input('[Enter password here]', hide=True, require=True)
    ##########################################################################################################################
    @staticmethod
    def input(prompt, hide, require):
        try:
            if hide:
                if require:
                    user_input = ''
                    while user_input == '':
                        user_input = getpass.getpass(prompt)
                else:
                    user_input = getpass.getpass(prompt)
                return user_input
            else:
                if require:
                    user_input = ''
                    while user_input == '':
                        user_input = raw_input(prompt)
                else:
                    user_input = raw_input(prompt)
                return user_input
        except Exception as e:
            sys.stderr.write('[-] ' + str(e))
