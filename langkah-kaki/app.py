# app.py (robust, tolerant, aesthetic-lite)
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Step → Calorie Interpolator", layout="wide")

# Header
st.markdown(
    "<h1 style='text-align:center;color:#2d2d80;'>👟 Step & Calorie Interpolator</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center;color:#666;'>Isi jam & langkah — aplikasi akan mengisi nilai yang hilang menggunakan interpolasi linear.</p>", unsafe_allow_html=True)
st.write("")

# --- Safe multiselect creation helper ---
def safe_multiselect(label, options, default=None, key=None):
    # ensure options are strings
    opts = [str(o) for o in options]
    # make default only those that exist in opts
    if default is None:
        safe_def = []
    else:
        safe_def = [str(d) for d in default if str(d) in opts]
    return st.multiselect(label, opts, default=safe_def, key=key)

# --- INPUT: pick hours + enter steps ---
st.subheader("Input Data (manual, no file)")

# Build options for hours 06:00..22:00
hour_options = [f"{h:02d}:00" for h in range(6, 23)]

# Use safe multiselect (will not crash if default mismatch)
chosen_hours = safe_multiselect("Pilih jam:", hour_options, default=["06:00","09:00","12:00","15:00","18:00"], key="hours")

# If user didn't select, show info
if not chosen_hours:
    st.info("Pilih minimal dua jam agar interpolasi dapat dilakukan.")
# Input steps as comma-separated aligned with selected hours
steps_input = st.text_input("Masukkan langkah sesuai urutan jam yang dipilih (pisahkan koma). Gunakan '-' atau kosong untuk missing.", "500, 1200, 2000, -, 1800")

# calories per step
cals_per_step = st.number_input("Kalori per langkah (kcal)", value=0.04, min_value=0.0, step=0.01)

run = st.button("Proses Interpolasi")

# When run, validate and process
if run:
    # validate chosen_hours length vs steps input count
    hours = chosen_hours
    steps_raw = [p.strip() for p in steps_input.split(",")]
    # If user provided fewer/more step values than selected hours, fail gracefully
    if len(steps_raw) != len(hours):
        st.error(f"Jumlah nilai langkah ({len(steps_raw)}) harus sama dengan jumlah jam yang dipilih ({len(hours)}).")
    else:
        # parse steps to floats or NaN
        steps_vals = []
        for s in steps_raw:
            if s in ("", "-", "nan", "None"):
                steps_vals.append(np.nan)
            else:
                try:
                    steps_vals.append(float(s))
                except:
                    st.error(f"Format langkah tidak valid: '{s}' (harus angka atau '-' untuk kosong)")
                    st.stop()

        # Build DataFrame (hour numeric for interp)
        hour_nums = [int(h.split(":")[0]) for h in hours]
        df = pd.DataFrame({"HourLabel": hours, "Hour": hour_nums, "Steps": steps_vals})
        df = df.sort_values("Hour").reset_index(drop=True)

        # need at least 2 known points to interpolate
        known_mask = ~np.isnan(df["Steps"])
        if known_mask.sum() < 2:
            st.error("Perlu minimal 2 nilai langkah yang terisi untuk melakukan interpolasi.")
        else:
            # full integer hour range between min and max selected hour
            hmin = int(df["Hour"].min())
            hmax = int(df["Hour"].max())
            full_hours = np.arange(hmin, hmax + 1)

            known_x = df.loc[known_mask, "Hour"].values
            known_y = df.loc[known_mask, "Steps"].values

            # np.interp is robust and fast
            interp_steps = np.interp(full_hours, known_x, known_y)
            interp_cal = interp_steps * cals_per_step

            # prepare result dataframe
            result = pd.DataFrame({
                "Hour": full_hours,
                "HourLabel": [f"{h:02d}:00" for h in full_hours],
                "Steps_interpolated": np.round(interp_steps, 2),
                "Calories_interpolated": np.round(interp_cal, 2)
            })

            # show original + interpolated alignment
            st.subheader("Hasil (interpolasi pada rentang jam yang dipilih)")
            st.dataframe(result, use_container_width=True)

            # summaries
            st.subheader("Ringkasan")
            total_steps = int(result["Steps_interpolated"].sum())
            total_cal = float(result["Calories_interpolated"].sum())
            c1, c2 = st.columns(2)
            c1.metric("Total Steps (interpolated)", f"{total_steps:,}")
            c2.metric("Total Calories (interpolated)", f"{total_cal:.2f} kcal")

            # simple line charts (native)
            st.subheader("Grafik")
            st.line_chart(result.set_index("HourLabel")[["Steps_interpolated", "Calories_interpolated"]])

            st.success("Interpolasi selesai ✅")
