#!/usr/bin/env python3

# ==== MODULES ==========================================================
import os
import subprocess

# ==== STATIC VARIABLES =================================================
JENKINS_URL = "http://JENKINS_CONTROLLER_IP:8080"
AGENT_NAME = "AGENT_NAME"
AGENT_SECRET = "AGENT_SECRET"
WORKDIR = "/home/jenkins"

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

# Set up Jenkins agent for an Ubuntu node
def setup_jenkins_agent_ubuntu():

    # Create the working directory for the Jenkins agent if it doesn't exist
    os.makedirs(WORKDIR, exist_ok=True)

    # Install required packages: Java 21 (runtime) and wget for downloading files
    run_cmd("sudo apt update && sudo apt install -y openjdk-21-jre wget")

    # Download the Jenkins agent JAR file from the Jenkins controller
    run_cmd(f"sudo wget {JENKINS_URL}/jnlpJars/agent.jar -O {WORKDIR}/agent.jar")

    # Launch the Jenkins agent using the JAR file with the specified secret and work directory
    run_cmd(f"java -jar {WORKDIR}/agent.jar "
            f"-jnlpUrl {JENKINS_URL}/computer/{AGENT_NAME}/jenkins-agent.jnlp "
            f"-secret {AGENT_SECRET} "
            f"-workDir {WORKDIR}")

# Set up Jenkins agent for a RedHat node
def setup_jenkins_agent_redhat():
    
    # Create the working directory for the Jenkins agent if it doesn't exist
    os.makedirs(WORKDIR, exist_ok=True)

    # Install required packages: Java 21 (runtime) and wget for downloading files
    run_cmd("sudo yum install -y java-21-openjdk wget")

    # Download the Jenkins agent JAR file from the Jenkins controller
    run_cmd(f"sudo wget {JENKINS_URL}/jnlpJars/agent.jar -O {WORKDIR}/agent.jar")

    # Launch the Jenkins agent using the JAR file with the specified secret and work directory
    run_cmd(f"java -jar {WORKDIR}/agent.jar "
            f"-jnlpUrl {JENKINS_URL}/computer/{AGENT_NAME}/jenkins-agent.jnlp "
            f"-secret {AGENT_SECRET} "
            f"-workDir {WORKDIR}")

# Main function to determine OS and call the appropriate setup function
def main():
    
    os_type = get_os()
    print(f"Detected OS: {os_type}")

    if os_type == 'Ubuntu':
        setup_jenkins_agent_ubuntu()
    elif os_type == 'RedHat':
        setup_jenkins_agent_redhat()
    else:
        print("This script couldn't determine your system's OS")
        sys.exit(1)
    
# ==== MAIN BODY ========================================================
if __name__ == "__main__":
    main()
