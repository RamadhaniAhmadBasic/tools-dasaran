#!/usr/bin/env python3
"""
con-res-5.py

Versi perbaikan:
- Memastikan semua output gambar/gif/video selalu memiliki resolusi genap.
- Video: gunakan ffmpeg filter "scale=ceil(iw/2)*2:ceil(ih/2)*2"
- Gambar/GIF: tambahkan padding 1 piksel bila ukuran ganjil.
"""

import os
import shutil
import re
import subprocess
from pathlib import Path
from typing import List, Dict
from PIL import Image
import imageio
import cv2

# ------------------ KONFIGURASI ------------------

ALLOWED_IMAGE_FORMATS = {'.png', '.gif'}
ALLOWED_VIDEO_FORMATS = {'.mp4'}

IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.ts', '.m4v'}

TARGET_SHORT_SIDE = 720

# ------------------ SORTING NATURAL ------------------

def alphanum_key(path: Path):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', path.stem)]

def sort_files_naturally(file_paths: List[Path]) -> List[Path]:
    return sorted(file_paths, key=alphanum_key)

# ------------------ FUNGSI BANTUAN ------------------

def force_even_size(image: Image.Image) -> Image.Image:
    """Pastikan width & height genap dengan padding 1px bila perlu"""
    w, h = image.size
    new_w = w + (w % 2)
    new_h = h + (h % 2)
    if (new_w, new_h) == (w, h):
        return image
    # Tambahkan padding
    new_img = Image.new(image.mode, (new_w, new_h), (0, 0, 0, 0) if image.mode == "RGBA" else 0)
    new_img.paste(image, (0, 0))
    image.close()
    return new_img

def resize_image_keep_aspect(image: Image.Image, target_short_side: int) -> Image.Image:
    width, height = image.size
    short_side = min(width, height)
    if short_side <= target_short_side:
        return force_even_size(image)
    scale_factor = target_short_side / short_side
    new_width = int(round(width * scale_factor))
    new_height = int(round(height * scale_factor))
    image = image.resize((new_width, new_height), Image.LANCZOS)
    return force_even_size(image)

def get_short_side_image(file_path: Path) -> int:
    image = Image.open(file_path)
    w, h = image.size
    image.close()
    return min(w, h)

def get_short_side_gif(file_path: Path) -> int:
    reader = imageio.get_reader(str(file_path))
    short_side = None
    for frame in reader:
        h, w = frame.shape[:2]
        side = min(w, h)
        if short_side is None or side < short_side:
            short_side = side
    reader.close()
    return short_side or 0

def get_short_side_video(file_path: Path) -> int:
    cap = cv2.VideoCapture(str(file_path))
    if not cap.isOpened():
        cap.release()
        return 0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return min(w, h)

# ------------------ KONVERSI ------------------

def convert_static_image_to_png(file_path: Path, output_path: Path) -> None:
    image = Image.open(file_path)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    image = resize_image_keep_aspect(image, TARGET_SHORT_SIDE)
    image.save(output_path, format="PNG")
    image.close()

def convert_gif(file_path: Path, output_path: Path) -> None:
    reader = imageio.get_reader(str(file_path))
    meta = reader.get_meta_data()
    frames = []
    durations = []
    for frame in reader:
        pil_frame = Image.fromarray(frame)
        pil_frame = resize_image_keep_aspect(pil_frame, TARGET_SHORT_SIDE)
        frames.append(pil_frame)
        durations.append(meta.get('duration', 0.1))
    reader.close()
    writer = imageio.get_writer(str(output_path), mode='I', duration=durations)
    for pil_frame in frames:
        writer.append_data(imageio.core.util.Array(pil_frame))
    writer.close()
    for f in frames:
        f.close()

def convert_video_to_mp4(file_path: Path, output_path: Path) -> None:
    """
    Konversi video ke MP4 dengan menjaga audio.
    Pastikan resolusi output genap (ceil ke atas).
    """
    cap = cv2.VideoCapture(str(file_path))
    if not cap.isOpened():
        cap.release()
        raise RuntimeError(f"Tidak bisa membuka video: {file_path}")
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    short_side = min(w, h)
    if short_side > TARGET_SHORT_SIDE:
        scale_filter = (
            f"scale='if(gt(iw,ih),-2,{TARGET_SHORT_SIDE})':'if(gt(ih,iw),-2,{TARGET_SHORT_SIDE})',"
            "scale=ceil(iw/2)*2:ceil(ih/2)*2"
        )
    else:
        scale_filter = "scale=ceil(iw/2)*2:ceil(ih/2)*2"

    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", str(file_path),
        "-vf", scale_filter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(output_path)
    ]

    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Gagal konversi video {file_path}, error:\n{result.stderr.decode()}")

