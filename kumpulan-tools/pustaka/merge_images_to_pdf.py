import os
import PIL.Image
import reportlab.lib.pagesizes
import reportlab.pdfgen.canvas
import pustaka.tabel_info

def f():
    image_folder = input("Masukkan direktori tempat gambar-gambar berada (biarkan kosong untuk menggunakan direktori program): ")
    if not image_folder:
        image_folder = os.path.dirname(os.path.abspath(__file__))
    else:
        image_folder = os.path.abspath(image_folder)

    output_pdf = input("Masukkan nama file PDF output: ")

    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            filepath = os.path.join(image_folder, filename)
            images.append(filepath)

    if images:
        c = reportlab.pdfgen.canvas.Canvas(output_pdf, pagesize=reportlab.lib.pagesizes.letter)
        for idx, image_path in enumerate(images):
            with PIL.Image.open(image_path) as img:
                width, height = img.size
                c.setPageSize((width, height))  # Menyesuaikan ukuran halaman dengan gambar
                c.drawImage(image_path, 0, 0)
                if idx != len(images) - 1:
                    c.showPage()  # Memisahkan halaman-halaman

            print(f"{idx + 1}/{len(images)}: {os.path.basename(image_path)} ++")

        c.save()
        pustaka.tabel_info.f("SUCCESS", f"File PDF berhasil dibuat: {output_pdf}")
    else:
        pustaka.tabel_info.f("ERROR", "Tidak ada file gambar (.jpg, .jpeg, .png, .bmp, .gif) ditemukan dalam direktori")
