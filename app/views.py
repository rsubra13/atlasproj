"""
    This script contains various views of Atlassian Parse Application

    views
    ```````
    1. /create_message
    2. /register

    run the views as http://127.0.0.1:5000/register

"""

# Import Statements
import datetime
import json
# from numpy import cast
import os
import sys
import messageDecode
import time

#from math import ceil
from collections import defaultdict
from flask import (session, redirect, url_for,
                   request, render_template, flash,
                   Response, send_from_directory,
                   Blueprint, make_response, g, current_app)
from flask.ext.login import (LoginManager, current_user,
                             logout_user, login_user, login_required
                             )
from werkzeug.security import check_password_hash
from flask.ext.login import AnonymousUserMixin
from flask import jsonify
from forms import (LoginForm, RegisterForm, ForgotForm,
                   CreateMessageForm
                   )

# Database imports
from models.user import User
from models.messages import Messages
from models.custom_classes import Pagination


from app.db import (db)
import sqlalchemy
from sqlalchemy import desc

MESSAGES_PER_PAGE = 6  # Pagination Macro


reload(sys)
sys.setdefaultencoding('utf-8')

# Initializing the Blueprint.
# Instead of @app the module will have @messageHandle
messageHandle = Blueprint('views', __name__, template_folder='../templates')
login_manager = LoginManager()

# Function to handle the initial load of login manager
@messageHandle.record_once
def on_load(state):
    """
    http://stackoverflow.com/questions/16273499/
    flask-login-can-not-be-used-in-blueprint-object
    """

    login_manager.init_app(state.app)

# Function to handle User Loader Feedback
# After the error "NoneType object not iterable"
@login_manager.user_loader

def load_user(username):
    return User.query.filter_by(username=username).first()


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"


"""
Dummy Views
"""
# # To catch the URLs which are not defined


@messageHandle.route('/', defaults={'path': ''})
@messageHandle.route('/<path:path>')
def catch_all(path):
    return 'You want this path: %s, \n  \
                But, this is an invalid path! Please check it once!' % path


"""
User Management Views
"""


@messageHandle.route('/index', methods=['GET', 'POST'])
def index():
    """
    When the user provides /index as the URL, it automatically gets routed
    to the login
    """
    if 'username' not in session:
        return redirect(url_for('.login'))
    else:
        return redirect(url_for('.user'))


@messageHandle.route('/', methods=['GET', 'POST'])
def home():
    """
    A dummy view for login routing.
    """
    return redirect(url_for('.login'))


@messageHandle.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        # else:
        # login_manager.anonymous_user = None
        #     g.user = None
        #     # db.session.add(g.user)
        #     # db.session.commit()


@messageHandle.route('/login/check', methods=['GET', 'POST'])
def login_route():

    print "session", session
    if 'username' in session:
        print "you have already logged in"
        flash("You have already logged in")
        return redirect(url_for('.user_dashboard',username=session['username']))
    else:
        print " not logged in"
        flash("You must be logged in first")
        return render_template('forms/login_new.html', form = LoginForm())

