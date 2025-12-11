import streamlit as st
import numpy as np

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="DailySteps",
    page_icon="👟",
    layout="wide"
)

# ----------------------------------------------------------
# CUSTOM CSS — BLUE SOFT AESTHETIC
# ----------------------------------------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #e7f2ff 0%, #b9d9ff 100%);
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 800;
    color: #0f5faa;
    text-align: center;
    margin-bottom: -8px;
}
.subtitle {
    font-size: 18px;
    color: #234b76;
    text-align: center;
    margin-bottom: 30px;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.55);
    padding: 25px;
    border-radius: 18px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.10);
}

/* Jam card */
.jam-card {
    background: white;
    padding: 15px;
    border-radius: 14px;
    margin-bottom: 12px;
    border-left: 5px solid #1675d1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Input dan Button */
.stTextInput > div > input {
    border-radius: 10px !important;
    border: 1px solid #8ec8ff !important;
}
.stNumberInput > div > input {
    border-radius: 10px;
    border: 1px solid #8ec8ff;
}
.stButton > button {
    background-color: #1675d1;
    color: white;
    padding: 10px 20px;
    border-radius: 12px;
}
.stButton > button:hover {
    background-color: #0f5faa;
}

/* Profile Card */
.creator-card {
    background: white;
    padding: 18px;
    width: 250px;
    border-radius: 16px;
    text-align: center;
    color: #003d66;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
}
.creator-name {
    font-weight: 700;
    font-size: 20px;
    margin-top: 10px;
    color: #005da3;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR MENU
# ----------------------------------------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Menu", "Input Your Step", "Count Your Calories", "Profile Creator"]
)

# ==========================================================
# 1. HALAMAN UTAMA
# ==========================================================
# ==========================================================
# 1. HALAMAN UTAMA — BABY BLUE iPHONE STYLE
# ==========================================================
if menu == "Halaman Utama":

    st.markdown("""
    <style>
        .hero-box {
            background: rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            padding: 55px;
            border-radius: 28px;
            width: 80%;
            margin: auto;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            text-align: center;
        }
        .hero-title {
            font-size: 46px;
            font-weight: 700;
            color: #0a4fa3; /* baby blue navy tone */
        }
        .hero-sub {
            font-size: 18px;
            color: #3c6fa8;
            margin-top: -8px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='hero-box'>", unsafe_allow_html=True)

    st.markdown("""
    <img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png"
         width="120" style="opacity:0.95; margin-bottom:15px;">
    """, unsafe_allow_html=True)

    st.markdown("<div class='hero-title'>DailySteps</div>", unsafe_allow_html=True)
    st.markdown("<p class='hero-sub'>Ayo Track Langkah mu! 💙</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# 2. INPUT YOUR STEP
# ==========================================================
elif menu == "Input Jam & Langkah":
    st.markdown("<h2 style='color:#1366c6;'>Input Langkah Per Jam</h2>", unsafe_allow_html=True)
    st.write("Scroll ke bawah lalu isi langkah sesuai jam. Jika ada jam yang kosong → nanti diisi otomatis.")

    jam_list = [f"{h:02d}:00" for h in range(6, 23)]

    if "langkah_per_jam" not in st.session_state:
        st.session_state["langkah_per_jam"] = {jam: 0 for jam in jam_list}

    langkah_data = st.session_state["langkah_per_jam"]

    # Scrollable column
    with st.container():
        for jam in jam_list:
            st.markdown(f"<div class='jam-card'>", unsafe_allow_html=True)
            langkah_data[jam] = st.number_input(
                f"Langkah pada {jam}",
                min_value=0,
                max_value=30000,
                value=langkah_data[jam],
                step=10,
                key=f"step_{jam}"
            )
            st.markdown("</div>", unsafe_allow_html=True)

    st.success("Semua input berhasil disimpan otomatis ✔")


# ==========================================================
# 3. COUNT YOUR CALORIES
# ==========================================================
elif menu == "Hitung Kalori":
    st.markdown("<h2 style='color:#1366c6;'>Perhitungan Kalori</h2>", unsafe_allow_html=True)

    if "langkah_per_jam" not in st.session_state:
        st.warning("Isi data di menu *Input Jam & Langkah* dulu ya 💙")
    else:
        data = list(st.session_state["langkah_per_jam"].values())
        idx = np.arange(len(data))

        data = np.array(data, dtype=float)
        missing = np.where(data == 0)[0]

        if len(missing) > 0:
            known = np.where(data != 0)[0]
            data_filled = data.copy()
            data_filled[missing] = np.interp(missing, known, data[known])
        else:
            data_filled = data

        total_steps = int(np.sum(data_filled))
        calories = round(total_steps * 0.04, 2)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.write(f"**Total Langkah (setelah interpolasi):** {total_steps:,}")
        st.write(f"**Estimasi Kalori Terbakar:** {calories} kcal")

        if calories < 150:
            st.info("🌥 Masih rendah nih, coba jalan santai 10–15 menit.")
        elif calories < 350:
            st.success("🌿 Aktivitasmu cukup baik! Lanjutkan ya.")
        else:
            st.success("🔥 Kamu super aktif! Jangan lupa hidrasi & istirahat.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# 4. PROFILE CREATOR
# ==========================================================
elif menu == "Profil Creator":
    st.markdown("<h2 style='color:#1366c6;'>Profil Creator</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='creator-card'>
            <img src='https://api.dicebear.com/9.x/thumbs/svg?seed=zahra' width='90'>
            <div class='creator-name'>Aulia Zahra</div>
            <p>NIM : K1323015</p>
            <p>Prodi : Pendidikan Matematika</p>
            <p>Universitas : UNS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='creator-card'>
            <img src='https://api.dicebear.com/9.x/thumbs/svg?seed=arum' width='90'>
            <div class='creator-name'>Arum Fajar R</div>
            <p>NIM : K1323011</p>
            <p>Prodi : Pendidikan Matematika</p>
            <p>Universitas : UNS</p>
        </div>
        """, unsafe_allow_html=True)
