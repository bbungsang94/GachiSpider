#!/bin/bash

# Print current directory
echo "$(pwd)"

# Activate virtual environment
source "./temp/Scripts/activate" || {
  echo "Failed to activate Python environment"
  sleep 5
  exit 1
}

echo "Activated temp environment to install latest version"
echo "Check your path"

# Change to parent directory
cd ..
echo "$(pwd)"

# Wait for 5 seconds
sleep 5
echo "Install latest version"

# Upgrade pip and install the latest version of the package
pip install --upgrade pip
pip install . --target ./aws/lambda/Lib --upgrade

# Sweep dump files (delete directories)
echo "Sweep dump files"
rm -rf "./build"
rm -rf "./spider.egg-info"
rm -rf "./aws/lambda/Lib/spider-1.2.dist-info"

# Wait for 30 seconds
sleep 30