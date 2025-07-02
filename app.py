import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 中文字型設定
font_path = "NotoSansTC-Regular.otf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

st.title("📈 每日發文數量折線圖")

uploaded_file = st.file_uploader("上傳包含『發文日期』欄的 CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "發文日期" not in df.columns:
        st.error("❌ 缺少『發文日期』欄位")
    else:
        df["發文日期"] = pd.to_datetime(df["發文日期"], errors="coerce")
        df = df.dropna(subset=["發文日期"])
        daily = df["發文日期"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily.index, daily.values, marker="o", color="orange")
        ax.set_title("每日發文數量", fontproperties=font_prop)
        ax.set_xlabel("日期", fontproperties=font_prop)
        ax.set_ylabel("發文數量", fontproperties=font_prop)
        plt.xticks(rotation=45, fontproperties=font_prop)
        plt.yticks(fontproperties=font_prop)
        st.pyplot(fig)
