import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Step & Calorie Interpolation", layout="centered")

# Aesthetic title
st.markdown("""
    <h1 style='text-align:center; font-size:40px; color:#5A4FCF;'>
        👟 Step Tracker & Calorie Interpolation 🔥
    </h1>
    <p style='text-align:center; color:gray; font-size:18px;'>
        Isi data langkah jam-jam tertentu ➜ sistem otomatis isi data kalori yang hilang
    </p>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# INPUT DATA MANUAL (TANPA CSV)
# ---------------------------------------------------

st.subheader("📝 Input Langkah")

col1, col2 = st.columns(2)

with col1:
    jam = st.multiselect(
        "Pilih jam:",
        options=[f"{h}:00" for h in range(6, 23)],
        default=["06:00", "09:00", "12:00", "15:00", "18:00"]
    )

with col2:
    langkah = st.text_input(
        "Masukkan jumlah langkah (pisahkan dengan koma)",
        "500, 1200, 2000, 1500, 1800"
    )

# Convert input
try:
    langkah_list = [int(x.strip()) for x in langkah.split(",")]
except:
    st.warning("Format langkah harus angka dipisah koma.")
    st.stop()

# Validasi
if len(jam) != len(langkah_list):
    st.error("Jumlah jam dan langkah HARUS sama!")
    st.stop()

# Buat dataframe
df = pd.DataFrame({
    "Jam": jam,
    "Langkah": langkah_list
})

# Konversi jam ke angka (06:00 → 6)
df["X"] = df["Jam"].str.slice(0, 2).astype(int)

# ---------------------------------------------------
# INTERPOLASI KALORI
# ---------------------------------------------------

st.subheader("🔥 Interpolasi Kalori Hilang")

# Rumus konversi sederhana: 1 langkah = 0.04 kalori
df["Kalori"] = df["Langkah"] * 0.04

# Buat jam lengkap 06–22
jam_lengkap = np.arange(6, 23)

# Interpolasi kalori
kalori_interpolated = np.interp(jam_lengkap, df["X"], df["Kalori"])

hasil = pd.DataFrame({
    "Jam": jam_lengkap,
    "Kalori": kalori_interpolated,
})

st.success("Interpolasi berhasil! 🎉 Semua jam sudah terisi.")

# ---------------------------------------------------
# TAMPILKAN DATA
# ---------------------------------------------------

st.subheader("📊 Hasil Interpolasi Kalori per Jam")

st.dataframe(hasil, use_container_width=True)

# Grafik simple (Streamlit native)
st.line_chart(hasil.set_index("Jam"))

st.divider()

st.markdown(
    "<p style='text-align:center; color:gray;'>Made with 💜 Interpolation</p>",
    unsafe_allow_html=True
)
