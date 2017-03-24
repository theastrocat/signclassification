from __future__ import division
from flask import Flask, render_template, request, jsonify, make_response
from cStringIO import StringIO
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from src.lrprobfinder import ProbabilityFinder
from src.image_get import RandImage
import requests
import pickle
import numpy as np
plt.style.use('ggplot')

ri = RandImage()
labelmaker = {
    u'addedLane': 'Added Lane',
    u'keepRight': 'Keep Right',
    u'laneEnds': 'Lane Ends',
    u'merge': 'Merge',
    u'pedestrianCrossing': 'Pedestrian Crossing',
    u'school': 'School',
    u'signalAhead': 'Signal Ahead',
    u'speedLimit25': 'Speed Limit 25',
    u'speedLimit30': 'Speed Limit 30',
    u'speedLimit35': 'Speed Limit 35',
    u'speedLimit45': 'Speed Limit 45',
    u'speedLimitUrdbl': 'Speed Limit',
    u'stop': 'Stop',
    u'stopAhead': 'Stop Ahead',
    u'yield': 'Yield'}

app = Flask(__name__)
imageurl  = 'http://0.0.0.0:5000/images/'

with open('data/model.pkl') as f:
    model = pickle.load(f)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/refresh', methods=['POST'])
def refresh():
    current_image_url, _  = ri.getrandomimage()
    return jsonify({
        'truelabel': labelmaker[ri.current_label],
        'current_image_url': current_image_url,
        'predictions_url': '{}currentplot'.format(imageurl)
    })


@app.route('/images/<cropzonekey>')
def images(cropzonekey):
    return render_template("images.html", title=cropzonekey)


@app.route("/images/currentplot")
def probplot():
    cnt_features = ri.current_features
    probs = model.predict_proba(cnt_features.reshape(1,-1))
    labels = model.classes_()
    fig, ax = plt.subplots(figsize=(15,15))
    sortargs = probs.argsort()[0][-3:]
    lbl = labels[sortargs]
    fig, ax = plt.subplots()
    y_pos = np.arange(len(lbl))
    y = probs[0][sortargs]
    N = len(y)
    x = range(N)
    width = 1/2.
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlim([0,1])
    rects = ax.barh(x, y, width, color="blue", alpha = 0.5)
    ax.vlines(x=0.005, ymin=-1.0, ymax=3.0,linewidth=2,color = 'k')
    ax.set_yticks(np.arange(3) + width/20.)
    for i, rect in enumerate(rects):
        length = round(rect.get_width(),4)
        ax.text(.5, rect.get_y() + rect.get_height()/10,
                '{} - {}%'.format(labelmaker[lbl[i]], round(100 * length,2)),
                ha='center', va='bottom',size=20)
    fig.figurePatch.set_alpha(0)
    plt.grid(False)
    ax.set_facecolor('white')
    plt.tight_layout
    canvas=FigureCanvas(fig)
    png_output = StringIO()
    canvas.print_png(png_output)
    plt.close(fig)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response





if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
