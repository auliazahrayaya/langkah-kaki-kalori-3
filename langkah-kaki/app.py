import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------------- STYLING ----------------------
st.set_page_config(page_title="DailyStep", layout="centered")

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0d0f1a;
}
h1, h2, h3, p, label {
    color: #e8eaff !important;
    font-family: 'Poppins', sans-serif;
}
.big-title {
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(90deg, #6a5cff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    padding: 20px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    box-shadow: 0px 0px 20px rgba(100,100,255,0.15);
    margin-bottom: 20px;
}
button, .stButton>button {
    background: linear-gradient(90deg, #6a5cff, #00d4ff) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


# ---------------------- SIDEBAR MENU ----------------------
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Input Langkah", "Hasil Perhitungan", "Profile Creator"],
    index=0
)

# Storage untuk antar menu
if "steps" not in st.session_state:
    st.session_state.steps = {}


# ---------------------- HOME ----------------------
if menu == "Home":
    st.markdown("<h1 class='big-title'>DailyStep</h1>", unsafe_allow_html=True)
    st.write("Aplikasi sederhana untuk mencatat langkah harian, mengisi data yang hilang, dan menghitung kalori.")
    st.write("")
    st.write("Mulai catat langkahmu ✨")


# ---------------------- INPUT LANGKAH ----------------------
elif menu == "Input Langkah":
    st.markdown("<h2>Input Langkah Per Jam</h2>", unsafe_allow_html=True)

    st.write("Isi jumlah langkah pada jam tertentu. Kosongkan jika lupa — sistem akan mengisi otomatis.")

    steps = {}
    hours = [f"{h:02}:00" for h in range(6, 22)]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for h in hours:
        val = st.number_input(f"Jam {h}", min_value=0, max_value=30000, step=100, key=h)
        steps[h] = None if val == 0 else val
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Simpan Data"):
        st.session_state.steps = steps
        st.success("Data berhasil disimpan! Lanjut ke 'Hasil Perhitungan'.")


# ---------------------- HASIL PERHITUNGAN ----------------------
elif menu == "Hasil Perhitungan":
    st.markdown("<h2>Hasil Perhitungan</h2>", unsafe_allow_html=True)

    if not st.session_state.steps:
        st.warning("Belum ada data. Isi dulu menu 'Input Langkah'.")
    else:
        steps = st.session_state.steps.copy()

        # Convert to series for interpolation
        s = pd.Series(steps)
        s = s.replace({None: np.nan})
        s_inter = s.interpolate(method="linear").fillna(method="bfill").fillna(method="ffill")

        total_steps = int(s_inter.sum())
        calories = round(total_steps * 0.04, 2)  # 0.04 kcal per langkah (standar)

        # Display
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Total Langkah Hari Ini", f"{total_steps:,}")
        st.metric("Estimasi Kalori Terbakar", f"{calories} kcal")
        st.markdown("</div>", unsafe_allow_html=True)

        # Simple Recommendation
        rec = ""
        if calories < 100:
            rec = "Tubuhmu butuh lebih banyak bergerak hari ini."
        elif calories < 250:
            rec = "Lumayan! Jalan sedikit lagi biar lebih aktif."
        elif calories < 400:
            rec = "Keren! Aktivitasmu cukup sehat hari ini."
        else:
            rec = "Bagus banget! Jangan lupa minum air dan istirahat."

        st.info(rec)

        # Graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=s_inter.index,
            y=s_inter.values,
            mode="lines+markers",
            line=dict(width=3),
        ))
        fig.update_layout(
            paper_bgcolor="#0d0f1a",
            plot_bgcolor="#0d0f1a",
            font=dict(color="white"),
            title="Grafik Langkah per Jam (Interpolasi Otomatis)"
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------- PROFILE CREATOR ----------------------
elif menu == "Profile Creator":
    st.markdown("<h2>Profile Creator</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Aulia Zahra")
        st.write("NIM: 123456789")  
        st.write("Prodi: Teknik Industri")
        st.write("Universitas: Nama Kampus")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Teman Zahra")
        st.write("NIM: 987654321")
        st.write("Prodi: Teknik Industri")
        st.write("Universitas: Nama Kampus")
        st.markdown("</div>", unsafe_allow_html=True)
