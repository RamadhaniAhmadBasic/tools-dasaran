# Python 3.10.6
# Import Module

# Define Variable
nilai_konten     = [60, 9, 97, 11, 42, 19, 92, 97, 12, 59, 91, 18, 75, 55, 23, 12, 51, 29, 43, 28, 55, 30, 1, 55, 7, 53, 68, 100, 47, 8, 45]
nilai_horizontal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
nilai_vertikal   = [110, 105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]

# Define Function
def fungsi_tabel_ascii(list_nilai_vertikal, list_nilai_horizontal, list_nilai_konten, integer_nilai_minimal=0):
	for integer_nilai_vertikal in list_nilai_vertikal:
		print("%3s |" % integer_nilai_vertikal, end='')

		for integer_nilai_konten, integer_nilai_horizontal in zip(list_nilai_konten, list_nilai_horizontal):
			if integer_nilai_vertikal <= integer_nilai_konten:
				print("██ ", end='')

			else:
				print("   ", end='')
		print()

	print("    +%s" % ("-"*93))
	print("    ", end='')

	for integer_nilai_horizontal in list_nilai_horizontal:
		print("%03s" % integer_nilai_horizontal, end='')

# Main Program
def main():
	fungsi_tabel_ascii(nilai_vertikal, nilai_horizontal, nilai_konten)

if __name__ == '__main__':
	main()