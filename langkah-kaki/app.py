import streamlit as st
import numpy as np
import pandas as pd

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="DailyStep",
    page_icon="💙",
    layout="wide"
)

# ================================
# BABY BLUE THEME CSS
# ================================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #dbefff, #b5d8ff);
    font-family: 'Poppins', sans-serif;
}

.main {
    background: transparent;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #0a4fa3;
    margin-bottom: -10px;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #3772a8;
    margin-bottom: 30px;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.55);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(140,180,255,0.45);
    box-shadow: 0 4px 14px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

/* Jam Card */
.jam-card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    border-left: 5px solid #1675d1;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton > button {
    background-color: #1675d1;
    color: white;
    padding: 10px 20px;
    border-radius: 12px;
    border: none;
}
.stButton > button:hover {
    background-color: #0f5faa;
}

/* Profile Card */
.profile-card {
    background: rgba(255, 255, 255, 0.55);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid rgba(120,160,255,0.45);
    box-shadow: 0 3px 10px rgba(0,0,0,0.12);
}

.creator-name {
    font-size: 20px;
    font-weight: 700;
    color: #0a4fa3;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)



# ================================
# SIDEBAR MENU
# ================================
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Input Langkah", "Hitung Kalori", "Profil Creator"]
)



# ================================
# 1. HOME PAGE
# ================================
if menu == "Home":

    st.markdown('<p class="title">DailyStep</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Track langkahmu dengan gaya baby blue aesthetic 💙✨</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass" style="text-align:center; padding:40px;">
        <img src="https://cdn-icons-png.flaticon.com/512/9297/9297257.png"
            width="110" style="margin-bottom:15px; opacity:0.95;">
        <h3 style="color:#0a4fa3; margin-bottom:5px;">Selamat datang di DailyStep 💙</h3>
        <p style="color:#3772a8; font-size:16px; margin-top:0px;">
            Mulai dari menu di kiri untuk input langkah atau hitung kalori.
        </p>
    </div>
    """, unsafe_allow_html=True)



# ================================
# 2. INPUT LANGKAH (SCROLLABLE)
# ================================
elif menu == "Input Langkah":

    st.markdown('<p class="title">Input Langkah Per Jam</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Scroll ke bawah & isi langkahmu 💙</p>', unsafe_allow_html=True)

    jam_list = [f"{h:02d}:00" for h in range(6, 23)]

    if "steps" not in st.session_state:
        st.session_state["steps"] = {jam: 0 for jam in jam_list}

    steps = st.session_state["steps"]

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    # SCROLL AREA
    for jam in jam_list:
        st.markdown(f"<div class='jam-card'>", unsafe_allow_html=True)
        steps[jam] = st.number_input(
            f"🕒 {jam}",
            min_value=0,
            max_value=30000,
            value=steps[jam],
            step=10,
            key=f"step_{jam}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.success("Data tersimpan otomatis ✔")


# ================================
# 3. HITUNG KALORI
# ================================
elif menu == "Hitung Kalori":

    st.markdown('<p class="title">Hitung Kalori</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Ayo cek total aktivitasmu hari ini 💙</p>', unsafe_allow_html=True)

    if "steps" not in st.session_state:
        st.warning("Isi langkah dulu di menu *Input Langkah* 💙")
    else:
        data = list(st.session_state["steps"].values())
        idx = np.arange(len(data))

        data = np.array(data, dtype=float)
        kosong = np.where(data == 0)[0]

        # INTERPOLASI
        if len(kosong) > 0:
            isi = np.where(data != 0)[0]
            data_interp = data.copy()
            data_interp[kosong] = np.interp(kosong, isi, data[isi])
        else:
            data_interp = data

        total_steps = int(np.sum(data_interp))
        kalori = round(total_steps * 0.04, 2)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📊 Hasil Perhitungan")
        st.write(f"Total langkah (setelah interpolasi): **{total_steps:,}**")
        st.write(f"Estimasi kalori terbakar: **{kalori} kcal**")

        st.subheader("💙 Saran Kesehatan")
        if kalori < 150:
            st.info("Coba jalan santai 10–15 menit yaa 💧")
        elif kalori < 350:
            st.success("Aktivitasmu cukup oke hari ini! 💙")
        else:
            st.success("Kamu aktif banget! Jangan lupa hidrasi & istirahat 💦")

        st.markdown('</div>', unsafe_allow_html=True)



# ================================
# 4. PROFIL CREATOR
# ================================
elif menu == "Profil Creator":

    st.markdown('<p class="title">Creator</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="profile-card">
            <img src="https://api.dicebear.com/9.x/thumbs/svg?seed=zahra" width="90">
            <div class="creator-name">Aulia Zahra</div>
            <p>NIM : K1323015
            <br>Prodi : Pendidikan Matematika
            <br>Universitas : UNS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-card">
            <img src="https://api.dicebear.com/9.x/thumbs/svg?seed=arum" width="90">
            <div class="creator-name">Arum Fajar R</div>
            <p>NIM : K1323011
            <br>Prodi : Pendidikan Matematika
            <br>Universitas : UNS</p>
        </div>
        """, unsafe_allow_html=True)
