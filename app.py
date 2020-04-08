#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template,request, session, url_for,escape, request, redirect,g
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
#from forms import *
import os
import sys
from module import splitter2
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

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
    session.pop('diagnosticvisit')
    return render_template('logout.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user=session['user']


@app.route('/pricing')
def about():
    return render_template('pricing.html')

@app.route('/upload')
def upload():
    return render_template ('upload.html')
@app.route('/uploadoutput')
def uploadoutput():
    pldf=request.args.get('plfile')
    transdf=request.args.get('transfile')
    transdf_output=splitter2(transdf,pldf).to_html()
    return render_template('uploadoutput.html',table=transdf_output)


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
