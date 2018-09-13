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
supported_coins = ['Tokugawa']

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
def generate_init_service(filename_abspath, name, start_command, stop_command):
    with open(filename_abspath, 'w') as config:
        config.write('#! /bin/sh\n');
        config.write('### BEGIN INIT INFO\n');
        config.write("# Provides:          %s\n" %name);
        config.write('# Required-Start:\n');
        config.write('# Required-Stop:\n');
        config.write('# Default-Start:     2 3 4 5\n');
        config.write('# Default-Stop:      0 1 6\n');
        config.write("# Short-Description: %s masternode service\n" %name);
        config.write('### END INIT INFO\n');
        config.write('\n')
        config.write("PIDOF_PROG=/bin/pidof\n");
        config.write('\n')
        config.write('case "$1" in\n');
        config.write('  start)\n');
        config.write("    echo \"Starting %s\";\n" %name);
        config.write("    sudo -u root %s;\n" %start_command);
        config.write('  ;;\n');
        config.write('  restart|reload|force-reload)\n');
        config.write('    echo "Error: argument \'$1\' not supported" >&2\n');
        config.write('    exit 3\n');
        config.write('  ;;\n');
        config.write('  status)\n');
        config.write("    PROG_PID=`sudo -u root ${PIDOF_PROG} %s`;\n" %start_command);
        config.write('    if [ $? -eq 0 ]; then\n');
        config.write("      echo \"%s is running with pid ${PROG_PID}\"\n" %name);
        config.write('    else\n');
        config.write("      echo \"%s is not running\"\n" %name);
        config.write('    fi\n');
        config.write('  ;;\n');
        config.write('  stop)\n');
        config.write("    PROG_PID=`sudo -u root ${PIDOF_PROG} %s`;\n" %start_command);
        config.write("    echo \"Stopping %s\";\n" %name);
        config.write("    sudo -u root %s;\n" %stop_command);
        config.write('  ;;\n');
        config.write('  *)\n');
        config.write('    echo "Usage: $0 start|stop" >&2\n');
        config.write('    exit 3\n');
        config.write('  ;;\n');
        config.write('esac\n');

    #Set access rights to file
    os.chmod(filename_abspath, 0o755)

#Function that returns start command depending on coin name
def get_masternode_start_command(coinname, masternode_executable_abspath, masternodedir_abspath):
    if coinname == 'Tokugawa':
        start_command = masternode_executable_abspath + " --datadir=%s" %masternodedir_abspath

    return start_command

#Function that returns stop command depending on coin name
def get_masternode_stop_command(coinname, masternode_executable_abspath):
    if coinname=='Tokugawa':
        stop_command = masternode_executable_abspath + " stop"

    return stop_command

def configure_init_service(coinname, mn_name, masternode_executable_abspath, masternode_datadir_abspath):
    masternode_fullname = "%s_%s".capitalize() %(coinname, mn_name)
    servicefile_abspath = "/etc/init.d/%s" %masternode_fullname
    #Masternode specific startup commands
    start_command = get_masternode_start_command(coinname, masternode_executable_abspath, masternode_datadir_abspath)
    stop_command  = get_masternode_stop_command (coinname, masternode_executable_abspath)
    #Generate init service
    generate_init_service(servicefile_abspath, masternode_fullname, start_command, stop_command)
    # Enable boot service
    if cfg['services'] == 'enabled':
        run_command("systemctl enable %s" %masternode_fullname, cfg['test']==enabled)

#Function to generate an UFW application profile
def generate_ufw_profile(filename_abspath, name, title, description, ports, protocols):
    #Write application profile
    with open(filename_abspath, 'w') as config:
        config.write("[%s]\n"           %name)
        config.write("title=%s\n"       %title)
        config.write("description=%s\n" %description)
        #Build string for ports
        str_ports     = "".join("%s," %p for p in ports)
        str_protocols = "".join("%s/" %p for p in protocols)
        #Add ports and protocols removing trainling char
        config.write("ports=%s/%s\n"    %(str_ports[:-1], str_protocols[:-1]))

    #Set access rights to file
    os.chmod(filename_abspath, 0o644)

