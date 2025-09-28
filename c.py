# Python 3.10.6
# Import Module
import os

# Define Variable
jumlah_harian = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 105, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 40]

# Define Function
def tabel(jumlah_harian):
    # Loop dari 100 ke 0, step -5 (agar ada baris 5, 15, dst)
    for tinggi in range(100, 0, -5):
        # hanya tampilkan label kiri untuk kelipatan 10
        if tinggi % 10 == 0:
            print(f"{tinggi:3} |", end=" ")
        else:
            print("    |", end=" ")

        # isi baris
        for index in jumlah_harian:
            if index >= tinggi:
                if tinggi % 10 == 0:
                    print("██", end=" ")
                else:  # kalau belakangnya 5
                    print("▄▄", end=" ")
            else:
                print("  ", end=" ")
        print()  # pindah baris

    # garis bawah
    print("      " + "_" * (len(jumlah_harian) * 3))
    # label bawah
    print("      ", end="")
    for i in range(1, len(jumlah_harian)+1):
        print(f"{i:02}", end=" ")
    print()

# Main Program
def main():
	tabel(jumlah_harian)

if __name__ == '__main__':
	main()