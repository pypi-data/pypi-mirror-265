from ultralytics import YOLO
import torch
import json
import os
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms
from keras.preprocessing import image
import cv2
import numpy as np

from IsoOCR.CharModel import CNNModel
from IsoOCR.modelForBoxes import FindTextBoxes, FindWordBoxes, FindCharBoxes
from IsoOCR.utils import Utilities
from IsoOCR.CharPredictor import CharPredictions

class OCR:

    def get_text_from_image(im_lst):
      '''

        Function to read words from image by character

        Args:

          im_list (List): List of images of characters

        Returns:

          wrd (str): Recognised word from image

      '''
      wrd = ''
      for chr in im_lst:
        ous = CharPredictions.predict_char_from_image(chr)
        wrd = wrd + ous
      wrd = Utilities.rectify_word(wrd)
      return wrd

    def get_words_from_blob(img):
      '''

        Function to create text blobs based on blob boundary boxes.

        Args:

          img (Image): Cropped image of text blob (dtype = 'uint8')

        Returns:

          s_data (str): String data from blob

      '''
      cntrs = FindWordBoxes.get_words_from_image(img)
      cntrs = Utilities.sort_words(cntrs)
      s_data = ''
      for cntr in cntrs:
        try:
          img1 = Utilities.crop_words_from_image(cntr, img)
          w_ltr = FindCharBoxes.get_chars_from_word(img1)
          wrd = get_text_from_image(w_ltr)
          s_data = s_data + wrd + ' '
        except:
          print('failed to recog')
          pass
      return s_data

    def read_text_from_image(pth):
      '''
        Main function to read parse the image path to get text from it.

        Args:

          pth (str): Path of the image

        Returns:

          data (str): Recognized text from image by the OCR model.

      '''
      data = []
      arr = FindTextBoxes.get_textboxes_from_image(pth)
      arr = Utilities.sort_bounding_box(pth, arr)
      for item in arr:
        img1 = Utilities.crop_textboxes_from_image(item, pth)
        blb_dt = get_words_from_blob(img1)
        data.append(blb_dt)
      return data