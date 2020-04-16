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
import dash
import dash_html_components as html
import dash_core_components as dcc

from module import splitter2,filetotable,groupdata,plwaterfall
#----------------------------------------------------------------------------#
# server Config.
#----------------------------------------------------------------------------#
UPLOAD_FOLDER = '/Users/jordanlange/Documents/projects/profitanalysis/uploads1'
ALLOWED_EXTENSIONS = {'csv'}
server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#----------------------------------------------------------------------------#
# Functions.
#----------------------------------------------------------------------------#




#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#pages

@server.route('/')
def login():
    return render_template('login.html')
@server.route('/home')
def home():
    return render_template('home.html')


@server.route('/login', methods=['GET','POST'])
def index():
    if request.method=='POST':
        session.pop('user',None)
        if request.form['password']=='password':
            session['user']=request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html')
@server.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not Logged in!'
@server.route('/logout')
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
@server.route('/upload',methods=['GET','POST'])
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
            plfilename = os.path.join(server.config['UPLOAD_FOLDER'], plfilename)
            transfilename = os.path.join(server.config['UPLOAD_FOLDER'], transfilename)
            plfile.save(plfilename)
            transfile.save(transfilename)
            return redirect(url_for('rawoutput'))
    return render_template('upload.html')

#pulls from the defined upload folder and converts to tables using predefined functions
@server.route('/rawoutput',methods=['GET','POST'])
def rawoutput():
    currentdir=os.curdir
    os.chdir(server.config['UPLOAD_FOLDER'])
    transfig=filetotable('transaction.csv')
    plfig=filetotable('pl.csv')
    os.chdir(currentdir)
    return render_template('rawoutput.html',pltable=plfig.to_html(),transtable=transfig.to_html())



@server.route('/analysis',methods=['GET'])
def analysis():
    #change directory to upload folder
    currentdir=os.curdir
    os.chdir(server.config['UPLOAD_FOLDER'])
    analysistable=splitter2('transaction.csv','pl.csv')
    analysistable.to_csv(os.path.join(server.config['UPLOAD_FOLDER'],r'allocation.csv'))
    fig=filetotable('allocation.csv').to_html()
    productfig=groupdata('allocation.csv','PartName','Profit').to_html()
    customerfig=groupdata('allocation.csv','CustomerName','Profit').to_html()
    plwaterfall1=plwaterfall('pl.csv').to_html()
    #Stacked bar figure showing where the biggest chunks are
    os.chdir(currentdir)
    return render_template('analysis.html',analysistable=fig,plwaterfall=plwaterfall1,productbar=productfig,customerbar=customerfig)

#Dash App allows users to explore the data themselves. 

@server.route('/explore')
def explore():
    return redirect('/explore/')
df=pd.read_csv('/Users/jordanlange/Documents/projects/profitanalysis/uploads1/pl.csv')
app = dash.Dash(
__name__,
server=server,
routes_pathname_prefix='/explore/'
) 
app.layout = html.Div([

    html.H3("Explore Your Transaction Data"),
    dcc.Graph(id='transaction-graph',
    figure={
        'data':[
            {'x':df['Account'],'y':df['Amount'],'type':'bar','name':'pl'}
            ],
        'layout':{
            'title':'Basic Dash Example'
            }
        })
])
   


# Error handlers.
@server.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@server.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if not server.debug:
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
    app.run_server(host='0.0.0.0', port=5000, debug=True)
