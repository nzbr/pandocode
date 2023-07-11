# print every line back
import os
import subprocess
import sys
from io import BytesIO

import numpy
from PIL import Image
from pdf2image import convert_from_bytes

from pandocode.codeprocessor import process_code

options = os.environ['QUERY_STRING'].split('&')

output = 'pdf'
extraOpt = []
inputData = sys.stdin.read()
content_type = 'image/webp'

if 'markdown' in options:
    extraOpt = ['--filter', 'pandocode', '--standalone', '--metadata=documentclass:standalone', '--metadata=classoption:preview']
else:
    extraOpt = ['--template', '/etc/template.tex']
    inputData = process_code(inputData)

if 'code' in options:
    output = 'latex'
    content_type = 'text/plain'

print(f"Content-type: {content_type}")
print("Access-Control-Allow-Origin: *")
print("")
sys.stdout.flush()

process = subprocess.run(
    [
        'pandoc',
        '-f', 'markdown',
        '-t', output,
    ] + extraOpt + [
        '--pdf-engine', 'pdflatex',
        '--pdf-engine-opt', '-disable-write18',
        '-o', '-'
    ],
    input=inputData.encode('utf-8'),
    stdout=subprocess.PIPE,
)
if process.returncode != 0:
    exit(process.returncode)

if 'code' in options:
    sys.stdout.buffer.write(process.stdout)
    sys.stdout.flush()
    exit(0)

images = convert_from_bytes(process.stdout)
image = images[0]

# Remove background (https://stackoverflow.com/a/21228321/12852285)
image = image.convert('RGBA')
data = numpy.array(image)
rgb = data[:, :, :3]
color = [255, 255, 255]  # Original value
mask = numpy.all(rgb == color, axis=-1)
data[mask] = [0, 0, 0, 0]
image = Image.fromarray(data)

# Crop out transparent padding
image = image.crop(image.getbbox())

image_bytes = BytesIO()
image.save(image_bytes, format='WebP')
image_bytes = image_bytes.getvalue()

sys.stdout.buffer.write(image_bytes)
sys.stdout.flush()
