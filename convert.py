#!/usr/bin/env python3
"""
process_media.py

Python 3.10.6
Dependencies:
    pip install pillow imageio opencv-python
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Dict
from PIL import Image
import imageio
import cv2

# ------------------ KONFIGURASI ------------------

ALLOWED_IMAGE_FORMATS = {'.png', '.gif'}
ALLOWED_VIDEO_FORMATS = {'.mp4'}

IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}

TARGET_SHORT_SIDE = 720


# ------------------ SORTING NATURAL ------------------

def alphanum_key(path: Path):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', path.stem)]

def sort_files_naturally(file_paths: List[Path]) -> List[Path]:
    return sorted(file_paths, key=alphanum_key)


# ------------------ FUNGSI BANTUAN ------------------

def resize_image_keep_aspect(image: Image.Image, target_short_side: int) -> Image.Image:
    width, height = image.size
    short_side = min(width, height)
    if short_side <= target_short_side:
        return image
    scale_factor = target_short_side / short_side
    new_width = int(round(width * scale_factor))
    new_height = int(round(height * scale_factor))
    return image.resize((new_width, new_height), Image.LANCZOS)

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
    cap = cv2.VideoCapture(str(file_path))
    if not cap.isOpened():
        cap.release()
        raise RuntimeError("Tidak bisa membuka video: %s" % file_path)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    short_side = min(w, h)
    if short_side > TARGET_SHORT_SIDE:
        scale_factor = TARGET_SHORT_SIDE / short_side
        new_w = int(round(w * scale_factor))
        new_h = int(round(h * scale_factor))
    else:
        new_w, new_h = w, h
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (new_w, new_h))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if (new_w, new_h) != (w, h):
            frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        out.write(frame)
    cap.release()
    out.release()


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
    print("Scanning: %s\n" % root)
    media_directories = find_media_files(root)

    total_skip = total_convert = total_error = 0

    for directory, media_files in media_directories.items():
        print("[%s]" % directory)
        print("-" * 64)

        conversion_counter = {}

        for file_path in media_files:
            try:
                ext = file_path.suffix.lower()
                target_ext = None
                short_side = 0

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
                    print("[SKP] %s" % file_path.name)
                    total_skip += 1
                    continue

                if ext in ALLOWED_IMAGE_FORMATS.union(ALLOWED_VIDEO_FORMATS) and short_side <= TARGET_SHORT_SIDE:
                    if target_ext not in conversion_counter:
                        conversion_counter[target_ext] = 1
                    new_name = "%d%s" % (conversion_counter[target_ext], target_ext)
                    new_path = file_path.parent / new_name

                    if file_path.name != new_name:
                        shutil.move(str(file_path), str(new_path))
                        print("[CON] %s : %s" % (file_path.name, new_path.name))
                        total_convert += 1
                    else:
                        print("[SKP] %s" % file_path.name)
                        total_skip += 1

                    conversion_counter[target_ext] += 1
                    continue

                temp_name = "temp_%s%s" % (file_path.stem, target_ext)
                temp_output = file_path.parent / temp_name

                if target_ext == ".png":
                    convert_static_image_to_png(file_path, temp_output)
                elif target_ext == ".gif":
                    convert_gif(file_path, temp_output)
                elif target_ext == ".mp4":
                    convert_video_to_mp4(file_path, temp_output)

                if target_ext not in conversion_counter:
                    conversion_counter[target_ext] = 1
                new_name = "%d%s" % (conversion_counter[target_ext], target_ext)
                final_output = file_path.parent / new_name
                conversion_counter[target_ext] += 1

                shutil.move(str(temp_output), str(final_output))
                file_path.unlink(missing_ok=True)

                print("[CON] %s : %s" % (file_path.name, final_output.name))
                total_convert += 1

            except Exception:
                print("[ERR] %s" % file_path.name)
                total_error += 1
                continue

        print("")

    print("Processing selesai.")
    print("=" * 64)
    print("Total SKP : %d" % total_skip)
    print("Total CON : %d" % total_convert)
    print("Total ERR : %d" % total_error)
    print("=" * 64)

    # Integrasi tampilan dari h.py
    try:
        import h
        print("\nTampilan tambahan dari h.py:\n")
        h.fungsi_tampilan_terminal()
    except Exception as e:
        print("Gagal memanggil tampilan dari h.py: %s" % e)


# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    working_directory = Path(os.getcwd())
    process_directory_tree(working_directory)
