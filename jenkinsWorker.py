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
def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

# tmp
def setup_jenkins_agent():
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

# ==== MAIN BODY ========================================================
if __name__ == "__main__":
    setup_jenkins_agent()
