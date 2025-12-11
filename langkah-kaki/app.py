import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Step & Calorie Tracker",
    page_icon="👟",
    layout="wide"
)

# ============ DARK MODE CUSTOM CSS ============
dark_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0F1117;
    color: #FFFFFF;
}

.card {
    background: rgba(255,255,255,0.07);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.01);
    border-color: rgba(0,255,255,0.4);
}

.center { text-align: center; }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ============ MENU =============
menu = st.sidebar.radio(
    "Menu",
    ["🏠 Home", "📊 Hitung Langkah & Kalori", "👤 Profil Pembuat"]
)

# ================================================================
# 🏠 HOME
# ================================================================
if menu == "🏠 Home":
    st.markdown("<h1 class='center'>👟 Step & Calorie Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='center'>Menghitung langkah per jam, mengisi data hilang dengan interpolasi, dan menghitung kalori harian secara rasional.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Fitur:")
    st.write("""
    - Input langkah per jam  
    - Data kosong akan dihitung otomatis menggunakan **Interpolasi Linier**  
    - Perhitungan kalori menggunakan standar konversi aktivitas manusia  
    - Tampilan elegan dark mode  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ================================================================
# 📊 HITUNG
# ================================================================
elif menu == "📊 Hitung Langkah & Kalori":
    st.markdown("<h1 class='center'>📊 Hitung Langkah & Kalori</h1>", unsafe_allow_html=True)
    st.markdown("<p class='center'>Isi langkah per jam. Kosongkan jika lupa — interpolasi akan menyelesaikannya.</p>", unsafe_allow_html=True)

    hours = [f"{h:02d}:00" for h in range(24)]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Input Data Langkah per Jam")

    langkah_input = {}
    for h in hours:
        langkah_input[h] = st.text_input(f"Langkah pada {h}", "")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Hitung Interpolasi + Kalori"):
        df = pd.DataFrame({
            "Jam": hours,
            "Langkah": [
                float(x) if x.strip() != "" else np.nan
                for x in langkah_input.values()
            ]
        })

        df["Langkah"] = df["Langkah"].interpolate(method="linear")

        df["Kalori"] = df["Langkah"] * 0.04

        total = df["Kalori"].sum()

        st.success("Interpolasi berhasil dilakukan.")

        st.dataframe(df)

        st.markdown(f"### 🔥 Total Kalori Terbakar Hari Ini: **{total:.2f} kcal**")

# ================================================================
# 👤 PROFIL
# ================================================================
elif menu == "👤 Profil Pembuat":
    st.markdown("<h1 class='center'>👤 Profil Pembuat</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Mahasiswa 1")
    st.write("""
    **Nama:** Aulia Zahra  
    **NIM:** K1323015  
    **Prodi:** Pendidikan Matematika 
    **Universitas:** Universitas Sebelas Maret (UNS)
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Mahasiswa 2")
    st.write("""
    **Nama:** Arum Fajar Rahmawati 
    **NIM:** K1323011 
    **Prodi:** Pendidikan Matematika 
    **Universitas:** Universitas Sebelas Maret (UNS) 
    """)
    st.markdown("</div>", unsafe_allow_html=True)
