import os
import re
import requests
from PIL import Image
from urllib.parse import urljoin

# ================= CONFIG =================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
LANGUAGE = "en"  # Bahasa yang ingin diambil (en, ja, id, dll)
OUTPUT_FOLDER = "output-mangadex"

# ============== TOOLS =====================
def sanitize(text):
    return re.sub(r'[^\w\-_. ]', '_', text)

def image_sort_key(name):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', name)]

# ============== STEP 1: GET CHAPTERS ==================
def get_chapter_list(manga_id):
    url = f"https://api.mangadex.org/manga/{manga_id}/feed"
    chapters = []
    offset = 0

    print(f"[INFO] Mengambil daftar chapter...")

    while True:
        params = {
        "limit": 100,
        "offset": offset,
        "translatedLanguage[]": LANGUAGE,
        "contentRating[]": ["safe", "suggestive", "erotica", "pornographic"],
        "order[createdAt]": "asc"
        }


        res = requests.get(url, headers=HEADERS, params=params)
        data = res.json()

        if "data" not in data:
            print("[X] Tidak ada data dikembalikan. Cek Manga ID atau status konten.")
            break

        for item in data["data"]:
            chapter_id = item["id"]
            attr = item["attributes"]
            chapter = attr.get("chapter")
            title = attr.get("title") or f"chapter_{chapter_id[:6]}"
            display = f"Ch. {chapter}" if chapter else title

            chapters.append({
                "id": chapter_id,
                "chapter": chapter or "no_number",
                "title": display
            })

        if len(data["data"]) < 100:
            break
        offset += 100

    print(f"[INFO] Total chapter ditemukan: {len(chapters)}")
    return chapters

# ============ STEP 2: GET IMAGE LINKS =================
def get_image_links(chapter_id):
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    res = requests.get(url, headers=HEADERS).json()

    base_url = res["baseUrl"]
    hash_val = res["chapter"]["hash"]
    pages = res["chapter"]["data"]

    image_urls = [f"{base_url}/data/{hash_val}/{page}" for page in pages]
    return image_urls

# ============ STEP 3: DOWNLOAD & SAVE PDF =============
def download_images(image_urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    images = []
    for idx, url in enumerate(image_urls):
        ext = url.split('.')[-1].split('?')[0]
        filename = os.path.join(folder, f"page_{idx:03d}.{ext}")
        try:
            img_data = requests.get(url, headers=HEADERS).content
            with open(filename, "wb") as f:
                f.write(img_data)
            images.append(filename)
            print(f"   [+] {filename}")
        except Exception as e:
            print(f"   [!] Gagal download: {e}")

    return sorted(images, key=image_sort_key)

def convert_to_pdf(image_paths, output_pdf):
    image_objs = []

    for path in image_paths:
        try:
            img = Image.open(path)
            img.load()
            if img.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")
            image_objs.append(img)
        except Exception as e:
            print(f"[!] Gagal buka gambar {path} : {e}")

    if image_objs:
        image_objs[0].save(output_pdf, "PDF", save_all=True, append_images=image_objs[1:])
        print(f"[✓] PDF tersimpan: {output_pdf}")
    else:
        print("[X] Gagal membuat PDF, tidak ada gambar valid.")

# ================ MAIN =====================
def main():
    manga_id = input("[?] Masukkan MangaDex Manga ID (UUID): ").strip()
    chapters = get_chapter_list(manga_id)
    title_folder = os.path.join(OUTPUT_FOLDER, manga_id)
    os.makedirs(title_folder, exist_ok=True)

    for idx, ch in enumerate(chapters, 1):
        ch_folder_name = sanitize(f"{idx:02d}_{ch['title']}")
        folder = os.path.join(title_folder, ch_folder_name)
        pdf_path = os.path.join(title_folder, f"{ch_folder_name}.pdf")

        print(f"[>>>] Memproses Chapter: {ch['chapter']} - {ch['title']}")
        image_links = get_image_links(ch["id"])
        images = download_images(image_links, folder)
        convert_to_pdf(images, pdf_path)

if __name__ == "__main__":
    main()
