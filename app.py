import streamlit as st

st.set_page_config(page_title="澳門學術引用生成器", layout="centered")

# --- 1. 配置字典 ---
CONFIG = {
    "著作": {
        "fields": ["作者", "書名", "版本", "出版地", "出版社", "出版年份", "頁數"],
        "template": "{作者}：《{書名}》{版本}，{出版地}：{出版社}，{出版年份}，{頁數}。"
    },
    "古籍": {
        "fields": ["作者", "篇名", "編者", "書名", "卷數", "部類", "出版地", "出版年份", "版本", "頁數"],
        "template": "{作者}：〈{篇名}〉，{編者}：《{書名}》{卷數}、{部類}，{出版地}，{出版年份}，{版本}，{頁數}。"
    },
    "期刊": {
        "fields": ["作者", "篇名", "期刊名", "出版年份", "期數", "頁數"],
        "template": "{作者}：〈{篇名}〉，《{期刊名}》，{出版年份}年第{期數}期，{頁數}。"
    },
    "報紙": {
        "fields": ["作者", "篇名", "報紙名稱", "出版日期", "版次"], 
        "template": "{作者}：〈{篇名}〉，《{報紙名稱}》，{出版日期}，{版次}。"
    }, # <--- 修正處：補上逗號
    "澳門憲報": {
        "fields": ["標題", "法規編號", "憲報編號", "副刊", "發布日期", "頁數"],
        "template": "〈{標題}〉，第{法規編號}號，載《澳門特別行政區憲報》第{憲報編號}期{副刊}，{發布日期}，{頁數}。"
    }
}

# --- 工具函式 ---
def clean_input(val, prefix="", suffix="", wrap=""):
    v = str(val).strip()
    if v:
        if wrap == "〈〉": return f"〈{v}〉"
        if wrap == "《》": return f"《{v}》"
        if wrap == "（）": return f"（{v}）"
        return f"{prefix}{v}{suffix}"
    return ""

# --- UI 介面 ---
st.title("📚 學術引用格式生成器")

source_type = st.selectbox("📌 請選擇資料類型", list(CONFIG.keys()))
current_config = CONFIG[source_type]
user_data = {}

with st.container():
    st.subheader(f"📝 填寫 {source_type} 資訊")
    cols = st.columns(2)
    for i, field_name in enumerate(current_config["fields"]):
        with cols[i % 2]:
            # 這裡可以透過 label 提示使用者「可不填」
            label = field_name if "可不填" in field_name else f"{field_name}"
            user_data[field_name] = st.text_input(label, key=f"{source_type}_{field_name}")

    submit_btn = st.button("🚀 生成引用格式")

# --- 3. 處理生成邏輯 ---
if submit_btn:
    processed_data = {}
    for k, v in user_data.items():
        # 針對不同欄位做預處理
        if k in ["書名", "期刊名", "報紙名稱"]:
            processed_data[k] = v.strip() # 模板裡已有《》
        elif k in ["篇名", "標題"]:
            processed_data[k] = v.strip() # 模板裡已有〈〉
        elif k == "作者" and v:
            processed_data[k] = f"{v.strip()}："
        elif k == "版本" and v:
            processed_data[k] = f"（{v.strip()}）"
        elif k == "頁數" and v:
            processed_data[k] = f"頁{v.strip()}"
        elif k == "版次" and v:
            processed_data[k] = f"頁{v.strip()}"
        else:
            processed_data[k] = v.strip()

    try:
        # 生成原始字串
        res = current_config["template"].format(**processed_data)
        
        # 強力清理標點符號邏輯
        res = res.replace("，，", "，").replace("：，", "：").replace("、，", "，")
        res = res.replace("，。", "。").replace("：：", "：").replace("（）", "")
        
        # 如果某些欄位完全沒填，可能會留下孤單的關鍵字，這裡做最後修飾
        res = res.replace("頁。", "。").replace("年第期", "")

        st.success("✅ 生成成功！")
        st.code(res, language=None)
        
    except KeyError as e:
        st.error(f"發生錯誤：模板中缺少欄位 {e}")
