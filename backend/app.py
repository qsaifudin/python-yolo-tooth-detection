from flask import Flask, request, jsonify, send_from_directory
import os
import json
import subprocess
from subprocess import Popen
from flask_cors import CORS
import shutil
import base64
from PIL import Image

app = Flask(__name__)
CORS(app, origins='*')
# Mendefinisikan path untuk menyimpan file gambar
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mendefinisikan path untuk menyimpan data dalam file JSON
JSON_FILE = 'data.json'

# Fungsi untuk membaca data dari file JSON


def read_data():
    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, 'r') as file:
        data = json.load(file)
        return data

# Fungsi untuk menulis data ke file JSON


def write_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file)

# Mendefinisikan endpoint untuk membuat entri data baru


# Menentukan direktori file gambar
app.config['RESULT_TEST_FOLDER'] = 'detect/exp'


@app.route('/gambar/<path:filename>')
def get_gambar(filename):
    # Mengirim file gambar dari direktori upload
    return send_from_directory(app.config['RESULT_TEST_FOLDER'], filename)


@app.route('/data', methods=['POST'])
def create_data():

    # print('-------------')
    # print(request.is_json)
    # for field_name, field_value in request.form.items():
    #     print(f'{field_name}: {field_value}')

    # print('-------------')
    # files = request.files.getlist('file_gambar')
    # for file in files:
    #     # Access file properties
    #     filename = file.filename
    #     content_type = file.content_type
    #     file_size = len(file.read())

    #     print(f'File Name: {filename}')
    #     print(f'Content Type: {content_type}')
    #     print(f'File Size: {file_size} bytes')
    # # print(request.get_json())
    # # print(request.files['file_gambar'])
    # # print(request.form.get('file_gambar'))
    # print('-------------')

    # return jsonify({"req": 's'}), 201

    data = read_data()
    # Menerima input dari request body
    # id = request.form.get('id')
    nama = request.form.get('nama')
    rekam_medik = request.form.get('rekam_medik')
    file_gambar = request.files['file_gambar']

    # Menyimpan file gambar dengan penomoran bertambah
    # file_name = str(len(data) + 1) + '.' + file_gambar.filename.split('.')[-1]
    file_name = 'img.' + file_gambar.filename.split('.')[-1]
    # id = str(len(data) + 1)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    # file_gambar.save(file_path)

    # Buka gambar menggunakan Pillow
    image = Image.open(file_gambar)

    # Resize gambar menjadi lebar 640
    new_width = 1200
    width, height = image.size
    new_height = int(new_width * height / width)
    resized_image = image.resize((new_width, new_height))

    # Simpan gambar yang telah diresize
    resized_image.save(file_path)

    # Menyimpan data baru ke dalam list
    new_data = {
        # 'id': id,
        'nama': nama,
        'rekam_medik': rekam_medik,
        'file_gambar': file_path
    }

    # Specify the path to the "detect/exp" folder
    exp_folder = os.path.join('detect', 'exp')

    # Delete the contents of the "detect/exp" folder if it exists
    if os.path.exists(exp_folder):
        shutil.rmtree(exp_folder)

    process = Popen(['python', '../detection/yolov5/detect.py',
                     '--weights', '../detection/model/best.pt',
                    '--img', '608',
                     '--conf-thres', '0.2',
                     '--source', file_path,
                     '--line-thickness', '1',
                     '--save-crop',
                     '--exist-ok',
                     '--project', 'detect',
                     '--save-conf'], shell=True)
    process.wait()
    print(new_data)
    # data.append(new_data)

    # Menulis data ke file JSON
    # write_data(data)
    write_data(new_data)

    return jsonify(new_data), 201

# Mendefinisikan endpoint untuk mendapatkan semua data


@ app.route('/data', methods=['GET'])
def get_all_data():
    # Define the path to the image file

    data = read_data()
    if not data:
        return jsonify({}), 200

    data['gambar'] = "http://localhost:5000/gambar/img.jpg"
    return jsonify(data), 200

# Mendefinisikan endpoint untuk mendapatkan data berdasarkan ID


@ app.route('/data/<id>', methods=['GET'])
def get_data(id):
    data = read_data()
    for item in data:
        if item['id'] == id:
            return jsonify(item), 200

    return jsonify({'message': 'Data not found'}), 404

# Mendefinisikan endpoint untuk mengupdate data berdasarkan ID


@ app.route('/data/<id>', methods=['PUT'])
def update_data(id):
    data = read_data()
    for item in data:
        if item['id'] == id:
            item['nama'] = request.form.get('nama')
            item['rekam_medik'] = request.form.get('rekam_medik')
            write_data(data)
            return jsonify(item), 200

    return jsonify({'message': 'Data not found'}), 404

# Mendefinisikan endpoint untuk menghapus data berdasarkan ID


@ app.route('/data', methods=['DELETE'])
def delete_data_static():

    file_path = 'data.json'
    data = {}
    with open(file_path, 'w') as file:
        json.dump(data, file)

    # Specify the path to the "detect/exp" folder
    exp_folder = os.path.join('detect', 'exp')
    # Delete the contents of the "detect/exp" folder if it exists
    if os.path.exists(exp_folder):
        shutil.rmtree(exp_folder)

    folder_path = 'upload'
    # Get all file names in the directory
    file_names = os.listdir(folder_path)
    # Iterate over the file names and delete each file
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return jsonify({'message': 'Data deleted'}), 200


@ app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    data = read_data()
    for item in data:
        if item['id'] == id:
            # Menghapus file gambar terkait
            if os.path.exists(item['file_gambar']):
                os.remove(item['file_gambar'])
            data.remove(item)
            write_data(data)
            return jsonify({'message': 'Data deleted'}), 200
    return jsonify({'message': 'Data not found'}), 404


if __name__ == '__main__':
    # Membuat folder 'detect/test' jika belum ada
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # app.run(debug=True, port=5001)
    app.run(debug=True, port=5000)
