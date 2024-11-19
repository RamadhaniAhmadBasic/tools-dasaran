import os

import pustaka.tabel_info

# Files menu

import pustaka.merge_images_to_pdf
import pustaka.brute_force_zip
import pustaka.brute_force_rar
import pustaka.docx_to_pdf
# import pustaka.mp4_to_mp3
# import pustaka.
# import pustaka.

#Images menu

# import pustaka.image_resizer
# import pustaka.webp_to_png
import pustaka.png_to_jpg
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.metadata_viewer

# Units menu

import pustaka.byte_meter
import pustaka.kilobyte_meter
import pustaka.megabyte_meter
import pustaka.byte_finder
import pustaka.kilobyte_finder
import pustaka.megabyte_finder
# import pustaka.

# Network menu

# import pustaka.connection_logger
import pustaka.url_ip
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.

# X menu

# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.

# Settings menu

# import pustaka.scan_directory
# import pustaka.find_a_file
# import pustaka.
# import pustaka.
# import pustaka.
# import pustaka.find_in_file
# import pustaka.spam_tools

class Main():
	def __init__(self):
		self.lvl_1 = None
		self.lvl_2 = None

		self.main_menu()

	def clear_screen(self):
		os.system("cls" if os.name == "nt" else "clear")

	def menu_skeleton(self, title, *options):
		while True:
			self.clear_screen()
			print("+==========================================+")
			print("|" + title.center(42) + "|")
			print("+====+=====================================+")
			print("| NO | FUNCTION                            |")
			print("+====+=====================================+")
			for i, a in enumerate(options[0]):
				if a == "Exit" or a == "Back":
					print("| 0. | {:<35} |".format(a))
				else:
					print("| {}. | {:<35} |".format(i + 1, a))
			print("+====+=====================================+")
			print("| BY: ACH. KANGGO                          |")
			print("+==========================================+")

			choice = input("Pilih menu: ")
			if choice.isdigit():
				choice = int(choice)
				if 0 < choice <= len(options[0]):
					return choice
				elif choice == 0:
					return 0

	def main_menu(self):
		while True:
			self.lvl_1 = self.menu_skeleton("KANGGO PROJECT - MAIN MENU", ["Files", "Images", "Units", "Networks", "X", "Settings", "Help", "About", "Exit"])

			if self.lvl_1 == 0:
				pustaka.tabel_info.f("WARNING", "Program will be exit")
				break

			elif self.lvl_1 == 1:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (1) FILES MENU", ["Merge image -> PDF", "Brute-force ZIP", "Brute-force RAR", "DOCX > PDF", "MP4 > MP3", "X", "X", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pustaka.merge_images_to_pdf.f()

					elif self.lvl_2 == 2:
						pustaka.brute_force_zip.f()

					elif self.lvl_2 == 3:
						pustaka.brute_force_rar.f()

					elif self.lvl_2 == 4:
						pustaka.docx_to_pdf.f()

					elif self.lvl_2 == 5:
						pustaka.mp4_to_mp3.f()

					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass


			elif self.lvl_1 == 2:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (2) IMAGES MENU", ["Image resizer", "WEBP > PNG", "PNG > JPG", "X", "X", "X", "Metadata viewer", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pass

					elif self.lvl_2 == 2:
						pass

					elif self.lvl_2 == 3:
						pass

					elif self.lvl_2 == 4:
						pass
					
					elif self.lvl_2 == 5:
						pass
					
					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass

			elif self.lvl_1 == 3:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (3) UNITS MENU", ["Byte meter", "Kilobyte meter", "Megabyte meter", "Byte finder", "Kilobyte finder", "Megabyte finder", "X", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pustaka.byte_meter.f()

					elif self.lvl_2 == 2:
						pustaka.kilobyte_meter.f()

					elif self.lvl_2 == 3:
						pustaka.megabyte_meter.f()

					elif self.lvl_2 == 4:
						pustaka.byte_finder.f()
					
					elif self.lvl_2 == 5:
						pustaka.kilobyte_finder.f()
					
					elif self.lvl_2 == 6:
						pustaka.megabyte_finder.f()

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass


			elif self.lvl_1 == 4:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (4) NETWORK MENU", ["Connection logger", "URL > IP", "X", "X", "X", "X", "X", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pass

					elif self.lvl_2 == 2:
						pustaka.url_ip.f()

					elif self.lvl_2 == 3:
						pass

					elif self.lvl_2 == 4:
						pass
					
					elif self.lvl_2 == 5:
						pass
					
					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass

			elif self.lvl_1 == 5:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (5) X MENU", ["X", "X", "X", "X", "X", "X", "X", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pass

					elif self.lvl_2 == 2:
						pass

					elif self.lvl_2 == 3:
						pass

					elif self.lvl_2 == 4:
						pass
					
					elif self.lvl_2 == 5:
						pass
					
					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass

			elif self.lvl_1 == 6:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (6) SETTINGS MENU", ["Scan Directory", "Find a file", "X", "X", "X", "Find in file", "Spam tools", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pass

					elif self.lvl_2 == 2:
						pass

					elif self.lvl_2 == 3:
						pass

					elif self.lvl_2 == 4:
						pass
					
					elif self.lvl_2 == 5:
						pass
					
					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass

			elif self.lvl_1 == 7:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (7) HELP MENU", ["X", "X", "X", "X", "X", "X", "X", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pass

					elif self.lvl_2 == 2:
						pass

					elif self.lvl_2 == 3:
						pass

					elif self.lvl_2 == 4:
						pass
					
					elif self.lvl_2 == 5:
						pass
					
					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass



			elif self.lvl_1 == 8:
				while True:
					self.lvl_2 = self.menu_skeleton("KANGGO PROJECT - (8) ABOUT MENU", ["Biodata", "instagram", "Twitter X", "Website", "X", "X", "X", "Help", "Back"])
					if self.lvl_2 == 0:
						break

					elif self.lvl_2 == 1:
						pass

					elif self.lvl_2 == 2:
						pass

					elif self.lvl_2 == 3:
						pass

					elif self.lvl_2 == 4:
						pass
					
					elif self.lvl_2 == 5:
						pass
					
					elif self.lvl_2 == 6:
						pass

					elif self.lvl_2 == 7:
						pass

					elif self.lvl_2 == 8:
						pass

if __name__ == '__main__':
	Main()
