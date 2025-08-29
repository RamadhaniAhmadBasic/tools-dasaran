# Python 3.10.6
# Import Module
import datetime as dt

# Define Variable
date_start_channel = dt.datetime.strptime("2025-08-20", "%Y-%m-%d")
date_today = dt.datetime.now()

video_mode = 1
video_name = "UNTITLED"

greeting = "Halo, terimakasih telah mau berkunjung ke channel ini. Ini adalah video perjalanan saya belajar 3D dengan Blender (4.5.1) secara mandiri dan hanya mengandalkan tutorial. Tujuan dokumentasi ini adalah agar dapat membandingkan progress dari hari ke hari serta dapat menjadi motivasi bagi penonton. Semoga dimasa depan kita dapat bertemu kembali dengan diri yang lebih baik.\n"
additional_note = "-"
social_media = """
+---------[MEDIA SOSIAL]---------+
Instagram : https://www.instagram.com/ramahmbsc
Youtube   : https://www.youtube.com/@RamAchBsc
GitHub    : https://github.com/RamadhaniAhmadBasic
+--------------------------------+
"""
hashtag = "#Belajar #Blender #Mandiri #BelajarBlender #3DModeling #3DDesign #BlenderArt"

# Define Function
def video_title(video_mode):
	if video_mode == 1:
		return "[HARI - %s] BELAJAR 3D MANDIRI DENGAN BLENDER" % (date_today - date_start_channel).days

	elif video_mode == 2:
		return "[SPECIAL] %s" % video_name

	else:
		print("[ERROR] Invalid Mode")

def video_description(video_mode):
	global additional_note

	if additional_note == "-":
		additional_note = ""
	else:
		additional_note = "Catatan : \n" + additional_note

	if video_mode == 1:
		return "[%s] - %s\n%s\n%s\n%s" % (date_today.strftime("%d/%m/%Y"), greeting, additional_note, social_media, hashtag)

	elif video_mode == 2:
		return "[%s] - %s\n%s\n%s" % (date_today.strftime("%d/%m/%Y"), additional_note, social_media, hashtag)

# Main Program
def main():
	global additional_note
	global video_name

	print("Masukkan mode video :")
	print("| 1. Harian")
	print("| 2. Spesial")
	video_mode = int(input("> "))

	if video_mode == 2:
		print("Masukkan judul video :")
		video_name = input("> ").upper()

	print("Masukkan nota tambahan : ")
	additional_note = input("> ")

	print("JUDUL :")
	print("\033[33m")
	print(video_title(video_mode))
	print("\033[0m")

	print("DESKRIPSI :")
	print("\033[33m")
	print(video_description(video_mode))
	print("\033[0m")

if __name__ == '__main__':
	main()