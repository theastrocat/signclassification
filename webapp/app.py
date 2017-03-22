from __future__ import division
from flask import Flask, render_template, request, jsonify, make_response
from cStringIO import StringIO
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
plt.style.use('ggplot')
import requests
import numpy as np
from

app = Flask(__name__)
r_labels = requests.get("https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/test.npy")
r_features = requests.get("https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/test_features.npy")
test_features = np.load(StringIO(r_features.content))
test_paths = np.load(StringIO(r_labels.content))
test_set = np.concatenate((test_features, test_paths[:,1].reshape(-1,1)), axis = 1)



@app.route('/', methods=['GET'])
def index():
    current_image, current_features = getrandomimage()

    return render_template('index.html',
                            sign=current_image,
                            predictions='http://0.0.0.0:5000/plot/2/3')

def getrandomimage():
    current_index = np.random.choice(range(len(test_set)))
    current_features = test_set[current_index][:-1]
    current_image = "https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/{}".format(test_set[current_index][-1])
    return current_image, current_features


# @app.route('/solve', methods=['POST'])
# def solve():
#     user_data = request.json
#     a, b, c = user_data['a'], user_data['b'], user_data['c']
#     root_1, root_2 = _solve_quadratic(a, b, c)
#     return jsonify({'root_1': root_1, 'root_2': root_2})


# def _solve_quadratic(a, b, c):
#     disc = b*b - 4*a*c
#     root_1 = (-b + sqrt(disc))/(2*a)
#     root_2 = (-b - sqrt(disc))/(2*a)
#     return root_1, root_2


#@app.route("/plot/<int:x>/<int:y>")
@app.route("/plot/currentplot")
def plot(x, y):

    fig, ax = plt.subplots()

    ax.plot([0, x], [0, y])
    ax.set_xlim(-max(abs(x), abs(y)), max(abs(x), abs(y)))
    ax.set_ylim(-max(abs(x), abs(y)), max(abs(x), abs(y)))
    canvas=FigureCanvas(fig)
    png_output = StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
