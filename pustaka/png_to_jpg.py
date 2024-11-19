from PIL import Image
import os
import pustaka.tabel_info

def f():

    directory = input("Masukkan direktori tempat gambar-gambar berada (biarkan kosong untuk menggunakan direktori program): ")

    if not image_folder:
        image_folder = os.path.dirname(os.path.abspath(__file__))
    else:
        image_folder = os.path.abspath(image_folder)
    
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            # Load image
            png_image_path = os.path.join(directory, filename)
            png_image = Image.open(png_image_path)

            # Convert to JPEG
            jpg_image_path = os.path.splitext(png_image_path)[0] + ".jpg"
            jpg_image = png_image.convert("RGB")
            jpg_image.save(jpg_image_path, "JPEG")
            pustaka.tabel_info.f("SUCCESS", f"Converted {filename} to {jpg_image_path}")
        else:
            pustaka.tabel_info.f("ERROR", "Tidak ada file .png ditemukan dalam direktori")