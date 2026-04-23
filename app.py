import streamlit as st

st.set_page_config(page_title="引用格式生成器", layout="centered")

st.title("📚 學術引用格式生成器")

# --- 1. 設定 12 種可選項 ---
options = [
    "古籍", 
    "著作", 
    "析出文獻", 
    "期刊", 
    "報紙", 
    "政府出版物", 
    "連續出版物", 
    "小冊子", 
    "學位論文及會議論文", 
    "手稿及歷史檔案", 
    "字典及詞典", 
    "澳門憲報"
]

source_type = st.selectbox("📌 請選擇資料類型", options)

# --- 2. 建立輸入表單 ---
with st.form("citation_form"):
    st.write(f"當前編輯：**{source_type}**")
    
    # 這裡預留 12 個判斷空間，之後我們一個個補齊欄位
    if source_type == "古籍":
        st.info("待設定：古籍欄位")
        
    elif source_type == "著作":
        st.info("待設定：著作欄位")
        
    elif source_type == "析出文獻":
        st.info("待設定：析出文獻欄位")
        
    elif source_type == "期刊":
        st.info("待設定：期刊欄位")
        
    elif source_type == "報紙":
        st.info("待設定：報紙欄位")
        
    elif source_type == "政府出版物":
        st.info("待設定：政府出版物欄位")
        
    elif source_type == "連續出版物":
        st.info("待設定：連續出版物欄位")
        
    elif source_type == "小冊子":
        st.info("待設定：小冊子欄位")
        
    elif source_type == "學位論文及會議論文":
        st.info("待設定：學位論文及會議論文欄位")
        
    elif source_type == "手稿及歷史檔案":
        st.info("待設定：手稿及歷史檔案欄位")
        
    elif source_type == "字典及詞典":
        st.info("待設定：字典及詞典欄位")
        
    elif source_type == "澳門憲報":
        st.info("待設定：澳門憲報欄位")

    # 提交按鈕
    submitted = st.form_submit_button("🚀 生成引用格式")

# --- 3. 生成結果區 ---
if submitted:
    st.write("格式生成邏輯待補齊...")
