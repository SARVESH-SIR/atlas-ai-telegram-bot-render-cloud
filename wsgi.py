#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI entry point for Render with gunicorn
"""

from media_app_server import app

if __name__ == "__main__":
    app.run()
