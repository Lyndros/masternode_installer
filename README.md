# Masternode installer instructions

A beautiful python installer that allows you to install your beloved masternodes within minutes.
 
NOTE: Currently the installer ONLY supports TOKUGAWA coin, more coins will be added.

# 1. Requirements

In order to run this program the below python3 libraries need to be installed:
```
$sudo apt-get install python3-pip python3-yaml
```
In addition the installer the needs:
* A precompiled binary containing the latest version of the masternode daemon.
* [Optional] A bootstrap.dat file to accelerate the initial blockchain synchronisation.

# 2. Copying the necessary files

```
$mkdir -p /tmp/masternode_installer/
$cd /tmp/masternode_installer/
$wget https://raw.githubusercontent.com/Lyndros/masternode_installer/master/masternode_installer.py 
$chmod a+x masternode_installer.py
```

-- This is a configuration example, please modify as needed before running the installer--
```
$wget https://raw.githubusercontent.com/Lyndros/masternode_installer/master/masternode_installer.py/config/tokugawa_masternode.yml
```

A bootstrap.dat file is optional but very recommended if you want to have your MNs running asap.

The bootstrap for Tokugawa coin can be obtained from <a href="https://github.com/mangae/Tokugawa_mangae">here</a>.

# 3. Setting your configuration file

Modify the configuration file to match your needs: mainly IP, port and masternode privkey settings...
If you run multiple masternodes in the same VPS, you can share the IP, take into account that ports must be different.

# 4. Running the installer
```
$./masternode_installer.py installdir executable configuration.yml [ --bootstrap bootstrap.dat ]
```

Execution examples:
```
$./masternode_installer.py /opt/tokugawa ./Tokugawad ./tokugawa_masternode.yml --bootstrap /tmp/bootstrap.dat
$./masternode_installer.py /opt/tokugawa ./Tokugawad ./tokugawa_masternode.yml
```

# 5. Manually starting stopping masternode services

During the installation boot services for your masternodes had been configured if services was enabled in the 
configuration file.

You can manually start/stop a masternode executing: 
```
$systemctl enable tokugawa_mn01 ... mn02
```

# 6. Firewall
During the installation ufw firewall profiles had been installed.
Before activating firewall please check that SSH rule is present and configured, the file can be found in /etc/ufw/applications.d/openssh-server.

Finally activate with:
```
$systemctl enable ufw;
```

# 7. Donations
If you want to motivate me and support this repository I accept donations even 1 TOK is always welcome :-)!
* ethereum address:</b> <i>0x44F102616C8e19fF3FED10c0b05B3d23595211ce</i>
* tokugawa address:</b> <i>TjrQBaaCPoVW9mPAZHPfVx9JJCq7yZ7QnA</i>

For any questions feel free to contact me at <i>lyndros at hotmail.com</i>