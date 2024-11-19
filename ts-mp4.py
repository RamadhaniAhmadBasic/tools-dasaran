import os
from moviepy.editor import VideoFileClip

def convert_format(input_format, output_format):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    for filename in os.listdir(current_directory):
        if filename.endswith(f".{input_format}"):
            input_file = os.path.join(current_directory, filename)
            output_file = os.path.join(current_directory, f"{os.path.splitext(filename)[0]}.{output_format}")

            try:
                clip = VideoFileClip(input_file)
                clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
                
                print(f"File {filename} berhasil dikonversi ke {output_file}")
            except Exception as e:
                print(f"Gagal mengonversi file {filename}. Error: {str(e)}")

if __name__ == "__main__":
    input_format = input("Masukkan format awal (ts/mp4): ").lower()
    output_format = input("Masukkan format tujuan (ts/mp4): ").lower()

    convert_format(input_format, output_format)
