#!/usr/bin/env python3

# ==== MODULES ==========================================================
import os
import subprocess

# ==== STATIC VARIABLES =================================================
JENKINS_URL = "http://<JENKINS_MASTER_IP>:8080"
AGENT_NAME = "ubuntu-agent"
AGENT_SECRET = "<YOUR_SECRET_HERE>"
WORKDIR = "/home/jenkins"

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
def setup_jenkins_agent_ubuntu():
    os.makedirs(WORKDIR, exist_ok=True)

    # Install Java if not installed
    run_cmd("sudo apt update && sudo apt install -y openjdk-21-jre")

    # Download agent.jar
    run_cmd(f"wget {JENKINS_URL}/jnlpJars/agent.jar -O {WORKDIR}/agent.jar")

    # Start the agent (you can background this or create a systemd service)
    run_cmd(f"java -jar {WORKDIR}/agent.jar "
            f"-jnlpUrl {JENKINS_URL}/computer/{AGENT_NAME}/jenkins-agent.jnlp "
            f"-secret {AGENT_SECRET} "
            f"-workDir {WORKDIR}")

def setup_jenkins_agent_redhat():
    # Create working directory
    os.makedirs(WORKDIR, exist_ok=True)

    # Install Java (OpenJDK 21)
    run_cmd("sudo yum install -y java-21-openjdk")

    # Download agent.jar
    run_cmd(f"wget {JENKINS_URL}/jnlpJars/agent.jar -O {WORKDIR}/agent.jar")

    # Start the Jenkins agent
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
        print("Couldn't determine your system's OS")
        sys.exit(1)
    
# ==== MAIN BODY ========================================================
if __name__ == "__main__":
    main()
