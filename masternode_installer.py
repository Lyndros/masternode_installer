#!/usr/bin/env python3
# Copyright (c) 2018 Lyndros <lyndros@hotmail.com>
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

###############################################################################
# MASTERNODE AUTOINSTALLER by Lyndros <lyndros@hotmail.com>                   #
###############################################################################
# Repository: https://github.com/Lyndros/crypto_tools                         #
#                                                                             #
# If you want to support and motivate me I accept donations even 1 TOK is     #
# always welcome :-)!                                                         #
# > ethereum address: 0x44F102616C8e19fF3FED10c0b05B3d23595211ce              #
# > tokugawa address: TjrQBaaCPoVW9mPAZHPfVx9JJCq7yZ7QnA                      #
#                                                                             #
###############################################################################
import yaml
import argparse
import sys
import os
import errno
import string
import random
import subprocess
from shutil import copyfile 

#List of supported coins by the installer
supported_coins = ['TOKUGAWA']

def show_banner():
    print('')
    print('###############################################################################')
    print('# MASTERNODE AUTOINSTALLER by Lyndros <lyndros@hotmail.com>                   #')
    print('###############################################################################')
    print('# Repository: https://github.com/Lyndros/crypto_tools                         #')
    print('#                                                                             #')
    print('# If you want to support and motivate me I accept donations even 1 TOK is     #')
    print('# always welcome :-)!                                                         #')
    print('# > ethereum address: 0x44F102616C8e19fF3FED10c0b05B3d23595211ce              #')
    print('# > tokugawa address: TjrQBaaCPoVW9mPAZHPfVx9JJCq7yZ7QnA                      #')
    print('#                                                                             #')
    print('###############################################################################')
    print('')

def show_warning(os_name):
    print('This installer is configured to run on %s' %os_name)
    input('Press ENTER to continue, or CTRL+C to abort installation.\n')

#Function to generate a random password
#Note: Passwords are enforced to be 12 characters long
def generate_password():
    min_char = 12
    max_char = 12
    allchar = string.ascii_letters + string.punctuation + string.digits
    password = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))
    
    return password

