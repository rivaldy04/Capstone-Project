from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model
modelKlasifikasi = joblib.load("model_klasifikasi.pkl")
modelClustering = joblib.load("model_clustering.pkl")
label_encoder = joblib.load("encoder.joblib")

# Inisialisasi aplikasi
app = FastAPI()

# Definisikan format input
class InputData(BaseModel):
    PU: float
    PBM: float
    PPU: float
    PK: float
    BIndo: float
    BIng: float
    PM: float

@app.post("/predict")
def predict(data: InputData):
    nilai = [data.PU, data.PBM, data.PPU, data.PK, data.BIndo, data.BIng, data.PM]
    fitur = ["PU", "PBM", "PPU", "PK", "BIndo", "BIng", "PM"]

    RATAAN = np.mean(nilai)
    SBAKU = np.std(nilai)
    MIN = np.min(nilai)
    MAX = np.max(nilai)
    TOTAL = np.sum(nilai)

    cluster_array = np.array([[RATAAN, TOTAL]])
    cluster = modelClustering.predict(cluster_array)

    belajar = {
        "PU": ["PU : Kesesuaian Pernyataan, Logika Matematika, Analisis Data Sederhana, Pemodelan Matematika,  Pola Bilangan"],
        "PBM": ["PBM : Kata Baku dan Tidak Baku, Kalimat Efektif, Penyuntingan Kalimat, Konjungsi, Penggunaan Tanda Baca"],
        "PPU": ["PPU : Tujuan atau Gagasan Utama, Inti Kalimat, Hubungan Antarkalimat, Kelogisan Kalimat, Rujukan pada Teks"],
        "PK": ["PK : Dimensi 0-1-2 & Relasinya, Fungsi Komposisi dan Invers, Peluang dan Kombinatorika, Barisan dan Deret, Statistika"],
        "BIndo": ["LBI : Inti Bacaan,  Topik dalam Bacaan, Simpulan Isi Bacaan, Makna Kontekstual Kata, Inferensi dalam Bacaan"],
        "BIng": ["LBE : Topic and Main Idea,  Stated Detail Information, Purpose of the Text, Synonym and Reference, Tone and Writer’s Attitude"],
        "PM": ["PM :  Geometri dan Trigonometri, Fungsi Komposisi dan Invers, Statistika Dasar, Peluang dan Kombinatorika, Sistem Persamaan Linear"]
    }

    saran = []

    if cluster[0] == 1 or RATAAN < 550:
        for i in range(len(nilai)):
            if nilai[i] < 550:
                saran.extend(belajar[fitur[i]])
        PTN_array = np.array([[RATAAN, SBAKU, MIN, MAX]])
        PTN = modelKlasifikasi.predict(PTN_array)
        if len(saran) > 1:
            return {"prediction": PTN.tolist(), 
                    "message": saran}
    elif cluster[0] == 0 or RATAAN < 750:
        for i in range(len(nilai)):
            if nilai[i] < 700:
                saran.extend(belajar[fitur[i]])
        PTN_array = np.array([[RATAAN, SBAKU, MIN, MAX]])
        PTN = modelKlasifikasi.predict(PTN_array)
        PTN = np.argmax(PTN, axis=1)
        PTN = label_encoder.inverse_transform(PTN)
        if len(saran) > 1:
            return {"prediction": PTN.tolist(), 
                    "message": saran}
        else :
            return {"prediction": PTN.tolist()}
    else:
        PTN_array = np.array([[RATAAN, SBAKU, MIN, MAX]])
        PTN = modelKlasifikasi.predict(PTN_array)
        PTN = np.argmax(PTN, axis=1)
        PTN = label_encoder.inverse_transform(PTN)
        return {"prediction": PTN.tolist()}