import streamlit as st
import numpy as np
import pandas as pd

# ===============================
#  GLOBAL STYLING (Aesthetic Dark Mode)
# ===============================
st.set_page_config(page_title="DailyStep", page_icon="🦶", layout="centered")

st.markdown("""
<style>
    body {background-color: #0d0f19;}
    .main {background-color: #0d0f19;}
    .title {
        font-size: 38px; 
        color: #8ab4f8; 
        text-align: center; 
        font-weight: 700;
        margin-bottom: -10px;
    }
    .subtitle {
        font-size: 17px;
        color: #d1d5db;
        text-align: center;
        margin-bottom: 25px;
    }
    .card {
        background: #111321;
        padding: 18px 25px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #2a2d3a;
    }
</style>
""", unsafe_allow_html=True)


# ===============================
#       SIDEBAR MENU
# ===============================
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Input Langkah", "Profil Pembuat"],
    index=0
)


# ===============================
#             HOME
# ===============================
if menu == "Home":
    st.markdown('<p class="title">DailyStep</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Lihat langkahmu, temukan langkah yang hilang, dan hitung kalorinya ✨</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <b>Apa yang bisa kamu lakukan di sini?</b>
        <ul>
            <li>Input jumlah langkah tiap jam</li>
            <li>Kalau ada jam yang lupa dicatat, akan <i>diinterpolasi otomatis</i></li>
            <li>Hitung total kalori harian</li>
            <li>Lihat saran kesehatan berdasarkan kondisi tubuhmu</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ===============================
#       INPUT LANGKAH & INTERPOLASI
# ===============================
elif menu == "Input Langkah":

    st.markdown('<p class="title">Input Langkah Harian</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Isi sesuai jam. Kosongkan kalau lupa, nanti aku interpolasi ✨</p>', unsafe_allow_html=True)

    # Jam 06:00–21:00
    jam_list = [f"{h:02d}:00" for h in range(6, 22)]

    langkah_dict = {}
    st.markdown('<div class="card">', unsafe_allow_html=True)

    for jam in jam_list:
        val = st.number_input(f"Langkah di jam {jam}", min_value=0, value=None, step=1, key=jam)
        langkah_dict[jam] = val

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Proses Data 🚀"):

        df = pd.DataFrame({
            "jam": jam_list,
            "langkah": list(langkah_dict.values())
        })

        # Convert None → NaN
        df["langkah"] = df["langkah"].astype("float")

        # Interpolasi linear
        df["hasil"] = df["langkah"].interpolate(method="linear")

        # Hitung total langkah
        total_langkah = int(df["hasil"].sum())

        # Rumus kalori yang LOGIS
        total_kalori = round(total_langkah * 0.04, 2)  # 0.04 kcal per step

        st.success("Data berhasil diproses!")

        # Tampilkan tabel
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("Hasil interpolasi data langkah:")
        st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)

        # Summary Kalori
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Ringkasan Hari Ini")
        st.write(f"• Total langkah: **{total_langkah} langkah**")
        st.write(f"• Perkiraan kalori terbakar: **{total_kalori} kcal**")

        # Saran kesehatan
        st.subheader("💡 Saran kesehatan")
        if total_kalori < 150:
            st.write("Kamu kurang bergerak hari ini. Coba jalan santai bentar yuk! 🚶‍♀️")
        elif total_kalori < 350:
            st.write("Aktivitasmu oke! Tetap pertahankan 💪")
        else:
            st.write("Keren! Kamu sangat aktif hari ini 🔥🔥 Tapi jangan lupa istirahat juga ya!")
        st.markdown('</div>', unsafe_allow_html=True)


# ===============================
#          PROFIL PEMBUAT
# ===============================
elif menu == "Profil Pembuat":

    st.markdown('<p class="title">Creator</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Profile Creator ✨</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card">
            <b>👤 Aulia Zahra </b><br>
            NIM: K1323015 <br>
            Prodi: Pendidikan Matematika <br>
            Universitas Seblas Maret (UNS)
        </div>

        <div class="card">
            <b>👤 Arum Fajar R</b><br>
            NIM: K1323011 <br>
            Prodi: Pendidikan Matematika <br>
            Universitas Sebelas Maret (UNS)
        </div>
    """, unsafe_allow_html=True)
