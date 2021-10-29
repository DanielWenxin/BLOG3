# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run

from flask import Flask, Blueprint, current_app, g, render_template, redirect, request, flash, url_for, session
from flask.cli import with_appcontext

from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
import click

import random
import string

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main_better.html')

@app.route('/Submit/', methods=['POST', 'GET'])
def Submit():
    if request.method == 'GET':
        return render_template('Submit.html')
    if request.method == 'POST':
        try: 
            insert_message(request)
            return render_template('Submit.html', thanks=True)
        except:
            return render_template('Submit.html', error=True)

@app.route('/View/')
def View():
    message=random_messages(6)
    return render_template('View.html',messages=message)


def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')

    cursor = g.message_db.cursor()
    cmd1 = """CREATE TABLE IF NOT EXISTS messages(id INTEGER,
                                                handle TEXT,
                                                message TEXT)"""
    cursor.execute(cmd1)
    return g.message_db


def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    TB = get_message_db()
    cursor = TB.cursor()
    cmd2 = """SELECT COUNT(*) FROM messages"""
    cursor.execute(cmd2)
    TB.execute(f""" INSERT INTO messages(id, handle, message) VALUES ({cursor.fetchone()[0]+1}, "{handle}", "{message}");""")
    TB.commit()
    TB.close()



def random_messages(n):
    TB = get_message_db()
    cursor = TB.cursor()
#    cmd3 = """SELECT COUNT(*) FROM messages"""
#    cursor.execute(cmd3)
    cmd4 = f"""SELECT handle,message FROM messages order by RANDOM() LIMIT {n}"""
    cursor.execute(cmd4)
    result = cursor.fetchall()
    return result 








