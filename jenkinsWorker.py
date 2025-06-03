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

# tmp
def get_os():

    # tmp
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            if 'ubuntu' in content:
                return 'Ubuntu'
            elif 'red hat' in content:
                return 'RedHat'
            elif 'centos' in content:
                return 'CentOS'
    # tmp
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
def setup_jenkins_agent_ubuntu():
    os.makedirs(WORKDIR, exist_ok=True)

    # tmp
    run_cmd("sudo apt update && sudo apt install -y openjdk-21-jre wget")

    # tmp
    run_cmd(f"sudo wget {JENKINS_URL}/jnlpJars/agent.jar -O {WORKDIR}/agent.jar")

    # tmp
    run_cmd(f"java -jar {WORKDIR}/agent.jar "
            f"-jnlpUrl {JENKINS_URL}/computer/{AGENT_NAME}/jenkins-agent.jnlp "
            f"-secret {AGENT_SECRET} "
            f"-workDir {WORKDIR}")

# tmp
def setup_jenkins_agent_redhat():
    
    # tmp
    os.makedirs(WORKDIR, exist_ok=True)

    # tmp
    run_cmd("sudo yum install -y java-21-openjdk wget")

    # tmp
    run_cmd(f"sudo wget {JENKINS_URL}/jnlpJars/agent.jar -O {WORKDIR}/agent.jar")

    # tmp
    run_cmd(f"java -jar {WORKDIR}/agent.jar "
            f"-jnlpUrl {JENKINS_URL}/computer/{AGENT_NAME}/jenkins-agent.jnlp "
            f"-secret {AGENT_SECRET} "
            f"-workDir {WORKDIR}")

# tmp
def main():
    
    # tmp
    os_type = get_os()

    # tmp
    print(f"Detected OS: {os_type}")

    # tmp
    if os_type == 'Ubuntu':
        setup_jenkins_agent_ubuntu()
    # tmp
    elif os_type == 'RedHat':
        setup_jenkins_agent_redhat()
    # tmp
    else:
        print("This script couldn't determine your system's OS")
        sys.exit(1)
    
# ==== MAIN BODY ========================================================
if __name__ == "__main__":
    main()
