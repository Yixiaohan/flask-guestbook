#!/usr /bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jiangge'

import shelve
from datetime import datetime
from flask import Flask, request, render_template, redirectp

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'


def save_data(name, comment, create_at):
    """
    save data from form submitted
    """
    database = shelve.open(DATA_FILE)

    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']

    greeting_list.insert(
        0, {'name': name, 'comment': comment, 'create_at': create_at})

    database['greeting_list'] = greeting_list

    database.close()


def load_data():
    """
    load saved data
    """
    database = shelve.open(DATA_FILE)

    greeting_list = database.get('greeting_list', [])

    database.close()

    return greeting_list


@application.route('/')
def index():
    """Top page
    Use template to show the page
    """
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)


@application.route('/post', methods=['POST'])
def post():
    """Comment's target url
    """
    name = request.form.get('name')
    comment = request.form.get('comment')
    create_at = datetime.now()

    save_data(name, comment, create_at)

    return redirect('/')


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
