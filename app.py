import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ===== 字型設定 =====
# 確保你已將 NotoSansTC-Regular.otf 上傳至 repo 根目錄
font_path = "NotoSansTC-Regular.otf"  # 請確認這個檔案存在於你的 GitHub repo
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示錯誤

# ===== Streamlit UI =====
st.set_page_config(page_title="每日發文數量分析", layout="centered")
st.title("📈 每日發文數量折線圖")
st.markdown("請上傳包含「發文日期」欄位的 CSV 檔案。")

uploaded_file = st.file_uploader("選擇你的 CSV 檔案", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if "發文日期" not in df.columns:
            st.error("❌ 找不到「發文日期」欄位，請確認欄位名稱正確。")
        else:
            # 日期轉換與清洗
            df["發文日期"] = pd.to_datetime(df["發文日期"], errors="coerce")
            df = df.dropna(subset=["發文日期"])

            # 計算每日發文數
            daily_counts = df["發文日期"].value_counts().sort_index()

            # ===== 畫圖 =====
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(daily_counts.index, daily_counts.values, marker="o", color="orange")
            ax.set_title("每日發文數量", fontproperties=font_prop)
            ax.set_xlabel("日期", fontproperties=font_prop)
            ax.set_ylabel("發文數量", fontproperties=font_prop)
            plt.xticks(rotation=45, fontproperties=font_prop)
            plt.yticks(fontproperties=font_prop)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
else:
    st.info("請上傳包含「發文日期」欄位的 CSV 檔案。")
