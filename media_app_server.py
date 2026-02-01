#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media HTTP Server for Render Port Binding
Runs Media Telegram Bot with Voice & Document Features
"""

import os
import sys
import threading
import time
from flask import Flask, jsonify
from media_bot import MediaAtlasBot

# Create Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "bot": "ATLAS AI Telegram Bot - Media Edition",
        "features": ["Voice Messages", "PDF Generation", "Word Documents", "Excel Sheets"],
        "creator": "K.V.SARVESH"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "atlas-ai-telegram-bot",
        "version": "media-edition"
    })

def run_bot():
    """Run the Telegram bot in background"""
    try:
        bot = MediaAtlasBot()
        bot.run()
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv('PORT', 8000))
    
    print(f"🌐 Starting HTTP server on port {port} for Render")
    print("🎵 Starting Media Telegram bot in background")
    print("🎯 Features: Voice, PDF, Word, Excel")
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Give bot time to start
    time.sleep(2)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
