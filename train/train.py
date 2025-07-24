# train.py

import os
import torch
from torchvision import transforms, datasets, models
from torch import nn, optim
from torch.utils.data import DataLoader
import sys

# 训练参数和数据路径
DATA_DIR = "data"
MODEL_PATH = "models/model.pth"
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-4

# 图像预处理
train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])
val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 加载数据集
train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=train_transforms)
val_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), transform=val_transforms)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

# 获取类别信息和设置设备
class_names = train_dataset.classes
num_classes = len(class_names)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载预训练的ResNet18模型并修改最后一层
model = models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=LR)

#  训练循环，手动打印进度
for epoch in range(EPOCHS):
    model.train() # 训练模式
    running_loss = 0.0
    total_batches = len(train_loader)

    print(f"\n🌿 Epoch {epoch+1}/{EPOCHS} 开始训练...")
    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        # 手动打印进度条
        percent = int((i + 1) / total_batches * 100)
        bar = "█" * (percent // 4) + "-" * (25 - percent // 4)
        sys.stdout.write(f"\r[{bar}] {percent}% | 当前 loss: {loss.item():.4f}")
        sys.stdout.flush()

    print(f"\n✅ Epoch {epoch+1} finished. Total loss: {running_loss:.4f}")

# 保存模型
os.makedirs("models", exist_ok=True)
torch.save(model.state_dict(), MODEL_PATH)
print(f"\n🎉 模型训练完成并保存到 {MODEL_PATH}")
print(f"📦 类别数：{num_classes}")
print("🌿 所有类别名：")
print(class_names)

