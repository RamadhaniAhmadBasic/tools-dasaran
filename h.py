# Python 3.10.6
# Import Module
import os

# Define Variable
angka = 1024
lokasi_kerja = os.path.abspath(__file__)

# Define Function
def fungsi_tampilan_terminal():
	print()
	print("[ %s ]" % lokasi_kerja)
	print("================================================================")
	print(" %40s %10s %10s " % ("", "Total", "Size (MB)"))
	print(" %-42s %8d %8dMB " % ("File .JPG", angka, angka))
	print(" %-42s %8d %8dMB " % ("File .PNG", angka, angka))
	print(" %-42s %8d %8dMB " % ("File .GIF", angka, angka))
	print(" %-42s %8d %8dMB " % ("File .WEBP", angka, angka))
	print(" %-42s %8d %8dMB " % ("File .MOV", angka, angka))
	print(" %-42s %8d %8dMB " % ("File .TS", angka, angka))
	print(" %-42s %8d %8dMB " % ("File .MP4", angka, angka))
	print()
	print(" %-42s %8d %8dMB "% ("Exist Total", angka*7, angka*7))
	print()
	print(" %-42s %8s %8sMB " % ("Converted (.MP4)", angka, angka))
	print(" %-42s %8s %8sMB " % ("Converted (.PNG)", angka, angka))
	print(" %-42s %8s %8sMB " % ("Resized (720p)", angka, angka))
	print(" %-42s %8s %8sMB " % ("Success", angka, angka))
	print(" %-42s %8s %8sMB " % ("Skip", angka, angka))
	print(" %-42s %8s %8sMB " % ("Error", angka, angka))
	print()
	print(" %-42s %8d %8dMB "% ("Process Total", angka*7, angka*7))
	print(" %-42s %8d %8dMB "% ("Skip Total", angka*7, angka*7))
	print("----------------------------------------------------------------")
	print(" %-42s %8d %8dMB "% ("Grand Total", angka*7, angka*7))
	print("================================================================")

# Main Program
def main():
	fungsi_tampilan_terminal()

if __name__ == '__main__':
	main()