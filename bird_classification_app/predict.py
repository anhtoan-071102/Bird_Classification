import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import os

# Tên các lớp dựa trên thư mục dữ liệu huấn luyện
CLASS_NAMES = ['AMERICAN_GOLDFINCH', 'BARN_OWL', 'CARMINE_BEE_EATER', 
               'DOWNY_WOODPECKER', 'EMPORER_PENGUIN', 'FLAMINGO']

# Tải mô hình đã huấn luyện
def load_model(model_path=os.path.join(os.getcwd(), 'model', 'bird_classification_model_RN50.pth')):
    model = models.resnet50(weights='IMAGENET1K_V1')
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, len(CLASS_NAMES))
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

model = load_model()

# Các bước tiền xử lý hình ảnh
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Hàm dự đoán
def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # Chuyển đổi thành batch kích thước (1, 3, 224, 224)
    
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        class_name = CLASS_NAMES[predicted.item()]
    return class_name
