import streamlit as st
from app.page_recognition import recognition_tab
from app.page_qa import qa_tab
from app.page_history import history_tab
from app.page_knowledge import knowledge_tab

st.set_page_config(page_title="☀️我是老爹终将成熟的作物的守护者", layout="wide")

# 🌿 页面顶部标题和副标题（始终不变）
st.markdown("""
    <div style="text-align:left; padding-left: 20px;">
        <h1 style="margin-bottom: 10px;">🌱农业病虫害识别与防治助手</h1>
        <div style="font-size:16px; margin-bottom: 10px;">o((≧ω≦;))o「我是哀丽密榭的白厄！」⊃</div>
        <div style="font-size:16px; margin-bottom: 20px;">o((≧ω≦;))o「（三位白厄、足矣、、、）」⊃</div>
    </div>
""", unsafe_allow_html=True)


# 🌾 背景渐变 + 块状背景样式
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, rgba(179, 217, 157, 0.5), rgba(230, 229, 159, 0.5));
    }
    .block {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# 🌱 页面选择侧边栏
page = st.sidebar.radio("请选择功能 👇", [
    "🌿 病虫害识别助手",
    "🍓 病害问答助手",
    "📜 历史记录",
    "📚 知识库助手"
])

# 🍀 页面切换
if page == "🌿 病虫害识别助手":
    recognition_tab()
elif page == "🍓 病害问答助手":
    qa_tab()
elif page == "📜 历史记录":
    history_tab()
elif page == "📚 知识库助手":
    knowledge_tab()
