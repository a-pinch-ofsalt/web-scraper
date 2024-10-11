#!/bin/bash

# Install necessary dependencies for Chrome
microdnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm jq unzip wget

# Add Google Chrome repository and install Google Chrome
echo -e "[google-chrome]\n\
name=google-chrome\n\
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64\n\
enabled=1\n\
gpgcheck=1\n\
gpgkey=https://dl.google.com/linux/linux_signing_key.pub" > /etc/yum.repos.d/google-chrome.repo

# Import the GPG key
wget https://dl.google.com/linux/linux_signing_key.pub && rpm --import linux_signing_key.pub && rm -f linux_signing_key.pub

# Install Google Chrome
microdnf install -y google-chrome-stable

# Install ChromeDriver (ensure it matches the installed Chrome version)
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/

# Verify installations
google-chrome --version
chromedriver --version

echo "Google Chrome and ChromeDriver installation complete."
