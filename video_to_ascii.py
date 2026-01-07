import cv2
import os
import time
import sys
import threading
import queue
from blessed import Terminal

# --- KONFIGURASI ---
# Karakter ASCII dari yang paling 'gelap' (padat) ke paling 'terang' (tipis)
# Kamu bisa bereksperimen dengan mengganti urutan atau jenis karakternya.
# Urutan dibalik: spasi di depan, simbol padat di belakang
ASCII_CHARS = " .:-=+*#%@"
# Lebar terminal yang diinginkan (lebih kecil agar lebih ringan)
NEW_WIDTH = 100

def pixel_to_ascii(image):
    pixels = image.flatten()
    ascii_str = ""
    # Bagi rentang 0-255 menjadi beberapa bagian sesuai jumlah karakter ASCII kita
    bucket_size = 256 / len(ASCII_CHARS)
    
    for pixel_val in pixels:
        # Tentukan index karakter berdasarkan kecerahan pixel
        index = int(pixel_val / bucket_size)
        # Pastikan index tidak keluar batas (jika pixel_val 255)
        if index >= len(ASCII_CHARS):
            index = len(ASCII_CHARS) - 1
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def play_video_ascii(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Tidak bisa membuka file video.")
        return

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1.0 / fps
    except:
        frame_delay = 0.03



    frame_queue = queue.Queue(maxsize=5)
    stop_flag = threading.Event()

    def frame_reader():
        while not stop_flag.is_set():
            ret, frame = cap.read()
            if not ret:
                frame_queue.put(None)
                break
            frame_queue.put(frame)

    reader_thread = threading.Thread(target=frame_reader, daemon=True)
    reader_thread.start()


    term = Terminal()
    print(term.clear + term.hide_cursor)
    try:
        while True:
            frame = frame_queue.get()
            if frame is None:
                break
            height, width, _ = frame.shape
            aspect_ratio = height / width
            new_height = int(aspect_ratio * NEW_WIDTH * 0.55)
            resized_frame = cv2.resize(frame, (NEW_WIDTH, new_height))
            grayscale_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

            ascii_lines = []
            for y in range(grayscale_frame.shape[0]):
                line = ""
                for x in range(grayscale_frame.shape[1]):
                    pixel_val = grayscale_frame[y, x]
                    bucket_size = 256 / len(ASCII_CHARS)
                    index = int(pixel_val / bucket_size)
                    if index >= len(ASCII_CHARS):
                        index = len(ASCII_CHARS) - 1
                    char = ASCII_CHARS[index]
                    line += char
                ascii_lines.append(line)

            print(term.move(0, 0) + '\n'.join(ascii_lines), end="")
            sys.stdout.flush()
            time.sleep(frame_delay)
    finally:
        print(term.normal_cursor)

    stop_flag.set()
    reader_thread.join()
    cap.release()
    print(term.normal + term.clear)
    print("Video selesai diputar dalam mode ASCII!")

# --- CARA MENJALANKAN ---
if __name__ == "__main__":
    # Ganti 'contoh_video.mp4' dengan path file videomu sendiri.
    # Gunakan video pendek dengan kontras tinggi (hitam putih jelas) untuk hasil terbaik.
    video_path = r"D:\MAGANG\TENXI.mp4"
    
    # Bersihkan layar dulu sebelum mulai
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        play_video_ascii(video_path)
    except KeyboardInterrupt:
        # Tangani jika user menekan Ctrl+C untuk berhenti
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nProgram dihentikan oleh pengguna.")