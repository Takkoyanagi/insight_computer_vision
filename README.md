# Project Title: Gym Equipment Decoder
Webapp to help guide users to short video tutorials from pictures of gym equipment taken on their mobile devices<br />
[Gym equipment decoder](http://computervisionclassifier.me) <br />
[Video presentation](https://www.youtube.com/watch?v=OmrdY8uHJoI)

## Introduction

![](readme/high_level_overview.png)
Working out is good for our health, but gyms can be intimidating with complicated machines. One solution is to hire a personal trainer, but personal trainers are expensive for someone who just want to start. To mitigate this problem, I developed Gym Equipment Decoder as my Insight Data Science project in less than 3 weeks that guides users to short video tutorials on how to use gym equipment properly and safely. 

## Data Product Architecture

![](readme/deployment.png)
Initially, fitness equipment image data was scraped using icrawler from google, bing, baidu images that were then fed into a CNN model. ResNet50 architecture was selected due to the low computation cost and high accuracy relative to other models (VGG16, Alexnet, ResNet152, ResNet-18, GoogLeNet). In addition, Inception V3 architecture was also investigated, however, I chose ResNet50 because Inception V3 had marginal improvement on accuracy (0.5 %), but was more computationally costly and I didn't want users waiting for their videos. The pre-trained ResNet50 model was used and transfer learning was applied that trained the last newly created fully connected layer for the 27 gym equipment categories. Both Tensorflow (Keras) and Pytorch frameworks were investigated, however, because Tensorflow had higher latency to start and required more memory when deployed on aws, Pytorch was used that had lower latency and required less memory to deploy on AWS EC2. Ultimately, The webapp was deployed using Flask, Nginx, Gunicorn and hosted on AWS. <br />

Lastly, the output of the ResNet50 model (category keywords) were fed to Youtube with "short video string identification syntax" concatenated and searched to give users video tutorials that are under 4 minutes on how to use the gym equipment of interest.

## Model Metrics

![](readme/metrics.png)
To this end, the image classification model performed well with 91 % accuracy for both test and validation sets. In addition to the overall accuracy of the model, accuracy of individual image classes were examined during model optimization that yielded greater than 85 % accuracy for all 27 categories. Next, metrics for the video recommender system, focused on accuracy of top 3 videos being relevant to the image input to the model. Specifically, top 3 videos were chosen because the user interface of Youtube allows for only 3 visible videos when there are advertisements that pushes videos down. With minor changes to searching keywords, 100 % of categories displayed 3 out of 3 relevant videos and 89 % of categories showed  2 out of 3 relevant videos.

## Conclusion
Web app, Gym equipment decoder was created and deployed to guide users to short video tutorial on how to use gym equipment safely and effectively using computer vision. 

### Let's go workout and be healthy together!

