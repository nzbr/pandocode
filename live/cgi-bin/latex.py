import sys
from pandocode.codeprocessor import process_code

print("Content-type: text/plain")
print("Access-Control-Allow-Origin: *")
print("")
sys.stdout.flush()

sys.stdout.write(process_code(sys.stdin.read()))
sys.stdout.flush()
