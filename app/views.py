from flask import Flask,Response,render_template,request
import os
import cv2
from app.Face_recognition import FaceRecognition_Pipeline 
import matplotlib.image as implt

UPLOAD_FOLDER = 'static/upload'
def home():
    return render_template('index.html')

def app():
    return render_template('app.html')

def genderapp():
    if request.method=="POST":
        f = request.files['image_name']
        filename = f.filename
        # save image in the upload folder
        path = os.path.join(UPLOAD_FOLDER,filename)
        f.save(path)
        # get the predictions
        pred_image,pred=FaceRecognition_Pipeline(path)
        pred_filename = "prediction _image.jpg"
        cv2.imwrite(f'./static/predict/{pred_filename}',pred_image)
        # generate report
        report=[]
        for i,obj in enumerate(pred):
            gray_image = obj['roi']
            eigen_image = obj['eig_img'].reshape(100,100)
            gender = obj['prediction_name']
            score = round(obj['score']*100,2)

            # saving the image
            gray_image_name = f'roi_{i}.jpg'
            eigen_image_name = f'eigen_image{i}.jpg'
            implt.imsave(f'./static/predict/{gray_image_name}',gray_image,cmap='gray')
            implt.imsave(f'./static/predict/{eigen_image_name}',eigen_image,cmap='gray')

            # save report in the list
            report.append([gray_image_name,
                           eigen_image_name,
                           gender,
                           score])

        return render_template('gender.html',fileupload=True,report=report)#POST request
        
    return render_template('gender.html',fileupload=False)#GET Request