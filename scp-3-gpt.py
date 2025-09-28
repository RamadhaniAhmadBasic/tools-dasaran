import os
import re
import time
import urllib
from urllib.parse import urlparse, urljoin
import requests
from PIL import Image
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

visited_pages = set()

def natural_sort_key(text):
	parts = re.split(r'(\d+)', text)
	key = []
	for part in parts:
		if part.isdigit():
			key.append(int(part))
		else:
			key.append(part.lower())
	return key

def fetch_html(url):
	print('[INFO] Mengambil HTML dari:', url)
	options = uc.ChromeOptions()
	options.headless = True
	browser = uc.Chrome(options=options)
	browser.get(url)
	time.sleep(1)
	html = browser.page_source
	browser.quit()
	print('[DEBUG] Panjang HTML:', len(html))
	return html

def download_image(img_url, save_dir):
	print('[INFO] Mengunduh gambar:', img_url)
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)
	parsed = urlparse(img_url)
	filename = os.path.basename(parsed.path)
	local_path = os.path.join(save_dir, filename)
	try:
		r = requests.get(img_url, stream=True, timeout=10)
		with open(local_path, 'wb') as f:
			for chunk in r.iter_content(1024):
				f.write(chunk)
	except Exception as e:
		print('[ERROR] Gagal mengunduh:', img_url, '-', e)
	return local_path

def images_to_pdf(image_paths, pdf_path):
	print('[INFO] Mengonversi gambar ke PDF:', pdf_path)
	images = []
	for path in image_paths:
		try:
			img = Image.open(path)
			if img.mode == 'RGBA':
				rgb = Image.new('RGB', img.size, (255,255,255))
				rgb.paste(img, mask=img.split()[3])
				img = rgb
			else:
				img = img.convert('RGB')
			images.append(img)
		except Exception as e:
			print('[WARNING] Lewati gambar gagal:', path, '-', e)
	if images:
		first = images[0]
		rest = images[1:]
		first.save(pdf_path, save_all=True, append_images=rest)
		print('[INFO] PDF selesai:', pdf_path)


def scrape_page(base_url, work_dir):
	if base_url in visited_pages:
		print('[SKIP] Sudah dikunjungi:', base_url)
		return
	print('[SCRAPE] Halaman:', base_url)
	visited_pages.add(base_url)

	domain = urlparse(base_url).netloc
	html = fetch_html(base_url)
	soup = BeautifulSoup(html, 'html.parser')

	img_tags = soup.find_all('img')
	valid_ext = ['.jpg', '.jpeg', '.png', '.webp']
	img_urls = []
	for tag in img_tags:
		src = tag.get('src') or tag.get('data-src')
		if not src:
			continue
		full = urljoin(base_url, src)
		ext = os.path.splitext(urlparse(full).path)[1].lower()
		if ext in valid_ext:
			img_urls.append(full)

	img_urls = sorted(set(img_urls), key=natural_sort_key)
	print('[INFO] Total gambar ditemukan:', len(img_urls))

	site_name = domain.replace(':', '_')
	page_name = re.sub(r'[^0-9a-zA-Z]+', '_', base_url)
	img_out = os.path.join(work_dir, 'output-image', site_name, page_name)
	pdf_out_dir = os.path.join(work_dir, 'output-pdf', site_name)
	os.makedirs(pdf_out_dir, exist_ok=True)

	local_images = []
	for url in img_urls:
		local_images.append(download_image(url, img_out))
	pdf_path = os.path.join(pdf_out_dir, '%s.pdf' % page_name)
	images_to_pdf(local_images, pdf_path)

	links = soup.find_all('a', href=True)
	page_urls = []
	for a in links:
		href = urljoin(base_url, a['href'])
		if urlparse(href).netloc == domain:
			page_urls.append(href)

	page_urls = sorted(set(page_urls))
	print('[INFO] Link internal ditemukan:', len(page_urls))

	for p_url in page_urls:
		scrape_page(p_url, work_dir)

def main():
	url = input('Masukkan URL manga: ')
	work_dir = os.getcwd()
	scrape_page(url, work_dir)

if __name__ == '__main__':
	main()