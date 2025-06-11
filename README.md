## Proses Machine Learning

Berikut langkah-langkah membangun model untuk rekomendasi perguruan tinggi :
1. Melakukan clutering dengan metode K-Means
    Proses clustering dilakukan melalui tahapan-tahapan berikut:
    - Scraping Data
    Data diperoleh melalui proses web scraping dari situs online dengan URL: https://hasilto.bimbelssc.com/storage/ponorogo/intipa/data/TO_SNBT_JANUARI.html.

    - Pembersihan Data
    Kolom yang tidak relevan seperti participant_no, name, status_kelulusan, dan timestamp dihapus untuk menyederhanakan data dan fokus pada fitur yang penting.

    - Pra-Pemrosesan Nilai
    Nilai nol yang ditandai dengan “X” digantikan dengan angka 0. Selain itu, spasi dihapus dan tanda koma (,) diganti dengan titik (.) agar sesuai dengan format angka desimal.

    - Konversi Tipe Data
    Semua nilai numerik diubah ke tipe data float guna memfasilitasi proses rekayasa fitur (feature engineering).

    - Penanganan Nilai Hilang
    Nilai yang hilang diisi dengan nilai rata-rata kolom terkait, karena metode ini mempertahankan distribusi data serta tidak mengurangi ukuran sampel secara signifikan.

    - Penghapusan Duplikasi
    Data yang terduplikasi dihapus untuk menjaga keunikan setiap entri.

    - Rekayasa Fitur
    Ditambahkan beberapa fitur baru seperti rata-rata (RATAAN), simpangan baku (S.BAKU), total nilai (Total), nilai terkecil (MIN), dan nilai terbesar (MAX) pada setiap baris untuk memperkaya representasi data.

    - Seleksi Fitur
    Dipilih dua fitur utama yaitu Mean dan Total, karena keduanya merepresentasikan performa keseluruhan peserta dan memiliki kontribusi besar dalam membedakan klaster.

    - Normalisasi Data
    Dilakukan normalisasi menggunakan metode Min-Max Scaling, karena metode ini menjaga bentuk distribusi asli dan cocok digunakan pada algoritma berbasis jarak seperti K-Means.

    - Penentuan Jumlah Klaster Optimal
    Metode Elbow digunakan untuk menentukan jumlah klaster yang paling optimal dengan mengidentifikasi titik siku dari grafik inertia.

    - Proses Clustering
    Clustering dilakukan menggunakan algoritma K-Means dengan jumlah klaster sesuai hasil metode Elbow. Algoritma ini dipilih karena kemampuannya mengelompokkan data berdasarkan kemiripan fitur secara efisien.

    - Analisis Cluster
    Hasil clustering dianalisis untuk memahami karakteristik masing-masing klaster. Dalam kasus ini, diperoleh tiga klaster yang merepresentasikan tiga tingkatan performa peserta: rendah, sedang, dan tinggi.

2. Melakukan klasifikasi dengan metode random forest
    Proses klasifikasi dilakukan melalui tahapan-tahapan berikut:
    - Sumber Data
    Data utama untuk proses klasifikasi diambil dari Kaggle dengan tautan sebagai referensi: https://www.kaggle.com/datasets/rezkyyayang/passing-grade-utbk-in-science-major.

    - Seleksi Fitur
    Dilakukan feature selection untuk memilih fitur yang paling relevan. Pada proyek ini digunakan kolom-kolom: RATAAN, S.BAKU, MIN, dan MAX sebagai fitur, dengan PTN (Perguruan Tinggi Negeri) sebagai variabel target.

    - Pembangunan Model
    Model klasifikasi dibangun menggunakan algoritma Random Forest. Seluruh data utama digunakan sebagai data latih (training data) dalam proses ini.

    - Prediksi pada Data Dummy
    Model yang telah dilatih digunakan untuk memprediksi kolom target (PTN) pada data dummy, yaitu data hasil scraping dari tahap sebelumnya yang telah melalui proses feature engineering dan memiliki kolom yang sama: RATAAN, S.BAKU, MIN, dan MAX.

    - Penggabungan Data
    Setelah proses prediksi, data dummy yang telah dilabeli target digabungkan dengan data utama untuk memperbesar ukuran dataset dan meningkatkan potensi generalisasi model pada tahap selanjutnya.
    
