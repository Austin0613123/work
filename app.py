# --- 1. 配置字典 (拿掉模板裡的標點) ---
CONFIG = {
    "著作": {
        "fields": ["作者", "書名", "版本", "出版地", "出版社", "出版年份", "頁數"],
        "template": "{作者}{書名}{版本}{出版地}{出版社}{出版年份}{頁數}"
    },
    "報紙": {
        "fields": ["作者", "篇名", "報紙名稱", "出版日期", "版次"], 
        "template": "{作者}{篇名}{報紙名稱}{出版日期}{版次}"
    }
}

# --- 3. 處理生成邏輯 (這部分雖然有幾行，但執行極快) ---
if submit_btn:
    d = user_data
    p = {} # 存放處理後的資料
    
    # 使用我們進化的函式，把標點「封裝」進去
    if source_type == "著作":
        p["作者"] = clean_input(d.get("作者"), suffix="：")
        p["書名"] = clean_input(d.get("書名"), wrap="《》")
        p["版本"] = clean_input(d.get("版本"), wrap="（）")
        p["出版地"] = clean_input(d.get("出版地"), prefix="，", suffix="：")
        p["出版社"] = clean_input(d.get("出版社"))
        p["出版年份"] = clean_input(d.get("出版年份"), prefix="，")
        p["頁數"] = clean_input(d.get("頁數"), prefix="，頁")

    elif source_type == "報紙":
        p["作者"] = clean_input(d.get("作者"), suffix="：")
        p["篇名"] = clean_input(d.get("篇名"), wrap="〈〉")
        p["報紙名稱"] = clean_input(d.get("報紙名稱"), prefix="，", wrap="《》")
        p["出版日期"] = clean_input(d.get("出版日期"), prefix="，")
        p["版次"] = clean_input(d.get("版次"), prefix="，頁")

    # 最後一併生成並加上句號
    try:
        res = current_config["template"].format(**p)
        res = res.strip("，").strip("：") # 清除尾端多餘符號
        if res: res += "。"
        
        st.code(res)
    except:
        st.error("生成失敗，請檢查欄位。")
