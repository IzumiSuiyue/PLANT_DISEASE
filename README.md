# 🌿 PLANT_DISEASE · 智能病虫害识别系统

这是一个基于深度学习的智能农业项目，结合图像识别和大语言模型技术，实现农作物病虫害的自动识别与诊断建议生成。用户可通过网页上传作物图像，获取识别结果、防治建议，支持问答查询与历史记录管理。

---

## 📦 项目结构说明

本项目包含以下模块：

- `train.py`：用于训练 ResNet18 模型（迁移学习）
- `split_dataset.py`：对原始数据集进行三层结构划分（作物 / 健康状态 / 病害类型）
- `flatten_dataset.py`：将三层结构“扁平化”为二层目录，适用于 ImageFolder 加载
- `model.pth`：训练完成后的模型参数
- `web_app.py`：基于 Streamlit 的前端入口
- `app/`：页面模块与功能模块（图像识别、问答、知识库、历史记录）
- `utils/`：包含历史记录数据库管理
- `models/`：保存训练好的模型文件
- `records/`：运行后自动生成，保存上传图像与识别记录

---

## ⚠️ 使用须知

> 本项目**未包含完整训练数据**，需自行下载数据集并执行数据预处理流程。

### 数据准备步骤：

1. 前往 [PlantVillage 数据集下载地址](https://www.kaggle.com/datasets/emmarex/plantdisease) 下载完整数据集；
2. 解压至项目根目录，重命名为 `PlantVillage`；
3. **删除本仓库 `data/` 下的 `train/` 与 `val/` 文件夹（仅为展示示例）**；
4. 依次运行以下脚本：

```bash
python split_dataset.py     # 三层结构划分
python flatten_dataset.py   # 二层结构转化，适用于模型训练
python train.py             # 开始训练模型，输出 models/model.pth
```

---

## 🚀 启动应用

确保已安装依赖包（建议使用 Python 3.10+ 环境）：

```bash
pip install -r requirements.txt
```

创建 `.env` 文件，添加你的 Qwen 接口密钥：

```env
DASHSCOPE_API_KEY=你的千问Key
```

启动 Streamlit 前端：

```bash
streamlit run web_app.py
```

---

## 🧠 项目功能总览

| 模块 | 功能说明 |
|------|----------|
| 🖼️ 病虫害识别助手 | 上传图像 → 模型预测 → 若非“健康”则调用大模型生成防治建议 |
| 🍓 病害问答助手   | 输入病害名 → 匹配本地知识库 / 千问生成推荐建议 |
| 📜 历史记录       | 分别记录识图与问答的历史，支持缩略图展示、删除单条或全部 |
| 📚 知识库助手     | 本地维护病害资料，支持添加、修改与删除 |

---

## 🧪 模型训练信息

- 模型结构：ResNet18（预训练）
- 数据增强：随机水平翻转、随机旋转、标准归一化
- 训练方式：冻结前几层，微调最后一层
- 精度目标：验证集 ≥ 85%

---

## 💬 鸣谢

- 本项目基于 [PlantVillage](https://www.kaggle.com/datasets/emmarex/plantdisease) 数据集
- 千问 Qwen 提供大模型问答与文本生成能力

---

