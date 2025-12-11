import streamlit as st
import numpy as np
import pandas as pd

# ---------------------------
# GLOBAL: jam list 06:00-24:00
# ---------------------------
jam_list = [f"{h:02d}:00" for h in range(6, 25)]  # 06..24

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="DailyStep", page_icon="💙", layout="wide")

# ================================
# BABY BLUE THEME (CSS)
# ================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #dff4ff 0%, #cfeaff 100%);
    font-family: 'Poppins', sans-serif;
}

/* Titles */
.title {
    font-size: 36px;
    font-weight: 800;
    text-align: center;
    color: #0b66b2;
    margin-bottom: -6px;
}
.subtitle {
    text-align: center;
    color: #2e5f86;
    margin-bottom: 20px;
}

/* glass card */
.glass {
    background: rgba(255,255,255,0.60);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(120,170,255,0.35);
    box-shadow: 0 6px 22px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

/* jam row */
.jam-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
    background: white;
    border-radius: 12px;
    margin-bottom: 8px;
    border-left: 5px solid #1675d1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.profile {
    background: rgba(255,255,255,0.6);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(120,170,255,0.35);
}

.stButton>button {
    background-color: #1675d1;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ================================
# SIDEBAR NAVIGATION (labels exact)
# ================================
menu = st.sidebar.radio("Menu", ["Home", "Input Jam & Langkah", "Hitung Kalori", "Profil Creator"])

# ------------------------------
# Initialize session state store
# ------------------------------
if "steps" not in st.session_state:
    # None = missing, will be interpolated
    st.session_state["steps"] = {jam: None for jam in jam_list}

# ================================
# 1) HOME
# ================================
if menu == "Home":
    st.markdown("<div class='title'>DailyStep</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Track langkah harianmu — baby blue aesthetic</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<img src='https://cdn-icons-png.flaticon.com/512/1077/1077114.png' width='90' style='opacity:0.95;margin-bottom:10px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#0b66b2; margin-bottom:6px;'>Selamat datang</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#2e5f86; margin-top:0px;'>Pilih menu <b>Input Jam & Langkah</b> untuk mulai, lalu cek <b>Hitung Kalori</b>.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ================================
# 2) INPUT JAM & LANGKAH (selectbox scroll)
# ================================
elif menu == "Input Jam & Langkah":
    st.markdown("<div class='title'>Input Jam & Langkah</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Pilih jam (scroll) — masukkan langkah — klik Simpan</div>", unsafe_allow_html=True)

    # left: selectbox + input, right: progress table
    left, right = st.columns([1, 1])

    with left:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        selected = st.selectbox("Pilih Jam", jam_list, index=0)
        # show current stored (None -> 0 placeholder), but we keep None when saving 0
        current_val = st.session_state["steps"].get(selected)
        default_value = 0 if (current_val is None) else int(current_val)
        langkah = st.number_input(f"Langkah pada {selected}", min_value=0, max_value=50000, value=default_value, step=10)
        if st.button("Simpan Langkah"):
            # treat 0 as missing (None) — avoids accidental zero entries being treated as real
            if langkah == 0:
                st.session_state["steps"][selected] = None
                st.success(f"Langkah untuk {selected} disimpan sebagai kosong (akan diinterpolasi).")
            else:
                st.session_state["steps"][selected] = int(langkah)
                st.success(f"Langkah untuk {selected} = {int(langkah)} tersimpan.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("<b style='color:#0b66b2;'>Progress Langkah Hari Ini</b>", unsafe_allow_html=True)

        preview_df = pd.DataFrame({
            "Jam": jam_list,
            "Langkah (input)": [("" if st.session_state["steps"][j] is None else st.session_state["steps"][j]) for j in jam_list]
        })
        st.dataframe(preview_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ================================
# 3) HITUNG KALORI (INTERPOLASI BENAR)
# ================================
elif menu == "Hitung Kalori":
    st.markdown("<div class='title'>Hitung Kalori</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Interpolasi langkah yang hilang — hitung kalori per jam & total</div>", unsafe_allow_html=True)

    steps_dict = st.session_state.get("steps", None)
    if steps_dict is None:
        st.warning("Belum ada data. Isi di menu Input Jam & Langkah.")
    else:
        # build dataframe
        df = pd.DataFrame({
            "Jam": jam_list,
            "Langkah_input": [steps_dict[j] for j in jam_list]
        })

        # Convert to float and mark missing as NaN
        df["Langkah_num"] = df["Langkah_input"].apply(lambda x: np.nan if x is None else float(x))

        # Check number of known points
        known_mask = ~df["Langkah_num"].isna()
        known_count = known_mask.sum()

        if known_count == 0:
            st.error("Belum ada jam yang diisi. Isi minimal 1 jam agar interpolasi bisa dilakukan.")
        elif known_count == 1:
            # With only 1 known point, fill all with that value (logical fallback)
            single_val = float(df.loc[known_mask, "Langkah_num"].iloc[0])
            df["Langkah_interpolated"] = single_val
        else:
            # Linear interpolation across index (hour positions)
            df["Langkah_interpolated"] = df["Langkah_num"].interpolate(method="linear")
            # fill edges (leading/trailing NaN) with nearest valid (forward/backward fill)
            df["Langkah_interpolated"] = df["Langkah_interpolated"].fillna(method="bfill").fillna(method="ffill")

        # Ensure numeric int for display
        df["Langkah_interpolated"] = df["Langkah_interpolated"].round(0).astype(int)

        # CALORIE: per hour
        # Use standard conversion: 1 step ≈ 0.04 kcal
        df["Kalori_per_jam"] = (df["Langkah_interpolated"] * 0.04).round(2)

        total_steps = int(df["Langkah_interpolated"].sum())
        total_kalori = float(df["Kalori_per_jam"].sum().round(2))

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("Hasil Interpolasi & Kalori")
        st.write(f"Total langkah (hasil interpolasi): **{total_steps:,} langkah**")
        st.write(f"Total kalori (hasil per-jam): **{total_kalori} kcal**")
        st.markdown("</div>", unsafe_allow_html=True)

        # Health advice based on total_kalori
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("Saran Kesehatan")
        if total_kalori < 100:
            st.info("Kurang gerak—coba jalan santai 10-15 menit dan makan yang bergizi.")
        elif total_kalori < 250:
            st.success("Cukup aktif — pertahankan. Perhatikan asupan karbohidrat sehat.")
        elif total_kalori < 400:
            st.success("Aktif banget — istirahat yang cukup dan konsumsi protein.")
        else:
            st.warning("Sangat aktif — pastikan hidrasi, istirahat, dan pemulihan yang cukup.")
        st.markdown("</div>", unsafe_allow_html=True)

        # show per-hour table
        st.markdown("<h4 style='color:#0b66b2;'>Rincian per jam</h4>", unsafe_allow_html=True)
        display_df = df[["Jam", "Langkah_input", "Langkah_interpolated", "Kalori_per_jam"]].copy()
        display_df = display_df.rename(columns={
            "Langkah_input": "Langkah (input)",
            "Langkah_interpolated": "Langkah (interp)",
            "Kalori_per_jam": "Kalori (kcal)"
        })
        st.dataframe(display_df, use_container_width=True)


# ================================
# 4) PROFIL CREATOR
# ================================
elif menu == "Profil Creator":
    st.markdown("<div class='title'>Creator</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Informasi pembuat</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='profile'>", unsafe_allow_html=True)
        st.image("https://api.dicebear.com/9.x/thumbs/svg?seed=zahra", width=90)
        st.markdown("<div class='creator-name'>Aulia Zahra</div>", unsafe_allow_html=True)
        st.markdown("<div> NIM: K1323015<br>Prodi: Pendidikan Matematika<br>UNS</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='profile'>", unsafe_allow_html=True)
        st.image("https://api.dicebear.com/9.x/thumbs/svg?seed=arum", width=90)
        st.markdown("<div class='creator-name'>Arum Fajar R</div>", unsafe_allow_html=True)
        st.markdown("<div> NIM: K1323011<br>Prodi: Pendidikan Matematika<br>UNS</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
