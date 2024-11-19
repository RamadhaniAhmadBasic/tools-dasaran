import socket

def ip_to_url(ip_address):
    try:
        url = socket.gethostbyaddr(ip_address)
        return url[0]
    except socket.herror:
        return "Tidak dapat mengonversi IP ke URL"

def url_to_ip(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return "Tidak dapat mengonversi URL ke IP"

def main():
    while True:
        print("\nPilih operasi:")
        print("1. IP ke URL")
        print("2. URL ke IP")
        print("0. Keluar")
        choice = input("Masukkan pilihan: ")

        if choice == "1":
            ip_address = input("Masukkan alamat IP: ")
            print("URL: ", ip_to_url(ip_address))
        elif choice == "2":
            url = input("Masukkan URL: ")
            print("IP Address: ", url_to_ip(url))
        elif choice == "0":
            print("Terima kasih! Keluar.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
