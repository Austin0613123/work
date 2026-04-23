import streamlit as st

st.set_page_config(page_title="學術引用格式生成器", layout="centered")
st.title("📚 學術引用格式生成器")
st.caption("請選擇資料類型，輸入資訊後即可生成標準格式。")

# 1. 選項定義
options = [
    "古籍", "著作", "析出文獻", "期刊", "報紙", "轉引文獻", 
    "政府出版物、報告", "連續出版物", "小冊子", 
    "學位論文、會議論文", "電子資源", "手稿、歷史檔案", "字典、詞典"
]
source_type = st.selectbox("📌 請選擇資料類型", options)

with st.form("citation_form"):
    # --- 1. 先初始化所有變數，防止 NameError ---
    author = title = pub_year = page = pub_loc = publisher = ""
    part_author = part_title = whole_author = whole_title = ""
    version = volume = journal = vol_num = issue_num = ""
    # (依此類推，把所有 {} 裡出現過的名稱都寫上 = "")

    # --- 2. 顯示輸入框 (維持原樣) ---
    if source_type == "古籍":
        part_author = st.text_input("析出文獻責任者")
        # ... 其他輸入框 ...

    # --- 3. 生成邏輯 (維持原樣) ---
    if submitted:
        # 這裡就不會因為變數沒被定義而崩潰了
        if source_type == "古籍":
             res = f"{part_author}..."

# 2. 表單輸入區
with st.form("citation_form"):
    st.subheader(f"輸入【{source_type}】內容")
    
    # 建立兩欄式輸入，節省空間
    col1, col2 = st.columns(2)
    
    with col1:
        if source_type == "古籍":
            part_author = st.text_input("析出文獻責任者 (如：蘇軾)")
            part_title = st.text_input("析出文獻題名")
            whole_author = st.text_input("原書責任者與方式 (如：張三校注)")
            whole_title = st.text_input("原書題名")
            volume = st.text_input("卷次、部類")
            
        elif source_type == "著作":
            author = st.text_input("責任者與責任方式")
            title = st.text_input("文獻題名")
            version = st.text_input("版本", placeholder="無則免填")
            
        elif source_type == "析出文獻":
            part_author = st.text_input("析出文獻責任者")
            part_title = st.text_input("析出文獻題名")
            whole_author = st.text_input("原書責任者與方式")
            whole_title = st.text_input("原書題名")

        elif source_type == "期刊":
            author = st.text_input("責任者")
            title = st.text_input("篇名")
            journal = st.text_input("期刊名")
            
        elif source_type == "報紙":
            author = st.text_input("責任者")
            title = st.text_input("篇名")
            newspaper = st.text_input("報紙名稱")

        elif source_type == "轉引文獻":
            orig_author = st.text_input("原始文獻責任者")
            orig_title = st.text_input("原始文獻題名")
            orig_year = st.text_input("原始文獻出版時間")
            trans_author = st.text_input("轉引文獻責任者")
            trans_title = st.text_input("轉引文獻題名")

        elif source_type in ["政府出版物、報告", "連續出版物"]:
            author = st.text_input("責任者")
            title = st.text_input("刊物名")

        elif source_type == "小冊子":
            title = st.text_input("刊物名")

        elif source_type == "學位論文、會議論文":
            author = st.text_input("責任者")
            title = st.text_input("篇名")
            nature = st.text_input("文獻性質 (如：碩士論文)")

        elif source_type == "電子資源":
            author = st.text_input("責任者")
            title = st.text_input("資料標題")
            site_name = st.text_input("網站／數據庫名稱")

        elif source_type == "手稿、歷史檔案":
            author = st.text_input("責任者")
            title = st.text_input("文獻標題")
            location = st.text_input("所藏地")

        elif source_type == "字典、詞典":
            item = st.text_input("條目名稱")
            title = st.text_input("書名")
            version = st.text_input("版本")

    with col2:
        # 共通或後續欄位
        if source_type in ["古籍", "著作", "析出文獻", "轉引文獻", "小冊子", "字典、詞典"]:
            pub_loc = st.text_input("出版地")
            publisher = st.text_input("出版者")
            
        if source_type in ["期刊"]:
            vol_num = st.text_input("卷號 (如無則免填)")
            issue_num = st.text_input("當年期號")
            
        if source_type == "報紙":
            pub_date = st.text_input("出版日期 (YYYY/MM/DD)")
            page_pos = st.text_input("版次")
            
        if source_type in ["古籍", "著作", "析出文獻", "期刊", "政府出版物、報告", "連續出版物", "小冊子", "學位論文、會議論文", "字典、詞典"]:
            pub_year = st.text_input("出版年份/文獻形成時間")

        if source_type == "轉引文獻":
            trans_loc = st.text_input("轉引文獻出版地")
            trans_pub = st.text_input("轉引文獻出版者")
            trans_year = st.text_input("轉引文獻出版時間")

        if source_type == "電子資源":
            pub_date = st.text_input("發布日期")
            url = st.text_input("網址")
            access_date = st.text_input("瀏覽日期")

        if source_type == "手稿、歷史檔案":
            form_time = st.text_input("文獻形成時間")
            archive_num = st.text_input("卷宗號或其他編號")
            access_date = st.text_input("瀏覽日期")

        if source_type == "學位論文、會議論文":
            place = st.text_input("地點或學校")

        if source_type != "報紙": # 報紙通常不用填頁碼
            page = st.text_input("頁碼")

    submitted = st.form_submit_button("🚀 生成引用格式")

