#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template,request, session, url_for,escape, request, redirect,g,flash, request, redirect
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
#from forms import *
import os
import sys

import pandas as pd
from werkzeug.utils import secure_filename


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
UPLOAD_FOLDER = '/Users/jordanlange/Documents/projects/profitanalysis/uploads1'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#----------------------------------------------------------------------------#
# Functions.
#----------------------------------------------------------------------------#
from module import splitter2,filetotable,groupdata



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#pages

@app.route('/')
def login():
    return render_template('login.html')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET','POST'])
def index():
    if request.method=='POST':
        session.pop('user',None)
        if request.form['password']=='password':
            session['user']=request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not Logged in!'
@app.route('/logout')
def dropsession():
    session.pop('user', None)
    return render_template('logout.html')


#----------
#Uploads
#----------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#uploads the files by their form names to a pre-defined os location ("uploads1")
@app.route('/upload',methods=['GET','POST'])
def upload(): 
    if request.method == 'POST':
         # check if the post request has the file part
        if 'plfile' not in request.files and 'transfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        plfile = request.files['plfile']
        transfile=request.files['transfile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if plfile.filename == '' and transfile.filename=='':
            flash('No selected file')
            return redirect(request.url)
        if plfile and transfile and allowed_file(plfile.filename) and allowed_file(transfile.filename):
            plfilename = secure_filename(plfile.filename)
            transfilename=secure_filename(transfile.filename)
            plfilename = os.path.join(app.config['UPLOAD_FOLDER'], plfilename)
            transfilename = os.path.join(app.config['UPLOAD_FOLDER'], transfilename)
            plfile.save(plfilename)
            transfile.save(transfilename)
            return redirect(url_for('rawoutput'))
    return render_template('upload.html')

#pulls from the defined upload folder and converts to tables using predefined functions
@app.route('/rawoutput',methods=['GET','POST'])
def rawoutput():
    currentdir=os.curdir
    os.chdir(app.config['UPLOAD_FOLDER'])
    transfig=filetotable('transaction.csv')
    plfig=filetotable('pl.csv')
    os.chdir(currentdir)
    return render_template('rawoutput.html',pltable=plfig.to_html(),transtable=transfig.to_html())



@app.route('/analysis',methods=['GET'])
def analysis():
    #change directory to upload folder
    currentdir=os.curdir
    os.chdir(app.config['UPLOAD_FOLDER'])
    analysistable=splitter2('transaction.csv','pl.csv')
    analysistable.to_csv(os.path.join(app.config['UPLOAD_FOLDER'],r'allocation.csv'))
    fig=filetotable('allocation.csv').to_html()
    productfig=groupdata('allocation.csv','PartName','Profit').to_html()
    customerfig=groupdata('allocation.csv','CustomerName','Profit').to_html()
    os.chdir(currentdir)
    return render_template('analysis.html',analysistable=fig,productbar=productfig,customerbar=customerfig)


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)
