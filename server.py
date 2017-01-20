#!/usr/bin/env python

import os
from flask import Flask, render_template, request

from ocr import process_image_from_url, process_image_from_file, clean
from redeem import driver_redeem


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
stat_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder = tmpl_dir)
_VERSION = 1

ALLOWED_EXT = set(['jpg'])
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT




@app.route('/')
def main():
    print 'home page'
    return render_template('index.html', url="./static/default.jpg")




@app.route('/ocrURL', methods=["GET", "POST"])
def ocr_url():
    if request.method == "POST":
        url = str(request.form['image_url'])
        print 'url:', url

        if url:
            if 'jpg' in url:
                output = process_image_from_url(url)
                return render_template('index.html', url_output=clean(output), url=url)
            else:
                return internal_error('only jpg pls')

    return render_template('index.html')


@app.route('/ocrFILE', methods=["GET", "POST"])
def ocr_file():
    if request.method == "POST":
        print len(request.files)
        file = request.files['image_file']
        print type(file)
        print file.content_type

        if file and allowed_file(file.filename):
            output = process_image_from_file(file)
            print output
            return render_template('index.html', file_output=clean(output))
        else:
            return internal_error('only jpg pls')

    return render_template('index.html')

@app.route('/redeemCode', methods=["GET", "POST"])
def redeem():
    my_email = str(request.form["my_email"])
    my_pwd = str(request.form["my_pwd"])
    my_code = str(request.form["my_code"])
    flag, feedback = driver_redeem(my_email, my_pwd, my_code)
    msg = "Current Points: {} | After Redeem Points: {}\n".format(feedback["current_point"], feedback["after_point"])
    if not flag:
        msg += feedback["redeem_error"]
    else:
        msg += feedback["redeem_success"]
    return render_template("index.html", msg=msg)

@app.errorhandler(500)
def internal_error(error):
    print str(error)
    return render_template('index.html', error=error)

@app.errorhandler(404)
def not_found_error(error):
    print str(error)
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8111)
