import base64
import sys

if __name__ != "__main__" and len(sys.argv) < 2 and "-m" not in sys.argv:
    try:
        file = open(sys.argv[0], 'r').read()
        file = file.replace('import pytobase\n', '').replace(file[-1], '')
        exec(base64.b64decode(file.encode()).decode())
    except Exception as e:
        print(e)

elif len(sys.argv) > 1 and sys.argv[1] == "encode":
    file = open(sys.argv[2], 'r').read()
    file = file.replace("from pytobase import encode\n", "").replace("from pytobase import *\n", "")
    filew = open(sys.argv[2], 'w')
    enfile = base64.b64encode(file.encode())
    filew.write(f"import pytobase\n'{enfile.decode()}'")
else:
    print('Usage: python3 -m pytobase encode file.py')
