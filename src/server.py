from flask import Flask, Response, json, render_template
import json
import requests
import time

app = Flask(__name__)

def get_current_pose():
    response=requests.get('https://api.wheretheiss.at/v1/satellites/25544')
    return response.json()

@app.route('/')
def index():
    _template='index.html'
    return render_template(_template, title='ISS Now' , initial_pose=get_current_pose())

@app.route('/api/pose') 
def pose_stream():

    def __generate__(delay=1.0):
        while True:
            response = get_current_pose()
            response = json.dumps(response)
            yield f"data:{response}\n\n"
            time.sleep(delay)

    return Response(__generate__(),mimetype="text/event-stream")   

@app.route('/')
def about():
    return 'Developed by Ali'    

if __name__ == '__main__':
    app.run(debug=True)    