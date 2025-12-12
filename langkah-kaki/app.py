import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="DailyStep", page_icon="👟", layout="wide")

# =========================
# CSS — BIRU LANGIT / ESTETIK
# =========================
st.markdown("""
<style>
body {background: linear-gradient(135deg, #d6ecff, #b7dbff); font-family: 'Poppins', sans-serif;}
.title {font-size:42px; font-weight:800; text-align:center; color:#0a4fa3; margin-bottom:-5px;}
.subtitle {text-align:center; font-size:18px; color:#3c6fa8; margin-bottom:25px;}
.hero {background: rgba(255,255,255,0.55); padding:40px; border-radius:26px; backdrop-filter:blur(10px); width:85%; margin:auto; text-align:center; box-shadow:0 8px 20px rgba(0,0,0,0.08);}
.creator-card {background:white; padding:20px; border-radius:18px; text-align:center; width:250px; box-shadow:0px 4px 12px rgba(0,0,0,0.15); margin-bottom:20px;}
.creator-name {font-size:20px; font-weight:bold; color:#0a4fa3;}
.stButton > button {background:#1675d1; color:white; border-radius:12px; padding:10px 22px;}
.stButton > button:hover {background:#0f5faa;}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Input Your Step", "Count Your Calories", "Profile Creator"]
)

# =========================
# HOME PAGE
# =========================
if menu == "Home":
    st.markdown('<p class="title">DailyStep</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Ayo Track Langkah mu! 💙</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero">
        <img src="https://cdn-icons-png.flaticon.com/512/869/869869.png" width="100">
        <h3 style="color:#0a4fa3; font-size:26px; margin-top:10px;">Halo!</h3>
        <p style="color:#3c5f8a; font-size:17px;">Pilih jam dan masukkan langkahmu 😄</p>
        <p style="color:#0a4fa3; font-size:16px; margin-top:10px;">Klik menu sebelah kiri! 💙</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# INPUT YOUR STEP
# =========================
elif menu == "Input Your Step":
    st.markdown('<p class="title">Input Your Step</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Pilih jam → masukkan langkah → simpan 💙</p>', unsafe_allow_html=True)

    jam_list = [f"{h:02d}:00" for h in range(6, 25)]

    if "steps" not in st.session_state:
        st.session_state["steps"] = {jam: None for jam in jam_list}

    selected_jam = st.selectbox("Pilih jam:", jam_list)
    langkah = st.number_input("Masukkan langkah:", 0, 30000, step=10)

    if st.button("Simpan Langkah"):
        st.session_state["steps"][selected_jam] = langkah
        st.success(f"Langkah pada jam {selected_jam} tersimpan!")

    df_display = pd.DataFrame({
        "Jam": jam_list,
        "Langkah": [st.session_state["steps"][j] for j in jam_list]
    })
    st.write("### Langkah per jam")
    st.dataframe(df_display, height=400)

# =========================
# COUNT YOUR CALORIES
# =========================
elif menu == "Count Your Calories":
    st.markdown('<p class="title">Count Your Calories</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Langkah hilang otomatis diisi 💙</p>', unsafe_allow_html=True)

    # Cek apakah user sudah input data
    if "steps" not in st.session_state or all(v is None for v in st.session_state["steps"].values()):
        st.warning("Isi langkahmu dulu di menu 'Input Your Step'.")
        st.stop()

    # Buat dataframe
    df = pd.DataFrame({
        "Jam": [f"{h:02d}:00" for h in range(6, 25)],
        "Langkah": list(st.session_state["steps"].values())
    })

    # Ubah None → NaN supaya bisa diinterpolasi
    df["Langkah"] = df["Langkah"].replace({None: np.nan}).astype(float)

    # Cegah error: kalau semua NaN, interpolasi tidak mungkin dilakukan
    if df["Langkah"].notna().sum() < 2:
        st.error("Minimal butuh 2 data langkah untuk interpolasi.")
        st.stop()

    # Interpolasi linearnya
    df["Interpolated"] = df["Langkah"].interpolate(method="linear")

    # Ambil hanya jam yang awalnya kosong
    missing_filled = df[df["Langkah"].isna()][["Jam", "Interpolated"]]

    if missing_filled.empty:
        st.success("Tidak ada langkah yang hilang hari ini 💙")
    else:
        st.subheader("Langkah hilang yang diisi otomatis")
        st.dataframe(
            missing_filled.rename(columns={"Interpolated": "Langkah (Hasil Interpolasi)"})
        )

    # Hitung langkah terakhir (bukan total)
    last_steps = df["Interpolated"].dropna().iloc[-1]
    calories = round(last_steps * 0.04, 2)

    # BOX Kalori + Saran
    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    st.write(f"**Langkah terakhir (hari ini):** {int(last_steps):,}")
    st.write(f"**Kalori perkiraan:** {calories} kkal")

    if calories < 80:
        st.info("🌥 Kamu kurang bergerak, jalan santai 5 menit yuk 💙")
    elif calories < 200:
        st.success("🌿 Mantap! Aktivitasmu seimbang hari ini 💙")
    else:
        st.success("🔥 Kamu aktif banget hari ini! Jangan lupa minum 💧")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PROFILE CREATOR
# =========================
elif menu == "Profile Creator":
    st.markdown('<p class="title">Profile Creator</p>', unsafe_allow_html=True)
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



