from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import numpy as np

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from io import BytesIO
import io
import os
import streamlit as st
import requests
    
subscription_key = '42f6fb25ddea41638ac14d6c948c5431'
endpoint = 'https://20211212test-kengo.cognitiveservices.azure.com/'
 
st.title('物体検出アプリ')

uploaded_file = st.file_uploader("choose an image . . . ", type='jpg')
if uploaded_file is not None:
        
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'model-version': 'latest',
    })
    
    img = Image.open(uploaded_file)
    
    #バイナリ取得
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() 
    # Open local image file
    #local_image = open(uploaded_file.name, 'rb')
    
    conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v3.2/detect?%s" % params,binary_img, headers)
    response = conn.getresponse()
    response = json.load(response) #byte型から辞書型にする
    response = response['objects']

    # Print results of detection with bounding boxes
    print("Detecting objects in local image:")
    if len(response) == 0:
        print("No objects detected.")
                  
    draw = ImageDraw.Draw(img)

    #リストから辞書型へ取り出し
    for object in response:
        #物体の要素の取り出し
        #print(object.get("object"))
        #物体の位置の取り出し
        rect = object.get("rectangle")
        
        #物体を矩形で囲む
        draw.rectangle([(rect['x'], rect['y'] + rect['h']),(rect['x'] + rect['w'],rect['y'])], fill=None, outline='green', width=4)
        txpos = (rect['x'], rect['y']-14-4//2)
        txw,txh = draw.textsize(object.get("object"))
        draw.rectangle([txpos, (rect['x']+txw, rect['y'])], outline='green', fill='green', width=4)
        draw.text((rect['x'], rect['y']-14-4//2),object.get("object"), fill='white')
    
    
    st.image(img,caption='Uploaded Image.', use_column_width=True)