#Function to create a directory
#Note: All non existing parent directories will be created
def create_directory(absfolder_path):
    try:
        os.makedirs(absfolder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

#Function to generate the tokugawa service
def generate_systemd_service(filename_abspath, description, username, working_directory, start_command, stop_command):
    with open(filename_abspath, 'w') as config:
        config.write('[Unit]\n');
        config.write("Description=%s\n"%description);
        config.write('After=network-online.target\n');

        config.write('[Service]\n');
        config.write("User=%s\n"%username);
        config.write('Type=forking\n');
        config.write("WorkingDirectory=%s\n"%working_directory);
        config.write('Restart=always\n');
        config.write('RestartSec=10\n');
        config.write("ExecStart=%s\n"%start_command);
        config.write("ExecStop=%s\n"%stop_command);

        config.write('[Install]\n');
        config.write('WantedBy=multi-user.target\n');

    #Set access rights to file
    os.chmod(filename_abspath, 0o644)

#Function that returns start command depending on coin name
def get_masternode_start_command(masternode_executable_abspath, masternodedir_abspath):
    if CONFIG['coinname'].upper() == 'TOKUGAWA':
        start_command = masternode_executable_abspath + " --datadir=%s" %masternodedir_abspath

    return start_command

#Function that returns stop command depending on coin name
def get_masternode_stop_command(masternode_executable_abspath, masternodedir_abspath):
    if CONFIG['coinname'].upper() == 'TOKUGAWA':
        stop_command = masternode_executable_abspath + " --datadir=%s stop" %masternodedir_abspath

    return stop_command

def configure_service(masternode_name, masternode_executable_abspath, masternode_datadir_abspath):
    #Create service filename
    servicefile_abspath = os.path.abspath(CONFIG['SYSTEM']['services_directory']+"/%s.service" %masternode_name.lower())
    #Masternode specific startup commands
    start_command = get_masternode_start_command(masternode_executable_abspath, masternode_datadir_abspath)
    stop_command  = get_masternode_stop_command (masternode_executable_abspath, masternode_datadir_abspath)
    #Generate systemd service
    description       = "Service for %s" %masternode_name.lower()
    working_directory = os.path.dirname(masternode_executable_abspath)
    username          = CONFIG['username']
    generate_systemd_service(servicefile_abspath, description, username, working_directory, start_command, stop_command)
    # Enable at boot
    if CONFIG['services'] == 'enabled':
        run_command("systemctl enable %s" %masternode_name.lower())

#Function to generate an UFW application profile
def generate_ufw_profile(filename_abspath, name, title, description, ports, protocols):
    #Write application profile
    with open(filename_abspath, 'w+') as config:
        config.write("[%s]\n"           %name.lower())
        config.write("title=%s\n"       %title)
        config.write("description=%s\n" %description)
        #Build string for ports
        str_ports     = "".join("%s," %p for p in ports)
        str_protocols = "".join("%s/" %p for p in protocols)
        #Add ports and protocols removing trainling char
        config.write("ports=%s/%s\n"    %(str_ports[:-1], str_protocols[:-1]))

    #Set access rights to file
    os.chmod(filename_abspath, 0o644)

def configure_ufw_firewall(masternode_name, ports, protocols):
    #Create profile filename
    ufwprofile_abspath = os.path.abspath(CONFIG['SYSTEM']['firewall_profiles']+"/%s" %masternode_name.lower())
    #Generating firewall profile
    generate_ufw_profile(ufwprofile_abspath, masternode_name, "Masternode %s" %masternode_name.lower(), "Provides %s masternode service" %CONFIG['coinname'].lower(), ports, protocols)
    #Allow firewall profile
    run_command("ufw allow %s" %masternode_name.lower())

# Function to generate the Tokugawa.conf file under the MN directory
def generate_masternode_tokugawaconf(filename_abspath, masternode_name, rcpport, ip, port, privkey):
    with open(filename_abspath, 'w+') as config:
        config.write('rpcuser=myrpcuser%s\n' %masternode_name.lower())
        config.write('rpcpassword=%s\n' % generate_password())
        config.write('rpcport=%s\n' %rcpport)
        config.write('server=1\n')
        config.write('listen=1\n')
        config.write('daemon=1\n')
        config.write('port=%s\n' %port)
        config.write('masternodeaddr=%s:%s\n' % (ip, port))
        config.write('masternode=1\n')
        config.write('masternodeprivkey=%s\n' % mn['privkey'])

    #Set access rights to file
    os.chmod(filename_abspath, 0o644)

#Function to install binaries in the desire location
def install_masternode_binaries(executable_abspath, masternode_executable_abspath):
    #Copy daemon file with the following name
    copyfile(executable_abspath, masternode_executable_abspath)
    #Set execution rights to file
    os.chmod(masternode_executable_abspath, 0o755)

#Function to deploy a masternode configuration in the desire location
def deploy_masternode_configuration(mn, masternodedir_abspath):
    #Masternode specific configuration
    if CONFIG['coinname'].upper() == 'TOKUGAWA':
        #Tokugawa.conf file generation
        masternode_tokugawaconf_abspath = os.path.abspath(masternodedir_abspath +'/Tokugawa.conf')
        generate_masternode_tokugawaconf(masternode_tokugawaconf_abspath, mn['name'], mn['rpcport'], mn['ip'], mn['ports'][0], mn['privkey'])
        #Set access rights to file
        os.chmod(masternode_tokugawaconf_abspath, 0o644)


#Function to deploy a masternode configuration in the desire location
def deploy_masternode_bootstrap(bootstrap_abspath, masternodedir_abspath):
    #Copy bootstrap if present
    if CONFIG['coinname'].upper() == 'TOKUGAWA':
        masternode_bootstrap_basename = os.path.basename(bootstrap_abspath)
        masternode_bootstrap_abspath  = os.path.abspath(masternodedir_abspath+'/'+masternode_bootstrap_basename)
        copyfile(bootstrap_abspath, masternode_bootstrap_abspath)
        #Set access rights to file
        os.chmod(masternode_bootstrap_abspath, 0o644)

def run_command(command):
    # Launch the command with pexpect need to send the command join reverse the shlex
    #command_child = subprocess.list2cmdline(self.command)
    if TEST_MODE:
        print("[TEST_MODE]: %s" %command)
        return
    try:
        subprocess.call(command, shell=True)
    except OSError as e:
        print ("Error executing command %s" %command)

###############################################################################
#                                    MAIN                                     #
###############################################################################

#Chek user rights
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.")

#Program input parameters
parser = argparse.ArgumentParser()
parser.add_argument("installdir",    help="The installation directory.")
parser.add_argument("executable",    help="The masternode daemon file.")
parser.add_argument("configuration", help="The installer configuration file.")
parser.add_argument("--bootstrap",   help="The masternode daemon bootstrap file.")
args = parser.parse_args()

#Build abs names to avoid problems
installdir_abspath    = os.path.abspath(args.installdir)
executable_abspath    = os.path.abspath(args.executable)
configuration_abspath = os.path.abspath(args.configuration)

if args.bootstrap:
    bootstrap_abspath = os.path.abspath(args.bootstrap)
else:
    bootstrap_abspath = ""

#Check input files
if (not os.path.exists(executable_abspath)) or (not os.path.exists(configuration_abspath)):
    print("Error! One of the supplied files does not exist.")
    sys.exit(-1)

#Parse the configuration file
with open(configuration_abspath, 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile)

#Set global test mode
TEST_MODE=CONFIG.get('test', 'disabled')=='enabled'

if CONFIG['coinname'].upper() not in supported_coins:
    print('Sorry the selected coin is not yet supported!')
    print('List of supported coins: %s' %supported_coins)

#Show presentation
show_banner()
show_warning(CONFIG['SYSTEM']['os'])

print('[PREREQUISITES]')
print('  >> Installing required packages')
print('     NOTE: The installer will download and install the packages automatically')
input('           Press ENTER to continue, or CTRL+C to abort installation.\n')
for cmd in CONFIG['SYSTEM']['requires']:
    run_command(cmd)

print('')
print('[INSTALLATION START]')
# Create installation directory
print('>> Creating daemon user')
run_command("useradd -r -M -N %s" %CONFIG['username'])

for mn in CONFIG['MASTERNODES']:
    #Masternode configuration parameters
    masternode_name                = "%s_%s".lower() %(CONFIG['coinname'], mn['name'])
    masternode_datadir_abspath     = os.path.abspath(installdir_abspath + "/." + mn['name'].lower())
    masternode_executable_abspath  = os.path.abspath(installdir_abspath + '/' + os.path.basename(executable_abspath + "_" + mn['name']).lower())
    #Masternode name
    print("  %s" %masternode_name.upper())
    #Create installation directory
    print('    >> Creating binaries installation directory')
    create_directory(installdir_abspath)
    #Install masternode binaries
    print('    >> Installing binaries')
    install_masternode_binaries(executable_abspath, masternode_executable_abspath)
    #Masternode directory creation
    print('    >> Creating masternode data directory')
    create_directory(masternode_datadir_abspath)
    #Configuration deployment
    print('    >> Deploying masternode configuration')
    deploy_masternode_configuration(mn, masternode_datadir_abspath)
    #Bootstrap deployment
    if bootstrap_abspath:
        print('    >> Deploying masternode bootstrap')
        deploy_masternode_bootstrap(bootstrap_abspath, masternode_datadir_abspath)
    #Init service
    print('    >> Configuring systemd service')
    configure_service(masternode_name, masternode_executable_abspath, masternode_datadir_abspath)
    #Firewall
    print('    >> Configuring firewall')
    configure_ufw_firewall(masternode_name, mn['ports'], mn['protocols'])

# Create installation directory
print('>> Setting user access rights')
run_command("chown %s:users %s -R" %(CONFIG['username'], installdir_abspath))

print('[INSTALLATION FINISH]')
print('')

#Allow SSH and enable firewall
print('')
if CONFIG['firewall'] == 'enabled':
    print('SSH ACCESS COULD BE BLOCKED!!!')
    print('The installer will proceed now to enable the firewall')
    input('Press ENTER to continue, or CTRL+C to abort to enable the firewall now.\n')
    run_command("ufw allow openssh")
    run_command("ufw enable")
else:
    print('To enable the firewall, please check that OpenSSH access rule is set:')
    print('\'$ufw allow openssh\'')
    print('And then activate firewall with:')
    print('\'$ufw enable\'')
print('')
