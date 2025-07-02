
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import jieba.posseg as pseg
from collections import Counter
import re
import os

# ===== Safe Font Setting =====
font_path = "NotoSansTC-Regular.otf"
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
else:
    font_prop = None  # fallback: no custom font
plt.rcParams['axes.unicode_minus'] = False

# ===== Streamlit UI =====
st.set_page_config(page_title="Daily Post & Keyword Analysis", layout="centered")
st.title("📈 Daily Post, Likes & Keywords Visualization")
st.markdown("Please upload a CSV file that includes '發文日期', '發文內容', and '按讚數' columns.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # 檢查必要欄位
        required_cols = ["發文日期", "發文內容", "按讚數"]
        if not all(col in df.columns for col in required_cols):
            st.error("❌ CSV must include: 發文日期, 發文內容, 按讚數")
        else:
            df["發文日期"] = pd.to_datetime(df["發文日期"], errors="coerce")
            df = df.dropna(subset=["發文日期"])

            # ===== 每日發文數量折線圖 =====
            st.subheader("📆 Posts per Day")
            daily_counts = df["發文日期"].value_counts().sort_index()
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(daily_counts.index, daily_counts.values, marker="o", color="orange")
            ax1.set_title("Number of Posts per Day", fontproperties=font_prop)
            ax1.set_xlabel("Date", fontproperties=font_prop)
            ax1.set_ylabel("Post Count", fontproperties=font_prop)
            plt.xticks(rotation=45, fontproperties=font_prop)
            plt.yticks(fontproperties=font_prop)
            st.pyplot(fig1)

            
            # ===== 每篇發文的按讚數（依時間）折線圖 =====
            st.subheader("🕒 Likes per Post Over Time")
            df_time_likes = df.copy()
            df_time_likes = df_time_likes.dropna(subset=["發文日期", "按讚數"])
            df_time_likes = df_time_likes.sort_values("發文日期")

            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.plot(df_time_likes["發文日期"], df_time_likes["按讚數"], marker="o", linestyle="-", color="green")
            ax2.set_xlabel("Post Time", fontproperties=font_prop)
            ax2.set_ylabel("Like Count", fontproperties=font_prop)
            ax2.set_title("Likes per Post Over Time", fontproperties=font_prop)
            plt.xticks(rotation=45, fontproperties=font_prop)
            plt.yticks(fontproperties=font_prop)
            st.pyplot(fig2)

# ===== 每篇貼文常見關鍵名詞分析 =====

            st.subheader("🔍 Top 15 Chinese Noun Keywords from Posts")

            texts = df["發文內容"].dropna().astype(str).tolist()
            text_all = " ".join(texts)
            text_all = re.sub(r"[^一-鿿A-Za-z0-9]", " ", text_all)
            words = pseg.cut(text_all)
            nouns = [word for word, flag in words if flag.startswith("n") and len(word) >= 2]
            counter = Counter(nouns)
            most_common = counter.most_common(15)

            if most_common:
                keywords_df = pd.DataFrame(most_common, columns=["Keyword", "Frequency"])
                st.dataframe(keywords_df)

                fig3, ax3 = plt.subplots(figsize=(10, 5))
                ax3.bar([kw for kw, _ in most_common], [freq for _, freq in most_common], color="coral")
                ax3.set_title(f"Top {top_n} Chinese Nouns", fontproperties=font_prop)
                ax3.set_ylabel("Frequency", fontproperties=font_prop)
                plt.xticks(rotation=45, fontproperties=font_prop)
                plt.yticks(fontproperties=font_prop)
                st.pyplot(fig3)
            else:
                st.info("沒有足夠的中文名詞資料可以顯示。")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("Please upload a CSV file with '發文日期', '發文內容', and '按讚數'.")
