import streamlit as st
import numpy as np
import pandas as pd

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="DailyStep",
    page_icon="👟",
    layout="wide"
)

# ============================================================
# BABY BLUE AESTHETIC CSS
# ============================================================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #dff1ff 0%, #b8dcff 100%);
    font-family: 'Poppins', sans-serif;
}

.main {
    background: transparent;
}

/* Title */
.title {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    background: -webkit-linear-gradient(#0a66c2, #4da3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: -5px;
}
.subtitle {
    text-align: center;
    font-size: 17px;
    color: #2d5f88;
    margin-top: -12px;
    margin-bottom: 25px;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(80, 150, 255, 0.35);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
    margin-bottom: 18px;
}

/* Profile Card */
.profile {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 22px;
    text-align:center;
    border: 1px solid rgba(120, 170, 255, 0.35);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Input Jam & Langkah", "Hitung Kalori", "Profil Creator"]
)

# ============================================================
# 1. HOME PAGE
# ============================================================
if menu == "Home":
    st.markdown("<p class='title'>DailyStep</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Track langkah harianmu dengan vibe biru elegan 💙</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass" style="text-align:center;">
        <h3 style="color:#0a66c2; font-weight:700;">Selamat datang!</h3>
        <p style="color:#2d5f88; font-size:17px;">
            Masukkan langkahmu tiap jam, biarin aku isi yang hilang pakai interpolasi.<br>
            Lalu aku hitungin kalorinya secara rasional & make sense.
        </p>
        <p style="margin-top:10px; font-size:16px; color:#0f5faa;">
            Ayo mulai dari menu di kiri!
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 2. INPUT JAM & LANGKAH
# ============================================================
elif menu == "Input Jam & Langkah":
    st.markdown("<p class='title'>Input Jam & Langkah</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Pilih jam → masukkan langkah → simpan 💙</p>", unsafe_allow_html=True)

    jam_list = [f"{h:02d}:00" for h in range(6, 25)]  # 06:00 - 24:00

    if "steps" not in st.session_state:
        st.session_state["steps"] = {jam: None for jam in jam_list}

    selected_jam = st.selectbox("Pilih Jam", jam_list)

    langkah = st.number_input(
        f"Langkah pada {selected_jam}",
        min_value=0,
        max_value=50000,
        value=st.session_state["steps"][selected_jam] if st.session_state["steps"][selected_jam] else 0,
        step=10
    )

    if st.button("Simpan Langkah"):
        st.session_state["steps"][selected_jam] = langkah
        st.success(f"Data langkah untuk jam {selected_jam} tersimpan ✔")

    # PROGRESS TABLE
    st.markdown("<br><h4 style='color:#0a66c2;'>Progress Langkah Hari Ini</h4>", unsafe_allow_html=True)

    df = pd.DataFrame({
        "Jam": jam_list,
        "Langkah": [st.session_state["steps"][j] for j in jam_list]
    })

    st.dataframe(df, use_container_width=True)


# ============================================================
# 3. HITUNG KALORI
# ============================================================
elif menu == "Hitung Kalori":
    st.markdown("<p class='title'>Hitung Kalori</p>", unsafe_allow_html=True)

    steps = st.session_state.get("steps", None)

    if steps is None:
        st.warning("Isi langkah dulu ya 💙")
    else:
        df = pd.DataFrame({
            "Jam": jam_list,
            "Langkah": [steps[j] for j in jam_list]
        })

        df["Langkah"] = df["Langkah"].astype(float)

        # Fill missing with interpolation
        df["Interpolasi"] = df["Langkah"].interpolate()

        total_steps = int(df["Interpolasi"].sum())

        # Formula: 1 langkah = ±0.04 kcal (5.000 langkah ≈ 200 kcal)
        calories = round(total_steps * 0.04, 2)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("📊 Hasil Perhitungan")

        st.write(f"Total Langkah (setelah interpolasi): **{total_steps:,}**")
        st.write(f"Estimasi Kalori Terbakar: **{calories} kcal**")

        if calories < 120:
            st.info("💧 Masih rendah… mungkin kamu butuh jalan santai sebentar.")
        elif calories < 300:
            st.success("🌿 Aktivitasmu lumayan baik, lanjutkan ritmenya!")
        else:
            st.success("🔥 Kamu aktif banget hari ini! Jangan lupa hidrasi & istirahat.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#0a66c2;'>Tabel Data</h4>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)


# ============================================================
# 4. PROFIL CREATOR
# ============================================================
elif menu == "Profil Creator":
    st.markdown("<p class='title'>Profil Creator</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='profile'>
            <img src='https://api.dicebear.com/9.x/thumbs/svg?seed=zahra' width='90'>
            <h4 style='color:#0a66c2;'>Aulia Zahra</h4>
            <p>NIM: K13xxxxx <br> Prodi: Pendidikan Matematika <br> Universitas: UNS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='profile'>
            <img src='https://api.dicebear.com/9.x/thumbs/svg?seed=teman' width='90'>
            <h4 style='color:#0a66c2;'>Nama Temanmu</h4>
            <p>NIM: K13xxxxx <br> Prodi: Pendidikan Matematika <br> Universitas: UNS</p>
        </div>
        """, unsafe_allow_html=True)
