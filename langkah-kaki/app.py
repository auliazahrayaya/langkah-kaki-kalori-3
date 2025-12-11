import streamlit as st
import numpy as np
import pandas as pd

# ----------- AESTHETIC BLUE THEME -----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #b3d9ff, #e6f2ff);
}

.title {
    text-align:center;
    color:#0b63c5;
    font-size:48px;
    font-weight:800;
    margin-top:-20px;
}

.subtitle {
    text-align:center;
    color:#084c8d;
    font-size:20px;
    margin-top:-20px;
}

.glass {
    background: rgba(255,255,255,0.45);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.1);
    backdrop-filter: blur(8px);
    margin-top:20px;
}

.btn {
    background-color:#0b63c5 !important;
    color:white !important;
    border-radius:10px !important;
}
</style>
""", unsafe_allow_html=True)

# ----------- MENU ----------
menu = st.sidebar.selectbox("Menu", ["Home", "Input Langkah per Jam", "Profil Pembuat"])

# ----------- HOME PAGE ----------
if menu == "Home":
    st.markdown('<p class="title">DailyStep</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Tracking langkah harian dengan tampilan biru yang calming 💙</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass" style="text-align:center;">
        <h3 style="color:#0b63c5; font-weight:700;">Selamat datang!</h3>
        <p style="color:#0d4d80; font-size:17px;">
            Masukkan data langkah di jam tertentu,<br>
            dan biarkan interpolasi mengisi langkah yang hilang ✨<br>
            Total kalori dihitung otomatis dan tampil lebih rapi.
        </p>
        <p style="color:#0b63c5; margin-top:12px;">
            Mulai dari menu "Input Langkah per Jam" di sebelah kiri 💙
        </p>
    </div>
    """, unsafe_allow_html=True)


# ----------- INPUT LANGKAH PER JAM ----------
elif menu == "Input Langkah per Jam":
    st.markdown('<p class="title" style="font-size:40px;">Input Langkah</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("Isi langkah berdasarkan jam")

    # List jam otomatis 24 jam
    jam_list = [f"{i:02d}:00" for i in range(24)]

    # User memilih jam
    jam = st.selectbox("Pilih Jam", jam_list)

    langkah = st.number_input(
        f"Jumlah langkah di jam {jam}",
        min_value=0,
        value=0
    )

    if "data" not in st.session_state:
        st.session_state.data = {}

    if st.button("Simpan Langkah", type="primary"):
        st.session_state.data[jam] = langkah
        st.success(f"Langkah untuk jam {jam} berhasil disimpan!")

    st.divider()

    st.subheader("Data Langkah yang Sudah Diinput")
    if st.session_state.data:
        df = pd.DataFrame(
            {"Jam": list(st.session_state.data.keys()),
             "Langkah": list(st.session_state.data.values())}
        ).sort_values("Jam")

        st.dataframe(df, use_container_width=True)

        # Interpolasi
        full_df = pd.DataFrame({"Jam": jam_list})
        full_df["Langkah"] = full_df["Jam"].map(st.session_state.data)
        full_df["Langkah"] = full_df["Langkah"].astype("float")
        full_df["Langkah"] = full_df["Langkah"].interpolate()

        total_kalori = full_df["Langkah"].sum() * 0.04

        st.subheader("Total Kalori Harian")
        st.write(f"🔥 **{total_kalori:.2f} kalori**")

        if total_kalori < 150:
            st.info("Kamu butuh sedikit gerak lagi hari ini 💙")
        elif total_kalori < 400:
            st.success("Cukup aktif! Tetap jaga pola makan ya 🫶")
        else:
            st.warning("Kamu sangat aktif! Jangan lupa istirahat yang cukup 💙")

    else:
        st.info("Belum ada data tersimpan.")

    st.markdown("</div>", unsafe_allow_html=True)


# ----------- PROFIL ----------
elif menu == "Profil Pembuat":
    st.markdown('<p class="title" style="font-size:40px;">Creator</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">

        <div style="display:flex; gap:25px; justify-content:center; margin-top:20px;">

            <div style="background:white; padding:18px; border-radius:15px; width:40%; 
                        text-align:center; box-shadow:0 3px 12px rgba(0,0,0,0.1);">
                <h4 style="color:#0b63c5; margin-bottom:8px;">Aulia Zahra</h4>
                <p style="margin:0; color:#0d4d80;">NIM : K1323015</p>
                <p style="margin:0; color:#0d4d80;">Prodi : Pendidikan Matematika</p>
                <p style="margin:0; color:#0d4d80;">Universitas : UNS</p>
            </div>

            <div style="background:white; padding:18px; border-radius:15px; width:40%; 
                        text-align:center; box-shadow:0 3px 12px rgba(0,0,0,0.1);">
                <h4 style="color:#0b63c5; margin-bottom:8px;">Arum Fajar R</h4>
                <p style="margin:0; color:#0d4d80;">NIM : K1323011</p>
                <p style="margin:0; color:#0d4d80;">Prodi : Pendidikan Matematika</p>
                <p style="margin:0; color:#0d4d80;">Universitas : UNS</p>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)
