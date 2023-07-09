# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# For downloading the image.
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
import io
import base64
from io import BytesIO
import numpy as np

# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub

# For measuring the inference time.
import time

from PIL import Image
from PIL import ImageOps
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont


from flask import Flask, request, Response, jsonify


app = Flask(__name__)


detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

def image_base64_to_input_format(image_data):
    imgdata = base64.b64decode(image_data)
    image = Image.open(BytesIO(imgdata))
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((1, im_height, im_width, 3)).astype(np.uint8)

def detection_loop(images_base64):
    bounding_boxes = []
    inf_times = []
    upload_times = []
    
    for image in images_base64:
        # decode image string:
        upload_start = time.time()
        image_tensor = image_base64_to_input_format(image)
        upload_end = time.time()

        start_time = time.time()
        result = detector(image_tensor)
        end_time = time.time()

        boxes = result["detection_boxes"]
        #print(boxes)
        result_list = []
        for box in boxes[0]:
            result_list.append(box.numpy().tolist())

        bounding_boxes.append(result_list)
        inf_times.append(end_time-start_time)
        upload_times.append(upload_end-upload_start)
        print("Done!")
    
    data = {"status": 200,
            "bounding_boxes": bounding_boxes,
            "inf_time": inf_times,
            "avg_inf_time": str(np.mean(inf_times)),
            "upload_time": upload_times,
            "avg_upload_time": str(np.mean(upload_times))}
    return jsonify(data)

#initializing the flask app
app = Flask(__name__)

#routing http posts to this method
@app.route('/api/detect', methods=['POST', 'GET'])
def main():
  data = request.get_json(force = True)
  #get the array of images from the json body
  imgs = data['images']
  
  return detection_loop(imgs)
  
# status_code = Response(status = 200)
#  return status_code
# image=cv2.imread(args.input)
# image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
