import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
# Use a pipeline as a high-level helper
from transformers import pipeline
import os

from sentence_transformers import SentenceTransformer, util

pipe = pipeline("image-classification", model="google/vit-base-patch32-384")

feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch32-384')
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch32-384")

images = []
names = []
dir = 'test_data'
for name in os.listdir(dir):
    path = os.path.join(dir, name)
    image = Image.open(path)
    images.append(image)
    names.append(name)

print('image size :', len(images))
inputs = feature_extractor(images=images, return_tensors="pt")

outputs = model(**inputs)

logits = outputs.logits

features = []
for logit in logits:
    features.append(logit.resize(1, 1000))
    # model predicts one of the 1000 ImageNet classes
    predicted_class_idx = logit.argmax(-1).item()
print('features[0]:', features[0].shape)
feature_save = torch.concat(features)
print('feature_save.shape:', feature_save.shape)

hits = util.semantic_search(features[0], feature_save, top_k=10)
for it in hits[0]:
    print(names[it['corpus_id']])
