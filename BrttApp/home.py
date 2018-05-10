from flask import Flask, render_template, request
from rlogic import rlogic_fun
import os
import datetime

app = Flask(__name__)

@app.route('/')
def upload_file():
	return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		f = request.files['file']
        email_id = request.form['email']
        esn = request.form['esn']
	fname = "/var/tmp" + datetime.datetime.now().isoformat() + f.filename
        print fname
	f.save(fname)
        result = rlogic_fun(fname,email_id,esn)
        cleanupxlsx = "rm *.xlsx"
        os.system(cleanupxlsx)
        cleanupxls = "rm *.xls"
        os.system(cleanupxls)
	return render_template('success.html',fname = result[2],success=result[0],failure=result[1])

if __name__ == '__main__':
	app.run()
