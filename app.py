import streamlit as st

st.set_page_config(page_title="澳門學術引用生成器", layout="centered")
# --- 1. 配置字典 (核心邏輯) ---
# 這裡定義了每一類型的：
# fields: 需要顯示的輸入框標籤
# template: 生成格式的模板，{key} 必須對應 fields 的名稱
CONFIG = {
    "著作": {
        "fields": ["作者", "書名", "版本", "出版地(可不填)", "出版社", "出版年份", "頁數"],
        "template": "{作者}：《{書名}》{版本}，{出版地(可不填)}：{出版社}，{出版年份}，{頁數}。"
    },
    "古籍": {
        "fields": ["作者", "篇名", "編者", "書名", "卷數", "部類", "出版地", "出版年份", "版本", "頁數"],
        "template": "{作者}：〈{篇名}〉，{編者}：《{書名}》{卷數}、{部類}，{出版地}，{出版年份}，{版本}，{頁數}。"
    },
    "期刊": {
        "fields": ["作者", "篇名", "期刊名", "出版年份", "期數", "頁數"],
        "template": "{作者}：〈{篇名}〉，《{期刊名}》，{出版年份}年第{期數}期，{頁數}。"
    },
    "澳門憲報": {
        "fields": ["標題", "法規編號", "憲報編號", "副刊", "發布日期", "頁數"],
        "template": "〈{標題}〉，第{法規編號}號，載《澳門特別行政區憲報》第{憲報編號}期{副刊}，{發布日期}，{頁數}。"
    }
}

# --- 工具函式 ---
def clean_input(val, prefix="", suffix="", wrap=""):
    """自動處理標點：如果有值就加前後綴，沒有就回傳空字串"""
    v = str(val).strip()
    if v:
        if wrap == "〈〉": return f"〈{v}〉"
        if wrap == "《》": return f"《{v}〉"
        if wrap == "（）": return f"（{v}）"
        return f"{prefix}{v}{suffix}"
    return ""

# --- UI 介面 ---
st.title("📚 學術引用格式生成器")

source_type = st.selectbox("📌 請選擇資料類型", list(CONFIG.keys()))

# 根據選擇的類型，取出對應的配置
current_config = CONFIG[source_type]
user_data = {}

# --- 2. 動態生成輸入表單 ---
with st.container():
    st.subheader(f"📝 填寫 {source_type} 資訊")
    
    # 使用 columns 讓排版好看一點
    cols = st.columns(2)
    for i, field_name in enumerate(current_config["fields"]):
        with cols[i % 2]: # 交替在左右兩欄顯示
            user_data[field_name] = st.text_input(field_name, key=field_name)

    submit_btn = st.button("🚀 生成引用格式")

# --- 3. 處理生成邏輯 ---
if submit_btn:
    # 預處理：對輸入的資料做初步的標點包裝（例如書名自動加《》）
    processed_data = {}
    for k, v in user_data.items():
        if k in ["書名", "期刊名"]:
            processed_data[k] = clean_input(v, wrap="《》")
        elif k in ["篇名", "標題"]:
            processed_data[k] = clean_input(v, wrap="〈〉")
        elif k == "作者" and v:
            processed_data[k] = f"{v.strip()}："
        elif k == "版本" and v:
            processed_data[k] = f"（{v.strip()}）"
        elif k == "頁數" and v:
            processed_data[k] = f"頁{v.strip()}"
        else:
            processed_data[k] = v.strip()

    # 從字典拿到模板，用 .format() 把處理好的資料填進去
    try:
        raw_res = current_config["template"].format(**processed_data)
        
        # 清理連續的多餘逗號（例如某個欄位沒填時產生的情況）
        res = raw_res.replace("，，", "，").replace("：，", "：").replace("、，", "，")
        
        st.success("✅ 生成成功！")
        st.code(res, language=None)
    except KeyError as e:
        st.error(f"發生錯誤：模板中缺少欄位 {e}")

    # 修正標點
    res = res.replace("，，", "，").replace("：：", "：").replace("，。", "。")
    
    st.success("✅ 生成成功！")
    st.code(res, language=None)
