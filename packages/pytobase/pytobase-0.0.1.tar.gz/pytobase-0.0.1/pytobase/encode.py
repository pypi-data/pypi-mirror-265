import sys
import base64

file = open(sys.argv[0], 'r').read()
if file == "":
    sys.exit()
file = file.replace("from pytobase import encode\n", "").replace("from pytobase import *\n", "")
filew = open(sys.argv[0], 'w')
enfile = base64.b64encode(file.encode())
filew.write(f"import pytobase\n'{enfile.decode()}'")