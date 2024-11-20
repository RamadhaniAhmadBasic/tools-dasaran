import os

def format_size(bytes, unit='MB'):
    """Format ukuran byte menjadi unit tertentu."""
    units = {
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    if unit not in units:
        raise ValueError('Unit tidak didukung. Gunakan: KB, MB, GB, atau TB.')

    formatted_size = bytes / units[unit]
    return f'{formatted_size:.2f} {unit}'

def scan_directory_tree(directory):
    """Memindai direktori dan menghitung ukuran folder dan file."""
    items = []
    total_size = 0
    
    for entry in os.scandir(directory):
        if entry.is_file():
            try:
                size = os.path.getsize(entry.path)
                items.append((entry.name, size))
                total_size += size
            except Exception as e:
                items.append((entry.name, 0))  # Jika error, masukkan ukuran 0
        elif entry.is_dir():
            folder_size, sub_items = scan_directory_tree(entry.path)
            items.append((entry.name, folder_size, sub_items))
            total_size += folder_size
    
    return total_size, items

def sort_items(items):
    """Mengurutkan folder dan file berdasarkan ukuran terbesar ke terkecil."""
    return sorted(items, key=lambda x: x[1], reverse=True)

def display_tree(items, indent=0):
    """Menampilkan struktur direktori dalam format pohon."""
    for item in sort_items(items):
        if len(item) == 2:  # File
            name, size = item
            print(f"{'  ' * indent}{name} - {format_size(size)}")
        elif len(item) == 3:  # Folder
            name, size, sub_items = item
            print(f"{'  ' * indent}{name} - {format_size(size)}")
            display_tree(sub_items, indent + 1)

if __name__ == "__main__":
    folder_path = input("Masukkan path direktori yang ingin dipindai: ")
    if os.path.isdir(folder_path):
        print("\nStruktur direktori dan ukurannya (urut terbesar):")
        total_size, items = scan_directory_tree(folder_path)
        print(f"Root - {format_size(total_size)}")
        display_tree(items)
    else:
        print("Path yang dimasukkan bukan direktori yang valid.")
