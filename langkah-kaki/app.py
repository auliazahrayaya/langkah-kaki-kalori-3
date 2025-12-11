import streamlit as st
import numpy as np
import pandas as pd

# =====================================================================
# PAGE CONFIG — BLUE SOFT MODE
# =====================================================================
st.set_page_config(page_title="DailyStep", page_icon="👟", layout="wide")

# =====================================================================
# CSS — BABY BLUE iPHONE STYLE
# =====================================================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #d6ecff, #b7dbff);
    font-family: 'Poppins', sans-serif;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #0a4fa3;
    margin-bottom: -5px;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #3c6fa8;
    margin-bottom: 25px;
}

/* Glass box */
.hero {
    background: rgba(255, 255, 255, 0.45);
    padding: 45px;
    border-radius: 26px;
    backdrop-filter: blur(12px);
    width: 80%;
    margin: auto;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

/* Jam cards */
.jam-card {
    background: white;
    padding: 15px;
    border-radius: 14px;
    border-left: 5px solid #1675d1;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

/* Profile */
.creator-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    width: 250px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}
.creator-name {
    font-size: 20px;
    font-weight: bold;
    color: #0a4fa3;
}

/* Button */
.stButton > button {
    background: #1675d1;
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
}
.stButton > button:hover {
    background: #0f5faa;
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# SIDEBAR MENU
# =====================================================================
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Input Jam & Langkah", "Hitung Kalori", "Profil Creator"]
)

# =====================================================================
# 1 — HOME PAGE
# =====================================================================
if menu == "Home":
    st.markdown('<p class="title">DailyStep</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Track aktivitasmu dengan vibe biru iPhone 💙</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <img src="https://cdn-icons-png.flaticon.com/512/5968/5968875.png" width="105">
        <h3 style="color:#0a4fa3; font-size:26px; margin-top:10px;">Selamat Datang! </h3>
        <p style="color:#3c5f8a; font-size:17px;">
            Masukkan langkahmu berdasarkan jam.  
            Kalau ada jam yang ketinggalan → nanti aku isi pakai interpolasi otomatis.  
            Hasil akhirnya: langkah harian + kalori realistik & saran kesehatan ✨
        </p>
        <p style="color:#0a4fa3; font-size:16px; margin-top:10px;">
            Mulai dari menu sebelah kiri 💙
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# 2 — INPUT JAM & LANGKAH
# =====================================================================
elif menu == "Input Jam & Langkah":
    st.markdown('<p class="title">Input Jam & Langkah</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Pilih jam → isi langkah → nanti aku simpan otomatis 💙</p>', unsafe_allow_html=True)

    jam_list = [f"{h:02d}:00" for h in range(6, 25)]

    if "steps" not in st.session_state:
        st.session_state["steps"] = {jam: None for jam in jam_list}

    selected_jam = st.selectbox("Pilih jam:", jam_list)
    langkah = st.number_input("Masukkan langkah:", 0, 30000, step=10)

    if st.button("Simpan"):
        st.session_state["steps"][selected_jam] = langkah
        st.success(f"Langkah pada jam {selected_jam} berhasil disimpan!")

    # tampilkan tabel scrollable
    df = pd.DataFrame({
        "Jam": jam_list,
        "Langkah": [st.session_state["steps"][j] for j in jam_list]
    })
    st.dataframe(df, height=400)

# =====================================================================
# 3 — HITUNG KALORI (FINAL FIX)
# =====================================================================
elif menu == "Hitung Kalori":
    st.markdown('<p class="title">Hitung Kalori</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Interpolasi + Kalori yang REALISTIK 💙</p>', unsafe_allow_html=True)

    if "steps" not in st.session_state:
        st.warning("Isi dulu langkah di menu *Input Jam & Langkah* ✨")
    else:
        df = pd.DataFrame({
            "jam": [f"{h:02d}:00" for h in range(6, 25)],
            "langkah": list(st.session_state["steps"].values())
        })

        df["langkah"] = df["langkah"].astype("float")
        df["filled"] = df["langkah"].interpolate(method="linear")

        # **LOGIC FIX:** total langkah 1 hari = langkah kumulatif terakhir
        last_value = df["filled"].iloc[-1]

        # Kalori realistis → 0.04 kkal/step
        kalori = round(last_value * 0.04, 2)

        st.markdown("<div class='hero'>", unsafe_allow_html=True)

        st.write(f"**Langkah terakhir (total harian):** {int(last_value):,}")
        st.write(f"**Kalori terbakar:** {kalori} kkal")

        # HEALTH SUGGESTION
        if kalori < 80:
            st.info("🌥 Jalan sedikit lagi ya, 5–10 menit aja sudah cukup 💙")
        elif kalori < 200:
            st.success("🌿 Aktivitasmu oke! Jaga pola makan juga yaa 💙")
        else:
            st.success("🔥 Kamu aktif banget hari ini! Jangan lupa minum air 💧")

        st.markdown("</div>", unsafe_allow_html=True)

        st.dataframe(df, height=350)

# =====================================================================
# 4 — PROFILE CREATOR
# =====================================================================
elif menu == "Profil Creator":
    st.markdown('<p class="title">Profil Creator</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="creator-card">
            <img src="https://api.dicebear.com/9.x/thumbs/svg?seed=Zahra" width="90">
            <div class="creator-name">Aulia Zahra</div>
            <p>NIM: K1323015<br>Prodi: Pendidikan Matematika<br>UNS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="creator-card">
            <img src="https://api.dicebear.com/9.x/thumbs/svg?seed=Arum" width="90">
            <div class="creator-name">Arum Fajar R</div>
            <p>NIM: K1323011<br>Prodi: Pendidikan Matematika<br>UNS</p>
        </div>
        """, unsafe_allow_html=True)
