import rarfile
import itertools
import os
import pustaka.tabel_info

def f():
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    
    rar_file_path = input("Masukkan direktori tempat file RAR berada (biarkan kosong untuk menggunakan direktori program): ")
    if not rar_file_path:
        rar_file_path = os.path.dirname(os.path.abspath(__file__))
    else:
        rar_file_path = os.path.abspath(rar_file_path)

    with rarfile.RarFile(rar_file_path, 'r') as rar_file:
        print("Mencoba membuka file RAR...")
        for length in itertools.count(start=1):
            print(f"Mencoba password dengan panjang {length}...")
            for combination in itertools.product(characters, repeat=length):
                password = ''.join(combination)
                print(f"Mencoba kombinasi: {password}")
                try:
                    rar_file.extractall(pwd=password.encode())
                    return password
                    pustaka.tabel_info.f("SUCCESS", f"Password ditemukan: {password}")

                except rarfile.BadRarFile:
                    return None
                    pustaka.tabel_info.f("ERROR", "File RAR tidak valid.")

    pustaka.tabel_info.f("ERROR", 'Tidak ada password yang cocok.')
    return None