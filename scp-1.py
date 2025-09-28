# Python 3.10.6 ==================================
# IMPORT MODULE ==================================
import os
import re
#import time as tm
#import undetected_chromedriver as uc
import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
#import img2pdf as ip

# VARIABLE DEFINITION ============================
browserHeader = {
	"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

outputImage = 'output-image'
outputPDF = 'output-pdf'

# URL SCRAPE FUNCTION DEFINITION =================
def sanitizeText(url):
	output = re.sub(r'[^a-zA-Z0-9_-]', '_', url)
	return output

def getChapterLinks(url):
	try:
		pageRequests = rq.get(url, headers=browserHeader)
		pageParser = BeautifulSoup(pageRequests.content, 'html.parser')

		chapterLinks = []

		for link in pageParser.find_all('a', href=True):
			linkTag = link['href']

			fullURL = urljoin(url, linkTag)
			titleURL = link.text.strip() or fullURL

			chapterLinks.append((titleURL, fullURL))

		chapterLinks = list(dict.fromkeys(chapterLinks))
		print("[V] Total link found : %s" % len(chapterLinks))

		return chapterLinks

	except Exception as e:
		print("[!] %s" % e)
		return chapterLinks

# IMAGE SCRAPE FUNCTION DEFINITION ===============
def imageSorter(list):
	result = []

	for text in re.split(r'(\d+)', list):
		if text.isdigit():
			result.append(int(text))

		else:
			result.append(text.lower())

	return result

def getImageLinks(url):
	try:
		pageRequests = rq.get(url, headers=browserHeader)
		pageParser = BeautifulSoup(pageRequests.content, 'html.parser')

		imageList = []

		for image in pageParser.find_all('img'):
			imageTag = image.get("src")

			fullURL = urljoin(url, imageTag)
			imageList.append(fullURL)

		print("[V] Total image found : %s" % len(imageList))
		return imageList

	except Exception as e:
		print("[!] %s" % e)
		return imageList

# DOWNLOAD AND CONVERT FUNCTION DEFINITION =======
def downloadImagesAsPdf(imageList, folder, outputPDFPath):
	if not os.path.exists(folder):
		os.makedirs(folder)

	downloadedImages = []

	for i, imageURL in enumerate(imageList):
		try:
			validExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
			extensionGuess = imageURL.split('.')[-1].split('?')[0].lower()
			if extensionGuess in validExtensions:
				imageExtension = extensionGuess
			else:
				imageExtension = 'jpg'
			
			imageName = os.path.join(folder, "page-%03d.%s" % (i, imageExtension))
			imageData = rq.get(imageURL, headers=browserHeader).content

			with open(imageName, 'wb') as file:
				file.write(imageData)

			downloadedImages.append(imageName)
			print("   [+] Image Downloaded : %s" % imageName)

		except Exception as e:
			print("[!] %s" % e)

	downloadedImages.sort(key=imageSorter)

	try:
		imageObjects = []
		for imgPath in downloadedImages:
			img = Image.open(imgPath)
			if img.mode in ('RGBA', 'LA'):
				bg = Image.new("RGB", img.size, (255, 255, 255))
				bg.paste(img, mask=img.split()[-1])
				img = bg

			else:
				img = img.convert("RGB")
			imageObjects.append(img)

		if imageObjects:
			imageObjects[0].save(outputPDFPath, "PDF", resolution=100.0, save_all=True, append_images=imageObjects[1:])
			print("[V] PDF created : %s" % outputPDFPath)

		else:
			print("[X] No images to convert")

	except Exception as e:
		print("[X] PDF failed : %s" % e)

# USER INPUT =====================================
url = input("[?] URL : ").strip()

# PROCESS URL ====================================
folderName = sanitizeText(urlparse(url).path.strip("/").split("/")[-1])
outputFolder = os.path.join(outputPDF, folderName)

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)


# LINK SCRAPE ====================================
chapterList = getChapterLinks(url)
if not chapterList:
	print("[!] No link found")

# IMAGE SCRAPE ===================================
for titleLink, LinkFound in chapterList:
	safeTitle = sanitizeText(titleLink)
	chapterFolder = os.path.join(outputFolder, safeTitle)
	pdfFilePath = os.path.join(outputFolder, "%s.pdf" % safeTitle)

	print("[>>>] Processing %s" % titleLink)

	imageToDownload = getImageLinks(LinkFound)

	if imageToDownload:
		downloadImagesAsPdf(imageToDownload, chapterFolder, pdfFilePath)

	else:
		print("[!] No image found : %s" % LinkFound)

# END ============================================