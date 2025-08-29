# Python 3.10.6
# Import Module
import os

# Define Variable
path = "D:/Automation/"

# Define Function

# Main Program
def main():
	for file in os.listdir(path):
		if file.endswith(".py"):
			print("\033[33m%s\033[0m" % file)

		else:
			print("%s" % file)

if __name__ == '__main__':
	main()