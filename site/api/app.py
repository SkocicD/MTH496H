from flask import Flask, request, jsonify
from flask_cors import CORS
from delaunay_triangulation import delaunay_api
from voronoi_diagram import voronoi_api
from crust import crust_api

app = Flask(__name__)
CORS(app)  # allows Angular to talk to backend


@app.route('/delaunay', methods=['POST'])
def delaunay():
    data = request.json
    points = data.get("points", [])
    edges = delaunay_api(points)

    return jsonify(edges)


@app.route('/voronoi', methods=['POST'])
def voronoi():
    data = request.json
    points = data.get("points", [])
    edges = voronoi_api(points)

    return jsonify(edges)


@app.route('/crust', methods=['POST'])
def crust():
    data = request.json
    points = data.get("points", [])
    edges = crust_api(points)

    return jsonify(edges)


if __name__ == '__main__':
    app.run(debug=True)
