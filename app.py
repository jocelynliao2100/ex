import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ===== Font Setup =====
font_path = "NotoSansTC-Regular.otf"  # Make sure this file exists in your repo
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign displays correctly

# ===== Streamlit UI =====
st.set_page_config(page_title="Daily Post Count Chart", layout="centered")
st.title("📈 Daily Post Count Line Chart")
st.markdown("Please upload a CSV file that includes a column named '發文日期'.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if "發文日期" not in df.columns:
            st.error("❌ Column '發文日期' not found. Please check your file.")
        else:
            # Date conversion and cleaning
            df["發文日期"] = pd.to_datetime(df["發文日期"], errors="coerce")
            df = df.dropna(subset=["發文日期"])

            # Count daily posts
            daily_counts = df["發文日期"].value_counts().sort_index()

            # ===== Plotting =====
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(daily_counts.index, daily_counts.values, marker="o", color="orange")
            ax.set_title("Number of Posts per Day", fontproperties=font_prop)
            ax.set_xlabel("Date", fontproperties=font_prop)
            ax.set_ylabel("Post Count", fontproperties=font_prop)
            plt.xticks(rotation=45, fontproperties=font_prop)
            plt.yticks(fontproperties=font_prop)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("Please upload a CSV file with a column named '發文日期'.")
