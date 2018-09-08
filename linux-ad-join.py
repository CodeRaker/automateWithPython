""" This script will setup and add a Linux server to an AD domain.
It is made from the instructions at: https://www.tecmint.com/join-ubuntu-to-active-directory-domain-member-samba-winbind/
"""

import toolbox, sys, os

ntp_path = '/etc/ntp.conf'
prerequisite_packages = ['samba', 'krb5-config', 'krb5-user', 'winbind', 'libpam-winbind', 'libnss-winbind', 'ntp']

def main():
    # Get user inputs
    domain_controller_fqdn = toolbox.system.input(prompt='Provide Domain Controller FQDN: ', hide=False, require=True)
    search_domain = domain_controller_fqdn.split('.', 1)[1]
    domain_user = toolbox.system.input(prompt='Provide domain username: ', hide=False, require=True)

    # Collect System Information
    print('[+] Starting installation')
    try:
        #Find hostname
        hostname = toolbox.system.command(command='hostname', show_output=False, verbose=False).rstrip('\n')
        if not hostname:
            sys.exit('[-] Failed getting hostname!\nExiting...')

        #Get DC IP
        domain_controller_ip = toolbox.system.command(command='nslookup ' + domain_controller_fqdn + ' | tail -n 2 | cut -d : -f 2', show_output=False, verbose=False).strip('\n ')
        if not toolbox.network.check_ipv4_syntax(ip=domain_controller_ip, verbose=True):
            sys.exit('[-] Failed validating IP address!\nExiting...')

        #Check if DC IP is a nameserver
        if not domain_controller_ip in toolbox.system.command(command="cat /etc/resolv.conf", show_output=False, verbose=False):
            sys.exit('[-] ' + domain_controller_ip + ' is not configured as nameserver. Fix it and try again\nExiting...')

        #Check search domain
        if not domain_controller_fqdn.split('.', 1)[1] in toolbox.system.command(command='cat /etc/resolv.conf', show_output=False, verbose=False):
            print('[!] ' + search_domain + ' is not configured as search domain. Adding temporary entry to /etc/resolv.conf')
            toolbox.system.command('echo "search ' + search_domain + '" >> /etc/resolv.conf', show_output=False, verbose=True)

        #Check Ports on DC
        if not toolbox.network.check_tcp_port(ip=domain_controller_ip, port=389, verbose=True):
            sys.exit('Exiting...')

        #Setting noninteractive mode because otherwise krb5 pops up and interrupts installation
        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
        toolbox.apt.install_packages(packages=prerequisite_packages, True)

        #Correcting krb5.conf file, since it didnt get info from suppressed popup
        toolbox.file.editor(mode='replace', filepath='/etc/krb5.conf', line_startswith='default_realm', text_to_add='default_realm = ' + search_domain, verbose=True)

        #Verifying installed packages
        packages_installed, packages_not_installed = toolbox.apt.check_packages(packages=prerequisite_packages, verbose=True)
        if len(packages_not_installed) > 0:
            print('[-] Please install the following packages: ' + str(packages_not_installed) + ' and run the script again')
            sys.exit('Exiting...')

        #Configuring NTP configuration file
        toolbox.file.editor(mode='comment', filepath=ntp_path, line_startswith='pool ', text_to_add='pool ' + search_domain, verbose=True)
        toolbox.system.service(['ntp'], 'restart', True)

        #Integrate with AD
        adconfig = '''
[global]
workgroup = {workgroup}
realm = {realm}
netbios name = {netbios}
security = ADS
dns forwarder = {forwarder}
idmap config * : backend = tdb
idmap config *:range = 50000-1000000
template homedir = /home/%D/%U
template shell = /bin/bash
winbind use default domain = true
winbind offline logon = false
winbind nss info = rfc2307
winbind enum users = yes
winbind enum groups = yes
vfs objects = acl_xattr
map acl inherit = Yes
store dos attributes = Yes
'''.format(workgroup=search_domain.split('.')[0].upper(), realm=search_domain, netbios=hostname, forwarder=domain_controller_ip)
        toolbox.file.writer(filepath='/etc/samba/smb.conf', text_to_add=adconfig, verbose=True)
        toolbox.system.service(services=['smbd', 'nmbd', 'winbind'], action='restart', verbose=True)
        toolbox.system.service(services=['samba-ad-dc'], action='stop', verbose=True)
        toolbox.system.service(services=['smbd', 'nmbd', 'winbind'], action='enable', verbose=True)

        #Runs authentication command against AD
        os.system('net ads join -U ' + domain_user + ' 2> /dev/null')

        #Configure AD authentication on localhost
        toolbox.file.editor(mode='replace', filepath='/etc/nsswitch.conf', line_startswith='passwd: ', text_to_add='passwd: compat winbind', verbose=True)
        toolbox.file.editor(mode='replace', filepath='/etc/nsswitch.conf', line_startswith='group: ', text_to_add='group: compat winbind', verbose=True)
        toolbox.system.service(services=['winbind'], action='restart', verbose=True)

    except Exception as e:
        print('[ERROR] ' + str(e))
        sys.exit('Exiting...')

main()
