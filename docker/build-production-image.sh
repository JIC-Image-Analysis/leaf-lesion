#!/bin/bash

IMAGE_NAME="leaf-lesion-production"

cp ../requirements.txt $IMAGE_NAME
tar -zcvf $IMAGE_NAME/scripts.tar.gz -C ../ scripts
sleep 1
cd $IMAGE_NAME
docker build --no-cache -t $IMAGE_NAME .
rm requirements.txt
rm scripts.tar.gz
cd ../
