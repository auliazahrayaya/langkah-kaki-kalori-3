import streamlit as st
import numpy as np
import pandas as pd

# ---------------------
# PAGE CONFIG
# ---------------------
st.set_page_config(
    page_title="Ayo Menghitung Kalori mu dari Langkah Kaki!",
    layout="wide",
    page_icon="✨"
)

# ---------------------
# AESTHETIC CSS
# ---------------------
css = """
<style>
body {
    background: linear-gradient(135deg, #ffdbe6, #e4eaff, #c8fff1);
    background-attachment: fixed;
    font-family: 'Helvetica Neue', sans-serif;
}

.card {
    background: rgba(255,255,255,0.55);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.12);
    transition: 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 12px 30px rgba(0,0,0,0.18);
}

.main-title {
    font-size: 44px;
    text-align: center;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #7f00ff, #e100ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-box {
    background: rgba(255,255,255,0.6);
    padding: 20px;
    border-radius: 15px;
    text-align:center;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ---------------------
# MENU
# ---------------------
menu = st.sidebar.selectbox(
    "✨ Menu",
    ["Home", "Profile Creator"]
)

# =============================
#          HOME PAGE
# =============================
if menu == "Home":
    st.markdown("<h1 class='main-title'>✨ Step Interpolator ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Menghitung langkah & kalori hilang pakai interpolasi yang aesthetic 💗</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 Input Data Harian")

        hours = [f"{h:02d}:00" for h in range(6, 23)]
        selected_hours = st.multiselect("🕒 Pilih jam:", hours, default=["06:00", "09:00", "12:00", "15:00", "18:00"])

        raw_steps = st.text_input("👟 Masukkan langkah (pisah koma, '-' jika lupa):",
                                  "500, 1400, -, 2000, 1500")

        cal_per_step = st.number_input("🔥 Kalori per langkah:",
                                       min_value=0.0, max_value=1.0, value=0.04)

        run = st.button("✨ Jalankan Interpolasi")

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------
    # PROCESSING
    # ----------------------
    if run:
        step_list = [s.strip() for s in raw_steps.split(",")]
        if len(step_list) != len(selected_hours):
            st.error("Jumlah langkah tidak sesuai dengan jumlah jam 😞")
            st.stop()

        parsed_steps = []
        for s in step_list:
            if s in ["", "-", "NaN"]:
                parsed_steps.append(np.nan)
            else:
                parsed_steps.append(float(s))

        hour_num = [int(h.split(":")[0]) for h in selected_hours]

        df = pd.DataFrame({
            "Hour": hour_num,
            "Label": selected_hours,
            "Steps": parsed_steps
        }).sort_values("Hour")

        known_mask = ~np.isnan(df["Steps"])
        if known_mask.sum() < 2:
            st.error("Butuh minimal 2 data untuk interpolasi 😭")
            st.stop()

        full_hours = np.arange(df["Hour"].min(), df["Hour"].max() + 1)
        interp_steps = np.interp(full_hours, df.loc[known_mask, "Hour"], df.loc[known_mask, "Steps"])
        interp_cal = interp_steps * cal_per_step

        result = pd.DataFrame({
            "Hour": full_hours,
            "Label": [f"{h:02d}:00" for h in full_hours],
            "Steps": interp_steps.round(2),
            "Calories": interp_cal.round(2)
        })

        # tampilkan hasil
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🌈 Hasil Interpolasi")
        st.dataframe(result, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Steps", f"{int(result['Steps'].sum()):,}")
        with col2:
            st.metric("Total Calories", f"{result['Calories'].sum():.2f} kcal")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 Grafik")
        st.line_chart(result.set_index("Label")[["Steps", "Calories"]])
        st.markdown("</div>", unsafe_allow_html=True)

# =============================
#       PROFILE CREATOR
# =============================
elif menu == "Profile Creator":
    st.markdown("<h1 class='main-title'>💖 About The Creator 💖</h1>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("✨ Aulia Zahra dan Arum Fajar")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**🎓 Universitas:** (Sebelas Maret)")
            st.write("**📚 Program Studi:** (Pendidikan Matematika)")

        with col2:
            st.write("Email: (auliaazahraa1905@gmail.com)")
            st.write("Instagram: @zahzahra19")

        st.markdown("</div>", unsafe_allow_html=True)
