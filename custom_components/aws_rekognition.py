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
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import get_component


import boto3


_LOGGER = logging.getLogger(__name__)

DOMAIN = 'aws_rekognition'
DEPENDENCIES = ['camera']


CONF_REGION = 'region_name'
CONF_ACCESS_KEY_ID = 'aws_access_key_id'
CONF_SECRET_ACCESS_KEY = 'aws_secret_access_key'



SERVICE_CREATE_COLLECTION  = 'CreateCollection '
SERVICE_LIST_COLLECTION  = 'ListCollections  '
SERVICE_DELETE_COLLECTION  = 'DeleteCollection'
SERVICE_DETECT_FACE = 'DetectFaces'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_REGION, default="us-east-1"): cv.string,
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Optional(CONF_SECRET_ACCESS_KEY): cv.string
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up microsoft face."""
    entity_id = 'aws_rekognition.last_message'
    _LOGGER.warning(config[DOMAIN])
    face = AwsFace(hass, config[DOMAIN].get(CONF_ACCESS_KEY_ID), config[DOMAIN].get(CONF_SECRET_ACCESS_KEY),
                   config[DOMAIN].get(CONF_REGION), entity_id)


    hass.services.register(DOMAIN, 'detect_faces', face.detect_faces)
    hass.services.register(DOMAIN, 'face_person', face.async_face_person)

    return True



class AwsFace(object):
    def __init__(self, hass, aws_access_key_id, aws_secret_access_key, region_name, entities):
        self.hass = hass
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self._entities = entities
        _LOGGER.warning(region_name)
        self.client = boto3.client(service_name='rekognition', region_name=self.region_name,
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)

    def detect_faces(self, call):
        bucket = call.data.get('bucket')
        fileName = call.data.get('fileName')
        try:
            response = self.client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}}, MinConfidence=75)
        except Exception as e:
            _LOGGER.error(e)
            return False
        _LOGGER.warning("response => %s" % response)
        Labels = response.get('Labels', [])
        self.hass.states.set(self._entities, Labels)
        return response

    @asyncio.coroutine
    def async_face_person(self, call):
        camera_entity = call.data['camera_entity']
        camera = get_component('camera')
        try:
            image = yield from camera.async_get_image(self.hass, camera_entity)
            response = self.client.detect_labels(
                Image={
                    'Bytes': image,
                }
            )
            _LOGGER.warning(response)
        except Exception as e:
            _LOGGER.error(e)




# def setup(hass, config):
#     """Set up microsoft face."""
#     entity_id = 'aws_rekognition.last_message'
#
#     def face_index(call):
#         bucket = call.data.get('bucket')
#         fileName = call.data.get('fileName')
#         response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}}, MinConfidence=75)
#         _LOGGER.warning("face_index => %s" % response)
#         hass.states.set(entity_id, 'hello aws')
#
#     hass.states.set(entity_id, 'No messages')
#
#     hass.services.register(DOMAIN, 'set_state', face_index)
#     return True


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
