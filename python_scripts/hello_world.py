#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 19:44
# @Author  : youqingkui
# @File    : hello_world.py.py
# @Desc    :


name = data.get('name', 'world')
logger.info("Hello {}".format(name))
hass.bus.fire(name, { "wow": "from a Python script!" })