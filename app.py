#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.config['JSON_AS_ASCII'] = False

CONFIG_DIR = Path("configs")
CONFIG_DIR.mkdir(exist_ok=True)

class ConfigManager:
    def __init__(self, config_file="default_config.json"):
        self.config_file = CONFIG_DIR / config_file
        self.config = self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self):
        return {
            "twitch": {"username": "", "password": "", "claim_drops_startup": False},
            "priority": ["STREAK", "DROPS", "ORDER"],
            "enable_analytics": False,
            "logger_settings": {"save": True, "console_level": "INFO", "emoji": True},
            "streamer_settings": {
                "make_predictions": True, "follow_raid": True, "claim_drops": True,
                "watch_streak": True, "community_goals": False, "chat": "ONLINE"
            },
            "bet_settings": {
                "strategy": "SMART", "percentage": 5, "percentage_gap": 20,
                "max_points": 50000, "stealth_mode": True, "delay_mode": "FROM_END",
                "delay": 6, "minimum_points": 20000
            },
            "streamers": [], "blacklist": [], "notifications": {}
        }
    
    def save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        self.config = config
        return True

config_manager = ConfigManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config_manager.config)

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    config_manager.save_config(data)
    return jsonify({"status": "success", "config": config_manager.config})

@app.route('/api/streamers', methods=['GET'])
def get_streamers():
    return jsonify(config_manager.config.get('streamers', []))

@app.route('/api/streamers', methods=['POST'])
def add_streamer():
    data = request.json
    if 'username' not in data:
        return jsonify({"error": "Username required"}), 400
    
    config = config_manager.config
    if any(s.get('username') == data['username'] for s in config.get('streamers', [])):
        return jsonify({"error": "Streamer already exists"}), 400
    
    new_streamer = {"username": data['username'], "settings": config['streamer_settings']}
    config['streamers'].append(new_streamer)
    config_manager.save_config(config)
    
    return jsonify({"status": "success", "streamer": new_streamer}), 201

@app.route('/api/streamers/<username>', methods=['DELETE'])
def delete_streamer(username):
    config = config_manager.config
    config['streamers'] = [s for s in config.get('streamers', []) if s.get('username') != username]
    config_manager.save_config(config)
    return jsonify({"status": "success"})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online", "version": "1.0.0", "timestamp": datetime.now().isoformat(),
        "streamers_count": len(config_manager.config.get('streamers', []))
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
