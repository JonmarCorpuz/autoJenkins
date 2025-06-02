#!/usr/bin/env python3

# ==== MODULES ==========================================================
import os
import subprocess
import sys

# ==== FUNCTIONS ========================================================

# tmp
def get_os():
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            if 'ubuntu' in content:
                return 'Ubuntu'
            elif 'red hat' in content:
                return 'RedHat'
            elif 'centos' in content:
                return 'CentOS'
    except Exception as e:
        print(f"Error reading OS info: {e}")
    return 'undetermined'

# tmp
def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)

# tmp
def install_jenkins_ubuntu():

    # tmp
    run_cmd('sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc '
            'https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key')

    # tmp
    run_cmd('echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] '
            'https://pkg.jenkins.io/debian-stable binary/" | sudo tee '
            '/etc/apt/sources.list.d/jenkins.list > /dev/null')

    # tmp
    run_cmd('sudo apt-get -y update')
    run_cmd('sudo apt-get -y install jenkins')

    # tmp
    run_cmd('sudo apt -y update')
    run_cmd('sudo apt install -y fontconfig openjdk-21-jre')

    # tmp
    run_cmd('java --version')
    run_cmd('sudo systemctl status jenkins')

# tmp
def install_jenkins_redhat():

    # tmp
    run_cmd('sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc '
            'https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key')

    # tmp
    run_cmd('echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] '
            'https://pkg.jenkins.io/debian-stable binary/" | sudo tee '
            '/etc/apt/sources.list.d/jenkins.list > /dev/null')

    # tmp
    run_cmd('sudo yum -y update')
    run_cmd('sudo yum -y install jenkins')

    # tmp
    run_cmd('sudo yum -y update')
    run_cmd('sudo yum -y install fontconfig openjdk-21-jre')

    # tmp
    run_cmd('java --version')
    run_cmd('sudo systemctl status jenkins')

# tmp
def install_jenkins_centos():
    
    # tmp
    run_cmd('sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc '
            'https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key')

    # tmp
    run_cmd('echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] '
            'https://pkg.jenkins.io/debian-stable binary/" | sudo tee '
            '/etc/apt/sources.list.d/jenkins.list > /dev/null')

    # tmp
    run_cmd('sudo dnf -y update')
    run_cmd('sudo dnf -y install jenkins')

    # tmp
    run_cmd('sudo dnf -y update')
    run_cmd('sudo dnf -y install fontconfig openjdk-21-jre')

    # tmp
    run_cmd('java --version')
    run_cmd('sudo systemctl status jenkins')

# tmp
def main():
    
    # tmp
    os_type = get_os()

    # tmp
    if os_type == 'undetermined':
        print("Couldn't determine your system's OS")
        sys.exit(1)

    # tmp
    print(f"Detected OS: {os_type}")

    # tmp
    if os_type == 'Ubuntu':
        install_jenkins_ubuntu()
    # tmp
    elif os_type == 'RedHat':
        install_jenkins_redhat()
    # tmp
    elif os_type == 'CentOS':
        install_jenkins_centos()

# ==== MAIN BODY ========================================================
if __name__ == "__main__":
    main()