# ------------------ UTILITY ------------------

def find_media_files(root: Path) -> Dict[Path, List[Path]]:
    result: Dict[Path, List[Path]] = {}
    for dirpath, _, filenames in os.walk(root):
        current_dir = Path(dirpath)
        files = [current_dir / f for f in filenames if (current_dir / f).is_file()]
        files = sort_files_naturally(files)
        media_files = [f for f in files if f.suffix.lower() in IMAGE_FORMATS.union(VIDEO_FORMATS)]
        if media_files:
            result[current_dir] = media_files
    return result

# ------------------ PROSES UTAMA ------------------

def process_directory_tree(root: Path):
    print(f"Scanning: {root}\n")
    media_directories = find_media_files(root)

    total_skip = total_convert = total_error = 0

    for directory, media_files in media_directories.items():
        print(f"[{directory}]")
        print("-" * 64)

        conversion_counter = {}

        for file_path in media_files:
            try:
                ext = file_path.suffix.lower()
                target_ext = None
                short_side = 0

                # Tentukan target format dan ukur sisi pendek
                if ext in IMAGE_FORMATS:
                    if ext == ".gif":
                        short_side = get_short_side_gif(file_path)
                        target_ext = ".gif"
                    elif ext == ".png":
                        short_side = get_short_side_image(file_path)
                        target_ext = ".png"
                    else:
                        short_side = get_short_side_image(file_path)
                        target_ext = ".png"
                elif ext in VIDEO_FORMATS:
                    short_side = get_short_side_video(file_path)
                    target_ext = ".mp4"
                else:
                    print(f"[SKP] {file_path.name}")
                    total_skip += 1
                    continue

                # --- Kasus file valid (format + ukuran <= target)
                if ext in ALLOWED_IMAGE_FORMATS.union(ALLOWED_VIDEO_FORMATS) and short_side <= TARGET_SHORT_SIDE:
                    if target_ext not in conversion_counter:
                        conversion_counter[target_ext] = 1
                    new_name = f"{conversion_counter[target_ext]}{target_ext}"
                    new_path = file_path.parent / new_name

                    if file_path.name != new_name:
                        shutil.move(str(file_path), str(new_path))
                        print(f"[CON] {file_path.name} : {new_path.name}")
                        total_convert += 1
                    else:
                        print(f"[SKP] {file_path.name}")
                        total_skip += 1

                    conversion_counter[target_ext] += 1
                    continue

                # --- Proses konversi file non-standar atau oversized
                temp_name = f"temp_{file_path.stem}{target_ext}"
                temp_output = file_path.parent / temp_name

                if target_ext == ".png":
                    convert_static_image_to_png(file_path, temp_output)
                elif target_ext == ".gif":
                    convert_gif(file_path, temp_output)
                elif target_ext == ".mp4":
                    convert_video_to_mp4(file_path, temp_output)

                if target_ext not in conversion_counter:
                    conversion_counter[target_ext] = 1
                new_name = f"{conversion_counter[target_ext]}{target_ext}"
                final_output = file_path.parent / new_name
                conversion_counter[target_ext] += 1

                file_path.unlink(missing_ok=True)
                shutil.move(str(temp_output), str(final_output))

                print(f"[CON] {file_path.name} : {final_output.name}")
                total_convert += 1

            except Exception as e:
                print(f"[ERR] {file_path.name} -> {e}")
                total_error += 1
                continue

        print("")

    # Ringkasan akhir
    print("Processing selesai.")
    print("=" * 64)
    print(f"Total SKP : {total_skip}")
    print(f"Total CON : {total_convert}")
    print(f"Total ERR : {total_error}")
    print("=" * 64)

# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    working_directory = Path(os.getcwd())
    process_directory_tree(working_directory)
