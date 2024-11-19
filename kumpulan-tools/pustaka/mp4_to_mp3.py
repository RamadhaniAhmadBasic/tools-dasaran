from moviepy.editor import VideoFileClip
import pustaka.tabel_info

def f():
    input_file = input("Input MP4 name: ")
    output_file = input("Input MP3 name: ")

    try:
        video = VideoFileClip(input_file)
        audio = video.audio
        audio.write_audiofile(output_file)
        audio.close()
        video.close()

        pustaka.tabel_info.f("SUCCESS", f"File {input_file} berhasil dikonversi menjadi {output_file}.")
        return True
    except Exception as e:
        pustaka.tabel_info.f("SUCCESS", f"Terjadi kesalahan: {e}")
        return False