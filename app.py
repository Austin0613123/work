import streamlit as st

st.title("學術引用格式生成器")

# 選擇類型
source_type = st.selectbox("請選擇資料類型", ["圖書", "網頁", "期刊"])

# 根據選擇顯示對應欄位
with st.form("citation_form"):
    if source_type == "圖書":
        author = st.text_input("作者")
        year = st.text_input("年份")
        title = st.text_input("書名")
        publisher = st.text_input("出版社")
        
    elif source_type == "網頁":
        author = st.text_input("作者/機構")
        year = st.text_input("年份")
        title = st.text_input("標題")
        url = st.text_input("網址")

    submitted = st.form_submit_button("生成引用格式")
    
    if submitted:
        if source_type == "圖書":
            result = f"{author} ({year})。{title}。{publisher}。"
        else:
            result = f"{author} ({year})。{title}。取自 {url}"
            
        st.success("生成的格式如下：")
        st.code(result)