# 3. 輸出生成邏輯
if submitted:
    res = ""
    if source_type == "古籍":
        res = f"{part_author}：〈{part_title}〉，{whole_author}：《{whole_title}》{volume}，{pub_loc}：{publisher}，{pub_year}，{version}，{page}。"
    elif source_type == "著作":
        ver_str = f"（{version}）" if version else ""
        res = f"{author}：《{title}》{ver_str}，{pub_loc}：{publisher}，{pub_year}，{page}。"
    elif source_type == "析出文獻":
        res = f"{part_author}：〈{part_title}〉，{whole_author}：《{whole_title}》，{pub_loc}：{publisher}，{pub_year}，{page}。"
    elif source_type == "期刊":
        vol_str = f"{vol_num}，" if vol_num else ""
        res = f"{author}：〈{title}〉，《{journal}》，{vol_str}{issue_num}（{pub_year}），{page}。"
    elif source_type == "報紙":
        res = f"{author}：〈{title}〉，《{newspaper}》，{pub_date}，{page_pos}。"
    elif source_type == "轉引文獻":
        res = f"{orig_author}：〈{orig_title}〉，{orig_year}，{trans_author}：《{trans_title}》，{trans_loc}：{trans_pub}，{trans_year}，{page}。"
    elif source_type == "政府出版物、報告":
        res = f"{author}：《{title}》，{pub_year}，{page}。"
    elif source_type == "連續出版物":
        res = f"{author}：《{title}》，{pub_year}（{pub_year}），{page}。"
    elif source_type == "小冊子":
        res = f"《{title}》，{pub_loc}：{publisher}，{pub_year}，{page}。"
    elif source_type == "學位論文、會議論文":
        res = f"{author}：〈{title}〉，{nature}，{place}，{pub_year}，{page}。"
    elif source_type == "電子資源":
        res = f"{author}︰〈{title}〉，{site_name}，{pub_date}，{url}，{access_date}。"
    elif source_type == "手稿、歷史檔案":
        res = f"{author}：〈{title}〉，{form_time}，{location}，{archive_num}，{access_date}。"
    elif source_type == "字典、詞典":
        ver_str = f"（{version}）" if version else ""
        res = f"{item}：《{title}》{ver_str}，{pub_loc}：{publisher}，{pub_year}：{page}。"

    st.success("✅ 生成成功！")
    st.code(res, language=None)