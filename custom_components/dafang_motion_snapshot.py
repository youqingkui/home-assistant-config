#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 15:19
# @Author  : youqingkui
# @File    : dafang_motion_snapshot.py
# @Desc    :

import asyncio
import json
import logging
import os

import homeassistant.loader as loader

_LOGGER = logging.getLogger(__name__)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = 'dafang_motion_snapshot'

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']


CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'myhome/dafang/motion/snapshot'


def setup(hass, config):
    """Set up the Hello MQTT component."""
    mqtt = loader.get_component(hass, 'mqtt')
    topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    entity_id = 'snapshot_mqtt.last_message'

    # Listener to be called when we receive a message.
    def message_received(topic, payload, qos):
        """Handle new MQTT messages."""
        print(payload)
        _LOGGER.warning("message_received %s" % topic)
        with open('/home/pi/.homeassistant/dafang_motion_snapshot/snapshot/test_hello.jpg') as f:
            f.write(payload)
        hass.states.set(entity_id, 'payload')
        _LOGGER.warning("message_received %s" % topic)

    # Subscribe our listener to a topic.
    mqtt.subscribe(hass, topic, message_received)

    # Set the initial state.
    hass.states.set(entity_id, 'No messages')

    # Service to publish a message on MQTT.
    def set_state_service(call):
        """Service to send a message."""
        mqtt.publish(hass, topic, call.data.get('new_state'))

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, 'set_state', set_state_service)

    # Return boolean to indicate that initialization was successfully.
    return True