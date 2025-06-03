#!/usr/bin/env python3

# ==== MODULES ==========================================================
import os
import subprocess
import sys

# ==== FUNCTIONS ========================================================

# Detect the Linux distribution by checking /etc/os-release content
def get_os():
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            if 'ubuntu' in content:
                return 'Ubuntu'
            elif 'red hat' in content:
                return 'RedHat'
    except Exception as e:
        print(f"Error reading OS info: {e}")
        return 'undetermined'

# Run a shell command and exit the script if it fails
def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)

# Install the Jenkins controller on an Ubuntu node
def install_jenkins_ubuntu():

    # Install wget
    run_cmd('sudo apt -y install wget')
    
    # Download and store the Jenkins GPG key securely in the apt keyrings directory
    run_cmd('sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc '
            'https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key')

    # Add the Jenkins APT repository with GPG key verification
    run_cmd('echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] '
            'https://pkg.jenkins.io/debian-stable binary/" | sudo tee '
            '/etc/apt/sources.list.d/jenkins.list > /dev/null')

    # Update package lists and install Jenkins
    run_cmd('sudo apt-get -y update')
    run_cmd('sudo apt-get -y install jenkins')

    # Ensure Java 21 and required font libraries are installed for Jenkins
    run_cmd('sudo apt -y update')
    run_cmd('sudo apt install -y fontconfig openjdk-21-jre')

    # Verify Java installation and check Jenkins service status
    run_cmd('java --version')
    run_cmd('sudo systemctl status jenkins')

# Install the Jenkins controller on a RedHat node
def install_jenkins_redhat():

    # Install wget
    run_cmd('sudo yum -y install wget')

    # Download the Jenkins YUM repository configuration file
    run_cmd('sudo wget -O /etc/yum.repos.d/jenkins.repo '
            'https://pkg.jenkins.io/redhat-stable/jenkins.repo')

    # Import the Jenkins GPG key for package verification
    run_cmd('sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key')

    # Upgrade all system packages to their latest version
    run_cmd('sudo yum upgrade -y')

    # Install required Java runtime and font libraries for Jenkins
    run_cmd('sudo yum install -y fontconfig java-21-openjdk')

    # Install the Jenkins package from the added repository
    run_cmd('sudo yum install -y jenkins')

    # Reload systemd to recognize Jenkins service
    run_cmd('sudo systemctl daemon-reload')

# Main function to determine OS and call the appropriate setup function
def main():
    
    os_type = get_os()
    print(f"Detected OS: {os_type}")

    if os_type == 'Ubuntu':
        install_jenkins_ubuntu()
    elif os_type == 'RedHat':
        install_jenkins_redhat()
    else:
        print("This script couldn't determine your system's OS")
        sys.exit(1)

# ==== MAIN BODY ========================================================
if __name__ == "__main__":
    main()
