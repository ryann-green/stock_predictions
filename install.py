# use the code below to use for importing packages within this instance of python
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    

install('dash')
