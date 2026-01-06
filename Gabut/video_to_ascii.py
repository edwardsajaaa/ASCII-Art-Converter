import cv2
import os
import time
import sys

# --- KONFIGURASI ---
# Karakter ASCII dari yang paling 'gelap' (padat) ke paling 'terang' (tipis)
# Kamu bisa bereksperimen dengan mengganti urutan atau jenis karakternya.
# Urutan dibalik: spasi di depan, simbol padat di belakang
ASCII_CHARS = " .:-=+*#%@" 
# Contoh lain: "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Lebar terminal yang diinginkan (semakin besar, semakin detail tapi butuh layar besar)
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
    # Buka file video menggunakan OpenCV
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Tidak bisa membuka file video.")
        return

    # Coba dapatkan FPS (Frames Per Second) video asli agar kecepatannya pas
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1.0 / fps # Waktu tunggu antar frame dalam detik
    except:
        frame_delay = 0.03 # Default manual jika gagal deteksi FPS (sekitar 30fps)


    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    while True:
        ret, frame = cap.read()
        if not ret:
            break # Video selesai

        # --- Resize frame ---
        height, width, _ = frame.shape
        aspect_ratio = height / width
        new_height = int(aspect_ratio * NEW_WIDTH * 0.55)
        resized_frame = cv2.resize(frame, (NEW_WIDTH, new_height))
        grayscale_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # --- Konversi ke ASCII dan warna ---
        ascii_img = ""
        for y in range(resized_frame.shape[0]):
            for x in range(resized_frame.shape[1]):
                pixel_val = grayscale_frame[y, x]
                bucket_size = 256 / len(ASCII_CHARS)
                index = int(pixel_val / bucket_size)
                if index >= len(ASCII_CHARS):
                    index = len(ASCII_CHARS) - 1
                char = ASCII_CHARS[index]
                b, g, r = resized_frame[y, x] # OpenCV uses BGR
                ansi_code = rgb_to_ansi(r, g, b)
                ascii_img += f"{ansi_code}{char}\033[0m"
            ascii_img += "\n"

        sys.stdout.write("\033[H")
        sys.stdout.write(ascii_img)
        sys.stdout.flush()
        time.sleep(frame_delay)

    cap.release()
    # Bersihkan layar setelah selesai
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Video selesai diputar dalam mode ASCII!")

# --- CARA MENJALANKAN ---
if __name__ == "__main__":
    # Ganti 'contoh_video.mp4' dengan path file videomu sendiri.
    # Gunakan video pendek dengan kontras tinggi (hitam putih jelas) untuk hasil terbaik.
    video_path = "D:\MAGANG\TENXI.mp4" 
    
    # Bersihkan layar dulu sebelum mulai
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        play_video_ascii(video_path)
    except KeyboardInterrupt:
        # Tangani jika user menekan Ctrl+C untuk berhenti
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nProgram dihentikan oleh pengguna.")