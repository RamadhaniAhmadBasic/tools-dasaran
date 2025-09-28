# IMPORT MODULE ==================================
import os
import re
import requests
import img2pdf
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# VARIABLE DEFINITIONS ===========================
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
output_folder = "manga_output"

# FUNGSI BANTUAN =================================
def sanitize(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)

def imageSorter(text):
    result = []
    for part in re.split(r'(\d+)', text):
        if part.isdigit():
            result.append(int(part))
        else:
            result.append(part.lower())
    return result

# SCRAPE SEMUA LINK CHAPTER ======================
def get_chapter_links(index_url):
    try:
        response = requests.get(index_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            if 'chapter' in href.lower():
                full_url = urljoin(index_url, href)
                links.append((a_tag.text.strip(), full_url))
        return links
    except Exception as e:
        print(f"[!] Error mengambil daftar chapter: {e}")
        return []

# SCRAPE GAMBAR DARI CHAPTER ======================
def get_images_from_chapter(chapter_url):
    try:
        response = requests.get(chapter_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = []
        for img in soup.find_all("img"):
            src = img.get("src")
            if src and "http" in src:
                images.append(urljoin(chapter_url, src))
        return images
    except Exception as e:
        print(f"[!] Error mengambil gambar dari {chapter_url}: {e}")
        return []

# DOWNLOAD DAN BUAT PDF ===========================
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
            print(f"[!] Gagal mengunduh gambar: {img_url} -> {e}")

    # Sort dan konversi ke PDF
    local_images.sort(key=imageSorter)
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(local_images))
    print(f"[✔] PDF berhasil dibuat: {output_pdf}")

# MAIN PROGRAM ====================================
def main():
    index_url = input("[?] Masukkan URL halaman indeks manga: ")
    manga_title = sanitize(index_url.split("/")[-1])
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

        print(f"\n[>>] Mengambil chapter: {title}")
        image_urls = get_images_from_chapter(chapter_url)

        if image_urls:
            download_images_to_pdf(image_urls, chapter_folder, pdf_path)
        else:
            print(f"[!] Tidak ada gambar di {chapter_url}")

if __name__ == "__main__":
    main()
