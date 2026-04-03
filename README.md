# 🌱 AI Energy Tracker | SMAN 2 Wates

**AI Energy Tracker** adalah sebuah dashboard interaktif berbasis Streamlit yang dirancang untuk melacak dan memvisualisasikan konsumsi energi, emisi karbon, serta penggunaan air secara *real-time* dari interaksi dengan model Generative AI (Google Gemini). 

Proyek ini merupakan bagian dari **Inovasi Konservasi Energi SMAN 2 Wates**.

👨‍💻 **Pengembang:** Tirtandro Meda

---

## ✨ Fitur Utama

- **Pemantauan Real-Time:** Menghitung estimasi penggunaan energi (kWh), jejak karbon (kgCO2eq), dan konsumsi air (m³) dari setiap prompt yang dikirim ke AI.
- **Visualisasi Dinamis:** Menyediakan grafik berbasis Plotly untuk membandingkan penggunaan token dengan konsumsi energi.
- **Smart Model Fallback:** Otomatis mencoba `gemini-3-flash-preview` dan mundur ke `gemini-2.0-flash` jika kuota limit (HTTP 429) tercapai.
- **Kustomisasi Zona Energi:** Memungkinkan pemilihan zona bauran listrik (seperti Indonesia, US, Eropa) untuk penghitungan emisi yang lebih akurat.

## 🚀 Instalasi dan Menjalankan Lokal

1. **Clone repository ini**
   ```shell
   git clone <url-repo-anda>
   cd "AI Energi Tracker"
   ```

2. **Install dependensi**
   Pastikan Anda sudah menginstal Python 3.10+. Jalankan perintah:
   ```shell
   pip install -r requirements.txt
   ```
   *(Dependensi utama: `streamlit`, `google-genai`, `pandas`, `plotly`, dan `ecologits`)*

3. **Jalankan Aplikasi**
   ```shell
   streamlit run dashboard.py
   ```
   Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`.

## 🌐 Deployment (Railway)

Repository ini telah dikonfigurasi untuk siap di-deploy ke **Railway** atau platform PaaS lainnya.
- File `requirements.txt` dan `Procfile` sudah disiapkan.
- Hubungkan repository ini ke Railway, atur Environment Variable `GEMINI_API_KEY`, dan aplikasi Anda akan otomatis ter-deploy.

---

### *Powered by*
Proyek ini ditenagai oleh **[EcoLogits](https://ecologits.ai/)**, sebuah pustaka open-source untuk melacak dampak lingkungan dari penggunaan API model AI Generatif.
