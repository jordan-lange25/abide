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
from module import splitter2,test1
import pandas as pd
from werkzeug.utils import secure_filename
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
UPLOAD_FOLDER = '/Users/jordanlange/Documents/projects/profitanalysis/uploads1'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['GET','POST'])
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


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user=session['user']


@app.route('/pricing')
def about():
    return render_template('pricing.html')


@app.route('/uploadoutput',methods=['GET'])
def uploadoutput():
    #pldf1=request.form.get('plfile')
    pldf1=pd.read_csv(request.form.get('plfile'),delimiter='\t')
    pldf=pd.DataFrame(pldf1)
    #transdf1=request.form.get('transfile')
    transdf1=pd.read_csv(request.form.get('transfile'),delimiter='\t')
    transdf=pd.DataFrame(transdf1)
    transdf_output=splitter2(transdf,pldf).to_html()
    return render_template('uploadoutput.html',table=transdf_output)




#----------
#Uploads
#----------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload',methods=['GET','POST'])
def upload(): 
    if request.method == 'POST':
         # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
            print("THIS IS THE FILENAME"+str(filename))
            file=pd.read_csv(str(filename)).to_html()
            return redirect(url_for('testoutput'))
    return render_template('upload.html')




#TEST - Create 2 pages. One that uploads the data and another that calls the request.files

@app.route('/testupload',methods=['GET'])
def testupload():
    #file=request.files['file']
    #fileoutput=pd.DataFrame(file).to_html()
    return render_template('upload.html')

@app.route('/testoutput',methods=['GET','POST'])
def testoutput():
    currentdir=os.curdir
    os.chdir(app.config['UPLOAD_FOLDER'])
    fileupload=pd.read_csv('transaction.csv')
    print(fileupload)
    #file=pd.DataFrame(fileupload).to_html()
    os.chdir(currentdir)
    return render_template('testoutput.html',file3=fileupload)



#TEST create the dataframe and pass the values by locating the uploaded file in local
@app.route('/upload2',methods=['GET','POST'])
def upload2():
    file=pd.read_csv('/Users/jordanlange/Documents/projects/profitanalysis/uploads1/transaction.csv')
    return render_template('uploadoutput.html',file3=file)
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
