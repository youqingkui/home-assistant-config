#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/23 18:08
# @Author  : youqingkui
# @File    : aws_rekognition.py
# @Desc    :

import asyncio
import json
import logging
import os

import aiohttp
from aiohttp.hdrs import CONTENT_TYPE
import async_timeout
import voluptuous as vol

import boto3


_LOGGER = logging.getLogger(__name__)

DOMAIN = 'aws_rekognition'
DEPENDENCIES = ['camera']


CONF_REGION_NAME = 'region_name'
# DEFAULT_CONF_REGION_NAME = 'us-east-1'
# CONF_ATTRIBUTES = 'attributes'

client = boto3.client('rekognition', region_name='us-east-1')



def setup(hass, config):
    """Set up microsoft face."""
    entity_id = 'aws_rekognition.last_message'

    def face_index(call):
        bucket = call.data.get('bucket')
        fileName = call.data.get('fileName')
        response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}}, MinConfidence=75)
        _LOGGER.warning("face_index => %s" % response)
        hass.states.set(entity_id, 'hello aws')

    hass.states.set(entity_id, 'No messages')

    hass.services.register(DOMAIN, 'set_state', face_index)
    return True


# class AwsFace(object):
#     def __init__(self, hass, region_name, timeout, entities):
#         self.hass = hass
#         self.websession = async_get_clientsession(hass)
#         self.timeout = timeout
#         self._store = {}
#         self._entities = entities
#
#     @property
#     def store(self):
#         """Store group/person data and IDs."""
#         return self._store
#
#     @asyncio.coroutine
#     def index_faces(self, image):
#         response = client.index_faces(Image={'Bytes': image})
#         return response
# @asyncio.coroutine
# def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
#     """Set up the Microsoft Face detection platform."""
#     # api = hass.data[DATA_MICROSOFT_FACE]
#     # attributes = config[CONF_ATTRIBUTES]
#     attributes = 'aws_rekognition'
#
#     entities = []
#     for camera in config[CONF_SOURCE]:
#         entities.append(AwsFaceDetectEntity(
#             camera[CONF_ENTITY_ID], attributes, camera.get(CONF_NAME)
#         ))
#
#     async_add_devices(entities)
#
#
# class AwsFaceDetectEntity(ImageProcessingEntity):
#     """Microsoft Face API entity for identify."""
#
#     def __init__(self, camera_entity, attributes, name=None):
#         """Initialize Microsoft Face."""
#         super().__init__()
#
#         self._camera = camera_entity
#         self._attributes = attributes
#
#         if name:
#             self._name = name
#         else:
#             self._name = "MicrosoftFace {0}".format(
#                 split_entity_id(camera_entity)[1])
#
#     @property
#     def camera_entity(self):
#         """Return camera entity id from process pictures."""
#         return self._camera
#
#     @property
#     def name(self):
#         """Return the name of the entity."""
#         return self._name
#
#     @asyncio.coroutine
#     def async_process_image(self, image):
#         """Process image.
#
#         This method is a coroutine.
#         """
#         face_data = None
#         # _LOGGER.warning("image ==> %s" % image)
#         try:
#             face_data = yield from client.index_faces(Image={'Bytes': image})
#             _LOGGER.warning("face_data ==> %s" % face_data)
#
#         except HomeAssistantError as err:
#             _LOGGER.error("Can't process image on microsoft face: %s", err)
#             return
#
#         if face_data is None or len(face_data) < 1:
#             return
#
#         faces = []
#         for face in face_data:
#             face_attr = {}
#             for attr in self._attributes:
#                 if attr in face['faceAttributes']:
#                     face_attr[attr] = face['faceAttributes'][attr]
#
#             if face_attr:
#                 faces.append(face_attr)
#
#         self.async_process_faces(faces, len(face_data))
