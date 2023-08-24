from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from PIL import Image
import collections


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"


@app.route("/", methods=["POST", "GET"])
def home():

    file_list = os.listdir("static/uploads")
    for file in file_list:
        file_path = os.path.join("static/uploads", file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    if request.method == "POST" and request.files.get("imageUpload"):
        num_of_colors = int(request.form.get("color-num"))

        image = request.files["imageUpload"]
        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        for filename in os.listdir("static/uploads/"):
            image_path = os.path.join("static/uploads/", filename)


        img = Image.open(image_path)
        width, height = img.size
        total_pixels = width*height
        img = img.convert("RGB")
        pixels = img.getdata()

        color_counts = collections.Counter(pixels)
        img_path = image_path.split("/")[2]
        color_count = {}

        for y in range(height):
            for x in range(width):
                pixels_color =img.getpixel((x, y))
                color_count[pixels_color] = color_counts.get(pixels_color, 0) + 1
        color_percentages = {color: (count / total_pixels) * 100 for color, count in color_counts.items()}

        color_items = list(color_percentages.items())[:num_of_colors]
        print(color_items)
        return render_template("index.html", colors=color_items, ig=img_path)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
