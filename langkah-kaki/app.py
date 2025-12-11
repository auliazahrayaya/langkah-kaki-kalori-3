import streamlit as st
import numpy as np
import pandas as pd

# =========================
#   AESTHETIC GEN-Z THEME
# =========================
st.set_page_config(page_title="Gen-Z Step Interpolator", layout="wide", page_icon="👟")

genz_css = """
<style>

:root {
    --bg: #0A0F1C;
    --card: rgba(255, 255, 255, 0.08);
    --accent: #A66BFF;
    --accent2: #4ED2F7;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0A0F1C 0%, #111B30 50%, #0A0F1C 100%);
    color: white;
    font-family: 'Inter', sans-serif;
}

/* Cards */
.card {
    background: var(--card);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    transition: 0.25s ease;
}
.card:hover {
    border-color: var(--accent);
    box-shadow: 0px 0px 18px rgba(166,107,255,0.4);
    transform: scale(1.01);
}

/* Title */
.bigtitle {
    font-size: 48px;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.subtle {
    opacity: 0.85;
    text-align: center;
    font-size: 17px;
}

</style>
"""
st.markdown(genz_css, unsafe_allow_html=True)


# ===============================
#          SIDEBAR
# ===============================
menu = st.sidebar.radio("Menu", ["🏠 Home", "⏱️ Input Per-Jam", "🔥 Hitung Kalori", "👥 Profil"])


# ===============================
#            HOME
# ===============================
if menu == "🏠 Home":
    st.markdown("<h1 class='bigtitle'>Gen-Z Step Interpolator 👟</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtle'>Hitung langkah yang hilang, estimasi kalori, dan cek kondisi tubuhmu ✨</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✨ Apa yang bisa dilakukan aplikasi ini?")
    st.write("""
    - Input jumlah langkah **setiap jam**  
    - Jika ada jam yang **lupa dihitung**, sistem akan *interpolasi otomatis*  
    - Menghitung kalori yang terbakar berdasarkan total langkah  
    - Memberikan **saran kesehatan** sesuai kalori yang keluar  
    - Tampilan aesthetic ala Gen-Z (dark neon vibes)  
    """)
    st.markdown("</div>", unsafe_allow_html=True)


# ===============================
#         INPUT PER JAM
# ===============================
elif menu == "⏱️ Input Per-Jam":
    st.markdown("<h1 class='bigtitle'>⏱️ Input Langkah Per Jam</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Masukkan langkah yang kamu hitung setiap jam. Kalau ada jam yang kamu lupa menghitung, biarkan kosong (nanti diinterpolasi).")

    jam_range = list(range(6, 23))   # 06.00 – 22.00
    langkah_dict = {}

    for j in jam_range:
        langkah = st.text_input(f"Jam {j}:00", placeholder="isi atau kosongkan…")
        langkah_dict[j] = langkah

    st.session_state["input_langkah"] = langkah_dict
    st.success("Data jam & langkah tersimpan. Lanjut ke menu **Hitung Kalori**.")
    st.markdown("</div>", unsafe_allow_html=True)


# ===============================
#         HITUNG KALORI
# ===============================
elif menu == "🔥 Hitung Kalori":
    st.markdown("<h1 class='bigtitle'>🔥 Hitung Interpolasi & Kalori</h1>", unsafe_allow_html=True)

    if "input_langkah" not in st.session_state:
        st.warning("Isi dulu langkah per jam di menu **Input Per-Jam**.")
        st.stop()

    data = st.session_state["input_langkah"]
    jam_arr = np.array(list(data.keys()))
    langkah_raw = np.array([None if v=="" else float(v) for v in data.values()])

    # Pisahkan yang diketahui dan tidak
    known_idx = np.where(langkah_raw != None)[0]
    missing_idx = np.where(langkah_raw == None)[0]

    if len(known_idx) < 2:
        st.error("Minimal isi 2 jam berbeda agar interpolasi bisa dilakukan!")
        st.stop()

    # Interpolasi linier untuk nilai yang hilang
    langkah_interp = langkah_raw.copy()
    langkah_interp[missing_idx] = np.interp(
        missing_idx,
        known_idx,
        langkah_raw[known_idx]
    )

    df = pd.DataFrame({
        "Jam": jam_arr,
        "Langkah": langkah_interp.astype(float)
    })

    # Rumus make-sense: 0.04 kcal per langkah
    df["Kalori"] = df["Langkah"] * 0.04
    total_kalori = df["Kalori"].sum()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Interpolasi")
    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔥 Total Kalori yang Terbakar")
    st.markdown(f"### **{total_kalori:.2f} kcal**")

    # =====================
    #     HEALTH ADVICE
    # =====================
    st.subheader("💡 Saran Kesehatan Hari Ini")

    if total_kalori < 150:
        st.write("⚠️ Kamu sangat kurang bergerak hari ini. Luangkan waktu 10 menit untuk stretching.")
    elif total_kalori < 350:
        st.write("✨ Kamu sudah bergerak, tapi masih santai. Jangan lupa minum air!")
    elif total_kalori < 550:
        st.write("🔥 Kamu cukup aktif! Saatnya makan makanan bergizi untuk isi energi lagi.")
    elif total_kalori < 800:
        st.write("💪 Kamu aktif banget! Jangan lupa istirahat sebentar dan hindari overwork.")
    else:
        st.write("🏆 Kamu SUPER aktif hari ini. Wajib istirahat cukup dan makan protein!")

    st.markdown("</div>", unsafe_allow_html=True)


# ===============================
#          PROFIL CREATOR
# ===============================
elif menu == "👥 Profil":
    st.markdown("<h1 class='bigtitle'>👥 Profil Creator</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("👩 Creator 1")
        st.write("""
        **Nama:** ARUM FAJAR R  
        **NIM:** K1323011
        **Prodi:** Pendidikan Matematika
        **Universitas:** Universitas Sebelas Maret (UNS)
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("👩 Creator 2")
        st.write("""
        **Nama:** AULIA ZAHRA
        **NIM:** K1323015
        **Prodi:** Pendidikan Matematika  
        **Universitas:** Universitas Sebelas Maret (UNS) 
        """)
        st.markdown("</div>", unsafe_allow_html=True)
