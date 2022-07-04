#!/bin/bash 

# Configure package
python3 setup.py check
if [ $? -ne 0 ]; then
    echo "<!> check failed"
    exit
fi 

python3 setup.py sdist
if [ $? -ne 0 ]; then
    echo "<!> sdist failed"
    exit
fi 

## EXECUTIBLE ##
pip3 install -r requirements.txt

# Create executible
pyinstaller --name slackTools --onefile slackTools/__main__.py 

# Test executible
./dist/slackTools --help

# Install to user
cp ./dist/slackTools ~/.local/bin/.

# Test executible
slackTools --help

echo
echo "<!> CHECK that local user programs are added to PATH in ~/.bashrc by adding: "
echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "And then reload bashrc:"
echo "source ~/.bashrc"
echo 

## LIBRARY ##

# Library install
pip3 install --upgrade . 

# Test Library
python3 slackTools -h