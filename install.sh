#!/bin/bash -x

uname -a

echo $CREDENTIALS > credentials.json

# install tesseract v5 (without this, ubuntu only has v4)
sudo add-apt-repository -y ppa:alex-p/tesseract-ocr5

sudo apt-get update
sudo apt-get install -y gifsicle imagemagick tesseract-ocr tesseract-ocr-eng

# extract data from png
pip install opencv-python-headless numpy pandas

# version check
convert --version
tesseract --version

npm i