3. Merancang model dengan arsitektur tensorflow
    Proses modeling dilakukan melalui tahapan-tahapan berikut:
    - dari data hasil gabungan pada tahap sebelumnya, akan dibagi menjadi 80% data latih dan 20% data uji. serta, melakukan label encoding untuk target
    - Membangun model tensorflow dengan arsitektur 
        - **Input Layer**: Model menerima input dengan bentuk `(4,)`, yang berarti setiap sampel memiliki 4 fitur.
        - **Hidden Layer 1**: Lapisan Dense dengan 64 unit, menggunakan aktivasi 'relu' untuk memperkenalkan non-linearitas. Regularisasi L2 dengan faktor 0.01 ditambahkan untuk mencegah overfitting.
        - **BatchNormalization**: Diterapkan setelah lapisan pertama untuk menormalkan aktivasi, meningkatkan stabilitas dan kecepatan pelatihan.
        - **Dropout (0.4)**: 40% unit dinonaktifkan secara acak selama pelatihan untuk mengurangi overfitting.
        - **Hidden Layer 2**: Lapisan Dense dengan 32 unit, juga menggunakan 'relu' dan regularisasi L2 (0.01).
        - **BatchNormalization**: Diterapkan lagi untuk menjaga stabilitas.
        - **Dropout (0.3)**: 30% unit dinonaktifkan untuk lebih lanjut mengontrol overfitting.
        - **Output Layer**: Lapisan Dense dengan 50 unit dan aktivasi 'softmax', yang menghasilkan probabilitas untuk 50 kelas (jumlah total probabilitas = 1).
    - Melakukan kompilasi Model:
        - **Optimizer**: Adam dengan learning rate awal 0.001, cocok untuk optimasi efisien.
        - **Loss Function**: 'sparse_categorical_crossentropy', digunakan untuk klasifikasi multi-kelas dengan label integer (0 hingga 49).
        - **Metrics**: 'accuracy', untuk memantau akurasi selama pelatihan.
    - Membuat callback:
        - **ReduceLROnPlateau**: Mengurangi learning rate sebesar faktor 0.5 jika 'val_loss' tidak membaik selama 5 epoch, dengan batas minimum 0.00001. Ini membantu model belajar lebih halus saat performa stagnan.

4. Membuat API dengan FastAPI
    Proses pembuatan API dilakukan melalui tahapan-tahapan berikut:
    - Pemuatan Model
    Memuat model klasifikasi, model clustering, dan label encoder menggunakan joblib, yang sebelumnya telah disimpan dari proses pelatihan.

    - Inisialisasi Aplikasi API
    Membuat aplikasi menggunakan FastAPI serta endpoint root ("/") untuk memastikan API berjalan dengan baik.

    - Definisi Format Input
    Menentukan struktur data input yang diperlukan oleh endpoint prediksi, yaitu tujuh nilai UTBK: PU, PBM, PPU, PK, BIndo, BIng, dan PM.

    - Perhitungan Fitur Tambahan
    Dari nilai-nilai UTBK tersebut, dihitung beberapa fitur baru seperti rata-rata, simpangan baku, nilai maksimum, nilai minimum, dan total nilai.

    - Prediksi Klaster Peserta
    Menggunakan model K-Means untuk mengelompokkan peserta ke dalam klaster performa (rendah, sedang, tinggi) berdasarkan rata-rata dan total nilai.

    - Pemberian Saran Pembelajaran
    Jika peserta berada dalam klaster rendah atau memiliki rata-rata nilai rendah, sistem memberikan saran materi pembelajaran berdasarkan mata pelajaran dengan skor di bawah ambang batas tertentu.

    - Prediksi PTN
    Jika peserta memiliki performa sedang atau tinggi, model klasifikasi digunakan untuk memprediksi PTN yang sesuai berdasarkan fitur tambahan yang telah dihitung.

    - Pengembalian Hasil
    API memberikan hasil prediksi berupa nama PTN dan/atau saran belajar, tergantung dari hasil klaster dan nilai peserta.

    - Membuat requirements.txt
    Untuk memastikan aplikasi dapat dijalankan dengan lingkungan yang konsisten di berbagai perangkat atau server, dibuat file requirements.txt yang berisi seluruh dependensi (library) yang digunakan dalam proyek ini, seperti : fastapi, uvicorn, scikit-learn, numpy, dan joblib

    - Membuat docker file
    Pembuatan Dockerfile bertujuan untuk membuat container yang dapat menjalankan aplikasi API secara konsisten di berbagai lingkungan. Dockerfile dimulai dengan menggunakan image dasar python:3.10, lalu menetapkan direktori kerja di /code. File requirements.txt disalin dan diinstal menggunakan pip untuk memastikan semua dependensi seperti FastAPI, scikit-learn, dan lainnya tersedia. Selanjutnya, seluruh isi proyek disalin ke dalam container. Terakhir, aplikasi dijalankan menggunakan perintah uvicorn pada host 0.0.0.0 dan port 7860, yang memungkinkan API diakses secara publik saat container dijalankan.
    
    - Deploy Model ke Hugging Face Spaces
    Proses deploy dilakukan dengan mengunggah seluruh komponen proyek, termasuk model machine learning, aplikasi FastAPI, file Dockerfile, dan requirements.txt, ke platform Hugging Face Spaces. Platform ini mendukung deployment berbasis kontainer, sehingga cocok untuk proyek yang menggunakan FastAPI dan Docker. Setelah file lengkap diunggah ke repository Space, Hugging Face secara otomatis membangun image Docker dan menjalankan aplikasi sesuai konfigurasi, menjadikan API dapat diakses publik secara online melalui URL yang disediakan.