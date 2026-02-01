#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple HTTP Server for Render Port Binding
Satisfies Render's port requirement while running Telegram bot
"""

import os
import sys
import threading
import time
from flask import Flask, jsonify
from atlas_ai_telegram_bot import AtlasAITelegramBot

# Create Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "bot": "ATLAS AI Telegram Bot",
        "message": "Multi-User Media Edition is running",
        "creator": "K.V.SARVESH"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "atlas-ai-telegram-bot",
        "version": "multi-user-media"
    })

@app.route('/ready')
def ready():
    return jsonify({
        "status": "ready",
        "bot_running": True
    })

def run_bot():
    """Run the Telegram bot in background"""
    try:
        bot = AtlasAITelegramBot()
        bot.run()
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv('PORT', 8000))
    
    print(f"🌐 Starting HTTP server on port {port} for Render")
    print("🤖 Starting Telegram bot in background")
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Give bot time to start
    time.sleep(2)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
