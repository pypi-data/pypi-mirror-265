<img src="misc/logo.jpg" alt="FastANPR logo" style="width:100%;">

[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/merge.yaml/badge.svg)](https://github.com/arvindrajan92/fastanpr/actions)
[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/merge_macos.yaml/badge.svg)](https://github.com/arvindrajan92/fastanpr/actions)
[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/merge_raspbian.yaml/badge.svg)](https://github.com/arvindrajan92/fastanpr/actions)
[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/merge_windows.yaml/badge.svg)](https://github.com/arvindrajan92/fastanpr/actions)
[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/push.yaml/badge.svg)](https://github.com/arvindrajan92/fastanpr/actions)
[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/publish.yaml/badge.svg)](https://github.com/arvindrajan92/fastanpr/actions)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/arvindrajan92/fastanpr)](https://github.com/arvindrajan92/fastanpr/releases)
[![Python Versions](https://img.shields.io/badge/python-3.8%20to%203.11-blue)](https://www.python.org/downloads/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/arvindrajan92/fastanpr?style=social)](https://github.com/arvindrajan92/fastanpr)

## Introduction
A fast *automatic number-plate recognition* (ANPR) library. This package employs [YOLOv8](https://github.com/ultralytics/ultralytics), a lightweight model, for detection, and [Paddle OCR](https://github.com/PaddlePaddle/PaddleOCR), a lightweight *optical character recognition* (OCR) library, for recognizing text in detected number plates.
![Example outputs](misc/sample.png)

## Installation
You can install the package using pip:
```bash
pip install fastanpr
```
### Requirements
- Windows:
  - Python >=3.8, <3.11
- Ubuntu, macOS, Raspbian:
  - Python >=3.8, <3.12

## Usage
```python
import cv2
from fastanpr import FastANPR

# Create an instance of FastANPR
fast_anpr = FastANPR()

# Load images (images should be of type numpy ndarray)
files = [...]
images = [cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB) for file in files]

# Run ANPR on the images
number_plates = await fast_anpr.run(images)

# Print out results
for file, plates in zip(files, number_plates):
    print(file)
    for plate in plates:
        print("Plate Attributes:")
        print("Detection bounding box:", plate.det_box)
        print("Detection confidence:", plate.det_conf)
        print("Recognition text:", plate.rec_text)
        print("Recognition polygon:", plate.rec_poly)
        print("Recognition confidence:", plate.rec_conf)
        print()
    print()
```
### Class: FastANPR

#### Methods

##### run(images: List[np.ndarray] -> List[List[NumberPlate]]

Runs ANPR on a list of images and return a list of detected number plates.

- **Parameters:**
  - `images` (List[np.ndarray]): A list of images represented as numpy ndarray.

- **Returns:**
  - `List[List[NumberPlate]]`: A list of detected number plates for every image.

### Class: NumberPlate

#### Attributes

- `det_box` (List[int]): Bounding box coordinates of detected number plate.
- `det_conf` (float): Confidence score of number plate detection.
- `rec_text` (str): Recognized plate number.
- `rec_poly` (List[List[int]]): Polygon coordinates of detected texts.
- `rec_conf` (float): Confidence score of recognition.

## FastAPI
To start a FastAPI server locally from your console:
```bash
uvicorn api:app
```
### Usage
```python
import base64
import requests

# Step 1: Read the image file
image_path = 'tests/images/image001.jpg'
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

# Step 2: Convert the image to a base64 encoded string
base64_image_str = base64.b64encode(image_data).decode('utf-8')

# Prepare the data for the POST request (assuming the API expects JSON)
data = {'image': base64_image_str}

# Step 3: Send a POST request
response = requests.post(url='http://127.0.0.1:8000/recognise', json=data)

# Check the response
if response.status_code == 200:
    # 'number_plates': [
    #       {
    #           'det_box': [682, 414, 779, 455], 
    #           'det_conf': 0.29964497685432434, 
    #           'rec_poly': [[688, 420], [775, 420], [775, 451], [688, 451]], 
    #           'rec_text': 'BVH826', 
    #           'rec_conf': 0.940690815448761
    #       }
    # ]
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}.")
```

## Docker
Hosting a FastAPI server can also be done by building a docker file as from console:
```bash
docker build -t fastanpr-app .
docker run -p 8000:8000 fastanpr-app
```

## Licence
This project incorporates the YOLOv8 model from Ultralytics, which is licensed under the AGPL-3.0 license. As such, this project is also distributed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) to comply with the licensing requirements.

For more details on the YOLOv8 model and its license, please visit the [Ultralytics GitHub repository](https://github.com/ultralytics/ultralytics).

## Contributing

We warmly welcome contributions from the community! If you're interested in contributing to this project, please start by reading our [CONTRIBUTING.md](CONTRIBUTING.md) guide.

Whether you're looking to submit a bug report, propose a new feature, or contribute code, we're excited to see what you have to offer. Please don't hesitate to reach out by opening an issue or submitting a pull request.

Thank you for considering contributing to our project. Your support helps us make the software better for everyone.