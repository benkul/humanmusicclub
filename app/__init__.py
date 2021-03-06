from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import boto3
import json
import uuid
import time
import functools


app = Flask(__name__)


client = boto3.client('dynamodb', region_name='us-west-2')
day = 86400
cache_date = time.time()


def get_current_results():
    global cache_date
    if check_freshness(time.time()):
        cache_date = time.time()
        return get_content()
    else:
        return results


def check_freshness(date_now):
    global cache_date
    delta = cache_date - date_now
    if delta > (day * 2):
        return True
    else:
        return False

def get_content():
    paginator = client.get_paginator('scan')
    items = paginator.paginate(
        TableName='HMC',
        Select='ALL_ATTRIBUTES',
        PaginationConfig={
            'MaxItems':25
        })
    content = []

    for i in items:
    	for p in i['Items']:
        	content.append({'Post': [p['title']['S'], p['link']['S']]})
    content.sort(key=lambda x: x['Post'][0], reverse=False)
    return content

results = get_content()

def add_content(title, link):
    uid = str(uuid.uuid4().time)
    results = client.put_item(
        TableName="HMC",
        Item = {'uid': {'S': uid},
            'title': {'S': title},
            'link': {'S': link}})
    return results


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    content = get_current_results()
    return render_template('content.html', content=content)


'''
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form.get('title')
        link = request.form.get('link')
        word = request.form.get('auth')
        if word != "yougotdis":
            return render_template('add.html', results="bad")
        results = add_content(title, link)
        return render_template('add.html', results=results)
    return render_template('add.html')
'''

@app.route('/<post_name>')
def get_post(post_name):
    content = get_current_results()
    return render_template('name.html', content=content, name=post_name)


if __name__ == '__main__':
    app.run()
