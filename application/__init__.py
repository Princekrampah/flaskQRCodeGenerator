from flask import Flask
import os
from flask_dropzone import Dropzone


app = Flask(__name__)
app.config['SECRET_KEY'] = "JLK24JO3I@!!$#Yoiouoln!#@oo=5y9y9youjuy952ou9859u923kjfhiy23ho"

dir_path = os.path.dirname(os.path.realpath(__file__))


app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'decoded'

dropzone = Dropzone(app)


from application import routes