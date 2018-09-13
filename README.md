<html>
<body style="font-family: Consolas, monospace; font-size:14pt;">
<b>Masternode installer instructions</b>
<br/> ────────────────────────────────────────────────────
<br/>
<br/> BROKEN BUILD WORK IN PROGRESS... SORRY
<br/>
<br/> A beautiful python installer that allows you to install your beloved masternodes withing minutes.
<br/> 
<br/> NOTE: Currently the installer ONLY supports TOKUGAWA coin, more coins will be added.
<br/>
<br/> <b>0. Requirements</b>
<br/>
<br/> In order to run this program the below python3 libraries need to be installed:
<br/> &nbsp; &nbsp; $sudo apt-get install python3-pip python3-yaml
<br/> Additionally ufw firewall must be installed:
<br/> $sudo apt install ufw
<br/> 
<br/> In addition the following files are needed:
<br/> &nbsp; &nbsp; - A precompiled binary containing the latest version of the masternode daemon 
<br/> &nbsp; &nbsp;   NOTE: that the binary dependant libraries must be pre-installed (Work on progress).
<br/> &nbsp; &nbsp; - Ufw firewall will be automatically configured to enable SSH/Tokugawa ports. ($apt install ufw).
<br/> &nbsp; &nbsp; - [Optional] A bootstrap file to accelerate the initial masternode synchronisation.
<br/>
<br/> <b>1. Copying the necessary files</b>
<br/>
<br/> &nbsp; &nbsp; $mkdir -p /tmp/masternode_installer/
<br/> &nbsp; &nbsp; $cd /tmp/masternode_installer/
<br/> &nbsp; &nbsp; $wget https://raw.githubusercontent.com/Lyndros/crypto_tools/master/masternode_installer/masternode_installer.py
<br/> &nbsp; &nbsp; $chmod a+x masternode_installer.py
<br/>
<br/> -- This is a configuration example, please modify as needed before running the installer--
<br/> &nbsp; &nbsp; $wget https://raw.githubusercontent.com/Lyndros/crypto_tools/master/masternode_installer/config_tokugawa.yml
<br/>
<br/> &nbsp; &nbsp; In addition get your tokugawad binary from your favourite source or compile it.
<br/> &nbsp; &nbsp; A bootstrap.dat file is optional but very recommended if you want to have your MNs running asap.
<br/>
<br/> <b>2. Setting your configuration file</b>
<br/> 
<br/> Modify the configuration file to match your needs: mainly IP, port and masternode privkey settings...
<br/> If you run multiple masternodes in the same VPS, you can share the IP, take into account that ports must be different.
<br/>
<br/> <b>3. Running the installer</b>
<br/> &nbsp; &nbsp; $./masternode_installer.py installdir executable configuration.yml [ --bootstrap bootstrap.dat ]
<br/>
<br/> &nbsp; &nbsp; Execution examples:
<br/> &nbsp; &nbsp; $./masternode_installer.py /opt/tokugawa ./tokugawad ./config_tokugawa.yml --bootstrap /tmp/bootstrap.dat
<br/> &nbsp; &nbsp; $./masternode_installer.py /opt/tokugawa ./tokugawad ./config_tokugawa.yml
<br/>
<br/> <b>4. Enabling tokugawa services automatically at boot</b>
<br/> &nbsp; &nbsp; $systemctl enable tokugawa_mn*
<br/> 
<br/> If during the installation ufw firewall was detected the following steps must be done:
<br/> &nbsp; &nbsp; $ufw stop; 
<br/> &nbsp; &nbsp; $ufw allow tokugawa_mn*; $ufw enable; 
<br/> &nbsp; &nbsp; $systemctl enable ufw;
<br/>
<br/> <b>5. Donations</b>
<br/> If you want to motivate me and support this repository I accept donations even 1 TOK is always welcome :-)!
<br/> &nbsp; &nbsp;> <b>ethereum address:</b> <i>0x44F102616C8e19fF3FED10c0b05B3d23595211ce</i>
<br/> &nbsp; &nbsp;> <b>tokugawa address:</b> <i>TjrQBaaCPoVW9mPAZHPfVx9JJCq7yZ7QnA</i>
<br/>
<br/> For any questions feel free to contact me at <i>lyndros@hotmail.com</i>
</body>
</html>
