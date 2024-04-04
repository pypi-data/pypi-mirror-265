import torch
from torchvision import transforms
from PIL import Image

from IcoOCR.CharModel import CNNModel
from IsoOCR.util import Utilities

model = CNNModel()
model = torch.load('IsoOCR/OCR1.pth')

class CharPredictions:

    def predict_char_from_image(img):
      '''

        Function to recieve character image and predict its class.

        Args:

          img(Image): Image from character fider

        Returns:

          Char: Character from image based on model prediction

      '''
      transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
      ])
      model_for_chars.eval()
      vocab = Utilities.LabelIndexer()
      image = Image.fromarray(img)
      image = transform(image)
      image = image.unsqueeze(0)
      output = model_for_chars(image)
      _, predicted = torch.max(output.data, 1)
      out = predicted.item()
      hh = list(vocab.keys())[list(vocab.values()).index(out)]
      alp_dict = Utilities.vocab_list()
      return alp_dict[hh]