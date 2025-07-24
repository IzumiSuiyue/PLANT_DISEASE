import streamlit as st
from app.disease_data import get_disease_dict, update_disease, delete_disease

def knowledge_tab():
    # ✅ 模拟刷新机制：靠 URL 参数变化触发重绘
    if "__refresh__" in st.session_state:
        st.session_state.pop("__refresh__")
        st.experimental_set_query_params()  # 清除参数 → 触发刷新

    st.subheader("📚 本地知识库管理")

    # ✅ 添加/修改表单
    st.markdown("### ✍️ 添加或修改病害资料")
    with st.form("edit_form"):
        name = st.text_input("病害名称", key="edit_name")
        symptom = st.text_area("症状描述", key="edit_symptom")
        cause = st.text_area("发病原因", key="edit_cause")
        control = st.text_area("防治措施（每行一条）", key="edit_control")
        saved = st.form_submit_button("提交更新")

    if saved:
        update_disease(name, symptom, cause, control.splitlines())
        st.success(f"✅ 病害“{name}”已成功添加/更新到本地知识库。")
        # ✅ 设置刷新标志，下一轮页面重绘将触发清空
        st.session_state["__refresh__"] = True
        st.experimental_set_query_params(submit="ok")

    # ✅ 浏览与删除模块
    st.markdown("---")
    st.markdown("### 🗂️ 当前知识库")
    disease_dict = get_disease_dict()
    if not disease_dict:
        st.info("📭 当前知识库为空。")
    else:
        for name, info in disease_dict.items():
            with st.expander(f"🌿 {name}"):
                st.write(f"🦠 **症状**：{info['symptom']}")
                st.write(f"📌 **发病原因**：{info['cause']}")
                st.write("🧪 **防治措施**：")
                for c in info['control']:
                    st.markdown(f"- {c}")
                if st.button(f"🗑️ 删除“{name}”", key=f"del_{name}"):
                    delete_disease(name)
                    st.success(f"✅ 已删除病害：{name}")
                    st.session_state["__refresh__"] = True
                    st.experimental_set_query_params(deleted="yes")

    # ✅ 强制白底样式
    st.markdown("""
        <style>
        textarea, input[type="text"] {
            background-color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
