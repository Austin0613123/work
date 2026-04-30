import streamlit as st
import datetime

st.set_page_config(page_title="澳門學術引用生成器", layout="centered")

# --- 1. 工具函式：核心邏輯（有值才加符號） ---
def clean_input(val, prefix="", suffix="", wrap=None):
    v = str(val).strip()
    if not v:
        return "" # 沒填寫時，回傳空字串，不顯示任何符號
    
    # 處理括號包裝
    if wrap == "〈〉": v = f"〈{v}〉"
    elif wrap == "《》": v = f"《{v}》"
    elif wrap == "（）": v = f"（{v}）"
    
    return f"{prefix}{v}{suffix}"

def to_roman(n):
    """將阿拉伯數字轉換為羅馬數字"""
    try:
        n = int(str(n).strip())
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_num = ''
        i = 0
        while n > 0:
            for _ in range(n // val[i]):
                roman_num += syb[i]
                n -= val[i]
            i += 1
        return roman_num
    except:
        return n # 如果不是純數字，則原樣回傳

# --- 2. 配置字典 ---
# 注意：template 裡只放變數，不放標點，標點改在後端動態加入
CONFIG = {
    "著作": {
        "fields": ["作者", "書名", "版本", "出版地", "出版社", "出版年份", "頁數"],
        "template": "{作者}{書名}{版本}{出版地}{出版社}{出版年份}{頁數}"
    },
    "古籍": {
        "fields": ["朝代","作者", "篇名", "編者", "書名", "卷數", "部類", "出版地", "出版社","出版年份", "版本", "頁數"],
        "template": "{朝代}{作者}{篇名}{編者}{書名}{卷數}{部類}{出版地}{出版社}{出版年份}{版本}{頁數}"
    },
    "期刊": {
        "fields": ["作者", "篇名", "期刊名", "卷數","出版年份", "期數", "頁數"],
        "template": "{作者}{篇名}{期刊名}{卷數}{出版年份}{期數}{頁數}"
    },
    "報紙": {
        "fields": ["作者", "篇名", "報紙名稱", "出版日期", "版次"], 
        "template": "{作者}{篇名}{報紙名稱}{出版日期}{版次}"
    },
    "回歸前澳門憲報": {
        "fields": ["標題", "憲報名稱", "憲報期數","號數", "副刊1/2", "發布日期", "頁數"],
        "template": "{標題}{憲報名稱}{憲報期數}{號數}{副刊1/2}{發布日期}{頁數}"
    },
    "析出文獻": {
        "fields": ["析出文獻責任者", "析出文獻題名", "文獻責任者", "文獻題名", "出版地", "出版者", "出版年份", "頁碼"],
        "template": "{析出文獻責任者}{析出文獻題名}{文獻責任者}{文獻題名}{出版地}{出版者}{出版年份}{頁碼}"
    },
    "政府出版物、報告": {
        "fields": ["責任者", "刊物名", "出版年份", "頁碼"],
        "template": "{責任者}{刊物名}{出版年份}{頁碼}"
    },
    "連續出版物": {
        "fields": ["責任者", "刊物名", "期數", "出版年份", "頁碼"],
        "template": "{責任者}{刊物名}{期數}{出版年份}{頁碼}"
    },
    "小冊子": {
        "fields": ["刊物名", "出版地", "出版者", "出版年份", "頁碼"],
        "template": "{刊物名}{出版地}{出版者}{出版年份}{頁碼}"
    },
    "學位論文、會議論文": {
        "fields": ["責任者", "篇名", "文獻性質", "地點或學校", "文獻形成時間", "頁碼"],
        "template": "{責任者}{篇名}{文獻性質}{地點或學校}{文獻形成時間}{頁碼}"
    },
    "電子資源": {
        "fields": ["責任者", "資料標題", "網站／數據庫名稱", "發布日期", "網址", "瀏覽日期"],
        "template": "{責任者}{資料標題}{網站／數據庫名稱}{發布日期}{網址}{瀏覽日期}"
    },
    "手稿及歷史檔案": {
        "fields": ["責任者", "文獻標題", "文獻形成時間", "所藏地", "卷宗號或其他編號", "瀏覽日期"],
        "template": "{責任者}{文獻標題}{文獻形成時間}{所藏地}{卷宗號或其他編號}{瀏覽日期}"
    },
    "字典、詞典": {
        "fields": ["條目名稱", "書名", "版本", "出版地", "出版者", "出版年份", "頁碼"],
        "template": "{條目名稱}{書名}{版本}{出版地}{出版者}{出版年份}{頁碼}"
    },
}

import datetime # 建議放在程式碼最上方

# --- 3. UI 介面 ---
st.title("📚 志書引用格式生成器")

source_type = st.selectbox("📌 請選擇資料類型", list(CONFIG.keys()))
current_config = CONFIG[source_type]
user_data = {}

with st.container():
    st.subheader(f"📝 填寫 {source_type} 資訊")
    cols = st.columns(2)
    for i, field_name in enumerate(current_config["fields"]):
        with cols[i % 2]:
            if source_type == "回歸前澳門憲報" and field_name == "發布日期":
                # 預設值設為回歸前夕
                user_data[field_name] = st.date_input(
                    field_name, 
                    value=datetime.date(1999, 12, 19),
                    key=f"{source_type}_{field_name}"
                )
            else:
                user_data[field_name] = st.text_input(field_name, key=f"{source_type}_{field_name}")

    submit_btn = st.button("🚀 生成引用格式")
# --- 4. 生成結果邏輯 ---
if submit_btn:
    d = user_data
    p = {} # 存放處理後（帶有標點）的字串
    
    # 根據不同類型，精確定義每個欄位的標點規則
    if source_type == "著作":
        p["作者"] = clean_input(d["作者"], suffix="：")
        p["書名"] = clean_input(d["書名"], wrap="《》")
        p["版本"] = clean_input(d["版本"], wrap="（）")
        p["出版地"] = clean_input(d["出版地"], prefix="，", suffix="：")
        p["出版社"] = clean_input(d["出版社"])
        p["出版年份"] = clean_input(d["出版年份"], prefix="，")
        p["頁數"] = clean_input(d["頁數"], prefix="，頁")

    elif source_type == "古籍":
        p["朝代"] = clean_input(d["朝代"], prefix="[", suffix="]")
        p["作者"] = clean_input(d["作者"], suffix="：")
        p["篇名"] = clean_input(d["篇名"], wrap="〈〉")
        p["編者"] = clean_input(d["編者"], prefix="，", suffix="：")
        p["書名"] = clean_input(d["書名"], wrap="《》")
        p["卷數"] = clean_input(d["卷數"], prefix="卷")
        p["部類"] = clean_input(d["部類"], prefix="、")
        p["出版地"] = clean_input(d["出版地"], prefix="，")
        p["出版社"] = clean_input(d["出版社"], prefix="：")
        p["出版年份"] = clean_input(d["出版年份"], prefix="，", suffix="年")
        p["版本"] = clean_input(d["版本"], prefix="，")
        p["頁數"] = clean_input(d["頁數"], prefix="，頁")
        
    elif source_type == "期刊":
        p["作者"] = clean_input(d["作者"], suffix="：")
        p["篇名"] = clean_input(d["篇名"], wrap="〈〉")
        p["期刊名"] = clean_input(d["期刊名"], prefix="，", wrap="《》")
        p["卷數"] = clean_input(d["卷數"], prefix="，卷")
        p["期數"] = clean_input(d["期數"], prefix="，第", suffix="期")
        p["出版年份"] = clean_input(d["出版年份"], wrap="（）")
        p["頁數"] = clean_input(d["頁數"], prefix="，頁")

    elif source_type == "報紙":
        p["作者"] = clean_input(d["作者"], suffix="：")
        p["篇名"] = clean_input(d["篇名"], wrap="〈〉")
        p["報紙名稱"] = clean_input(d["報紙名稱"], prefix="，", wrap="《》")
        p["出版日期"] = clean_input(d["出版日期"], prefix="，")
        p["版次"] = clean_input(d["版次"], prefix="，頁")


elif source_type == "回歸前澳門憲報":
        d_val = d["發布日期"] # 這是 st.date_input 回傳的 date 物件
        # 自動判定葡文名稱 (pt)
        if d_val >= datetime.date(1999, 12, 20):
            pt = "Boletim Oficial da RAEM"
        elif d_val >= datetime.date(1951, 7, 7):
            pt = "Boletim Oficial de Macau"
        elif d_val >= datetime.date(1951, 1, 6):
            pt = "Boletim Oficial do Governo da Colónia de Macau"
        elif d_val >= datetime.date(1943, 12, 31):
            pt = "Boletim Oficial da Colónia de Macau"
        elif d_val >= datetime.date(1937, 1, 2):
            pt = "Boletim Oficial da Colónia de Macau"
        elif d_val >= datetime.date(1936, 1, 4):
            pt = "Boletim Oficial"
        elif d_val >= datetime.date(1923, 7, 7):
            pt = "Boletim Oficial do Governo da Província de Macau"
        elif d_val >= datetime.date(1921, 9, 24):
            pt = "Boletim Oficial do Governo da Província de Macau"
        elif d_val >= datetime.date(1891, 1, 2):
            pt = "Boletim Official do Governo da Provincia de Macau e Timor"
        elif d_val >= datetime.date(1867, 2, 25):
            pt = "Boletim da Provincia de Macau e Timor"
        elif d_val >= datetime.date(1867, 2, 18):
            pt = "Boletim do Governo de Macau e Timor"
        elif d_val >= datetime.date(1856, 12, 13):
            pt = "O Boletim do Governo de Macao"
        elif d_val >= datetime.date(1850, 11, 16):
            pt = "Boletim do Governo da Provincia de Macao, Timor, e Solor"
        else:
            pt = "Boletim Oficial"
            
        p["標題"] = clean_input(d["標題"], prefix='"', suffix='"')
        p["憲報名稱"] = f"（*{pt}*）"
        # --- 呼叫轉換工具 ---
        roman_issue = to_roman(d["憲報編號"])
        p["憲報期號"] = clean_input(roman_issue, prefix=",Vol. ")
        p["號數"] = clean_input(d["號數"], prefix=',',suffix=".º ")
    
        # 2. 處理「號數」與「副刊」的整合
        issue_num = str(d["號數"]).strip() # 取得號數，例如 "13"
        supp_val = str(d["副刊"]).strip()  # 取得副刊類型 "1" 或 "2"

        if supp_val == "1":
            # 如果有副刊，將號數整合進副刊字串中
            p["副刊"] = f", 1.º Supplemento ao n.º {issue_num}" if issue_num else ", 1.º Supplemento"
            p["號數"] = "" # 清空號數，避免重複輸出
        elif supp_val == "2":
            p["副刊"] = f", 2.º Supplemento ao n.º {issue_num}" if issue_num else ", 2.º Supplemento"
            p["號數"] = "" # 清空號數，避免重複輸出
        else:
            # 如果沒有副刊，則單獨處理號數
            p["號數"] = clean_input(issue_num, prefix=", n.º ")
            p["副刊"] = ""

        p["發布日期"] = clean_input(d_val.strftime("%Y年%m月%d日"), prefix="，")
        p["頁數"] = clean_input(d["頁數"], prefix="，頁碼")

    
    elif source_type == "析出文獻":
        p["析出文獻責任者"] = clean_input(d["析出文獻責任者"], suffix="：")
        p["析出文獻題名"] = clean_input(d["析出文獻題名"], wrap="〈〉")
        p["文獻責任者"] = clean_input(d["文獻責任者"], prefix="，", suffix="：")
        p["文獻題名"] = clean_input(d["文獻題名"], wrap="《》")
        p["出版地"] = clean_input(d["出版地"], prefix="，", suffix="：")
        p["出版者"] = clean_input(d["出版者"])
        p["出版年份"] = clean_input(d["出版年份"], prefix="，")
        p["頁碼"] = clean_input(d["頁碼"], prefix="，頁")
    elif source_type == "政府出版物、報告":
        # 責任者後方接冒號
        p["責任者"] = clean_input(d["責任者"], suffix="：")
        # 刊物名加上書名號
        p["刊物名"] = clean_input(d["刊物名"], wrap="《》")
        # 出版年份前加逗號
        p["出版年份"] = clean_input(d["出版年份"], prefix="，")
        # 頁碼前加逗號與「頁」字
        p["頁碼"] = clean_input(d["頁碼"], prefix="，頁")
    elif source_type == "連續出版物":
        # 責任者後方接冒號
        p["責任者"] = clean_input(d["責任者"], suffix="：")
        # 刊物名加上書名號
        p["刊物名"] = clean_input(d["刊物名"], wrap="《》")
        # 期數前加逗號
        p["期數"] = clean_input(d["期數"], prefix="，")
        # 出版年份用實心括號包裝（注意：這裡不需要額外加逗號）
        p["出版年份"] = clean_input(d["出版年份"], wrap="（）")
        # 頁碼前加逗號與「頁」字
        p["頁碼"] = clean_input(d["頁碼"], prefix="，頁") 
    elif source_type == "小冊子":
        # 刊物名加上書名號
        p["刊物名"] = clean_input(d["刊物名"], wrap="《》")
        # 出版地前加逗號，後接冒號
        p["出版地"] = clean_input(d["出版地"], prefix="，", suffix="：")
        # 出版者（直接顯示）
        p["出版者"] = clean_input(d["出版者"])
        # 出版年份前加逗號
        p["出版年份"] = clean_input(d["出版年份"], prefix="，")
        # 頁碼前加逗號與「頁」字
        p["頁碼"] = clean_input(d["頁碼"], prefix="，頁")
    elif source_type == "學位論文、會議論文":
        # 責任者後接冒號
        p["責任者"] = clean_input(d["責任者"], suffix="：")
        # 篇名加上單書名號
        p["篇名"] = clean_input(d["篇名"], wrap="〈〉")
        # 文獻性質（如：碩士論文）前加逗號
        p["文獻性質"] = clean_input(d["文獻性質"], prefix="，")
        # 地點或學校前加逗號
        p["地點或學校"] = clean_input(d["地點或學校"], prefix="，")
        # 文獻形成時間（年份）前加逗號
        p["文獻形成時間"] = clean_input(d["文獻形成時間"], prefix="，")
        # 頁碼前加逗號與「頁」字
        p["頁碼"] = clean_input(d["頁碼"], prefix="，頁")
    elif source_type == "電子資源":
        # 責任者後接冒號
        p["責任者"] = clean_input(d["責任者"], suffix="：")
        # 資料標題加上單書名號
        p["資料標題"] = clean_input(d["資料標題"], wrap="〈〉")
        # 網站名稱前加逗號
        p["網站／數據庫名稱"] = clean_input(d["網站／數據庫名稱"], prefix="，")
        # 發布日期前加逗號
        p["發布日期"] = clean_input(d["發布日期"], prefix="，")
        # 網址前加逗號（通常網址後方不加標點，以免複製錯誤）
        p["網址"] = clean_input(d["網址"], prefix="，")
        # 瀏覽日期用實心括號包裝，前綴加「瀏覽於」
        p["瀏覽日期"] = clean_input(d["瀏覽日期"], prefix="，讀取")
    elif source_type == "手稿及歷史檔案":
        # 責任者後接冒號
        p["責任者"] = clean_input(d["責任者"], suffix="：")
        # 文獻標題加上單書名號
        p["文獻標題"] = clean_input(d["文獻標題"], wrap="〈〉")
        # 文獻形成時間前加逗號
        p["文獻形成時間"] = clean_input(d["文獻形成時間"], prefix="，")
        # 所藏地前加逗號
        p["所藏地"] = clean_input(d["所藏地"], prefix="，")
        # 卷宗號或其他編號前加逗號
        p["卷宗號或其他編號"] = clean_input(d["卷宗號或其他編號"], prefix="，")
        # 瀏覽日期（若為數位化檔案）前加逗號與提示字
        p["瀏覽日期"] = clean_input(d["瀏覽日期"], prefix="，瀏覽於")
    elif source_type == "字典、詞典":
        # 條目名稱後接冒號
        p["條目名稱"] = clean_input(d["條目名稱"], suffix="：")
        # 書名加上書名號
        p["書名"] = clean_input(d["書名"], wrap="《》")
        # 版本用括號包裝
        p["版本"] = clean_input(d["版本"], wrap="（）")
        # 出版地前加逗號，後接冒號
        p["出版地"] = clean_input(d["出版地"], prefix="，", suffix="：")
        # 出版者（直接顯示）
        p["出版者"] = clean_input(d["出版者"])
        # 出版年份前加逗號，後接冒號（連接頁碼）
        p["出版年份"] = clean_input(d["出版年份"], prefix="，", suffix="：")
        # 頁碼（直接顯示）
        p["頁碼"] = clean_input(d["頁碼"])

    
    # 執行生成
    try:
        # 建立一個與 template 欄位數量一致的 dict，避免 format 報錯
        # 若 p 裡面沒有該欄位，則補空字串
        final_p = {f: p.get(f, "") for f in current_config["fields"]}
        res = current_config["template"].format(**final_p)
        
        # 最後修整：清除可能因為拼接產生的多餘頭尾符號
       if res:
            st.success("✅ 生成成功！")
            
            # 顯示生成的引用字串
            st.code(res, language=None)
            
            # 加入專業標註提示
            st.caption("💡 **註：如果是英/葡文書籍、或憲報，需按學術規範改為斜體。**")
            
            # 如果你想讓提示更顯眼，也可以改用 info 樣式：
            # st.info("註：括號內之葡文名稱按學術規範建議改為斜體。")
        else:
            st.warning("請至少輸入一些資訊內容。")
            
    except Exception as e:
        st.error(f"生成失敗，請檢查欄位格式設定。")
