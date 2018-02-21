#!/usr/bin/python3
# -*- coding: utf-8 -*-
from application.app import create_app
from application.config import test_config

app = create_app(configs=[test_config])
app.run(host='127.0.0.1', port=5000)