def configure_ufw_firewall(masternode_name, ufwprofiledir_abspath, ports, protocols):
    #Parameters
    ufwprofile_abspath = os.path.abspath(ufwprofiledir_abspath+masternode_name.lower())
    #Generating firewall profile
    generate_ufw_profile(ufwprofile_abspath, masternode_name, "Masternode "+masternode_name, "Provides %s masternode service" %masternode_name, mn['ports'], mn['protocols'])
    # Allow firewall profile
    run_command("ufw allow %s" %masternode_name, cfg['test']==enabled)

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
def deploy_masternode_configuration(coinname, mn, installdir_abspath):
    #Masternode specific configuration
    if coinname == 'Tokugawa':
        #Tokugawa.conf file generation
        masternode_tokugawaconf_abspath = os.path.abspath(masternodedir_abspath +'/Tokugawa.conf')
        generate_masternode_tokugawaconf(masternode_tokugawaconf_abspath, mn['name'], mn['rpcport'], mn['ip'], mn['ports'][0], mn['privkey'])
        #Set access rights to file
        os.chmod(masternode_tokugawaconf_abspath, 0o644)


#Function to deploy a masternode configuration in the desire location
def deploy_masternode_bootstrap(coinname, bootstrap_abspath, masternodedir_abspath):
    #Copy bootstrap if present
    if coinname == 'Tokugawa':
        masternode_bootstrap_basename = os.path.basename(bootstrap_abspath)
        masternode_bootstrap_abspath  = os.path.abspath(masternodedir_abspath+'/'+masternode_bootstrap_basename)
        copyfile(bootstrap_abspath, masternode_bootstrap_abspath)
        #Set access rights to file
        os.chmod(masternode_bootstrap_abspath, 0o644)

def run_command(command, test = False):
    # Launch the command with pexpect need to send the command join reverse the shlex
    #command_child = subprocess.list2cmdline(self.command)
    if test:
        print("[TEST_MODE]: %s"%command)
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
parser.add_argument("executable",    help="The tokugawad binary file.")
parser.add_argument("configuration", help="The installer configuration file.")
parser.add_argument("--bootstrap",   help="The bootstrap file.")
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
    cfg = yaml.load(ymlfile)

if cfg['coinname'] not in supported_coins:
    print('Sorry the selected coin is not yet supported!')
    pritn('List of supported coins: %s' %supported_coins)

#Show presentation
show_banner()
show_warning(cfg['system'])

print('[PREREQUISITES]')
print('  >> Installing required packages')
print('     NOTE: The installer will download and install the packages automatically')
input('           Press ENTER to continue, or CTRL+C to abort installation.\n')
for cmd in cfg['preparation']:
    run_command(cmd, cfg['test']==enabled)
print('')
print('[INSTALLATION START]')
for mn in cfg['MASTERNODES']:
    #Masternode configuration parameters
    masternode_name                = "%s_%s".capitalize() %(cfg['coinname'], mn['name'])
    masternode_datadir_abspath     = os.path.abspath(installdir_abspath + "/." + mn['name'])
    masternode_executable_basename = os.path.basename(executable_abspath + "_" + mn['name'])
    masternode_executable_abspath  = os.path.abspath(installdir_abspath + '/' + masternode_executable_basename)
    ufwprofiledir_abspath          = os.path.abspath(cfg['firewall_profiles'])
    #Masternode name
    print("  %s" %masternode_name)
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
    deploy_masternode_configuration(cfg['coinname'], mn, masternode_datadir_abspath)
    #Bootstrap deployment
    if bootstrap_abspath:
        print('    >> Deploying masternode bootstrap')
        deploy_masternode_bootstrap(cfg['coinname'], bootstrap_abspath, masternode_datadir_abspath)
    #Init service
    print('    >> Configuring /etc/init.d service')
    configure_init_service(cfg['coinname'], mn['name'], masternode_executable_abspath, masternode_datadir_abspath)
    #Firewall
    print('    >> Configuring firewall')
    configure_ufw_firewall(masternode_name, ufwprofiledir_abspath, mn['ports'], mn['protocols'])

print('[INSTALLATION FINISH]')
print('')

#Enable firewall
print('')
print('IMPORTANT SSH ACCESS COULD BE BLOCKED!!!'
print('Check that OpenSSH access rule is set in UFW firewall before running:')
print('\'$ufw enable; $ufw start\'')
print('')
