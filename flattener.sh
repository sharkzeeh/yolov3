#!/bin/sh
for var in "train" "val" "test"
do
    imgs="../wider/images/WIDER_${var}"
    find "${imgs}/images" -name "*.jpg" -exec mv -t "${imgs}" {} +
    rm -rf "${imgs}/images"
    ls -d ${imgs}/* > "data/${var}.txt"
done