import cv2
import json
from PIL import Image
from keras.preprocessing import image

class Utilities:
  def sort_bounding_box(pth, bbox):
    '''

      Utility function to sort bounding boxes in the Cartesian Plane wrt image

      Args:

        pth (str): Path of the image file
        bbox (List): List of bounding boxes for each text blob

      Returns:

        sorted_bbx: List of sorted bounding boxes

    '''
    img1 = Image.open(pth)
    wd = img1.width
    sorted_bbx = sorted(bbox, key = lambda fxy: fxy[0] + fxy[1]*wd)
    return sorted_bbx

  def crop_textboxes_from_image(coords, pth):
    '''
  
      Function to crop textboxes from images.
  
      Args:
  
       cooords (List[x-min, y-min, x-max, y-max]): Co-ordinates of text boxes
       pth (str): Path of the image
  
      Returns:
  
        crop_im: cropped image of text box
  
    '''
    img1 = image.load_img(pth, grayscale = False)
    img1 = image.img_to_array(img1, dtype='uint8')
    x = int(coords[0])
    y = int(coords[1])
    w = int(coords[2])
    h = int(coords[3])
    crop_im = img1[y:h, x:w]
    return crop_im

  def crop_words_from_image(xyxy, img):
    '''

      Crops the word boxes from blob image.

      Args:

        xyxy (List[x-min, y-min, x-max, y-max]): Co-ordinates of bounding box
        img (Image): Image source converted to dtype = 'uint8'

      Returns:

        word: Cropped image of word (converted to uint8 type)

    '''
    x1, y1, x2, y2 = xyxy
    left = int(x1)
    right = int(x2)
    top = int(y1)
    bottom = int(y2)
    word = img[top:bottom, left:right]
    return word

  def create_bouding_box(cntrs):
    '''
  
      Utility function to create bounding boxes around contours
  
      Args:
  
        cntrs (List): List of contours from cv2.findContours()
  
      Returns:
  
        bbox_lst: List of bounding boxes for each contour (x-min, y-min, width, height)
  
    '''
    bbox_lst = []
    for cntr in cntrs:
      x, y, w, h = cv2.boundingRect(cntr)
      t = (x,y,w,h)
      bbox_lst.append(t)
    return bbox_lst

  def LabelIndexer():
    '''

      Utility function to create dictionary for labels of classes

      Args: None

      Returns:

          an_dc: dictionary of labels to classes

    '''
    an_dc = {}
    ind_lbl = 0
    f = open('IsoOCR/annotations.json')
    m_data = json.load(f)
    for en in m_data:
      if en['label'] not in an_dc.keys():
        an_dc[en['label']] = ind_lbl
        ind_lbl = ind_lbl + 1
    return an_dc

  def LabeltoClass(tup):
    '''

      Utility function to map prediction to class

      Args:

        tup(int): Return from character recognizer model

      Returns:

        Letter (int): Letter index as per mapping used

    '''
    vocab = LabelIndexer()
    if tup in vocab.keys():
      Letter = torch.tensor(vocab[tup])
      return Letter

  def vocab_list():
    '''

      Function to generate mapping from alphabet to letter index

      Args: None

      Returns:

        alp_dict (dict): Dictionary to hold index to character mapping

    '''
    alp_dict = {}
    strn = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,;:?!.@#$%&()}{[]'
    for i in range(len(strn)):
      alp_dict[str(i+1)] = strn[i]
    return alp_dict

  def replace_substrings(word, combinations, replacement):
    '''

      Utility function to rectify minor corrections

    '''
    for combination in combinations:
      if combination in word:
        word = word.replace(combination, replacement)
        return word
    return word

  def rectify_word(word):
    '''

      Utility function to rectify minor corrections

    '''
    combs = [',.', '.,', ',,']
    replacement = 'i'
    wrd = replace_substrings(word, combs, replacement)
    return wrd

  def make_subarrays(arr):
    '''

      Utility function to sort words by line in a blob

        Args:

          arr (List): List of bounding box coordiates for each word

        Returns:

          subarrays (List): List of list containing words in each line (nested list)

    '''
    subarrays = []
    start = 0
    end = 0
    for i in range(len(arr)):
      if i == 0:
        start = 0
        end = 0
      elif arr[i][5] - arr[i-1][5] <= 1:
        end = i
      else:
        subarrays.append(arr[start:end+1])
        start = i
        end = i
    subarrays.append(arr[start:end+1])
    return subarrays

  def sort_words(wrd_arr):
    '''
  
      Utility function to sort words in order within a blob
  
      Args:
  
        wrd_arr (List): List of bounding boxes of words within a blob
  
      Returns:
  
        fnwords (List): List of organized words within a blob
  
    '''
    lsts = []
    for it in wrd_arr:
      x1, y1, x2, y2, = it
      x1 = int(x1)
      x2 = int(x2)
      y1 = int(y1)
      y2 = int(y2)
      cx = (x2 + x1)/2
      cy = (y2 + y1)/2
      rank = cy*600 + cx
      line = int(y1/10)
      lsts.append([x1, y1, x2, y2, rank, line])
    lsts = sorted(lsts, key = lambda x:x[4])
    ss = make_subarrays(lsts)
    sorts = []
    for item in ss:
      inlnwrd = sorted(item, key = lambda x:x[0])
      sorts.append(inlnwrd)
    fnwords = []
    for i in range(len(sorts)):
      line = sorts[i]
      for j in range(len(line)):
        word = line[j]
        fnwords.append(word[:4])
    return fnwords