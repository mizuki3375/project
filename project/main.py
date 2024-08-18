from cgi import test
from flask import render_template, Flask, Response, Blueprint, request, session
import cv2
import numpy as np
import os 
from flask_sqlalchemy import SQLAlchemy
from .models import User
app = Flask(__name__)
main = Blueprint('main', __name__)
print(cv2.__version__)
from flask_login import login_required, current_user, login_user
# For each person, enter one numeric face id


@login_required
def picture(user_name):
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0
    count = 0
    
    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'kazuki', 'Paula', 'Ilza', 'Z', 'W'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    # Path = input("PATHを入力してください")
    Path = user_name
    while True:
       
        ret, img =cam.read()
        #img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                id = names[id]
                
                print(id)
                if Path == id:
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "no"
                    confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "no"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        if not test:
            break
        else:
            #フレームデータをjpgに圧縮
            ret, buffer = cv2.imencode('.jpg',img)
            # bytesデータ化
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

  

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    return render_template(user=current_user.name)
    




@main.route('/video_feed',methods=['GET'])
@login_required
def video_feed():
    # loginしているuserを取得
    user_name = current_user.name
    #imgタグに埋め込まれるResponseオブジェクトを返す
    return Response(picture(user_name=user_name), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/')
@login_required
def index2():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name   )
@main.route('/index', methods=['GET'])
@login_required
def index():
   
   user = {'username': 'FZ50'}
   return render_template('index2.html', title='home', user=current_user.name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)