import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="DailyStep", page_icon="🩷", layout="wide")

# ===============================
# PINK MODE CSS ✨ aesthetic
# ===============================
st.markdown("""
<style>

    body {
        background: linear-gradient(135deg, #ffd6e8, #ffecf4);
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background: transparent;
    }

    .title {
        font-size: 40px;
        text-align: center;
        font-weight: 800;
        background: -webkit-linear-gradient(#ff4f9a, #ff87b5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #633d52;
        margin-top: -15px;
        margin-bottom: 25px;
    }

    .glass {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(255, 150, 180, 0.4);
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(255, 120, 180, 0.25);
    }

    .profile-card {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(255, 180, 210, 0.5);
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(255, 120, 180, 0.25);
    }

</style>
""", unsafe_allow_html=True)



# ===============================
# Sidebar Menu
# ===============================
menu = st.sidebar.radio(
    "🌸 Menu",
    ["Home", "Input Langkah", "Profil Creator"]
)



# ===============================
# HOME PAGE
# ===============================
if menu == "Home":
    st.markdown('<p class="title">DailyStep</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Track langkahmu dengan gaya pink aesthetic 🩷✨</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass" style="padding: 30px; text-align:center;">
        <h3 style="color:#ff4f9a; font-weight:700; margin-bottom:10px;">
            Selamat datang di DailyStep 🩰
        </h3>

        <p style="color:#633d52; font-size:17px;">
            Aplikasi sederhana yang membantumu mencatat langkah harian,<br>
            mengisi data yang hilang dengan interpolasi,<br>
            dan menghitung kalori harian secara smooth & aesthetic.
        </p>

        <p style="margin-top:15px; font-size:16px; color:#ff4f9a;">
            Mulai dari menu di sebelah kiri 💗
        </p>
    </div>
    """, unsafe_allow_html=True)



# ===============================
# INPUT LANGKAH
# ===============================
elif menu == "Input Langkah":

    st.markdown('<p class="title">Input Langkah Harian</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Isi langkah sesuai jam — kosongin kalau lupa, nanti aku isi otomatis 💗</p>', unsafe_allow_html=True)

    jam_list = [f"{h:02d}:00" for h in range(6, 22)]
    langkah_map = {}

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    cols = st.columns(3)
    idx = 0

    for jam in jam_list:
        with cols[idx % 3]:
            langkah_map[jam] = st.number_input(
                f"🕒 {jam}",
                min_value=0,
                value=None,
                step=1
            )
        idx += 1

    st.markdown('</div>', unsafe_allow_html=True)


    if st.button("✨ Proses Data ✨"):
        df = pd.DataFrame({
            "jam": jam_list,
            "langkah": list(langkah_map.values())
        })
        df["langkah"] = df["langkah"].astype("float")

        df["hasil"] = df["langkah"].interpolate(method="linear")

        total_steps = int(df["hasil"].sum())
        total_kalori = round(total_steps * 0.04, 2)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📋 Hasil Interpolasi")
        st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🍓 Ringkasan Hari Ini")
        st.write(f"✨ Total langkah: **{total_steps} langkah**")
        st.write(f"✨ Kalori terbakar: **{total_kalori} kcal**")

        st.subheader("🌷 Saran Kesehatan")

        if total_kalori < 150:
            st.write("Kamu butuh gerak dikit lagi, sayang. Stretching yuk? 🩰")
        elif total_kalori < 350:
            st.write("Good job! Kamu cukup aktif hari ini 💗")
        else:
            st.write("OMG productive queen!! Tapi jangan lupa minum air 🍓🫧")

        st.markdown('</div>', unsafe_allow_html=True)



# ===============================
# PROFIL PEMBUAT — Pink Aesthetic Card
# ===============================
elif menu == "Profil Pembuat":

    st.markdown('<p class="title">Creator</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Dibuat dengan cinta & estetika pink 🩷✨</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="profile-card">
            <h3 style="color:#ff4f9a;">Aulia Zahra</h3>
            <p style="color:#633d52;">
                NIM: K1323015 <br>
                Prodi: Pendidikan Matematika <br>
                Universitas Sebelas Maret (UNS)
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-card">
            <h3 style="color:#ff4f9a;">Arum Fajar R</h3>
            <p style="color:#633d52;">
                NIM: K1323011 <br>
                Prodi: Pendidikan Matematika <br>
                Universitas Sebelas Maret (UNS)
            </p>
        </div>
        """, unsafe_allow_html=True)

