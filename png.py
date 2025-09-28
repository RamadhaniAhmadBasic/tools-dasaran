import zlib
import struct

def create_png_10x10(filename):
    width, height = 10, 10

    # Pola checkerboard 10x10
    # 0 = hitam, 1 = putih
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            bit = (x + y) % 2  # pola kotak-kotak
            row.append(bit)
        rows.append(row)

    # Data raw untuk PNG 1-bit: tiap baris diawali filter byte 0,
    # lalu piksel dikemas 1 bit per pixel dalam byte array.
    # Karena 10 bit per baris, kita butuh 2 byte per baris (16 bit),
    # 6 bit sisanya diisi 0.

    raw_data = []
    for row in rows:
        raw_data.append(0)  # filter byte no filter
        byte1 = 0
        byte2 = 0
        # 10 bit pixel
        for i in range(8):
            byte1 |= (row[i] & 1) << (7 - i)
        for i in range(8, 10):
            byte2 |= (row[i] & 1) << (7 - (i - 8))
        raw_data.append(byte1)
        raw_data.append(byte2)
    raw_bytes = bytes(raw_data)

    compressed = zlib.compress(raw_bytes)

    def png_chunk(chunk_type, data):
        chunk = struct.pack(">I", len(data))
        chunk += chunk_type
        chunk += data
        crc = zlib.crc32(chunk_type + data) & 0xffffffff
        chunk += struct.pack(">I", crc)
        return chunk

    png_header = b'\x89PNG\r\n\x1a\n'

    ihdr_data = struct.pack(">IIBBBBB",
                            width, height,
                            1,      # bit depth 1 bit
                            0,      # color type grayscale
                            0,      # compression method
                            0,      # filter method
                            0)      # interlace method
    ihdr = png_chunk(b'IHDR', ihdr_data)
    idat = png_chunk(b'IDAT', compressed)
    iend = png_chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(png_header)
        f.write(ihdr)
        f.write(idat)
        f.write(iend)

    print(f'File PNG {filename} berhasil dibuat!')

create_png_10x10('output_10x10_nolib.png')
