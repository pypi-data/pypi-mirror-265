from ultralytics import YOLO
import cv2

model_for_boxes = YOLO('model/Pg2Blb.pt')
model_for_words = YOLO('model/Blb2Wrd.pt')

class FindTextBoxes:
    def get_textboxes_from_image(pth):
      '''

        Function for getting coordinates for textboxes uning YOLO model

        Args:

          pth (str): Path for image

        Returns:

          box_arr: List of co-ordinates of text-boxes (x-min, y-min, x-max, y-max)

      '''
      box_arr = []
      textboxes = model_for_boxes([pth])
      for result in textboxes:
        txt_bxs = result.boxes
      for box in txt_bxs:
        b = box.xyxy[0]
        b = b.tolist()
        box_arr.append(b)
      return box_arr 

class FindWordBoxes:
    def get_words_from_image(img):
      '''

        Marks words from text blobs

        Args:

          img (Image) : Blob image source/Path

        Returns:

          wrdbx_arr: array of bounding boxes around words

      '''
      wrdbx_arr = []
      results = model_for_words([img])
      for result in results:
        wordboxes = result.boxes
      for wbox in wordboxes:
        wb = wbox.xyxy[0]
        wb = wb.tolist()
        wrdbx_arr.append(wb)
      return wrdbx_arr

class FindCharBoxes:
    def get_chars_from_word(spc):
      '''

        Function to get individual characters from word image

        Args:

          spc (Image): Image of word (converted to dtype = uint8)

        Returns:

          list_im: List having individual images of characters

      '''
      list_im = []
      gray = cv2.cvtColor(spc, cv2.COLOR_BGR2GRAY)
      _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
      contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
      bbox_cnt = create_bouding_box(contours)
      for cr in bbox_cnt:
          x, y, w, h = cr[0], cr[1], cr[2], cr[3]
          if x>2:
            left = x - 2
          else:
            left = x
          right = x + w + 2
          top = y - 2
          bottom = y + h + 2
          s_i = spc[top:bottom, left:right]
          list_im.append(s_i)
      return list_im