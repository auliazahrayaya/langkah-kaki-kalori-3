import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Interpolasi Langkah & Kalori", page_icon="👟", layout="wide")

st.title("👟 Dashboard Interpolasi Langkah Kaki & Kalori")
st.write("""
Aplikasi ini membaca data langkah & kalori, mendeteksi nilai yang hilang,
dan mengisi kekosongan tersebut menggunakan **Interpolasi Linier**.
""")

# -------------------------
# UPLOAD FILE
# -------------------------
uploaded = st.file_uploader("Upload file CSV (wajib ada kolom langkah & kalori)", type=["csv"])

def detect_columns(df):
    # Normalisasi kolom
    colmap = {c.lower().replace(" ", ""): c for c in df.columns}

    steps = None
    calories = None

    # Nama umum
    for k, v in colmap.items():
        if k in ["steps", "stepstotal", "stepcount", "stepscount"]:
            steps = v
        if k in ["calories", "kcal", "caloriestotal"]:
            calories = v

    return steps, calories


def interpolate_series(s):
    return s.astype(float).interpolate(method="linear", limit_direction="both")


if uploaded:

    # -------------------------
    # LOAD DATA
    # -------------------------
    try:
        df = pd.read_csv(uploaded)
    except:
        st.error("File tidak bisa dibaca. Pastikan format CSV benar.")
        st.stop()

    st.subheader("📄 Preview Data")
    st.dataframe(df.head(), use_container_width=True)

    # -------------------------
    # DETEKSI KOLOM
    # -------------------------
    step_col, cal_col = detect_columns(df)

    if step_col is None or cal_col is None:
        st.error("Kolom langkah atau kalori tidak ditemukan. Pastikan CSV ada kolom 'steps' dan 'calories'.")
        st.stop()

    st.success(f"Kolom terdeteksi → Steps: **{step_col}**, Calories: **{cal_col}**")

    # -------------------------
    # INTERPOLASI
    # -------------------------
    df["_steps_interp"] = interpolate_series(df[step_col])
    df["_cal_interp"] = interpolate_series(df[cal_col])

    # Summary missing
    st.subheader("📊 Ringkasan Missing Value")
    col1, col2 = st.columns(2)
    col1.metric("Missing Steps", int(df[step_col].isna().sum()))
    col2.metric("Missing Calories", int(df[cal_col].isna().sum()))

    # -------------------------
    # GRAFIK 1 — Steps ori vs interpolasi
    # -------------------------
    st.subheader("📈 Grafik Steps (Original vs Interpolated)")

    chart_df = df[["_steps_interp", step_col]].reset_index().melt(id_vars="index",
                                                                  var_name="Jenis",
                                                                  value_name="Nilai")

    chart = (
        alt.Chart(chart_df)
        .mark_line()
        .encode(
            x="index:Q",
            y="Nilai:Q",
            color="Jenis:N",
            tooltip=["index", "Jenis", "Nilai"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

    # -------------------------
    # GRAFIK 2 — Steps vs Calories (interpolated)
    # -------------------------
    st.subheader("🔥 Hubungan Steps & Calories (Interpolated)")

    scatter = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x="_steps_interp:Q",
            y="_cal_interp:Q",
            tooltip=[step_col, cal_col, "_steps_interp", "_cal_interp"]
        )
        .interactive()
    )
    st.altair_chart(scatter, use_container_width=True)

    # -------------------------
    # DOWNLOAD HASIL
    # -------------------------
    st.subheader("📥 Download Hasil Interpolasi")
    out = df.copy()
    st.download_button(
        label="Download CSV",
        data=out.to_csv(index=False).encode("utf-8"),
        file_name="hasil_interpolasi.csv",
        mime="text/csv"
    )
