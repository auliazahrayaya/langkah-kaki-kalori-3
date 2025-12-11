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
# CUSTOM CSS — BABY BLUE AESTHETIC
# ----------------------------------------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #e7f2ff 0%, #b9d9ff 100%);
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
# ✨ FIXED SIDEBAR NAVIGATION
# ----------------------------------------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Menu", "Input Your Step", "Count Your Calories", "Profile Creator"]
)

# ----------------------------------------------------------
# 1. Menu
# ----------------------------------------------------------
if menu == "Menu":

    st.markdown("""
    <style>
        .hero-box {
            background: rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(18px);
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
            color: #0a4fa3;
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
    st.markdown("<p class='hero-sub'>Ayo Track Langkah mu!💙</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# 2. INPUT YOUR STEP
# ----------------------------------------------------------
elif menu == "Input YOUR STEP":

    st.markdown("<h2 style='color:#1366c6;'>Input Langkah per Jam</h2>", unsafe_allow_html=True)
    st.write("Scroll dan isi langkah sesuai jam. Jam yang kosong akan diisi otomatis (interpolasi).")

    jam_list = [f"{h:02d}:00" for h in range(6, 23)]

    if "langkah_per_jam" not in st.session_state:
        st.session_state["langkah_per_jam"] = {jam: 0 for jam in jam_list}

    langkah = st.session_state["langkah_per_jam"]

    for jam in jam_list:
        st.markdown("<div class='jam-card'>", unsafe_allow_html=True)
        langkah[jam] = st.number_input(
            f"Langkah pada {jam}",
            min_value=0,
            max_value=20000,
            value=langkah[jam],
            step=5,
            key=f"step_{jam}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("Semua input disimpan otomatis ✔")


# ----------------------------------------------------------
# 3. COUNT YOUR CALORIES
# ----------------------------------------------------------
elif menu == "Count Your Calories":

    st.markdown("<h2 style='color:#1366c6;'>Perhitungan Kalori</h2>", unsafe_allow_html=True)

    if "langkah_per_jam" not in st.session_state:
        st.warning("Isi dulu langkah pada menu *Input Langkah per Jam* ya 💙")

    else:
        data = np.array(list(st.session_state["langkah_per_jam"].values()), dtype=float)

        missing = np.where(data == 0)[0]

        if len(missing) > 0:
            known = np.where(data != 0)[0]
            data_filled = data.copy()
            data_filled[missing] = np.interp(missing, known, data[known])
        else:
            data_filled = data

        total = int(np.sum(data_filled))
        kalori = round(total * 0.04, 2)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.write(f"**Total Langkah:** {total:,}")
        st.write(f"**Kalori Terbakar:** {kalori} kcal")

        if kalori < 150:
            st.info("🌥 Masih rendah, coba jalan 10–15 menit.")
        elif kalori < 350:
            st.success("💙 Bagus! Aktivitasmu stabil.")
        else:
            st.success("🔥 Kamu aktif banget hari ini! Jangan lupa minum air.")
        st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# 4. PROFILE CREATOR
# ----------------------------------------------------------
elif menu == "Profile Creator":

    st.markdown("<h2 style='color:#1366c6;'>Profil Creator</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='creator-card'>
            <img src='https://api.dicebear.com/9.x/thumbs/svg?seed=zahra' width='90'>
            <div class='creator-name'>Aulia Zahra</div>
            <p>NIM : K1323015</p>
            <p>Pendidikan Matematika</p>
            <p>UNS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='creator-card'>
            <img src='https://api.dicebear.com/9.x/thumbs/svg?seed=arum' width='90'>
            <div class='creator-name'>Arum Fajar R</div>
            <p>NIM : K1323011</p>
            <p>Pendidikan Matematika</p>
            <p>UNS</p>
        </div>
        """, unsafe_allow_html=True)
