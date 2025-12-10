import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Step & Calorie Dashboard",
    page_icon="👟",
    layout="wide"
)

# ------------------ CSS AESTHETIC ------------------
st.markdown("""
<style>
    .bg {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: radial-gradient(circle at top left, #6a5af950, transparent),
                    radial-gradient(circle at bottom right, #ff77e960, transparent);
        z-index: -1;
    }
    .title {
        font-size: 42px; 
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg,#6a5af9,#ff77e9);
        -webkit-background-clip: text;
        color: transparent;
        margin-top: 20px;
        margin-bottom: -10px;
    }
    .sub {
        text-align:center;
        color:#bbb;
        margin-bottom: 30px;
    }
    .card {
        padding: 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(12px);
        transition: 0.25s;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.25);
    }
</style>
<div class='bg'></div>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR MENU ------------------
menu = st.sidebar.radio(
    "Menu",
    ["🏠 Home", "📝 Input Langkah", "📈 Interpolasi"]
)

# ------------------ HOME PAGE ------------------
if menu == "🏠 Home":
    st.markdown("<h1 class='title'>Step & Calorie Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>Aplikasi interpolasi data hilang • tracking langkah • estimasi kalori</p>", unsafe_allow_html=True)

    st.image(
        "https://i.pinimg.com/originals/70/21/ae/7021ae9d635a6e28f29d135fea4b8c61.gif",
        use_column_width=True
    )

    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown("<div class='card'><b>Input Langkah Manual</b><br>Tambah data sesuai jam</div>", unsafe_allow_html=True)
    with c2: 
        st.markdown("<div class='card'><b>Hitung Kalori</b><br>Estimasi otomatis</div>", unsafe_allow_html=True)
    with c3: 
        st.markdown("<div class='card'><b>Interpolasi</b><br>Mengisi data langkah yang hilang</div>", unsafe_allow_html=True)

# ------------------ INPUT PAGE ------------------
if menu == "📝 Input Langkah":

    st.markdown("### 📝 Input Data Langkah & Kalori")

    # Inisialisasi session_state
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=["Jam", "Langkah", "Kalori"])

    jam = st.time_input("Jam")
    langkah = st.number_input("Jumlah Langkah", min_value=0)
    kalori = langkah * 0.04   # estimasi sederhana

    if st.button("Tambah Data"):
        new_row = {"Jam": str(jam), "Langkah": langkah, "Kalori": kalori}
        st.session_state.data.loc[len(st.session_state.data)] = new_row
        st.success("Data berhasil ditambahkan!")

    st.write("### 📄 Data Kamu")
    st.dataframe(st.session_state.data)

    if not st.session_state.data.empty:
        fig = px.line(
            st.session_state.data,
            x="Jam",
            y="Langkah",
            markers=True,
            title="Grafik Langkah"
        )
        st.plotly_chart(fig, use_container_width=True)

# ------------------ INTERPOLASI PAGE ------------------
if menu == "📈 Interpolasi":

    st.markdown("## 📈 Interpolasi Data Langkah Hilang")

    if st.session_state.data.empty:
        st.warning("Data masih kosong. Masukkan data dulu di menu Input.")
    else:
        df = st.session_state.data.copy()
        df["Jam"] = pd.to_datetime(df["Jam"])
        df = df.sort_values("Jam")

        # ubah jam menjadi menit supaya bisa diinterpolasi
        df["Menit"] = df["Jam"].dt.hour * 60 + df["Jam"].dt.minute

        df_inter = df[["Menit", "Langkah"]].set_index("Menit")
        df_inter = df_inter.interpolate(method="linear")

        # hasil interpolasi utk kalori
        df_inter["Kalori"] = df_inter["Langkah"] * 0.04

        st.write("### 🔍 Hasil Interpolasi")
        st.dataframe(df_inter)

        fig2 = px.line(
            df_inter,
            y="Langkah",
            title="Grafik Interpolasi Langkah",
            markers=True
        )
        st.plotly_chart(fig2, use_container_width=True)
