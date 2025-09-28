# Python 3.10.6
# Import Module
import os

# Define Variable

# Define Function
def fungsi_buka_file_laporan(nama_file):
	return os.path.exists(nama_file)

def fungsi_baca_file_laporan(nama_file):
	if fungsi_buka_file_laporan(nama_file):
		file = open(nama_file, 'r')
		file.read()

def fungsi_tulis_file_laporan(nama_file):
	pass

# Main Program
def main():
	pass

if __name__ == '__main__':
	main()