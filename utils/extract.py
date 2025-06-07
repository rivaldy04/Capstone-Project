import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import logging
import csv
import os

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_page(page_num):
    """Mengambil data dari masing-masing halaman website."""
    try:
        # URL halaman
        url = "https://hasilto.bimbelssc.com/storage/ponorogo/intipa/data/TO_SNBT_JANUARI.html"
        logging.info(f"Mencoba mengakses URL: {url}")
        
        # Tambahkan header untuk menghindari pemblokiran
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        logging.info(f"Berhasil mengakses URL: {url}")

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari tabel dengan id="example1"
        table = soup.find('table', id='example1')
        if not table:
            logging.error("Tabel dengan id='example1' tidak ditemukan. Periksa struktur HTML atau URL.")
            return []

        # Mengambil semua baris dalam <tbody>
        tbody = table.find('tbody')
        if not tbody:
            logging.error("Tag <tbody> tidak ditemukan di dalam tabel.")
            return []

        rows = tbody.find_all('tr')
        if not rows:
            logging.warning("Tidak ada baris data di dalam <tbody>.")
            return []

        data = []
        for row in rows:
            try:
                # Mengambil semua kolom dalam baris
                cols = row.find_all('td')

                # Pastikan jumlah kolom sesuai (harus ada 10 kolom: No, Nama, PU, PPU, KMBM, PK, LIT IND, LIT ING, PM, Total)
                if len(cols) < 10:
                    logging.warning(f"Baris tidak memiliki cukup kolom: {len(cols)} kolom ditemukan, diharapkan 10")
                    continue

                # Ekstrak data dari kolom yang sesuai
                participant_no = cols[0].text.strip()  # Nomor peserta
                name = cols[2].text.strip()           # Nama
                pu = cols[3].text.strip()             # PU
                ppu = cols[4].text.strip()            # PPU
                kmbm = cols[5].text.strip()           # KMBM
                pk = cols[6].text.strip()             # PK
                lit_ind = cols[7].text.strip()        # LIT IND
                lit_ing = cols[8].text.strip()        # LIT ING
                pm = cols[9].text.strip()             # PM
                total = cols[10].text.strip()          # Total
                status_kelulusan = cols[11].text.strip()

                # Validasi: pastikan nilai numerik tidak kosong atau tidak valid
                required_fields = [pu, ppu, kmbm, pk, lit_ind, lit_ing, pm, total,status_kelulusan]
                if any(field == '' for field in required_fields):
                    logging.info(f"Data untuk peserta '{name}' tidak diambil karena ada nilai yang kosong.")
                    continue

                # Simpan data dalam bentuk dictionary
                data.append({
                    'participant_no': participant_no,
                    'name': name,
                    'pu': pu,
                    'ppu': ppu,
                    'kmbm': kmbm,
                    'pk': pk,
                    'lit_ind': lit_ind,
                    'lit_ing': lit_ing,
                    'pm': pm,
                    'total': total,
                    'status_kelulusan': status_kelulusan,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

            except Exception as e:
                logging.warning(f"Error parsing baris di halaman {page_num}: {e}")
                continue

        if not data:
            logging.warning("Tidak ada data yang berhasil diekstrak setelah validasi.")
        return data

    except requests.RequestException as e:
        logging.error(f"Error mengambil halaman {page_num}: {e}")
        return []

def scrape_main():
    """Mengambil data dari semua halaman."""
    try:
        all_data = []
        logging.info("Mengambil data dari halaman")
        page_data = scrape_page(1)  # Hanya satu halaman
        all_data.extend(page_data)
        
        if not all_data:
            logging.warning("Tidak ada data yang berhasil diambil. Periksa log untuk detail.")
            return []  # Ubah raise ValueError menjadi return [] agar tidak langsung error
        
        return all_data
    
    except Exception as e:
        logging.error(f"Terjadi error di scrape_main: {e}")
        raise

def save_to_csv(data, filename='tryout_data.csv'):
    """Menyimpan data ke CSV dengan validasi."""
    try:
        if not data:
            logging.warning("Tidak ada data untuk disimpan ke CSV.")
            return

        # Pastikan direktori ada
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Konversi data ke DataFrame dan simpan ke CSV
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, quoting=csv.QUOTE_MINIMAL)
        
        # Validasi CSV
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Berkas CSV {filename} tidak dibuat")
        
        saved_df = pd.read_csv(filename)
        if len(saved_df) != len(df):
            raise ValueError(f"Berkas CSV {filename} memiliki {len(saved_df)} baris, diharapkan {len(df)}")
        
        logging.info(f"Berhasil menyimpan dan memvalidasi {len(df)} record ke {filename}")
    
    except (PermissionError, OSError) as e:
        logging.error(f"Error sistem berkas saat menyimpan CSV: {e}")
        raise
    except Exception as e:
        logging.error(f"Error menyimpan CSV: {e}")
        raise