# Python 3.10.6 ==================================
# IMPORT MODULE ==================================
import os
import re
import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image, ImageFile, ImageDraw

# PAKSA PIL LOAD FILE RUSAK ======================
ImageFile.LOAD_TRUNCATED_IMAGES = True

# VARIABLE DEFINITION ============================
browserHeader = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
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
        parsed = urlparse(url)
        base_title = parsed.path.strip("/").split("/")[-1].replace("manga/", "")
        if base_title == "":
            print("[X] Tidak bisa ambil nama manga dari URL.")
            return []

        for link in pageParser.find_all('a', href=True):
            fullURL = urljoin(url, link['href'])
            if "chapter" in fullURL.lower() or "read" in fullURL.lower():
                titleURL = link.text.strip() or fullURL
                chapterLinks.append((titleURL, fullURL))

        chapterLinks = list(dict.fromkeys(chapterLinks))
        print("[V] Total link chapter ditemukan : %s" % len(chapterLinks))
        return chapterLinks

    except Exception as e:
        print("[!] %s" % e)
        return []

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
            if imageTag:
                fullURL = urljoin(url, imageTag)
                imageList.append(fullURL)
        print("[V] Total image ditemukan : %s" % len(imageList))
        return imageList
    except Exception as e:
        print("[!] %s" % e)
        return []

# DOWNLOAD AND CONVERT FUNCTION DEFINITION =======
def downloadImagesAsPdf(imageList, folder, outputPDFPath):
    if not os.path.exists(folder):
        os.makedirs(folder)

    downloadedImages = []

    for i, imageURL in enumerate(imageList):
        try:
            validExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            extensionGuess = imageURL.split('.')[-1].split('?')[0].lower()
            imageExtension = extensionGuess if extensionGuess in validExtensions else 'jpg'

            imageName = os.path.join(folder, "page-%03d.%s" % (i, imageExtension))
            imageData = rq.get(imageURL, headers=browserHeader).content

            with open(imageName, 'wb') as file:
                file.write(imageData)

            downloadedImages.append(imageName)
            print("   [+] %s" % imageName)

        except Exception as e:
            print("[!] %s" % e)

    downloadedImages.sort(key=imageSorter)

    # KONVERSI KE PDF
    imageObjects = []
    for imgPath in downloadedImages:
        try:
            img = Image.open(imgPath)
            img.load()  # paksa load

            # Konversi transparansi dan RGBA
            if img.mode == 'P' and 'transparency' in img.info:
                img = img.convert('RGBA')

            if img.mode in ('RGBA', 'LA'):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")

            imageObjects.append(img)

        except Exception as e:
            print(f"[!] Gagal buka gambar {imgPath} : {e}")
            continue

    try:
        if imageObjects:
            imageObjects[0].save(outputPDFPath, "PDF", resolution=100.0, save_all=True, append_images=imageObjects[1:])
            print("[V] PDF created : %s" % outputPDFPath)
        else:
            print("[!] Semua gambar gagal dibuka. Membuat PDF kosong.")
            blank = Image.new("RGB", (800, 1200), (255, 255, 255))
            draw = ImageDraw.Draw(blank)
            draw.text((50, 600), "PDF Kosong - Semua gambar gagal dibuka", fill=(0, 0, 0))
            blank.save(outputPDFPath, "PDF")

    except Exception as e:
        print(f"[X] PDF tetap gagal disimpan : {e}")

# USER INPUT =====================================
url = input("[?] URL halaman manga : ").strip()

# PROCESS URL ====================================
folderName = sanitizeText(urlparse(url).path.strip("/").split("/")[-1])
outputFolder = os.path.join(outputPDF, folderName)

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# LINK SCRAPE ====================================
chapterList = getChapterLinks(url)
if not chapterList:
    print("[!] Tidak ada link chapter ditemukan")
    exit()

# IMAGE SCRAPE ===================================
for titleLink, LinkFound in chapterList:
    safeTitle = sanitizeText(titleLink)
    chapterFolder = os.path.join(outputFolder, safeTitle)
    pdfFilePath = os.path.join(outputFolder, "%s.pdf" % safeTitle)

    print("[>>>] Memproses %s" % titleLink)
    imageToDownload = getImageLinks(LinkFound)

    if imageToDownload:
        downloadImagesAsPdf(imageToDownload, chapterFolder, pdfFilePath)
    else:
        print("[!] Tidak ada gambar ditemukan di %s" % LinkFound)

# END ============================================
