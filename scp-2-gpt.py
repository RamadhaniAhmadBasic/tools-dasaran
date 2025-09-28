import os
import re
import requests
import img2pdf
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# === KONFIGURASI & HEADER ===
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
output_folder = "manga_output"

# === UTILITAS BANTUAN ===
def sanitize(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)

def imageSorter(text):
    result = []
    for part in re.split(r'(\d+)', text):
        result.append(int(part) if part.isdigit() else part.lower())
    return result

# === SCRAPE SEMUA LINK CHAPTER ===
def get_chapter_links(index_url):
    try:
        response = requests.get(index_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        links = []
        for a in soup.find_all("a", href=True):
            href = a['href']
            full_url = urljoin(index_url, href)
            title = a.text.strip() or full_url
            links.append((title, full_url))

        # Hilangkan duplikat
        links = list(dict.fromkeys(links))

        print(f"[i] Total semua link ditemukan: {len(links)}")
        return links
    except Exception as e:
        print(f"[!] Error ambil semua <a>: {e}")
        return []

# === SCRAPE GAMBAR DARI SETIAP CHAPTER ===
def get_images_from_chapter(chapter_url):
    try:
        response = requests.get(chapter_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = []
        for img in soup.find_all("img"):
            src = img.get("src")
            if src and "http" in src:
                full_src = urljoin(chapter_url, src)
                images.append(full_src)
        return images
    except Exception as e:
        print(f"[!] Gagal ambil gambar dari {chapter_url}: {e}")
        return []

# === DOWNLOAD GAMBAR DAN BUAT PDF ===
def download_images_to_pdf(image_urls, folder, output_pdf):
    if not os.path.exists(folder):
        os.makedirs(folder)

    local_images = []
    for i, img_url in enumerate(image_urls):
        try:
            ext = img_url.split('.')[-1].split('?')[0]
            filename = os.path.join(folder, f"page_{i:03d}.{ext}")
            img_data = requests.get(img_url, headers=headers).content
            with open(filename, 'wb') as f:
                f.write(img_data)
            local_images.append(filename)
            print(f"[+] Gambar disimpan: {filename}")
        except Exception as e:
            print(f"[!] Gagal download gambar: {img_url} -> {e}")

    # Sort gambar dan konversi ke PDF
    local_images.sort(key=imageSorter)
    try:
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(local_images))
        print(f"[✔] PDF selesai: {output_pdf}")
    except Exception as e:
        print(f"[!] Gagal buat PDF: {e}")

# === PROGRAM UTAMA ===
def main():
    index_url = input("[?] Masukkan URL halaman manga (daftar chapter): ").strip()
    manga_title = sanitize(urlparse(index_url).path.strip("/").split("/")[-1])
    manga_folder = os.path.join(output_folder, manga_title)

    chapter_links = get_chapter_links(index_url)
    if not chapter_links:
        print("[!] Tidak ada chapter ditemukan.")
        return

    print(f"[i] Total chapter ditemukan: {len(chapter_links)}")

    for title, chapter_url in chapter_links:
        safe_title = sanitize(title)
        chapter_folder = os.path.join(manga_folder, safe_title)
        pdf_path = os.path.join(manga_folder, f"{safe_title}.pdf")

        print(f"\n[>>] Proses: {title}")
        image_urls = get_images_from_chapter(chapter_url)

        if image_urls:
            download_images_to_pdf(image_urls, chapter_folder, pdf_path)
        else:
            print(f"[!] Tidak ada gambar dari chapter ini: {chapter_url}")

if __name__ == "__main__":
    main()
