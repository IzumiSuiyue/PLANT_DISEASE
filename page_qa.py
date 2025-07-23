import streamlit as st
from app.gpt_interface import query_disease
from app.disease_data import get_disease_dict, update_disease, delete_disease

def qa_tab():
    st.subheader("🧠 病害问答助手")

    # 🌾 问答模块
    with st.form("query_form"):
        query = st.text_input("请输入病害名称（如 LeafMold）", key="query_input")
        submitted = st.form_submit_button("查询")

    if submitted and query:
        result, source = query_disease(query)
        st.markdown(result)
        st.caption("📚 来源：本地知识库" if source == "local" else "🧠 来源：千问大模型")

    