import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Interpolasi Langkah Kaki", page_icon="👟", layout="wide")

st.title("👟 Dashboard Interpolasi Langkah Kaki")
st.write("""
Aplikasi ini melakukan interpolasi linier untuk mengisi **data langkah yang hilang**
berdasarkan waktu. Masukkan beberapa titik waktu & jumlah langkah, dan biarkan
sistem mengisi nilai yang kosong.
""")

st.header("📝 Input Data Langkah Kaki")

# ----------- INPUT MANUAL -----------
with st.form("input_form"):
    st.subheader("Masukkan Data (Jam & Langkah)")

    jam = st.text_input(
        "Contoh format jam: 08:00, 09:00, 10:00, 11:00",
        "08:00, 09:00, 10:00, 11:00"
    )
    langkah = st.text_input(
        "Isi langkah dengan koma. Gunakan 'kosong' atau '-' untuk data hilang.",
        "1000, -, 2500, 4000"
    )

    submitted = st.form_submit_button("Proses Interpolasi")

if submitted:
    # --- Convert input jam ---
    jam_list_raw = [j.strip() for j in jam.split(",")]
    langkah_raw = [l.strip() for l in langkah.split(",")]

    if len(jam_list_raw) != len(langkah_raw):
        st.error("Jumlah jam dan langkah harus sama!")
        st.stop()

    # --- Convert ke numeric ---
    langkah_num = []
    for x in langkah_raw:
        if x in ["-", "", "kosong"]:
            langkah_num.append(np.nan)
        else:
            try:
                langkah_num.append(float(x))
            except:
                langkah_num.append(np.nan)

    # --- Buat DataFrame ---
    df = pd.DataFrame({
        "Jam": jam_list_raw,
        "Langkah": langkah_num
    })

    # --- Interpolasi ---
    df["Interpolasi"] = df["Langkah"].interpolate(method="linear")

    st.subheader("📄 Tabel Hasil Interpolasi")
    st.dataframe(df, use_container_width=True)

    # --- Grafik ---
    st.subheader("📈 Grafik Langkah (Ori + Interpolasi)")

    chart_df = df.reset_index().melt(
        id_vars=["index", "Jam"],
        value_vars=["Langkah", "Interpolasi"],
        var_name="Jenis",
        value_name="Nilai"
    )

    chart = (
        alt.Chart(chart_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Jam:N", title="Waktu"),
            y=alt.Y("Nilai:Q", title="Jumlah Langkah"),
            color="Jenis:N",
            tooltip=["Jam", "Jenis", "Nilai"]
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # --- Fun Animation Message ---
    st.success("🎉 Interpolasi selesai! Nilai kosong berhasil diisi secara akurat.")
else:
    st.info("Masukkan data terlebih dahulu lalu klik *Proses Interpolasi*.")

