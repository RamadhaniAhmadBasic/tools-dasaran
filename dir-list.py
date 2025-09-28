# Python 3.10.6
import os
from pathlib import Path

# Lokasi kerja (folder tempat file .py dijalankan)
lokasi_kerja = Path(__file__).parent

# Daftar ekstensi yang mau dihitung
kategori = {
    "File .JPG": [".jpg", ".jpeg"],
    "File .PNG": [".png"],
    "File .GIF": [".gif"],
    "File .WEBP": [".webp"],
    "File .MOV": [".mov"],
    "File .TS": [".ts"],
    "File .MP4": [".mp4"],
}

# Fungsi untuk hitung jumlah & ukuran
def hitung_file(folder, ekstensi_list):
    total_file = 0
    total_size = 0
    for file in folder.rglob("*"):
        if file.is_file() and file.suffix.lower() in ekstensi_list:
            total_file += 1
            total_size += file.stat().st_size
    return total_file, total_size

# Fungsi tampilan terminal
def fungsi_tampilan_terminal():
    print()
    print("[ %s ]" % lokasi_kerja)
    print("================================================================")
    print(" %40s %10s %15s " % ("", "Total", "Size (MB)"))

    grand_total_file = 0
    grand_total_size = 0

    for nama, ekstensi in kategori.items():
        jumlah, ukuran = hitung_file(lokasi_kerja, ekstensi)
        grand_total_file += jumlah
        grand_total_size += ukuran
        print(" %-42s %8d %12.2fMB " % (nama, jumlah, ukuran/(1024*1024)))

    print()
    print(" %-42s %8d %12.2fMB " % ("Exist Total", grand_total_file, grand_total_size/(1024*1024)))
    print("----------------------------------------------------------------")
    print(" %-42s %8d %12.2fMB " % ("Grand Total", grand_total_file, grand_total_size/(1024*1024)))
    print("================================================================")

# Main Program
def main():
    fungsi_tampilan_terminal()

if __name__ == '__main__':
    main()
