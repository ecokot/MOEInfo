from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

# Путь к исполняемому файлу Python скрипта
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'main.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check_version', methods=['POST'])
def check_version():
    try:
        result = subprocess.run([sys.executable, SCRIPT_PATH, 'check_version'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return jsonify({'success': True, 'data': result.stdout.strip()})
        else:
            return jsonify({'success': False, 'error': result.stderr.strip()})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Таймаут выполнения команды'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_player_info', methods=['POST'])
def get_player_info():
    data = request.json
    player_name = data.get('player_name')
    if not player_name:
        return jsonify({'success': False, 'error': 'Имя игрока не указано'})
    
    try:
        result = subprocess.run([sys.executable, SCRIPT_PATH, 'get_player_info', player_name], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return jsonify({'success': True, 'data': result.stdout.strip()})
        else:
            return jsonify({'success': False, 'error': result.stderr.strip()})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Таймаут выполнения команды'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_server_info', methods=['POST'])
def get_server_info():
    data = request.json
    server_ip = data.get('server_ip')
    if not server_ip:
        return jsonify({'success': False, 'error': 'IP-адрес сервера не указан'})
    
    try:
        result = subprocess.run([sys.executable, SCRIPT_PATH, 'get_server_info', server_ip], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return jsonify({'success': True, 'data': result.stdout.strip()})
        else:
            return jsonify({'success': False, 'error': result.stderr.strip()})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Таймаут выполнения команда'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/check_ip', methods=['POST'])
def check_ip():
    data = request.json
    ip_address = data.get('ip_address')
    if not ip_address:
        return jsonify({'success': False, 'error': 'IP-адрес не указан'})
    
    try:
        result = subprocess.run([sys.executable, SCRIPT_PATH, 'check_ip', ip_address], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return jsonify({'success': True, 'data': result.stdout.strip()})
        else:
            return jsonify({'success': False, 'error': result.stderr.strip()})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Таймаут выполнения команды'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)