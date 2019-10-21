import os
import json
import requests
from flask import Flask, render_template, Response, request

# Get Vars
api_host = os.environ['API_HOST']
api_version = os.environ['API_VERSION']
refresh_rate = int(os.environ['REFRESH_MS'])
err_img_url = os.environ['ERROR_IMG']

api_url = api_host + '/v' + api_version + '/get_member?' 
error_member = {
    "name": "There has been an error",
    "img_url": err_img_url
}

# Call API
def fetch_member(name=None):
    ''' get a staff member from the API '''
    data = {}
    call = api_url
    if not name == None:
        call += "name={}".format(name.replace(' ', '%20'))
    try:
        response = requests.get(call, timeout=2)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            return error_member
    except:
        return error_member

# API
app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', None)
    member = fetch_member(name)
    return render_template(
        'frame.html',
        pagetitle='Staffbot',
        img_url=member.get('img_url'),
        name=member.get('name'),
        refresh_ms=refresh_rate
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)