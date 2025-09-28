# Python 3.10.6
# Import Module
import os

# Define Variable
string_direktori_kerja = os.getcwd()
string_direktori_file = os.path.abspath(__file__)

# Function to calculate number of files and total size
def hitung_file_dan_ukuran(path):
    total_file = 0
    total_ukuran = 0
    for root, dirs, files in os.walk(path):
        total_file += len(files)
        for f in files:
            try:
                total_ukuran += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass  # Abaikan file yang tidak bisa diakses
    total_ukuran_MB = total_ukuran / (1024 * 1024)
    return total_file, total_ukuran_MB

# Define Function
def fungsi_tampilan(path, file_path):
    # Info direktori
    file_count, size_MB = hitung_file_dan_ukuran(path)
    print()
    print("[ Direktori: %s ]" % path)
    print("="*64)
    print("Jumlah File : %49d" % file_count)
    print("Total Ukuran : %46.2f MB" % size_MB)

    # Info file
    if os.path.exists(file_path):
        size_file = os.path.getsize(file_path) / (1024 * 1024)
        print()
        print("[ File: %s ]" % file_path)
        print("="*64)
        print("Ukuran File : %54.2f MB" % size_file)
    else:
        print()
        print("[ File: %s ]" % file_path)
        print("="*64)
        print("File tidak ditemukan.")

# Main Program
def main():
    fungsi_tampilan(string_direktori_kerja, string_direktori_file)

if __name__ == '__main__':
    main()
