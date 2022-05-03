import os
from dotenv import load_dotenv, find_dotenv
from collections import Counter
from flask import Flask, render_template, request
from PIL import Image
from pytesseract import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.secret_key = os.getenv('secret_key')

possible_numbers = [25, 50, 100, 250, 500, 1000, 10_000, 100_000, 1_000_000]


def allowed_image(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def return_numbers(file):
    img = Image.open(file)
    numbers = pytesseract.image_to_string(img)
    lst = [int(i) for i in numbers.split()]
    return lst


def check_numbers(lst):
    for count in Counter(lst).values():
        if count >= 3:
            return True
    return False


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("index.html", error='No file part.')
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html", error='No selected file.')
        if allowed_image(file.filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], "image.jpg"))
            if check_numbers(return_numbers("static/images/image.jpg")):
                message = "This may be a winning ticket!"
            else:
                message = "Doesn't look like it.."
            os.remove("static/images/image.jpg")
            return render_template("index.html", message=message)
        else:
            return render_template("index.html", message="Invalid filetype, please use JPEG, JPG or PNG")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
