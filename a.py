# Python 3.10.6
# import module
import os
import re

# define variable
fg_red_c     = "\033[31m" # ERROR color
fg_green_c   = "\033[32m" # SUCCESS color
fg_yellow_c  = "\033[33m" # WARNING color
fg_cyan_c    = "\033[36m" # INFO color

bg_red_c     = "\033[41m" # ERROR color
bg_green_c   = "\033[42m" # SUCCESS color
bg_yellow_c  = "\033[43m" # WARNING color
bg_cyan_c    = "\033[46m" # INFO color

reset_c      = "\033[0m"  # RESET color
invert_c     = "\033[7m"  # INVERT color

# define function

# main program
def main():
	print("\033[33m")
	print("  _____         _      ")
	print(" | __  |___ ___|_|___  ")
	print(" | __ -| .'|_ -| |  _| ")
	print(" |_____|__,|___|_|___| ")
	print(" v0.1.1\n\033[0m")

	print("\033[7;36m * \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eget magna eget ligula laoreet iaculis eu ac urna. Praesent scelerisque ipsum condimentum, posuere diam et, efficitur tellus.\n")
	print("\033[7;33m ! \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n")
	print("\033[7;31m X \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eget magna eget ligula laoreet iaculis eu ac urna.\n")

	print("\033[7;36m 10:10 \033[0m \033[7;32m SCC \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eget magna eget ligula laoreet iaculis eu ac urna.")
	print("\033[7;36m 10:10 \033[0m \033[7;36m INF \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eget magna eget ligula laoreet iaculis eu ac urna.")
	print("\033[7;36m 10:10 \033[0m \033[7;31m ERR \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eget magna eget ligula laoreet iaculis eu ac urna.")

	print("\033[7;36m 10:10 \033[0m \033[7;33m QUE \033[0m Lorem ipsum dolor sit amet, consectetur adipiscing elit?")
	print("[\033[33m 1 \033[0m] Lorem ipsum dolor sit amet")
	print("[\033[33m 2 \033[0m] Lorem ipsum dolor sit amet")
	print("[\033[33m 3 \033[0m] Lorem ipsum dolor sit amet")
	print("[\033[33m 4 \033[0m] Lorem ipsum dolor sit amet")
	print("[\033[33m 5 \033[0m] Lorem ipsum dolor sit amet")
	print("[\033[33m 6 \033[0m] Lorem ipsum dolor sit amet")

if __name__ == '__main__':
	main()