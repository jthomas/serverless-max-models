# Model Asset eXchange + IBM Cloud Functions

This repo contains the instructions and scripts needed to run machine learning prediction models from the [Model Asset eXchange (MAX)](https://developer.ibm.com/exchanges/models/) on [IBM Cloud Functions](https://cloud.ibm.com/openwhisk) ([Apache OpenWhisk](https://openwhisk.apache.org/)).

MAX models [supporting deployment](https://developer.ibm.com/exchanges/models/all/?fa=date%3ADESC&fb=14525) are already published as [public images](https://hub.docker.com/u/codait) on Docker Hub. Augmenting these images to support the [Docker action interface](https://github.com/apache/incubator-openwhisk/blob/master/docs/actions-docker.md) used by Apache OpenWhisk means they can be executed as Apache OpenWhisk Actions. Apache OpenWhisk [Web Actions](https://github.com/apache/incubator-openwhisk/blob/master/docs/webactions.md) can be then be used to create the HTTP services to implement the prediction APIs.

## requirements

- [Docker](https://www.docker.com/)
- [Docker Hub account](https://hub.docker.com/)
- [IBM Cloud account](https://cloud.ibm.com/registration) 
- [IBM Cloud Functions CLI installed](https://cloud.ibm.com/openwhisk/learn/cli)

## usage

### build custom runtime images

- Set the following environment variables (`MODELS`) with MAX model names and run build script.
  - `MODELS`: MAX model names, e.g. `max-facial-emotion-classifier`
  - `USERNAME`: Docker Hub username.

```
MODELS="..." USERNAME="..." ./build.sh
```

This will create Docker images locally with the MAX model names and push to Docker Hub for usage in IBM Cloud Functions. IBM Cloud Functions only supports public Docker images as custom runtimes. 

### create actions using custom runtimes

- Create Web Action using custom Docker runtime.

```
ibmcloud wsk action create <MODEL_IMAGE> --docker <DOCKERHUB_NAME>/<MODEL_IMAGE> --web true -m 512
```

- Retrieve Web Action URL (`https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/<ACTION>`)

```
ibmcloud wsk action get <MODEL_IMAGE> --url
```

### invoke web action url with prediction api parameters

Use the same API request parameters as defined in the Prediction API specification with the Web Action URL. This will invoke model predictions and return the result as the HTTP response, e.g.

```
curl -F "image=@assets/happy-baby.jpeg" -XPOST <WEB_ACTION_URL>
```

*NOTE: The first invocation after creating an action may incur long cold-start delays due to the platform pulling the remote image into the local registry. Once the image is available in the platform, both further cold and warm invocations will be much faster.*

## models

The following MAX models have been tested with this library and can be confirmed as working...

### max-facial-emotion-classifier

- [Facial Emotion Classifier (`max-facial-emotion-classifier`)](https://developer.ibm.com/exchanges/models/all/max-facial-emotion-classifier/)

Here is an example of using this model. Start by creating the action using the custom runtime and then retrieve the Web Action URL.

```
$ ibmcloud wsk action create max-facial-emotion-classifier --docker <DOCKERHUB_NAME>/max-facial-emotion-classifier --web true -m 512
ok: created action max-facial-emotion-classifier
$ ibmcloud wsk action get max-facial-emotion-classifier --url
ok: got action max-facial-emotion-classifier
https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-facial-emotion-classifier
```

According to the [API definition](http://max-facial-emotion-classifier.max.us-south.containers.appdomain.cloud/) for this model, the prediction API expects a form submission with an image file to classify. Using a [sample image](https://github.com/IBM/MAX-Facial-Emotion-Classifier/blob/master/assets/happy-baby.jpeg) from the model repo, the model can be tested using curl.

```
$ curl -F "image=@happy-baby.jpeg" -XPOST https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-facial-emotion-classifier
```

```json
{
  "status": "ok",
  "predictions": [
    {
      "detection_box": [
        0.15102639296187684,
        0.3828125,
        0.5293255131964809,
        0.5830078125
      ],
      "emotion_predictions": [
        {
          "label_id": "1",
          "label": "happiness",
          "probability": 0.9860254526138306
        },
        ...
      ]
    }
  ]
}
```

#### performance

*Example Invocation Duration (Cold):* ~4.8 seconds

*Example Invocation Duration (Warm):* ~ 800 ms

### max-image-resolution-enhancer

- [Image Resolution Enhancer (`max-image-resolution-enhancer`)](https://developer.ibm.com/exchanges/models/all/max-image-resolution-enhancer/)

Here is an example of using this model. Start by creating the action using the custom runtime and then retrieve the Web Action URL.

```
$ ibmcloud wsk action create max-image-resolution-enhancer --docker <DOCKERHUB_NAME>/max-image-resolution-enhancer --web true -m 2048
ok: created action max-image-resolution-enhancer
$ ibmcloud wsk action get max-image-resolution-enhancer --url
ok: got action max-image-resolution-enhancer
https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-image-resolution-enhancer
```

According to the [API definition](http://max-facial-emotion-classifier.max.us-south.containers.appdomain.cloud/) for this model, the prediction API expects a form submission with an image file to classify. Using a [sample image](https://raw.githubusercontent.com/IBM/MAX-Image-Resolution-Enhancer/master/samples/test_examples/low_resolution/woman.png) from the model repo, the model can be tested using curl.

```
$ curl -F "image=@woman.png" -XPOST https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-facial-emotion-classifier > output.png
```

Opening the `output.png` should reveal the high-resolution version of the [sample image](https://raw.githubusercontent.com/IBM/MAX-Image-Resolution-Enhancer/master/samples/test_examples/low_resolution/woman.png).

#### performance

*Example Invocation Duration (Cold):* ~4.8 seconds

*Example Invocation Duration (Warm):* ~ 14 seconds

### max-human-pose-estimator

- [Human Pose Estimator (`max-human-pose-estimator`)](https://developer.ibm.com/exchanges/models/all/max-human-pose-estimator/)

Here is an example of using this model. Start by creating the action using the custom runtime and then retrieve the Web Action URL.

```
$ ibmcloud wsk action create max-human-pose-estimator --docker <DOCKERHUB_NAME>/max-human-pose-estimator --web true -m 512
ok: created action max-human-pose-estimator
$ ibmcloud wsk action get max-human-pose-estimator --url
ok: got action max-human-pose-estimator
https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-human-pose-estimator
```

According to the [API definition](https://github.com/IBM/MAX-Human-Pose-Estimator#3-use-the-model) for this model, the prediction API expects a form submission with an image file to classify. Using a [sample image](https://github.com/IBM/MAX-Human-Pose-Estimator/blob/master/assets/Pilots.jpg) from the model repo, the model can be tested using curl.

```
$ curl -F "file=@Pilots.jpg" -XPOST https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-human-pose-estimator
```

```json
{
  "status": "ok",
  "predictions": [
    {
      "human_id": 0,
      "pose_lines": [
        ...
      ],
      "body_parts": [
        ...
      ]
   }
    ...
}
```

#### performance

*Example Invocation Duration (Cold):* ~6 seconds

*Example Invocation Duration (Warm):* ~ 600 ms

### max-facial-age-estimator

- [Facial Age Estimator (`max-facial-age-estimator`)](https://developer.ibm.com/exchanges/models/all/max-human-pose-estimator/)

Here is an example of using this model. Start by creating the action using the custom runtime and then retrieve the Web Action URL.

```
$ ibmcloud wsk action create max-facial-age-estimator --docker <DOCKERHUB_NAME>/max-facial-age-estimator --web true -m 512
ok: created action max-facial-age-estimator
$ ibmcloud wsk action get max-facial-age-estimator --url
ok: got action max-facial-age-estimator
https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-facial-age-estimator
```

According to the [API definition](http://max-facial-age-estimator.max.us-south.containers.appdomain.cloud/) for this model, the prediction API expects a form submission with an image file to classify. Using a [sample image](https://raw.githubusercontent.com/IBM/MAX-Facial-Age-Estimator/master/assets/tom_cruise.jpg) from the model repo, the model can be tested using curl.

```
$ curl -F "image=@tom_cruise.jpg" -XPOST https://<REGION>.functions.cloud.ibm.com/api/v1/web/<NS>/default/max-facial-age-estimator
```

```json
{
  "status": "ok",
  "predictions": [
    {
      "age_estimation": 47,
      "detection_box": [
        0.147,
        0.3079667063020214,
        0.562,
        0.6813317479191439
      ]
    }
  ]
}
```

#### performance

*Example Invocation Duration (Cold):* ~7 seconds

*Example Invocation Duration (Warm):* ~500 ms

## issues

TensorFlow based models seem very memory hungry. Using larger images often needs the action memory increasing to the maximum 2 GB allowed and sometimes this is not enough. 