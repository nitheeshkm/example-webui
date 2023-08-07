from flask import Flask, render_template, jsonify, request
import random
import time
import subprocess
import json

app = Flask(__name__)

def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)

try:
    with open('data.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {'127.0.0.1': {'id': 0, 'temperature': 0, 'voltage': '0.0', 'updated': '00:00:00'}}
    save_data()

# # Fake data dictionary
# data = {
#     '192.168.50.1': {'id': 3, 'temperature': 0, 'voltage': '0.0', 'updated': '00:00:00'},
#     '192.168.50.2': {'id': 10, 'temperature': 0, 'voltage': '0.0', 'updated': '00:00:00'},
#     '192.168.50.3': {'id': 21, 'temperature': 0, 'voltage': '0.0', 'updated': '00:00:00'},
#     '192.168.50.4': {'id': 99, 'temperature': 0, 'voltage': '0.0', 'updated': '00:00:00'},
#     '192.168.50.5': {'id': 6, 'temperature': 0, 'voltage': '0.0', 'updated': '00:00:00'}
# }

def update_data():
    for ip in data:
        temperature = random.randint(0, 100)
        data[ip]['temperature'] = temperature
        data[ip]['voltage'] = f'{random.uniform(10.0, 14.0):.2f}'
        data[ip]['updated'] = time.strftime('%H:%M:%S')
        
        if temperature > 80:
            data[ip]['temp_msg'] = 'danger'
        elif temperature > 50:
            data[ip]['temp_msg'] = 'warning'
        else:
            data[ip]['temp_msg'] = 'normal'


@app.route('/')
def index():
    update_data()
    return render_template('index.html', data=data)

@app.route('/get_data' , methods=['GET'])
def get_data():
    update_data()
    return jsonify(data)

@app.route('/settings')
def settings():
    return render_template('settings.html', data=data)

@app.route('/add_ip', methods=['POST'])
def add_ip():
    new_ip = request.form.get('ip')
    data[new_ip] = {'id': random.randint(0, 100), 'temperature': None, 'voltage': None, 'updated': None}
    save_data()
    return 'Success'

@app.route('/save_all_edited_ips', methods=['POST'])
def save_all_edited_ips():
    edited_ips = json.loads(request.form.get('edited_ips'))
    for edited_ip in edited_ips:
        old_ip = edited_ip['oldIP']
        new_ip = edited_ip['newIP']
        if old_ip in data:
            data[new_ip] = data.pop(old_ip)
    save_data()  # Save the updated data to the local storage file
    return 'Success'

@app.route('/delete_ip', methods=['POST'])
def delete_ip():
    ip = request.form.get('ip')
    if ip in data:
        del data[ip]
    save_data()
    return 'Success'

@app.route('/ping_ip', methods=['POST'])
def ping_ip():
    ip = request.form.get('ip')
    try:
        result = subprocess.check_output(['ping', '-c', '1', ip]).decode('utf-8')
    except subprocess.CalledProcessError:
        result = "Ping request failed."
    return jsonify(result)

@app.route('/load_data', methods=['POST'])
def load_data():
    saved_data = request.form.get('data')
    global data
    data = json.loads(saved_data)
    return 'Success'

@app.route('/update_log_data', methods=['POST'])
def update_log_data():
    ip = request.form.get('ip')
    log_data = request.form.get('log_data') == 'true'
    data[ip]['log_data'] = log_data
    save_data()  # Save data to local storage
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
