import os
import streamlit.components.v1 as components
from PIL import Image,ImageFile
import streamlit as st
import numpy as np
import requests
from io import BytesIO

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_component_square_filler_cropper101",
        url="http://localhost:8501",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_component_square_filler_cropper101", path=build_dir)

if not _RELEASE:
    _component_func = components.declare_component(
        "st_img_label",
        url="http://localhost:8501",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_component_square_filler_cropper101", path=build_dir)


def fill_square_cropper(img: Image.Image):
    imgsz = [img.height, img.width]

    original_size = imgsz

    smallestsize = min(imgsz)
    biggestsize = max(imgsz)

    #get vertical color filler
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    if img.height > img.width:
      #height is bigger than width
      area = (0, 0, img.width + (img.height - img.width),img.height)
      cropped_img = img.crop(area)
      newimgsz = [cropped_img.height, cropped_img.width]
    
      newimg = Image.new('RGB', ([newimgsz[1],newimgsz[0]]), (round(avg_color[0]), round(avg_color[1]), round(avg_color[2])))

      newpos = (img.height-img.width)
      newpos = newpos/2
      newimg.paste(img,(int(newpos),0))

      return newimg

    #vertically add color
    if img.width > img.height: 
      area = (0, 0, img.width, img.height+ (img.width - img.height))
      cropped_img = img.crop(area)
      newimgsz = [cropped_img.height, cropped_img.width]
    
      newimg = Image.new('RGB', ([newimgsz[1],newimgsz[0]]), (round(avg_color[0]), round(avg_color[1]), round(avg_color[2])))
 
      newpos = (img.width-img.height)
      newpos = newpos/2
      newimg.paste(img,(0,(int(newpos))))

      return newimg
