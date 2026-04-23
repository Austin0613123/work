import streamlit as st

st.title("學術引用格式生成器")

# 1. 定義所有選項
options = ["古籍", "著作", "析出文獻", "期刊", "轉引文獻", "政府出版物、小冊子", "學位論文、會議論文", "電子資源", "手稿、歷史檔案", "字典、詞典", "澳門憲報", "葡國憲報"]
source_type = st.selectbox("請選擇資料類型", options)

with st.form("citation_form"):
    # 2. 根據不同類型顯示輸入框
    if source_type == "古籍":
        dynasty = st.text_input("朝代 (如：清)")
        author = st.text_input("作者")
        title = st.text_input("書名")
        version = st.text_input("版本/卷次")

    elif source_type == "著作":
        author = st.text_input("作者")
        year = st.text_input("年份")
        title = st.text_input("書名")
        location = st.text_input("出版地")
        publisher = st.text_input("出版社")

    elif source_type == "澳門憲報":
        gov_dept = st.text_input("頒佈部門")
        doc_type = st.text_input("文件種類 (如：第xx/2026號行政法規)")
        gazette_num = st.text_input("憲報編號/期數")
        date = st.text_input("日期 (YYYY/MM/DD)")

    # ... 其他選項請依此類推 ...

    submitted = st.form_submit_button("生成引用格式")
    
    # 3. 處理生成的格式
    if submitted:
        if source_type == "古籍":
            result = f"〔{dynasty}〕{author}：《{title}》，{version}。"
        
        elif source_type == "著作":
            result = f"{author}：《{title}》，{location}：{publisher}，{year}年。"
            
        elif source_type == "澳門憲報":
            result = f"{gov_dept}：{doc_type}，《澳門特別行政區公報》，{gazette_num}，{date}。"
        
        else:
            result = "此格式尚未設定邏輯，請補充程式碼。"

        st.success("生成的格式如下：")
        st.code(result)