from application import app, dropzone
from flask import render_template, request, redirect, url_for
from .forms import QRCodeData
import secrets
import cv2
import os
import qrcode

decoded_info = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        global decoded_info
        f = request.files.get('file')
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".png"
       

        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)
        f.save(file_location)

        print(file_location)
        # read and decode QRCode
        img = cv2.imread(file_location)

        det=cv2.QRCodeDetector()

        val, pts, st_code=det.detectAndDecode(img)
        print(val)
        
        os.remove(file_location)
        decoded_info = val
       
    else:
       return render_template("upload.html", title="Home")

@app.route("/decoded")
def decoded():
    global decoded_info
    return render_template("decoded.html", title="Decoded", data=decoded_info)


@app.route("/generate_qrcode", methods=["GET", "POST"])
def generate_qrcode():
    form =QRCodeData()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data.data
            image_name = f"{secrets.token_hex(10)}.png"
            qrcode_location = f"{app.config['UPLOADED_PATH']}/{image_name}"
            
            try:
                my_qrcode = qrcode.make(str(data))
                my_qrcode.save(qrcode_location)
            except Exception as e:
                print(e)

        return render_template("generated_qrcode.html", title="Generated", image=image_name)

    else:
        return render_template("generate_qrcode.html", title="Generate", form=form)
