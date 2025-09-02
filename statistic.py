# Python 3.10.6
# Import Module

# Define Variable
list_nilai_vertikal   = [110, 105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]
list_nilai_horizontal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
list_nilai_konten     = [60, 9, 97, 11, 42, 19, 92, 97, 12, 59, 91, 18, 75, 55, 23, 12, 51, 29, 43, 28, 55, 30, 1, 55, 7, 53, 68, 100, 47, 8, 45]

# Define Function
def fungsi_diagram_unicode(list_nilai_vertikal, list_nilai_horizontal, list_nilai_konten, string_nama_tabel):
	print("   [ %s ]" % string_nama_tabel)
	print("   +%s+" % ("-"*94))

	for integer_nilai_vertikal in list_nilai_vertikal:
		print("%3s| " % integer_nilai_vertikal, end='')

		for integer_nilai_horizontal, integer_nilai_konten in zip(list_nilai_horizontal, list_nilai_konten):
			if integer_nilai_vertikal <= integer_nilai_konten:
				print("\u2588\u2588 ", end='')

			elif integer_nilai_vertikal - 4 <= integer_nilai_konten:
				print("\u2584\u2584 ", end='')

			else:
				print("\u0020\u0020 ", end='')

		print("|")

	print("   +%s+" % ("-"*94))
	print("     ", end='')

	for integer_nilai_horizontal in list_nilai_horizontal:
		print("%02d " % integer_nilai_horizontal, end='')

# Main Program
def main():
	print("[\033[36m PROGRAM MANAJEMEN KEUANGAN \033[0m]")
	print("="*64)

	print("[?] Main Menu :")
	print("[1] Tampilkan Laporan Keuangan")
	print("[2] Tambah Pemasukan")
	print("[3] Tambah Pengeluaran")
	print("[4] Manipulasi Laporan")
	print("[5] Keluar")

if __name__ == '__main__':
	main()
