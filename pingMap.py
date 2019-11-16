#Creator : Elwan Mayencourt
#Date : 16.11.2019
#Version : 1
#Utility : Create graphic with response time of all IP in the network

from pythonping import ping
from PIL import Image, ImageDraw,ImageFont
import os 
import random
import math
import numpy
import time
font = ImageFont.truetype('/templates/arial.ttf', 60)
def normalize(number):
	number = math.ceil(number*60)
	return number
im = Image.new('RGBA', (4000, 4000)) 
draw = ImageDraw.Draw(im)
listIp = os.popen("arp -a").read()
listIp = listIp.split("\n")
dynamiqueIp = ""
result = ""
for x in range(len(listIp)):
	if("dynamique" in listIp[x]):
		dynamiqueIp = dynamiqueIp + listIp[x]+"\n"


dynamiqueIp = dynamiqueIp.split("\n")

ipTab = ""
numTab = 0
for y in dynamiqueIp:
	try:
		ipTab = ipTab + dynamiqueIp[numTab].split("  ")[1] +"\n"
		numTab = numTab + 1
	except:
		print("")

ipTab = ipTab.split("\n")
while '' in ipTab:
    ipTab.remove('')
ms = ""
for z in range(len(ipTab)):
	response_list = ping(ipTab[z], size=32, count=5)
	ms = ms+ str(normalize(response_list.rtt_avg_ms))+"\n"

msTab = ms.split("\n")
while '' in msTab:
    msTab.remove('')
for y in range(0,len(msTab)):
	msTab[y] = int(msTab[y])

msTab = numpy.array(msTab)
ipTab = numpy.array(ipTab)

inds = msTab.argsort()[::-1]
ipTab = ipTab[inds]

msTab = sorted(msTab)
msTab = msTab[::-1]
print("-----------------List IP ---------------------"+"\n")
print(ipTab)
print("-----------------List MS ---------------------"+"\n")
print(msTab)

pos = 0
boucle = 0
for num in msTab:
	rColor = random.randint(0,255)
	gColor = random.randint(0,255)
	bColor = random.randint(0,255)
	draw.ellipse((2000-(2*num), 2000-(2*num), 2000+num, 2000+num), fill = (rColor,gColor,bColor,255), outline=(0,0,0,255))
	draw.ellipse((100, 100+pos, 200, 200+pos), fill = (rColor,gColor,bColor,255), outline=(0,0,0,255))
	draw.text((250,200+pos-80), str(round(num/60,2))+"ms " + ipTab[boucle], fill=(0,0,0),font = font)
	pos = pos + 150
	boucle = boucle + 1

time.sleep(1)
im.save("pingMap.png", "PNG")
