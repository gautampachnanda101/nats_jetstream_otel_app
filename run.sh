# Check if Python is installed
python3 --version

# Try using pip3
pip3 --version

# If pip3 is not found, install it:
python3 -m ensurepip --upgrade

# If still not found, install with Homebrew (if you have Homebrew):
brew install python

pip3 --version

python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate


# Or, download and install Python from https://www.python.org/downloads/
pip3 install opentelemetry-instrumentation
pip3 install --upgrade pip
pip3 install --no-cache-dir -r requirements.txt
docker-compose down --volumes --remove-orphans
docker-compose up -d --build
