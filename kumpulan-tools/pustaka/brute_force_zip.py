import zipfile
import itertools
import os
import pustaka.tabel_info

def f():
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    
    zip_file_path = input("Masukkan direktori tempat file ZIP berada (biarkan kosong untuk menggunakan direktori program): ")
    if not zip_file_path:
        zip_file_path = os.path.dirname(os.path.abspath(__file__))
    else:
        zip_file_path = os.path.abspath(zip_file_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        print("Mencoba membuka file ZIP...")
        for length in itertools.count(start=1):
            print(f"Mencoba password dengan panjang {length}...")
            for combination in itertools.product(characters, repeat=length):
                password = ''.join(combination)
                print(f"Mencoba kombinasi: {password}")
                try:
                    zip_file.extractall(pwd=password.encode())
                    pustaka.tabel_info.f("SUCCESS", f"Password ditemukan: {password}")
                    return password
                except Exception as e:
                    continue

    print()
    pustaka.tabel_info.f("ERROR", 'Tidak ada password yang cocok')
    return None
