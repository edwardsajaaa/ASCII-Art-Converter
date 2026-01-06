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

    while True:
        ret, frame = cap.read()
        if not ret:
            break # Video selesai

        # --- LANGKAH 1 & 2: Resize dan Grayscale ---
        # Hitung aspek rasio agar gambar tidak gepeng
        height, width, _ = frame.shape
        aspect_ratio = height / width
        # Karakter terminal biasanya lebih tinggi daripada lebarnya (sekitar 2x), 
        # jadi kita sesuaikan tinggi barunya.
        new_height = int(aspect_ratio * NEW_WIDTH * 0.55) 
        
        resized_frame = cv2.resize(frame, (NEW_WIDTH, new_height))
        grayscale_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # --- LANGKAH 3: Konversi ke String ASCII ---
        ascii_str = pixel_to_ascii(grayscale_frame)
        
        # Format string menjadi baris-baris agar sesuai lebar terminal
        ascii_img = ""
        for i in range(0, len(ascii_str), NEW_WIDTH):
            ascii_img += ascii_str[i:i+NEW_WIDTH] + "\n"

        # --- LANGKAH 4: Tampilkan di Terminal ---
        # Trik untuk mengurangi kedipan (flicker) di terminal
        # Daripada membersihkan layar (cls/clear), kita pindahkan kursor ke kiri atas
        sys.stdout.write("\033[H") 
        sys.stdout.write(ascii_img)
        sys.stdout.flush()
        
        # Tunggu sebentar agar kecepatan video sesuai aslinya
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