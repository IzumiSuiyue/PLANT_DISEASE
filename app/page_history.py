import streamlit as st
from utils.history_recorder import load_records, delete_record, delete_all
from PIL import Image
import os

def history_tab():
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📜 历史记录")

    agent_tab = st.radio("🧠 请选择记录类型", ["🌿 病虫害识别", "🍓 病害问答"])

    if agent_tab == "🌿 病虫害识别":
        records = load_records("recognition")
        if not records:
            st.info("暂无识图记录 orz")
        else:
            if st.button("🗑️ 删除全部识别记录"):
                delete_all("recognition")
                st.success("已删除全部识别记录。")
                st.rerun()
            for record in records:
                st.markdown("---")
                col1, col2 = st.columns([1, 3])
                with col1:
                    if os.path.exists(record["image_path"]):
                        img = Image.open(record["image_path"])
                        st.image(img.resize((100, 100)), caption="缩略图")
                    else:
                        st.warning("找不到图片")
                with col2:
                    st.markdown(f"**预测结果：** {record['result']}")
                    if record["advice"]:
                        st.markdown(f"**建议：** {record['advice']}")
                    if st.button("删除这条记录", key=f"del_{record['id']}"):
                        delete_record(record["id"])
                        st.success("已删除")
                        st.rerun()

    elif agent_tab == "🍓 病害问答":
        records = load_records("qa")
        if not records:
            st.info("暂无问答记录喵")
        else:
            if st.button("🗑️ 删除全部问答记录"):
                delete_all("qa")
                st.success("已删除全部问答记录。")
                st.rerun()
            for record in records:
                st.markdown("---")
                st.markdown(f"**问题：** {record['question']}")
                st.markdown(f"**回答：** {record['advice']}")
                if st.button("删除这条记录", key=f"del_qa_{record['id']}"):
                    delete_record(record["id"])
                    st.success("已删除")
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
