# Python 3.10.6
# Import Module

# Define Variable
size_in_windows = 1024

# Define Function
def mb_to_gb(value):
	return value / size_in_windows

def gb_to_mb(value):
	return value * size_in_windows
# Main Program
def main():
	input_user = ""
	value_size = 0

	print("+========================================+")
	print("| \033[33mPARTISI PRESISI\033[0m                        |")
	print("+========================================+")

	print("[\033[33m?\033[0m] Menu :")
	print("[\033[36m1\033[0m] MB to GB")
	print("[\033[36m2\033[0m] GB to MB")
	print("[\033[36m3\033[0m] Exit")

	input_user = input("> ")

	if input_user == "1":
		print("[\033[33m?\033[0m] Masukkan ukuran value (MB) :")
		value_size = int(input("> "))
		print("Ukuran : \033[32m%29.1f\033[0m GB" % mb_to_gb(value_size))
		print("[o] SUCCESS - Prorgam Finish")

	elif input_user == "2":
		print("[\033[33m?\033[0m] Masukkan ukuran value (GB) :")
		value_size = int(input("> "))
		print("Ukuran : \033[32m%29.1f\033[0m MB" % gb_to_mb(value_size))
		print("[o] SUCCESS - Prorgam Finish")

	elif input_user == "3":
		print("[*] INFO - Prorgam Exit")
		exit()

if __name__ == '__main__':
	main()

