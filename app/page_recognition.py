import streamlit as st
from PIL import Image
import os
from app.model_infer import predict_top3
from app.gpt_interface import get_advice
from utils.history_recorder import save_record

def recognition_tab():
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("🖼️ 病虫害识别")
    uploaded_file = st.file_uploader("📤 搭档！请在这里上传作物图像！", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image.resize((300, 300)), caption="🌿 上传图像缩略图", use_column_width=False)

            with st.spinner("🌱 搭档！让俺寻思寻思！"):
                top3 = predict_top3(image)
                top1_label, _ = top3[0]

                st.markdown("### 📈 Top 3 预测结果：")
                for label, prob in top3:
                    st.write(f"- **{label}**（置信度：{prob:.2%}）")

                if top1_label.split('__')[1].lower() == "healthy":
                    st.success("🍀 这株植物很健康喵！")
                    suggestion = ""
                else:
                    st.markdown("### 📋 防治建议（由 Qwen 智能体生成）")
                    suggestion = get_advice(top1_label)
                    st.write(suggestion)
                    st.success("🍀 搭档你放心，我们一定可以治好这株植物的！")

                save_record(
                    agent="recognition",
                    image=image,
                    result=top1_label,
                    advice=suggestion
                )

        except Exception as e:
            st.error(f"❌ 图像处理失败orz：{e}")
    st.markdown("</div>", unsafe_allow_html=True)
