import pustaka.tabel_info

def f():
    size_input = input("Masukkan ukuran file (contoh: 10 GB, 500 MB, 2 TB): ")
    try:
        size_input = size_input.strip().upper()  # Menghapus spasi dan ubah ke huruf besar
        if size_input.isdigit():  # Jika hanya berisi angka
            size_bytes = float(size_input)
        else:
            size, unit = size_input.split()
            size_bytes = float(size) * {
                "B": 1,
                "KB": 1024,
                "MB": 1024 ** 2,
                "GB": 1024 ** 3,
                "TB": 1024 ** 4,
                "PB": 1024 ** 5,
                "EB": 1024 ** 6,
                "ZB": 1024 ** 7,
                "YB": 1024 ** 8
            }.get(unit, 1)

        if size_bytes == 0:
            pustaka.tabel_info.f("SUCCESS", f"Ukurannya adalah : 0 MB")
            return

        # Konversi ke MB
        size_mb = size_bytes / (1024 ** 2)

        pustaka.tabel_info.f("SUCCESS", f"Ukurannya adalah : {size_mb} MB")
    except ValueError:
        pustaka.tabel_info.f("ERROR", "Format input tidak valid")
    except Exception as e:
        pustaka.tabel_info.f("ERROR", str(e))