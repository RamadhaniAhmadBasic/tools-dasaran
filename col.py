import os
from PIL import Image

# Palet warna dari col.txt
palettes = {
    "Grey 1": ["fcfcfd","f9fafb","f2f4f7","e4e7ec","d0d5dd","98a2b3","667085","475467","344054","1d2939","101828"],
    "Grey 2": ["e8e8e8","d1d1d1","959693","a19f97","838079","626060","3f3838","1a1a1a"],
    "Red":    ["fffbfa","fef3f2","fee4e2","fecdca","fda29b","f97066","f04438","d92d20","b42318","912018","7a271a"],
    "Green":  ["f6fef9","ecfdf3","d1fadf","a6f4c5","6ce9a6","32d583","12b76a","039855","027a48","05603a","054f31"],
    "Blue":   ["f5fbff","f0f9ff","e0f2fe","b9e8fe","7cd4fd","36bffa","0ba5ec","0086c9","026aa2","065986","0b4a6f"],
    "Contrast 1": ["00d37f","aff8c8","0f2830","014751","f8fbff"],
    "Neon": ["ff1178","fe0000","fff205","01fff4","7cff01"],
    "Off Palette": ["122220","232023","c8d746","232e3f","3a3134","252729","e9e6e4","f8f3e6","edff00","faf8ea","e7301c"],
    "Gradient 1": ["ee4540","c72c41","801336","510a32","2d142c"],
    "Retro": ["dfa05d","ac5045","658761"],
    "Contrast 2": ["9dbdb8","f0e7d6","ea2e00"],
    "Contrast 3": ["fe7f2d","233d4d"],
    "Contrast 4": ["1e2b2f","ff7f50"],
    "Contrast 5": ["004643","fafafa"],
    "Contrast 6": ["d53302","fcc560","a0cbad","8fb18e","0c012a"],
    "Contrast 7": ["f0544d","ffffd8"],
    "Contrast 8": ["622872","caa5cb","c8ddea","faeaf6"],
    "Contrast 9": ["ff1637","491507"],
    "Contrast 10": ["ffef4d","2a323f"],
    "Contrast 11": ["21443e","f0edce","acce00"],
    "Gradient 2": ["f4efee","cdbbb9","49747f","e34b26","003447","441111"],
    "Contrast 12": ["1b1b1b","323232","ffe7d0","fc6e20"],
    "Contrast 13": ["abd1c6","312f2c","f0ede5"],
    "Contrast 14": ["ec5e27","2b323f"],
    "Contrast 15": ["0c0e0b","d6e8f4","d7303b"]
}

# Konversi point ke pixel @300dpi
dpi = 300
px_per_pt = dpi / 72  # 1pt = 4.166px
width_px = int(20 * px_per_pt)   # 20pt
height_px = int(10 * px_per_pt)  # 10pt

# Folder utama output
output_root = "output_colors"
os.makedirs(output_root, exist_ok=True)

for group, colors in palettes.items():
    group_dir = os.path.join(output_root, group.replace(" ", "_"))
    os.makedirs(group_dir, exist_ok=True)

    for hex_code in colors:
        color = f"#{hex_code}"
        img = Image.new("RGB", (width_px, height_px), color)
        filename = os.path.join(group_dir, f"{hex_code}.png")
        img.save(filename, dpi=(dpi, dpi))
        print(f"Saved {filename}")

print("Semua file warna berhasil dibuat, dikelompokkan per judul, dengan resolusi 300DPI!")
