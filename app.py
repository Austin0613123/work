import streamlit as st

st.set_page_config(page_title="引用格式生成器", layout="centered")

# --- 核心工具：自動處理標點符號 ---
def clean(text, prefix="", suffix=""):
    if text and str(text).strip():
        return f"{prefix}{text.strip()}{suffix}"
    return ""

st.title("📚 學術引用格式生成器")

# --- 1. 設定 12 種可選項 ---
options = [
    "古籍", "著作", "析出文獻", "期刊", "報紙", 
    "政府出版物", "連續出版物", "小冊子", 
    "學位論文及會議論文", "手稿及歷史檔案", "字典及詞典", "澳門憲報"
]

source_type = st.selectbox("📌 請選擇資料類型", options)

# --- 2. 建立輸入表單 (只有一個 form) ---
with st.form("citation_form"):
    st.write(f"請輸入 **{source_type}** 的詳細資訊：")
    
    col1, col2 = st.columns(2)

    with col1:
        # 定義基礎元素 (1-7)
        author = st.text_input("1. 作者 / 析出文獻責任者")
        title = st.text_input("2. 文獻／篇名／新聞標題")
        version = st.text_input("3. 版本（如：第二版、古籍版本）")
        volume = st.text_input("4. 卷數")
        issue = st.text_input("5. 期數")
        book_class = st.text_input("6. 部類（只適用於古籍）")
        editor = st.text_input("7. 編者／校對者")

    with col2:
        # 定義基礎元素 (8-14)
        bookname = st.text_input("8. 著作名稱／收錄書目／報社／刊名")
        time = st.text_input("9. 出版年份 / 文獻形成時間")
        place = st.text_input("10. 出版地／收藏地／學校")
        publisher = st.text_input("11. 出版社 / 網站名稱")
        link = st.text_input("12. 網址")
        page = st.text_input("13. 頁數")
        access_date = st.text_input("14. 瀏覽日期 / 發布日期")

    submitted = st.form_submit_button("🚀 生成引用格式")

# --- 3. 生成結果邏輯 ---
if submitted:
    res = ""
    
    if source_type == "古籍":
        # 格式：作者：〈篇名〉，編者：《書名》卷期、部類，地：者，年份，版本，頁。
        p1 = f"{clean(author, suffix='：')}{clean(title, '〈', '〉')}"
        p2 = f"{clean(editor, suffix='：')}{clean(bookname, '《', '》')}"
        sep = "，" if p1 and p2 else ""
        v_c = f"{volume}、{book_class}" if volume and book_class else f"{volume}{book_class}"
        
        # 拼接
        res = f"{p1}{sep}{p2}{v_c}{clean(place, '，', '：')}{clean(publisher)}{clean(time, '年，')}{clean(version, '，')}{clean(page, '，頁')}。"

    elif source_type == "著作":
        # 格式：作者：《書名》（版本），地：者，年份，頁。
        v = clean(version, "（", "）")
        res = f"{clean(author, suffix='：')}{clean(bookname, '《', '》')}{v}{clean(place, '，', '：')}{clean(publisher)}{clean(time, '，')}{clean(page, '，頁')}。"


    
    # ... 其他 10 種邏輯可以在此繼續補齊 ...
    else:
        res = f"【{source_type}】的生成邏輯開發中，目前僅支援古籍與著作。"

    # 修正標點
    res = res.replace("，，", "，").replace("：：", "：").replace("，。", "。")
    
    st.success("✅ 生成成功！")
    st.code(res, language=None)
