# IMPORT MODULE ==================================
import os
import re
import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image

# VARIABLE DEFINITION ============================
browserHeader = {
	"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

outputImage = 'output-image'
outputPDF = 'output-pdf'

# URL SANITIZER ==================================
def sanitizeText(url):
	return re.sub(r'[^a-zA-Z0-9_-]', '_', url)

# SCRAPE CHAPTER LINKS ===========================
def getChapterLinks(url):
	try:
		resp = rq.get(url, headers=browserHeader)
		soup = BeautifulSoup(resp.content, 'html.parser')

		chapterLinks = []
		for a in soup.find_all('a', href=True):
			href = a['href']
			fullURL = urljoin(url, href)
			if '/read/' in fullURL:
				title = a.text.strip() or fullURL
				chapterLinks.append((title, fullURL))

		chapterLinks = list(dict.fromkeys(chapterLinks))  # hapus duplikat
		print(f"[V] Total link chapter ditemukan : {len(chapterLinks)}")
		return chapterLinks

	except Exception as e:
		print(f"[!] {e}")
		return []

# SCRAPE IMAGE LINKS =============================
def getImageLinks(url):
	try:
		resp = rq.get(url, headers=browserHeader)
		soup = BeautifulSoup(resp.content, 'html.parser')
		imageList = []

		for img in soup.find_all('img'):
			src = img.get('src')
			if src:
				imageURL = urljoin(url, src)
				imageList.append(imageURL)

		print(f"[V] Total image ditemukan : {len(imageList)}")
		return imageList

	except Exception as e:
		print(f"[!] {e}")
		return []

# IMAGE SORTER ===================================
def imageSorter(text):
	result = []
	for part in re.split(r'(\d+)', text):
		result.append(int(part) if part.isdigit() else part.lower())
	return result

# DOWNLOAD & CONVERT =============================
def downloadImagesAsPdf(imageList, folder, outputPDFPath):
	if not os.path.exists(folder):
		os.makedirs(folder)

	downloadedImages = []

	for i, imageURL in enumerate(imageList):
		try:
			ext = imageURL.split('.')[-1].split('?')[0].lower()
			ext = ext if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp'] else 'jpg'
			filename = os.path.join(folder, f"page-{i:03d}.{ext}")
			data = rq.get(imageURL, headers=browserHeader).content

			with open(filename, 'wb') as f:
				f.write(data)

			downloadedImages.append(filename)
			print(f"[+] Image Downloaded : {filename}")
		except Exception as e:
			print(f"[!] Gagal download gambar: {e}")

	downloadedImages.sort(key=imageSorter)

	images = []
	for path in downloadedImages:
		try:
			img = Image.open(path)
			if img.mode in ('RGBA', 'LA'):
				bg = Image.new("RGB", img.size, (255, 255, 255))
				bg.paste(img, mask=img.split()[-1])
				img = bg
			else:
				img = img.convert("RGB")
			images.append(img)
		except Exception as e:
			print(f"[!] Gagal membuka atau mengonversi gambar {path}: {e}")

	if images:
		try:
			images[0].save(outputPDFPath, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
			print(f"[V] PDF created : {outputPDFPath}")
		except Exception as e:
			print(f"[X] Gagal membuat PDF: {e}")
	else:
		print("[X] Tidak ada gambar valid untuk dikonversi ke PDF.")

# MAIN LOGIC =====================================
url = input("[?] URL halaman manga (https://thrive.moe/title/...) : ").strip()

folderName = sanitizeText(urlparse(url).path.strip("/").split("/")[-1])
outputFolder = os.path.join(outputPDF, folderName)
os.makedirs(outputFolder, exist_ok=True)

chapterList = getChapterLinks(url)
if not chapterList:
	print("[!] Tidak ada link chapter ditemukan.")
	exit()

for title, link in chapterList:
	safeTitle = sanitizeText(title)
	chapterFolder = os.path.join(outputFolder, safeTitle)
	pdfFilePath = os.path.join(outputFolder, f"{safeTitle}.pdf")

	print(f"[>>>] Memproses {title}")
	images = getImageLinks(link)
	if images:
		downloadImagesAsPdf(images, chapterFolder, pdfFilePath)
	else:
		print(f"[!] Tidak ada gambar ditemukan di {link}")
