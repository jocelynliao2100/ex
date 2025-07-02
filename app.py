import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

st.set_page_config(page_title="每日發文數量分析", layout="centered")

st.title("📈 每日發文數量折線圖")
st.markdown("請上傳包含「發文日期」欄位的 CSV 檔案。")

# 設定 matplotlib 支援中文字型
plt.rcParams["font.sans-serif"] = ["Taipei Sans TC Beta", "Microsoft JhengHei", "Heiti TC", "Arial Unicode MS", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 避免負號顯示錯誤

# 上傳 CSV 檔案
uploaded_file = st.file_uploader("選擇你的 CSV 檔案", type=["csv"])

if uploaded_file:
    try:
        # 讀取 CSV
        df = pd.read_csv(uploaded_file)

        # 檢查必要欄位
        if "發文日期" not in df.columns:
            st.error("❌ 找不到名為「發文日期」的欄位，請確認欄位名稱是否正確。")
        else:
            # 日期處理
            df["發文日期"] = pd.to_datetime(df["發文日期"], errors="coerce")
            df = df.dropna(subset=["發文日期"])
            daily_counts = df["發文日期"].value_counts().sort_index()

            # 畫圖
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(daily_counts.index, daily_counts.values, marker='o', color='orange')
            ax.set_title("每日發文數量", fontsize=16)
            ax.set_xlabel("日期")
            ax.set_ylabel("發文數量")
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
else:
    st.info("請上傳包含「發文日期」欄位的 CSV 檔案。")
