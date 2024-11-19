import socket
import pustaka.tabel_info

def f():
	url = input("Masukkan URL: ")
	try:
		ip_address = socket.gethostbyname(url)
		pustaka.tabel_info.f("SUCCESS", f"Alamat IP ditemukan: {ip_address}")
	except socket.gaierror:
		pustaka.tabel_info.f("ERROR", "Alamat IP tidak dapat ditemukan")

	except Exception as e:
		pustaka.tabel_info.f("SUCCESS", "Input tidak valid")