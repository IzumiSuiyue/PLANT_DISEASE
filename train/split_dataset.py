import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

SOURCE_DIR = Path("PlantVillage")  # 你统一命名后的原始目录
OUTPUT_DIR = Path("data")          # 输出结构将是三层嵌套

for phase in ["train", "val"]:
    (OUTPUT_DIR / phase).mkdir(parents=True, exist_ok=True)

count = 0

for folder in SOURCE_DIR.iterdir():
    if folder.is_dir() and "_" in folder.name:
        parts = folder.name.split("_", 1)
        if len(parts) != 2:
            print(f"⚠️ 无法解析：{folder.name}")
            continue

        plant = parts[0]
        disease = parts[1]
        status = "healthy" if disease.lower() == "healthy" else "unhealthy"
        subclass = "healthy" if status == "healthy" else disease

        images = list(folder.glob("*.jpg"))
        if not images:
            print(f"⚠️ 无图像文件：{folder.name}")
            continue

        train_imgs, val_imgs = train_test_split(images, test_size=0.2, random_state=42)

        for phase, imgs in [("train", train_imgs), ("val", val_imgs)]:
            target = OUTPUT_DIR / phase / plant / status / subclass
            target.mkdir(parents=True, exist_ok=True)
            for img in imgs:
                shutil.copy(img, target / img.name)

        print(f"✅ 分类完成：{folder.name} → {plant}/{status}/{subclass}（共 {len(images)} 张）")
        count += 1

print(f"\n🎉 三层结构划分完成，共处理 {count} 个类别。")
