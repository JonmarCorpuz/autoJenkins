#!/bin/bash

OS="undetermined"
if grep -qi "Ubuntu" /etc/os-release;
then
  OS="Ubuntu"
elif grep -qi "Red Hat" /etc/os-release;
then
  OS="RedHat"
elif grep -qi "CentOS" /etc/os-release;
then
  OS="CentOS"
else
  echo "Couldn't determine your system's OS"
  exit 1
fi 

# ==== UBUNTU ==================================================================
if [[ $OS =~ "Ubuntu" ]];
then
  sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

  echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

  sudo apt-get -y update
  sudo apt-get -y install jenkins

  # Install OpenJDK 21 (Not all Java versions are compatible with Jenkins)
  sudo apt update
  sudo apt install fontconfig openjdk-21-jre
  java --version

  sudo systemctl status jenkins
fi 

# ==== RED HAT =================================================================
if [[ $OS =~ "RedHat" ]];
then
  echo "TMP"
fi 

# ==== CENTOS ==================================================================
if [[ $OS =~ "CentOS" ]];
then
  echo "TMP"
fi 
