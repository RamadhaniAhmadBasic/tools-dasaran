import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
output_dir = "output-chapter"

def sanitize(text):
    return re.sub(r'[^\w\-_. ]', '_', text)

def get_image_links(chapter_url):
    try:
        res = requests.get(chapter_url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        images = []

        for img in soup.select("div.reading-content img"):
            src = img.get("src")
            if not src or "dflazy" in src:
                src = img.get("data-src") or img.get("data-lazy-src")
            if src and "http" in src:
                images.append(src.strip())

        if images:
            print(f"[✓] Ditemukan {len(images)} gambar")
        else:
            print("[X] Tidak ada gambar ditemukan")
        return images
    except Exception as e:
        print(f"[!] Gagal ambil gambar: {e}")
        return []

def download_images(image_urls, folder):
    os.makedirs(folder, exist_ok=True)
    paths = []

    for i, url in enumerate(image_urls):
        ext = url.split('.')[-1].split('?')[0]
        ext = ext if ext in ['jpg', 'jpeg', 'png', 'webp'] else 'jpg'
        fname = os.path.join(folder, f"page_{i:03d}.{ext}")
        try:
            img = requests.get(url, headers=headers).content
            with open(fname, 'wb') as f:
                f.write(img)
            paths.append(fname)
            print(f"  [+] {fname}")
        except Exception as e:
            print(f"  [!] Gagal download {url}: {e}")
    return paths

def convert_to_pdf(image_paths, output_pdf):
    images = []
    for path in image_paths:
        try:
            img = Image.open(path).convert("RGB")
            images.append(img)
        except Exception as e:
            print(f"[!] Gagal buka {path}: {e}")

    if images:
        images[0].save(output_pdf, "PDF", save_all=True, append_images=images[1:])
        print(f"[✓] PDF berhasil dibuat: {output_pdf}")
    else:
        print("[X] Tidak ada gambar valid")

def main():
    url = input("[?] Masukkan URL chapter ValkyrieScan: ").strip()
    if not url or "/manga/" not in url and "/capitulo" not in url:
        print("[X] URL tidak valid")
        return

    slug = sanitize(url.strip("/").split("/")[-1])
    folder = os.path.join(output_dir, slug)
    pdf_path = os.path.join(output_dir, f"{slug}.pdf")

    print(f"[>>>] Proses: {url}")
    images = get_image_links(url)
    if images:
        paths = download_images(images, folder)
        convert_to_pdf(paths, pdf_path)
    else:
        print("[X] Tidak ada gambar di halaman ini")

if __name__ == "__main__":
    main()
