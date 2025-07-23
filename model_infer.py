import torch
from torchvision import models, transforms
from PIL import Image

# 模型路径
MODEL_PATH = "models/model.pth"

# 类别标签（根据你训练模型时使用的类别顺序）
class_names = [
    'Pepper__unhealthy__bell_BacterialSpot',
    'Pepper__unhealthy__bell_healthy',
    'Potato__healthy__healthy',
    'Potato__unhealthy__EarlyBlight',
    'Potato__unhealthy__LateBlight',
    'Tomato__healthy__healthy',
    'Tomato__unhealthy__BacterialSpot',
    'Tomato__unhealthy__EarlyBlight',
    'Tomato__unhealthy__LateBlight',
    'Tomato__unhealthy__LeafMold',
    'Tomato__unhealthy__SeptoriaLeafSpot',
    'Tomato__unhealthy__SpiderMites',
    'Tomato__unhealthy__TargetSpot',
    'Tomato__unhealthy__YellowLeafCurlVirus',
    'Tomato__unhealthy__mosaic_virus'
]

# 图像预处理流程
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 初始化模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

# 推理函数：返回 Top 3
def predict_top3(image: Image.Image):
    image_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)[0]
        top3 = torch.topk(probs, k=3)
        return [(class_names[i], probs[i].item()) for i in top3.indices]
