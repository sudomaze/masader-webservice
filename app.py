import hashlib
import urllib.request as req

from flask import Flask, jsonify
from datasets import DownloadMode, load_dataset

app = Flask(__name__)


def load_masader_dataset_as_dict():
    return list(
        load_dataset(
            'arbml/masader',
            download_mode=DownloadMode.FORCE_REDOWNLOAD,
        )['train']
    )

def get_masader_hashvalue():
    webf = req.urlopen('https://docs.google.com/spreadsheets/d/1YO-Vl4DO-lnp8sQpFlcX1cDtzxFoVkCmU1PVw_ZHJDg/gviz/tq?tqx=out:csv&sheet=filtered_clean')
    txt = webf.read()
    return hashlib.sha256(txt).hexdigest();


def get_masader_hashvalue_local():
    with open("data.csv", "rb") as f:
        file_data = f.read()
        return hashlib.sha256(file_data).hexdigest();

print('Downloading the dataset...')
masader = load_masader_dataset_as_dict()
masaderHash = get_masader_hashvalue()


@app.route('/datasets', defaults={'index': None})
@app.route('/datasets/<index>')
def datasets(index: str):
    global masader
    global masaderHash

    if masaderHash != get_masader_hashvalue():
        print('Re-downloading the dataset...')
        masader = load_masader_dataset_as_dict()
        masaderHash = get_masader_hashvalue()

    if index:
        index = int(index)

        if 1 <= index <= len(masader):a
            return jsonify(masader[index - 1])
        else:
            return jsonify(f'Dataset index is out of range, the index should be between 1 and {len(masader)}.'), 404
    else:
        return jsonify(masader)


#app.run(host="127.0.0.1", port=5000)