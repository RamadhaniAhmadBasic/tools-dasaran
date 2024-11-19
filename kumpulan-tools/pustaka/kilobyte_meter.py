import math
import pustaka.tabel_info

def f():
    size_kb = input("Masukkan ukuran file (dalam KB): ")
    try:
        size_bytes = float(size_kb) * 1024
        if size_bytes == 0:
            pustaka.tabel_info.f("SUCCESS", "Ukurannya adalah : 0 B")
            return

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = max(0, min(len(size_name) - 1, int(math.floor(math.log(size_bytes, 1024)))))
        p = 1024 ** i
        s = round(size_bytes / p, 2)

        pustaka.tabel_info.f("SUCCESS", f"Ukurannya adalah : {s} {size_name[i]}")
    except ValueError:
        pustaka.tabel_info.f("ERROR", "Input tidak valid")
    except Exception as e:
        pustaka.tabel_info.f("ERROR", str(e))
