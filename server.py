#!/usr/bin/env python

import os
from flask import Flask, render_template, request

from ocr import process_image_from_file
from redeem import driver_redeem


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
stat_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder = tmpl_dir)
app.config['UPLOAD_FOLDER']='uploads'
_VERSION = 1

ALLOWED_EXT = set(['jpg'])
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXT




@app.route('/')
def main():
    print 'home page'
    return render_template('index.html', url="./static/default.jpg")




@app.route('/ocrURL', methods=["GET", "POST"])
def ocr_url():
    if request.method == "POST":
        url = str(request.form['image_url'])
        print 'url:', url

        if url and allowed_file(url):
            filename = "temp_url"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # process the file
            output = process_image_from_file(filename, folder=app.config['UPLOAD_FOLDER'])


            return render_template('index.html', url_output=output, url=url)


    return render_template('index.html')


@app.route('/ocrFILE', methods=["GET", "POST"])
def ocr_file():
    if request.method == "POST":
        print len(request.files)
        file = request.files['image_file']
        # print type(file)
        # print file.content_type

        if file and allowed_file(file.filename):
            # save the file
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # process the file
            output = process_image_from_file(filename, folder=app.config['UPLOAD_FOLDER'])

            # print output
            return render_template('index.html', file_output=output)
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
