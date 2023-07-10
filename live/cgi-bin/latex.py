# print every line back
import sys
from pandocode.codeprocessor import process_code

print("Content-type: text/plain")
print("Access-Control-Allow-Origin: *")
print("")

print(process_code(sys.stdin.read()))
