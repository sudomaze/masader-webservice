from flask import Flask, jsonify, request

from utils.common_utils import dict_filter
from utils.dataset_utils import load_masader_dataset


app = Flask(__name__)


print('Preparing globals...')
masader, tags = load_masader_dataset()


@app.route('/datasets')
def get_datasets():
    global masader

    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=len(masader), type=int)
    features = request.args.get('features', default='all', type=str).split(',')

    masader_page = masader[(page - 1) * size : page * size]

    if not masader_page:
        response = jsonify('Page not found.')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    response = jsonify(list(map(lambda element: dict_filter(element, features), masader_page)))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/datasets/<int:index>')
def get_dataset(index: int):
    global masader

    features = request.args.get('features', default='all', type=str).split(',')

    if not (1 <= index <= len(masader)):
        response = jsonify(f'Dataset index is out of range, the index should be between 1 and {len(masader)}.')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    response = jsonify(dict_filter(masader[index - 1], features))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/datasets/tags')
def get_tags():
    global tags

    features = request.args.get('features', default='all', type=str).split(',')

    response = jsonify(dict_filter(tags, features))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/refresh')
def refresh():
    global masader, tags

    print('Refreshing globals...')
    masader, tags = load_masader_dataset()

    response = jsonify(f'The datasets updated successfully! The current number of available datasets is {len(masader)}.')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
