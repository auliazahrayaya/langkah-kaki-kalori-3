import streamlit as st
import numpy as np
import pandas as pd

# ================= PAGE CONFIG ===============
st.set_page_config(
    page_title="Step & Calorie Interpolation",
    page_icon="👟",
    layout="wide"
)

# ================= DARK MODE CSS ===============
dark_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0D1117;
    color: white;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(5px);
    transition: 0.3s;
}

.card:hover {
    border-color: #4ED2F7;
    transform: scale(1.01);
}

.center { text-align: center; }

.title {
    font-size: 42px;
    font-weight: 700;
    color: #4ED2F7;
    text-align: center;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ================= SIDEBAR MENU ===============
menu = st.sidebar.radio("Menu", ["🏠 Home", "📊 Hitung Langkah & Kalori", "👤 Profil"])

# ================= HOME PAGE ==================
if menu == "🏠 Home":
    st.markdown("<h1 class='title'>👟 Step & Calorie Interpolation</h1>", unsafe_allow_html=True)
    st.markdown("<p class='center'>Interpolasi data langkah yang hilang + perhitungan kalori rasional dalam 1 hari.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✨ Fitur Utama")
    st.write("""
    - Input jam & langkah manual  
    - Data langkah yang hilang diisi otomatis dengan **Interpolasi Linier**
    - Estimasi kalori menggunakan standar fisiologi manusia
    - Tampilan dark mode aesthetic
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ===================== HITUNG PAGE =======================
elif menu == "📊 Hitung Langkah & Kalori":
    st.markdown("<h1 class='title'>📊 Hitung Langkah & Kalori</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("1. Pilih jam/waktu")

    jam = st.multiselect(
        "Pilih jam aktivitas:",
        options=[f"{h}:00" for h in range(6, 23)],
        default=["06:00", "09:00", "12:00", "15:00", "18:00"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("2. Masukkan jumlah langkah (pisahkan koma)")

    langkah_text = st.text_input("Contoh: 500, 1200, 1800, 1500, 2000", "")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔍 Hitung Interpolasi + Kalori"):
        # Validasi
        try:
            langkah_list = [float(x.strip()) for x in langkah_text.split(",")]
        except:
            st.error("Format langkah harus angka dipisah koma!")
            st.stop()

        if len(jam) != len(langkah_list):
            st.error("Jumlah JAM dan LANGKAH harus sama!")
            st.stop()

        df = pd.DataFrame({
            "Jam": jam,
            "Langkah": langkah_list
        })

        df["X"] = df["Jam"].str.slice(0, 2).astype(int)

        # Buat jam lengkap 6–22
        jam_lengkap = np.arange(6, 23)

        # Interpolasi langkah
        langkah_interp = np.interp(jam_lengkap, df["X"], df["Langkah"])

        # Estimasi kalori = 0.04 kcal per langkah (standar fisiologis)
        kalori = langkah_interp * 0.04

        hasil = pd.DataFrame({
            "Jam": jam_lengkap,
            "Langkah (Interpolasi)": langkah_interp,
            "Kalori (kcal)": kalori
        })

        total_kal = hasil["Kalori (kcal)"].sum()

        st.success("Interpolasi selesai! Data lengkap dari jam 06:00 - 22:00")

        st.dataframe(hasil)

        st.markdown(f"### 🔥 Total Kalori Terbakar: **{total_kal:.2f} kcal**")

        st.line_chart(hasil.set_index("Jam")["Kalori (kcal)"])

# ===================== PROFILE PAGE =======================
elif menu == "👤 Profil":
    st.markdown("<h1 class='title'>👤 Profil Pembuat</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👩 Mahasiswa 1")
    st.write("""
    **Nama:** Aulia Zahra  
    **NIM:** K1323015  
    **Prodi:** Pendidikan Matematika
    **Universitas:** Universitas Sebelas Maret
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👩 Mahasiswa 2")
    st.write("""
    **Nama:** Arum Fajar Rahmawati 
    **NIM:** K1323011 
    **Prodi:** Pendidikan Matematika
    **Universitas:** Universitas Sebelas Maret
    """)
    st.markdown("</div>", unsafe_allow_html=True)
