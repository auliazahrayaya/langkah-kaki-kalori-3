import streamlit as st
import numpy as np

# -----------------------------
# 🎨 THEME & PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="DailySteps",
    page_icon="👟",
    layout="centered"
)

# -----------------------------
# 🌈 CUSTOM CSS (Aesthetic Blue)
# -----------------------------
st.markdown("""
<style>
/* Background gradient */
body {
    background: linear-gradient(135deg, #dff1ff 0%, #b3d9ff 100%);
}

/* Card glass */
.glass {
    background: rgba(255, 255, 255, 0.55);
    padding: 25px;
    border-radius: 18px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.10);
}

/* Section title */
.title {
    font-size: 36px;
    font-weight: 800;
    color: #1675d1;
    text-align: center;
    margin-bottom: 6px;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    text-align: center;
    color: #245a8f;
}

/* Input style */
.stTextInput > div > input {
    border-radius: 10px !important;
    border: 1px solid #8ec8ff !important;
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

/* Creator card */
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


# -----------------------------
# NAVIGATION
# -----------------------------
menu = st.sidebar.radio(
    "Menu",
    ["Halaman Utama", "Input Jam & Langkah", "Hitung Kalori", "Profil Creator"]
)

# ================================================================
# 🏠 1. HOME PAGE
# ================================================================
if menu == "Halaman Utama":
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>DailySteps</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Catat langkahmu, isi jam yang hilang, dan lihat total kalorimu 💙</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)



# ================================================================
# ⏰ 2. INPUT JAM & LANGKAH
# ================================================================
elif menu == "Input Jam & Langkah":
    st.markdown("<h2 style='color:#1366c6;'>Input Per Jam</h2>", unsafe_allow_html=True)
    st.write("Isi langkah yang tercatat. Jam kosong akan di-*interpolasi otomatis*.")

    jam_list = [f"{h:02d}:00" for h in range(6, 23)]

    langkah_dict = {}

    for jam in jam_list:
        langkah = st.number_input(f"Langkah pada {jam}", min_value=0, max_value=30000, step=10)
        langkah_dict[jam] = langkah

    st.session_state["langkah_per_jam"] = langkah_dict

    st.success("Data langkah berhasil disimpan!")
    


# ================================================================
# 🔥 3. HITUNG KALORI
# ================================================================
elif menu == "Hitung Kalori":
    st.markdown("<h2 style='color:#1366c6;'>Hitung Kalori Harian</h2>", unsafe_allow_html=True)

    if "langkah_per_jam" not in st.session_state:
        st.warning("Isi langkah dulu di menu *Input Jam & Langkah* ya 💙")
    else:
        data = list(st.session_state["langkah_per_jam"].values())
        jam_idx = np.arange(len(data))

        # cari index yang langkahnya 0 → interpolasi
        data = np.array(data, dtype=float)
        missing = np.where(data == 0)[0]

        if len(missing) > 0:
            data_interp = data.copy()
            known = np.where(data != 0)[0]
            data_interp[missing] = np.interp(missing, known, data[known])
        else:
            data_interp = data

        total_langkah = int(np.sum(data_interp))

        # rumus kalori make sense: 0.04 kcal per langkah rata-rata
        total_kalori = round(total_langkah * 0.04, 2)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.write(f"**Total Langkah (setelah interpolasi):** {total_langkah:,}")
        st.write(f"**Estimasi Kalori Terbakar:** {total_kalori} kcal")

        # saran
        if total_kalori < 150:
            st.info("🌤 Kamu butuh lebih banyak bergerak, jalan santai yuk!")
        elif total_kalori < 350:
            st.success("🌿 Aktivitasmu oke! Jangan lupa minum air.")
        else:
            st.success("🔥 Kamu aktif banget hari ini! Jangan lupa istirahat dan makan cukup ya.")
        st.markdown("</div>", unsafe_allow_html=True)



# ================================================================
# 👤 4. PROFILE CREATOR
# ================================================================
elif menu == "Profil Creator":
    st.markdown("<h2 style='color:#1366c6;'>Creator</h2>", unsafe_allow_html=True)

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
