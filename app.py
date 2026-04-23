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

with st.form("citation_form"):
    st.write(f"請輸入 **{source_type}** 的詳細資訊：")
    
col1, col2 = st.columns(2)

with col1:
        # 定義 14 個基礎元素
        author = st.text_input("1. 作者")
        title = st.text_input("2. 文獻／篇名／新聞標題 ")
        version = st.text_input("3. 版本（如：刑事訴訟教程（第二版）、古籍之版本）")
        volume = st.text_input("4. 卷數")
        issue = st.text_input("5. 期數 ")
        book_class = st.text_input("6. 部類（只適用於古籍）")
        editor = st.text_input("7. 編者／校對者")
    with col2:
        bookname = st.text_input("8. 著作名稱／／收錄書目／報社名稱／刊物名稱")
        time = st.text_input("9. 出版年份 / 文獻形成時間")
        place = st.text_input("10. 出版地／收藏地／學校（碩博士論文）")
        publisher = st.text_input("11. 出版社")
        link = st.text_input("12. 網址 (電子資源用)")
        page = st.text_input("13. 頁數")

    submitted = st.form_submit_button("🚀 生成引用格式")


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
