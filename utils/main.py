from extract import scrape_main, save_to_csv
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Konfigurasi
    config = {
        'csv_filename': 'data/tryout_data.csv'
    }
    
    try:
        # Ekstraksi
        logging.info("Mulai ekstraksi data")
        raw_data = scrape_main()
        
        # Pemuatan
        logging.info("Mulai load data")
        save_to_csv(raw_data, config['csv_filename'])
        
        logging.info("ETL selesai diekstraksi")
        
    except Exception as e:
        logging.error(f"ETL gagal: {e}")
        raise

if __name__ == "__main__":
    main()