@messageHandle.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login check for a user.

    If its successful user would be redirected to either
    "user" view or "admin" view.

    If the user is not registered then an error message is displayed and
    redirected to Login page.
    """

    # if session['username'] is not None:
    #     print "session", session['username']
    #     # To do :
    #     # Should not ask user to login again.
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # User Object from the DB
        retrieved_messages = None
        registered_user = User.query.filter_by(username=username).first()
        if registered_user is None:
            registered_user = User.query.filter_by(email=username).first()
            if registered_user is not None:
                retrieved_messages = Messages.query \
                                     .filter_by(sender_username=registered_user.username)\
                                     .first()
        #If User is not present
        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('.login'))

        if current_user.is_authenticated():
            g.user = current_user.get_id()
            print "guser", g.user

        if registered_user:
            # If he is a new user.
            if not retrieved_messages:
                if check_password_hash(registered_user.password, password):
                    registered_user.authenticated = True
                    db.session.add(registered_user)
                    db.session.commit()
                    login_user(registered_user, remember=True)
                    session['username'] = registered_user.username
                    print "user here", registered_user.username
                    return redirect(url_for('.user_with_no_jobs',
                                            username=registered_user.username))

                else:
                    flash('Please Check your password')
                    return redirect(url_for('.login'))
            else:
                # If he is an existing user.
                if check_password_hash(registered_user.password, password):
                    registered_user.authenticated = True
                    db.session.add(registered_user)
                    db.session.commit()
                    login_user(registered_user, remember=True)
                    session['username'] = registered_user.username
                    print "user here", registered_user.username
                    return redirect(url_for('.user_dashboard',
                                            username=registered_user.username))

                else:
                    flash('Please Check your password')
                    return redirect(url_for('.login'))

    return render_template('forms/login_new.html', form=form)


@messageHandle.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    Redirects to Login Page after register.
    """
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template('forms/register.html', form=form)
    print "form.validate in register", form.validate()
    if form.validate():
        user = User(
            request.form['name'],
            request.form['password'],
            request.form['email'],
            request.form['institution']
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered')

            # As per shon, directly route him to homepage, not to Login again.
            # Hence setting up the session variable.
            user.authenticated = True
            login_user(user, remember=True)
            session['username'] = request.form['name']

            return redirect(url_for('.user_with_no_jobs',
                                    username=request.form['name']))
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            # Log this properly and remove the print statement.
            print " The error is ", e
            flash('User is already registered.\
                 Please use "Forgot password" if needed')
            return redirect(url_for('.register'))

    flash("Please provide the proper input values")
    return render_template('forms/register.html',
                           form=form)
    # return redirect(url_for('.register'), form=form)


@messageHandle.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """
    This is when  user forgets his username / password
    This module is a TO- DO.
    """
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@messageHandle.route('/logout')
def logout():
    """
    When the User logs out, the session is ended and
    user is redirected to login page.
    """
    # session.pop('logged_in', None)
    user = current_user
    user.authenticated = False
    logout_user()
    flash('You have logged out')
    return redirect(url_for('.login'))


# List the users - check
@messageHandle.route('/userslist')
def userslist():
    usrs = User.query.all()
    print usrs, type(usrs)
    return Response([json.dumps([u.username for u in usrs])],
                    mimetype='application/json')

"""
Admin and User Views
"""

# Admin view
@messageHandle.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    Admin view.
    It has the admin functions like,
    Listing the users, delete the users and approve the users.
    """
    # Handling if normal users try accessing this view.
    if session['username'] != 'admin':
        flash("Only Admins can view this page!!")
        return redirect(url_for('.user'))

    if request.method == 'GET':
        columns = ['S.No', 'User Name', 'Institution', 'Email ID']
        results = [['1', 'Data#1156734', '20140408132211', 'dadsds'],
                   ['2', 'Data#2356734', '20140308092211', 'adasda'],
                   ['3', 'Data#4456734', '20140408112221', 'dadasd']]
    return render_template('pages/admin.home.html',
                           columns=columns, results=results)


@messageHandle.route('/<username>/dashboard', methods=['GET', 'POST'])
def user_dashboard(username=None):
    """
    User View
    """
    print "comes here in user_dashboard",
    # TO DO:
    # Handle here if username is None, some kinda decorator.
    if request.method == 'GET':
        print "User ID inside User", username
        #Recent Messages retrieval from the database

        retrieved_messages = None
        messages_new = None
        message_table_columns = None
        try:
            retrieved_messages = Messages.query.order_by('posted_date desc') \
                                 .filter_by(backup_1=username).limit(5).all()

        except sqlalchemy.exc.DataError as e:
            db.session.rollback()
            # Log this properly and remove the print statement.
            print " The error is ", e

        if retrieved_messages:
            message_table_columns = ['ID', 'Title',
                                 'Location', 'Status', 'Date posted']
            messages_new = [{
                        'id': u.job_id,
                        'title': u.job_title,
                        'location': u.job_location,
                        'status': u.job_status,
                        'date': u.posted_date}
                        for u in retrieved_messages]

            print "Jobs New", messages_new

        # Candidates retrieval from the database.
        retrieved_candidates = None
        candidates_new = None
        candidate_table_columns = None

        try:
            retrieved_user_row = User.query.filter_by(username=username).first()
            print "retrieved_user_row" , retrieved_user_row.id
            retrieved_candidates = Candidates.query.order_by('candidate_id desc') \
                                             .filter_by(userID=retrieved_user_row.id).all()

        # Except when there are no candidates with the given username
        except sqlalchemy.exc.DataError as e:
            db.session.rollback()
            # Log this properly and remove the print statement.
            print " The error is ", e

        if retrieved_candidates:
            print "retrieved_candidates row", retrieved_candidates
            candidate_table_columns = ['ID', 'Name', 'Skills',
                                       'Email', 'City']

            candidates_new = [{
                              'id': u.candidate_id,
                              'name': u.candidate_name,
                              'skills': u.candidate_skills,
                              'email': u.candidate_email,
                              'city': u.candidate_city}
                              for u in retrieved_candidates]

        print "candidates_new", candidates_new

        return render_template('pages/home.dashboard.html',
                               user=session['username'],
                               messages_new=messages_new,
                               candidates_new=candidates_new,
                               message_table_columns=message_table_columns,
                               candidate_table_columns=candidate_table_columns
                               )

    return redirect(url_for('.list_jobs'), username=session['username'])


@messageHandle.route('/user/home/', methods=['GET', 'POST'])
# @login_required
def user():
    """
    User View
    """
    if request.method == 'GET':
        print "340:", session['username']
        return render_template('pages/home.dashboard.landing.html',
                               user=session['username'])

    return redirect(url_for('.list_jobs'), username=session['username'])


@messageHandle.route('/<username>/new/dashboard', methods=['GET', 'POST'])
def user_with_no_jobs(username=None):
#@login_required

    """
    User with no JOBS View
    """
    print "username", username

    return render_template("pages/home.dashboard.landing.html",
                           username=username)



"""
Message Create GET
"""


@messageHandle.route('/message/create/', methods=['GET'])
# @login_required
def message_create_get():
    """
    Create Message
    """
    username = session['username']
    # Form details
    form = CreateMessageForm(request.form)

    return render_template('pages/create.message.html', user=username, form=form)


# Message create POST

@messageHandle.route('/message/create/', methods=['POST'])
# @login_required
def message_create_post():
    """
    Create Job
    """
    form = CreateMessageForm(request.form)
    username = session['username']

    print "Post Message to Database::::"

    if request.method == 'POST':
        print "did it come inside?", form, form.validate(), request.form
        print "errors", form.errors
        if form.validate():
            message = request.form['message']
            obj = messageDecode.MessageDecode()
            messageTime = time.ctime()
            formatted_json_message = obj.decode(message,messageTime)
            #print "Formatted JSON:::" , formatted_json_message
            msg = Messages(
                username,
                formatted_json_message
            )

            #print "comes till here", msg.sender_username, msg.message

            try:
                db.session.add(msg)
                db.session.commit()
                flash('Message successfully added to the database.')
                return render_template('pages/create.message.html',
                                        user=user, 
                                        form=form,
                                        jsonmsg=formatted_json_message)

            except sqlalchemy.exc.IntegrityError as e:
                db.session.rollback()
                # Log this properly and remove the print statement.
                print " The error is ", e
                flash('Job already Exists.\
                     Please check the details once')
                return redirect(url_for('.message_create_get'))

        else:

            flash("Please check the errors below")
            print "form is ", form, request.form
            return render_template('pages/create.message.html',
                                   user=user, form=form)

    return render_template('pages/create.message.html', user=user, form=form)



"""
List Messages
"""


#List Messages
@messageHandle.route('/messages/sent/', methods=['GET', 'POST'])
def sent_messages():
    """
    List the Jobs
    """
    if request.method == 'GET':
        retrieved_messages = Messages.query.all()
        print "retrieved_messages", retrieved_messages, type(retrieved_messages)
        msg_dict = {}
        sender_dict ={}

        for i,each_msg in enumerate(retrieved_messages):
            if each_msg.sender_username == session['username']:
                print "It comes here"
                msg_json = json.loads(each_msg.message)
                msg_dict[i] = msg_json
                print "Msg Dict", msg_dict

                # mentions = msg_json['emoticons']
                # emoticons = msg_json['mentions']
                # messagetime = msg_json['message_time']
                # time_list.append(messagetime)
                # links_list = msg_json['links']
                # big_list = mentions+emoticons+ time_list+links_list


        message_table_columns = ['ID', 'Mentions',
                             'Emoticons', 'Links', 'Time']
        print "msg_dict" , msg_dict
        print "message_table_colmns",message_table_columns
        return render_template('pages/list.sent.messages.html',
                               user=session['username'],
                               jobs=msg_dict,
                               message_table_columns=message_table_columns,
                               )





