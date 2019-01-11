from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import boto3
import json
import uuid
import functools
import datetime


app = Flask(__name__)


client = boto3.client('dynamodb', region_name='us-west-2')

def get_content():
    paginator = client.get_paginator('scan')
    items = paginator.paginate(
        TableName='HMC',
        Select='ALL_ATTRIBUTES',
        PaginationConfig={
            'MaxItems':10
        })
    for i in items:
        for p in i['Items']:
            content.append({'Post': [p['title']['S'], p['link']['S']]})
    return content

def add_content(title, link):
    uid = str(uuid.uuid4().time)
    results = client.put_item(
        TableName="HMC",
        Item = {'uid': {'S': uid},
            'title': {'S': title},
            'link': {'S': link}})
    return content


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    current = check_current()
    content = get_content()
    return render_template('content.html', content=content)



@app.route('/admin', methods['GET', 'POST'])
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


if __name__ == '__main__':
    app.run()
