'''
@Description: OCR Translation
@Author: Jack
@Date: 2019-05-26 10:22:43
@LastEditTime: 2019-05-26 16:05:00
@LastEditors: Please set LastEditors
'''
import os 
import pytesseract
import cv2 
import subprocess
from dict import Dict

def sendmessage(message):
    subprocess.Popen(['notify-send', '-i','dictionary',message])
    return

sendmessage('Start to capture')
# import pyscreenshot as ImageGrab
# 1. Screenshot
cmd = 'scrot -s -q 100 /tmp/foo.png ; xclip -selection c -t image/png < /tmp/foo.png'
os.system(cmd)
# 2. OCR
# Define config parameters.
# '-l eng'  for using the English language
# '--oem 1' for using LSTM OCR Engine
config = ('-l eng --oem 1 --psm 3')
im = cv2.imread('/tmp/foo.png', cv2.IMREAD_COLOR)
# print(im.size)
# Run tesseract OCR on image
text = pytesseract.image_to_string(im, config=config)
if(len(text) == 0):
    exit()
# print(text)
input_str = text.split()
# print(input_str)
# 3. Translation
dc = Dict(input_str)
result = dc.translate()
print(result)


# # 4. Output Result
sendmessage(result)
cmd_add_to_a = 'echo ' +'\"' + result + '\"' + '| xclip'
# print(cmd_add_to_a)
os.system(cmd_add_to_a)
