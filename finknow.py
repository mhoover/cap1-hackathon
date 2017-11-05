#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import requests

from flask import Flask, request, jsonify
from slackclient import SlackClient
from threading import Thread

from cap1Hackathon import run


app = Flask(__name__)

def process_request(resp_url, content, url):
    payload = {
        'text': content,
        'attachments': [
            {
                'title': 'Distributions',
                'image_url': url,
                'text': url
            }
        ]
    }
    return requests.post(resp_url, headers={'Content-type': 'application/json'},
                         data=json.dumps(payload))


@app.route('/finknow', methods=['POST', 'GET'])
def finknow():
    resp_url = request.form.get('response_url')
    text = request.form.get('text')
    text = str(text).split(' ')

    # get information
    args_dict = {
        'user': int(text[0]),
        'graph': text[1],
        'limit': int(text[2]),
    }
    content = run.run(args_dict)

    # # post information
    slack = SlackClient(os.getenv('SLACK_HFF_OAUTH'))
    files = {
        'file': (
            '{}_plt.png'.format(args_dict['graph']),
            open('{}_plt.png'.format(args_dict['graph']), 'r'),
            'png'
        )
    }
    payload = {
        'filename': '{}_plt.png'.format(args_dict['graph']),
        'token': os.getenv('SLACK_HFF_OAUTH')
    }
    r = requests.post('https://slack.com/api/files.upload',
                      params=payload, files=files)
    if r.status_code==200:
        url = r.json()['file']['url_private']

    thr = Thread(target=process_request, args=[resp_url, content, url])
    thr.start()

    return jsonify({'text': 'Got it... working on that request.'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
