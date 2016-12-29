#!/usr/bin/env python

import os
from flask import Flask, render_template, request

from ocr import process_image_from_url, process_image_from_path


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder = tmpl_dir)
_VERSION = 1

ALLOWED_EXT = set(['jpg'])

@app.route('/')
def main():
    print 'home page'
    return render_template('index.html')


@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
@app.route('/ocr', methods=["POST"])
def ocr():
    url = str(request.form['image_url'])
    print 'url:', url
    # file = request.files['image_file']
    # print type(file)
    # print file
    #
    # if file.filename == '' and url == '':
    #     # nothing upload
    #     pass


    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

    if url:
        if 'jpg' in url:
            output = process_image_from_url(url)
            print output
            return render_template('index.html', output=output)
        else:
            return internal_error('only jpg pls')

    else:  # path
        # if file and allowed_file(file.filename):
        #     output = process_image_from_path(file)
        #     print output
        #     return render_template('index.html', output=output)
        # else:
        #     return internal_error('only jpg pls')
        print "error"


@app.errorhandler(500)
def internal_error(error):
    print str(error)

@app.errorhandler(404)
def not_found_error(error):
    print str(error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8111)
