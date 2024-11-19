import os
from PIL import Image

def convert_webp_to_png(directory):
    # Loop melalui semua file di direktori
    for filename in os.listdir(directory):
        if filename.lower().endswith('.webp'):
            webp_path = os.path.join(directory, filename)
            png_path = os.path.join(directory, os.path.splitext(filename)[0] + '.png')
            
            try:
                # Membuka file webp dan menyimpannya sebagai png
                with Image.open(webp_path) as img:
                    img.save(png_path, 'PNG')
                print(f"Berhasil mengonversi: {filename} -> {os.path.basename(png_path)}")
            except Exception as e:
                print(f"Error saat mengonversi {filename}: {e}")

if __name__ == "__main__":
    # Mendapatkan direktori tempat script ini dijalankan
    current_directory = os.getcwd()
    print(f"Mengonversi file .webp di direktori: {current_directory}")
    convert_webp_to_png(current_directory)
