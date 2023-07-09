# print every line back
import sys
from pandocode.codeprocessor import process_code

print("Content-type: text/plain\n\n")

print(process_code(sys.stdin.read()))
