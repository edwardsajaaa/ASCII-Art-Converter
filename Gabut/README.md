# Video to ASCII Art Converter

Script ini mengubah video menjadi tampilan ASCII art secara real-time di terminal.

## Cara Pakai

1. **Instalasi Dependensi**

   Pastikan Python 3 sudah terpasang. Install dependensi berikut:
   
   ```bash
   pip install opencv-python
   ```

2. **Siapkan Video**

   Letakkan file video (misal: `TENXI.mp4`) di folder yang sama dengan script, atau ubah variabel `video_path` di dalam script sesuai lokasi file video kamu.

3. **Jalankan Script**

   ```bash
   python video_to_ascii.py
   ```

4. **Tips**
   - Gunakan video pendek dan kontras tinggi (hitam putih jelas) untuk hasil terbaik.
   - Tekan `Ctrl+C` untuk menghentikan program kapan saja.

## Penjelasan Singkat
- Script akan membaca setiap frame video, mengubahnya ke grayscale, lalu mengkonversi tiap pixel menjadi karakter ASCII sesuai tingkat kecerahan.
- Hasil ASCII akan ditampilkan langsung di terminal, frame demi frame, menyerupai animasi video.

## Konfigurasi
- Ubah variabel `NEW_WIDTH` untuk mengatur lebar output ASCII di terminal.
- Ubah urutan karakter di `ASCII_CHARS` untuk eksperimen tampilan.

---

Script ini cocok untuk demo efek visual, hiburan, atau belajar pemrosesan citra sederhana dengan Python.
