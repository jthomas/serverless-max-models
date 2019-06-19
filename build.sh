#!/bin/bash

set -e -u

for model in $MODELS; do
  echo "Building $model runtime image"
  docker build -t $model --build-arg model=$model .
  echo "Pushing $model to Docker Hub"
  docker tag $model $USERNAME/$model
  docker push $USERNAME/$model
done 
