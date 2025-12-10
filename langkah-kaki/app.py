import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Fitness Dashboard – Interpolasi Kalori",
    page_icon="🔥",
    layout="wide"
)

# ============================
# CUSTOM STYLE (AESTHETIC)
# ============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #3A0CA3, #7209B7);
    color: white;
}
.sidebar .sidebar-content {
    background: #240046;
}
.big-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    color: #4CC9F0;
}
.metric-card {
    background: #4CC9F022;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# SIDEBAR NAVIGATION
# ============================
menu = st.sidebar.radio("Navigasi", ["🏠 Home", "📝 Input Data", "📊 Grafik", "🔍 Insight"])

# -----------------------------
# PAGE 1 — HOME
# -----------------------------
if menu == "🏠 Home":
    st.markdown("<h1 class='big-title'>🔥 Fitness Dashboard – Interpolasi Kalori</h1>", unsafe_allow_html=True)

    st.write("### Selamat datang di dashboard fitness modern berbasis interpolasi!")
    st.write("""
    Aplikasi ini digunakan untuk:
    - Mendeteksi data langkah/kalori yang hilang
    - Mengisi nilai kosong secara otomatis dengan interpolasi linier
    - Menampilkan dashboard keren untuk presentasi
    """)

    st.image("https://i.gifer.com/7QEa.gif", width=350)  # GIF aesthetic

# -----------------------------
# PAGE 2 — INPUT DATA
# -----------------------------
elif menu == "📝 Input Data":

    st.header("📝 Input Data Langkah & Kalori")

    with st.form("input_form"):
        jam = st.text_input("Jam (pisahkan dengan koma)", "08:00, 09:00, 10:00, 11:00")
        langkah = st.text_input("Langkah (gunakan '-' untuk data hilang)", "1200, -, 3000, -")
        kalori = st.text_input("Kalori (gunakan '-' untuk data hilang)", "50, -, 120, -")

        submitted = st.form_submit_button("Proses Data")

    if submitted:
        jam_list = [j.strip() for j in jam.split(",")]
        langkah_raw = [l.strip() for l in langkah.split(",")]
        kalori_raw = [k.strip() for k in kalori.split(",")]

        def convert(x):
            if x in ["-", "", "none", "null"]:
                return np.nan
            try:
                return float(x)
            except:
                return np.nan

        langkah_num = [convert(x) for x in langkah_raw]
        kalori_num = [convert(x) for x in kalori_raw]

        df = pd.DataFrame({
            "Jam": jam_list,
            "Langkah": langkah_num,
            "Kalori": kalori_num
        })

        df["Langkah Interpolasi"] = df["Langkah"].interpolate()
        df["Kalori Interpolasi"] = df["Kalori"].interpolate()

        st.session_state["data"] = df

        st.success("Data berhasil diproses! Lanjut ke menu **Grafik**.")

# -----------------------------
# PAGE 3 — GRAFIK
# -----------------------------
elif menu == "📊 Grafik":

    if "data" not in st.session_state:
        st.error("Masukkan data dulu di menu Input Data.")
    else:
        df = st.session_state["data"]

        st.header("📊 Grafik Interpolasi Langkah & Kalori")

        melted = df.melt(
            id_vars="Jam",
            value_vars=["Langkah", "Langkah Interpolasi", "Kalori", "Kalori Interpolasi"],
            var_name="Jenis",
            value_name="Nilai"
        )

        chart = (
            alt.Chart(melted)
            .mark_line(point=True)
            .encode(
                x="Jam:N",
                y="Nilai:Q",
                color="Jenis:N",
                tooltip=["Jam", "Jenis", "Nilai"]
            )
            .properties(height=400)
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)

# -----------------------------
# PAGE 4 — INSIGHT
# -----------------------------
elif menu == "🔍 Insight":

    if "data" not in st.session_state:
        st.error("Masukkan data dulu di menu Input Data.")
    else:
        df = st.session_state["data"]

        st.header("🔍 Analisis & Insight")

        col1, col2, col3 = st.columns(3)

        col1.markdown("<div class='metric-card'><h3>Total Langkah</h3><h2>" +
                      str(int(df['Langkah Interpolasi'].sum())) + "</h2></div>", unsafe_allow_html=True)

        col2.markdown("<div class='metric-card'><h3>Total Kalori</h3><h2>" +
                      str(int(df['Kalori Interpolasi'].sum())) + "</h2></div>", unsafe_allow_html=True)

        missing = df["Kalori"].isna().sum()
        col3.markdown(f"<div class='metric-card'><h3>Data Hilang</h3><h2>{missing}</h2></div>", unsafe_allow_html=True)

        st.write("### Insight Otomatis")
        st.write("- Jam paling aktif: **{}**".format(df.loc[df["Langkah Interpolasi"].idxmax(), "Jam"]))
        st.write("- Pola kalori meningkat seiring jumlah langkah.")
        st.write("- Interpolasi mengisi data hilang dengan mulus.")

