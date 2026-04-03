import streamlit as st
import os
import time
import pandas as pd
import plotly.express as px
from google import genai
from ecologits import EcoLogits

# Konfigurasi Halaman
st.set_page_config(
    page_title="AI Energy Tracker | SMAN 2 Wates",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom untuk Tampilan Premium
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stChatFloatingInput {
        background-color: #161b22;
    }
    .title-text {
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Pengaturan
with st.sidebar:
    # Menampilkan Logo SMAN 2 Wates
    if os.path.exists("logo_sman2wates.png"):
        st.image("logo_sman2wates.png", width=170)
    
    st.title("⚙️ Pengaturan")
    st.markdown("---")
    api_key = st.text_input("Gemini API Key", value=os.environ.get("GEMINI_API_KEY", ""), type="password")
    
    st.subheader("Konfigurasi")
    electricity_zone = st.selectbox(
        "Zona Bauran Listrik",
        ["IDN (Indonesia)", "WOR (Dunia)", "USA (Amerika Serikat)", "FRA (Prancis)", "GBR (Inggris)"],
        index=0
    )
    
    st.info("AI Energy Tracker memantau panggilan API Anda untuk memperkirakan penggunaan energi, emisi karbon, dan konsumsi air secara real-time.")
    st.caption("Dikembangkan oleh TIM Inovasi Konservasi Energi SMAN 2 Wates.")

# Inisialisasi EcoLogits
if api_key:
    # Pastikan zona yang dikirim hanya kodenya saja (3 huruf)
    zone_code = electricity_zone.split(" ")[0]
    EcoLogits.init(providers=["google_genai"], electricity_mix_zone=zone_code)
    client = genai.Client(api_key=api_key)
else:
    st.warning("Silakan masukkan Gemini API Key Anda di sidebar.")
    st.stop()

# Judul dan Deskripsi
st.title("🚀 AI Energy Tracker SMAN 2 Wates")
st.subheader("(Inovasi Konservasi Energi)")
st.markdown("""
Pantau *environmental footprint* dari interaksi AI Generatif Anda secara real-time. 
Dashboard ini melacak dampak dari **Gemini 3.0 Flash** dengan *fallback* otomatis ke **Gemini 2.0 Flash**.
""")

# Inisialisasi Riwayat dalam Session State
if "history" not in st.session_state:
    st.session_state.history = []

# Layout: 4 Kolom untuk Metrik Utama
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

# Antarmuka Chat
prompt = st.chat_input("Kirim pesan ke Gemini...")

if prompt:
    # Logika fallback model
    models_to_try = ["gemini-3-flash-preview", "gemini-2.0-flash"]
    response = None
    used_model = None
    
    with st.spinner("Menghasilkan respons dan melacak dampak..."):
        for model in models_to_try:
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                used_model = model
                break
            except Exception as e:
                # Catch both Quota Exhausted (429) & Model Overloaded (503)
                if any(err in str(e) for err in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]):
                    st.toast(f"{model} sedang sibuk. Beralih ke model cadangan...", icon="⚠️")
                    continue
                st.error(f"Kesalahan tidak terduga pada {model}: {e}")
                break
    
    if response:
        # Ekstrak data dampak
        impacts = response.impacts
        st.session_state.history.append({
            "Waktu": time.strftime("%H:%M:%S"),
            "Prompt": prompt,
            "Respon": response.text,
            "Model": used_model,
            "Energi_kWh": impacts.energy.value.mean if impacts.energy else 0,
            "Emisi_kgCO2": impacts.gwp.value.mean if impacts.gwp else 0,
            "Air_m3": impacts.wcf.value.mean if impacts.wcf else 0,
            "Token": response.usage_metadata.candidates_token_count + (response.usage_metadata.prompt_token_count or 0)
        })
        
        # Tampilkan interaksi terbaru
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            st.write(response.text)
            st.caption(f"Dihasilkan melalui {used_model}")

# Bagian Visualisasi
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    
    # Perbarui Metrik ke interaksi terakhir
    latest = df.iloc[-1]
    m_col1.metric("Penggunaan Energi", f"{latest['Energi_kWh']:.6f} kWh", delta_color="inverse")
    m_col2.metric("Jejak Karbon", f"{latest['Emisi_kgCO2']:.6f} kgCO2eq", delta_color="inverse")
    m_col3.metric("Konsumsi Air", f"{latest['Air_m3']:.6f} m³", delta_color="inverse")
    m_col4.metric("Total Token", f"{latest['Token']}", delta_color="normal")
    
    st.markdown("---")
    st.subheader("📊 Analisis Lingkungan (Riwayat Sesi)")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Grafik Energi vs Token
        fig_energy = px.scatter(
            df, x="Token", y="Energi_kWh", color="Model",
            title="Konsumsi Energi vs. Jumlah Token",
            labels={"Token": "Jumlah Token", "Energi_kWh": "Energi (kWh)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig_energy, use_container_width=True)
        
    with viz_col2:
        # Distribusi Penggunaan Model
        model_counts = df["Model"].value_counts().reset_index()
        fig_model = px.pie(
            model_counts, names="Model", values="count",
            title="Distribusi Penggunaan Model (Pelacak Fallback)",
            template="plotly_dark",
            hole=0.4
        )
        st.plotly_chart(fig_model, use_container_width=True)

    # Tabel Detail
    st.subheader("📝 Log Aktivitas")
    st.dataframe(df[["Waktu", "Prompt", "Model", "Token", "Energi_kWh", "Emisi_kgCO2"]], use_container_width=True)

else:
    st.info("Mulai percakapan untuk melihat metrik energi muncul di sini!")
