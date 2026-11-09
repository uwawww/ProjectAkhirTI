import numpy as np
import matplotlib.pyplot as plt
ukuran_pesan = 10000
pesan_asli = np.random.randint(0, 2, ukuran_pesan)
print("Panjang pesan:", len(pesan_asli))
print("Cuplikan 30 bit pertama:", pesan_asli[:30])

def encoder_repetition(pesan, pengulangan=3):
    # Mengulang setiap bit pesan untuk proteksi (misal 1 menjadi 1 1 1)
    pesan_encoded = np.repeat(pesan, pengulangan)
    return pesan_encoded
1
def kanal_komunikasi(pesan, probabilitas_noise):
    # Hasilkan angka acak antara 0 dan 1 untuk setiap bit data
    peluang = np.random.rand(len(pesan))
    
    # Jika angka acak < probabilitas_noise, tandai sebagai error (True)
    mask_error = peluang < probabilitas_noise
    
    # Balikkan bit yang terkena error menggunakan XOR (^)
    pesan_diterima = pesan ^ mask_error 
    return pesan_diterima

def hitung_kerusakan(pesan_tx, pesan_rx):
    # Pastikan baris di bawah ini sejajar (1 Tab / 4 Spasi)
    jumlah_error = np.sum(pesan_tx != pesan_rx)
    ber = jumlah_error / len(pesan_tx)
    return jumlah_error, ber

# Daftar noise sesuai soal: 0%, 5%, 10%, 20%, 30%
skenario_noise = [0.0, 0.05, 0.10, 0.20, 0.30] 

print("=== HASIL: TANPA ERROR CORRECTION ===")
for noise in skenario_noise:
    # Lewatkan pesan ke kanal
    pesan_diterima = kanal_komunikasi(pesan_asli, noise)
    
    # Hitung jumlah error dan BER
    jml_error, nilai_ber = hitung_kerusakan(pesan_asli, pesan_diterima)
    
    # Tampilkan hasil
    print(f"Noise {int(noise*100)}% -> Jumlah Error: {jml_error} bit | BER: {nilai_ber:.4f}")

    # ==========================================
# FASE 4: SKENARIO DENGAN ERROR CORRECTION
# ==========================================

def encoder_repetition(pesan, pengulangan=3):
    # Mengulang setiap bit sebanyak 'pengulangan' kali (contoh: 1 -> 1 1 1)
    return np.repeat(pesan, pengulangan)

def decoder_repetition(pesan_rx, pengulangan=3):
    # Memecah pesan panjang menjadi kelompok-kelompok kecil (misal per 3 bit)
    pesan_reshaped = pesan_rx.reshape(-1, pengulangan)
    
    # Menghitung jumlah angka 1 dalam setiap kelompok (majority vote)
    jumlah_nilai = np.sum(pesan_reshaped, axis=1)
    
    # Jika mayoritas adalah 1 (jumlah >= 2 dari 3), maka hasilnya 1. Jika tidak, 0.
    pesan_terkoreksi = (jumlah_nilai > (pengulangan / 2)).astype(int)
    return pesan_terkoreksi

print("\n=== HASIL: DENGAN ERROR CORRECTION (Repetition Code 3x) ===")
for noise in skenario_noise:
    # 1. Encode pesan sebelum dikirim
    pesan_encoded = encoder_repetition(pesan_asli, 3)
    
    # 2. Lewatkan pesan panjang tersebut ke kanal (terkena noise)
    pesan_diterima = kanal_komunikasi(pesan_encoded, noise)
    
    # 3. Decode dan koreksi pesan yang kotor
    pesan_terkoreksi = decoder_repetition(pesan_diterima, 3)
    
    # 4. Hitung kerusakan dengan membandingkan pesan asli dan pesan terkoreksi
    jml_error, nilai_ber = hitung_kerusakan(pesan_asli, pesan_terkoreksi)
    
    # 5. Tampilkan hasil
    print(f"Noise {int(noise*100)}% -> Jumlah Error: {jml_error} bit | BER: {nilai_ber:.4f}")

    # ==========================================
# FASE 5: VISUALISASI DATA (GRAFIK BER)
# ==========================================
# Siapkan list untuk menyimpan data BER
ber_tanpa_koreksi = []
ber_dengan_koreksi = []

# Kumpulkan data ulang agar bisa dimasukkan ke dalam grafik
for noise in skenario_noise:
    # Data tanpa koreksi
    pesan_rx_tanpa = kanal_komunikasi(pesan_asli, noise)
    _, ber_tanpa = hitung_kerusakan(pesan_asli, pesan_rx_tanpa)
    ber_tanpa_koreksi.append(ber_tanpa)
    
    # Data dengan koreksi
    pesan_encoded = encoder_repetition(pesan_asli, 3)
    pesan_rx_dengan = kanal_komunikasi(pesan_encoded, noise)
    pesan_terkoreksi = decoder_repetition(pesan_rx_dengan, 3)
    _, ber_dengan = hitung_kerusakan(pesan_asli, pesan_terkoreksi)
    ber_dengan_koreksi.append(ber_dengan)

# Membuat plot grafik
plt.figure(figsize=(9, 5))
plt.plot(skenario_noise, ber_tanpa_koreksi, marker='o', color='red', label='Skenario A: Tanpa Error Correction')
plt.plot(skenario_noise, ber_dengan_koreksi, marker='s', color='blue', label='Skenario B: Dengan Repetition Code 3x')

# Memberi label dan judul
plt.title('Perbandingan Bit Error Rate (BER) terhadap Persentase Noise')
plt.xlabel('Probabilitas Noise (0.0 = 0%, 0.3 = 30%)')
plt.ylabel('Bit Error Rate (BER)')
plt.grid(True)
plt.legend()

# Menampilkan grafik ke layar
plt.show()
