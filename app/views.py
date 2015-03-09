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
Job Search Views
"""


@messageHandle.route('/job/search/q', methods=['GET', 'POST'])
def jobs_by_page():
    page = 1
    print "req args", request.args
    if request.args:
        print "comes inside"
        page = request.args.page
    print "page", page
    print g.user
    pagination = Jobs.query.paginate(page).all()
    print "pagination", pagination

    #pagination = Pagination(page, PER_PAGE, count)
    return render_template(
        'pages/candidates.view.html',
        pagination=pagination
    )


@messageHandle.route('/job/search', methods=['GET', 'POST'])
def job_search():
    """
    No login required for this view.
    Displays all the jobs to the user and allows him to apply for the job.
    Options available to refine the results as well
    """

    # Local Variables
    groups = []
    page = 1
    job_refine_filter = False

    print "request args", request.args

    # Check the Page in request args
    if 'page' in request.args:
        page = int(request.args['page'])
        print "page inside args is :", page

    print " common method : page is", page

    # Common Pagination
    retrieved_messages = Jobs.query.order_by(desc(Jobs.posted_date)).all()
    print "494 : retrieved jobs", retrieved_messages
    jobs = [(u.job_id, u.job_title, u.job_location, u.job_status,
             u.posted_date) for u in retrieved_messages]
    print " Jobs:", Jobs
    pagination = Pagination(page, MESSAGES_PER_PAGE, len(retrieved_messages))
    retrieved_messages = Jobs.query.order_by(desc(Jobs.posted_date)).limit(MESSAGES_PER_PAGE)\
                               .offset(MESSAGES_PER_PAGE * (page - 1)).all()
    groups = retrieved_messages

    # End of common Pagination

    # Get the args value from request
    # Start of job search refine
    if ('job_keyword' in request.args) or \
       ('job_companyname' in request.args) or ('job_title' in request.args):

        keywords = request.args['job_keyword'].strip()
        company = request.args['job_companyname'].strip()
        jobname = request.args['job_title'].strip()

        jobs = Jobs.query  # alias
        if keywords:
            jobs = jobs.filter(Jobs.job_description.ilike('%%%s%%' % keywords))

        if company:
            # jobs = jobs.filter_by(job_institution=company)
            jobs = jobs.filter(Jobs.job_institution.ilike('%%%s%%' % company))

        if jobname:
            # jobs = jobs.filter_by(job_institution=company)
            jobs = jobs.filter(Jobs.job_title.ilike('%%%s%%' % jobname))

        retrieved_messages = jobs.all()
        pagination = Pagination(page, MESSAGES_PER_PAGE, len(retrieved_messages))
        retrieved_messages = jobs.order_by(desc(Jobs.posted_date)) \
                             .limit(MESSAGES_PER_PAGE)\
                             .offset(MESSAGES_PER_PAGE * (page - 1)).all()
        print "retrieved_messages inside::", retrieved_messages,
        groups = retrieved_messages
        job_refine_filter = True  # set the job_refine_filter to 1.
        print "is it null", retrieved_messages

        if not retrieved_messages:
            print "its null"
            return render_template('pages/candidates.view.html',
                                   no_results='true'
                                   )

    # End of job refine

    print "job_refine filter", job_refine_filter

    # create a list of dictonaries to be parsed in the Jinja2 template.
    job_accordian_new = [{
                         'id': u.job_id,
                         'title': u.job_title,
                         'location': u.job_location,
                         'status': u.job_status,
                         'qualification': u.job_qualification,
                         'jobtype': u.job_type,
                         'experience': u.job_experience,
                         'summary': u.job_summary,
                         'description': u.job_description,
                         'institution': u.job_institution,
                         'date': u.posted_date}
                         for u in retrieved_messages]

    # For AJAX calls.
    # For Jobs table - Construct the makeID
    job_columns_for_makeID = ['id', 'title']
    job_columns_for_modelID = ['id', 'employer']
    jobs_for_makeID = [(u.job_id, u.job_title) for u in retrieved_messages]
    jobs_for_modelID = [(u.job_id, u.job_institution) for u in retrieved_messages]

    # Variables
    jobs_temp_dict = {}
    jobs_list_of_dicts = []
    jobs_list_of_model_dicts = []

    # Construct the List Dict of Job Titles
    for each_job in jobs_for_makeID:
        jobs_temp_dict = {}
        for each_item, each_column in zip(each_job, job_columns_for_makeID):
            jobs_temp_dict[each_column] = each_item

        jobs_list_of_dicts.append(jobs_temp_dict)

    # Construct the List Dict of Job Providers
    for each_job in jobs_for_modelID:
        jobs_temp_dict = {}
        for each_item, each_column in zip(each_job, job_columns_for_modelID):
            jobs_temp_dict[each_column] = each_item

        jobs_list_of_model_dicts.append(jobs_temp_dict)

    MAKE_LIST = jobs_list_of_dicts
    MODEL_LIST = jobs_list_of_model_dicts

    print "dummy:", MODEL_LIST    # to avoid PEP error
    form = VehicleForm(request.form)
    form.make.choices = [('', '--- Select One ---')] + [
        (x['id'], x['title']) for x in MAKE_LIST]

    chosen_make = None
    chosen_model = None

    ## End of AJAX Calls for select box.

    if request.method == 'POST':
        chosen_make = form.make.data
        chosen_model = form.model.data

        context = {
            'form': form,
            'chosen_make': chosen_make,
            'chosen_model': chosen_model,
        }

        return render_template('pages/candidates.view.html',
                               user=None,
                               jobs=jobs,
                               job_accordian_new=job_accordian_new,
                               pagination=pagination,
                               groups=groups,
                               **context
                               )

    if request.method == 'GET':
        print "comes here: in GET of job search"
        # print "job acc new", job_accordian_new

        context = {
            'form': form,
            'chosen_make': chosen_make,
            'chosen_model': chosen_model,
        }

        return render_template('pages/candidates.view.html',
                               user=None,
                               jobs=jobs,
                               job_accordian_new=job_accordian_new,
                               pagination=pagination,
                               groups=groups,
                               **context
                               )

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




"""
Message Details

"""


@messageHandle.route('/job/view/<data>', methods=['GET', 'POST'])
def job_stats(data=None):
    """
    List the stats for a selected Jobs Collection

    """

    if request.method == 'GET':
        print "Data is ", data
        u = Jobs.query.get(data)
        print "retrieved_messages", u.job_id, u.job_title

        job_accordian_new = [{
                             'id': u.job_id,
                             'title': u.job_title,
                             'location': u.job_location,
                             'status': u.job_status,
                             'qualification': u.job_qualification,
                             'jobtype': u.job_type,
                             'experience': u.job_experience,
                             'summary': u.job_summary,
                             'description': u.job_description,
                             'institution': u.job_institution,
                             'date': u.posted_date}
                             ]

        # print "{{job_accordian_new.description}}", job_accordian_new
        #print job_accordian_new
        return render_template('pages/manage.jobs.html',
                               user=session['username'],
                               data=data,
                               job_accordian_new=job_accordian_new)


