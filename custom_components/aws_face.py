#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/24 16:29
# @Author  : youqingkui
# @File    : aws_face.py
# @Desc    :


import asyncio
import logging
import boto3

import voluptuous as vol

from homeassistant.core import split_entity_id
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.microsoft_face import DATA_MICROSOFT_FACE
from homeassistant.components.image_processing import (
    PLATFORM_SCHEMA, CONF_SOURCE, CONF_ENTITY_ID, CONF_NAME)
from homeassistant.components.image_processing.microsoft_face_identify import (
    ImageProcessingFaceEntity, ATTR_GENDER, ATTR_AGE, ATTR_GLASSES)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.image_processing.microsoft_face_identify import (
    ImageProcessingFaceEntity, ATTR_NAME, ATTR_AGE, ATTR_GENDER)
from homeassistant.components.image_processing import ATTR_CONFIDENCE


_LOGGER = logging.getLogger(__name__)
client = boto3.client('rekognition', region_name='us-east-1')
DEPENDENCIES = ['camera']

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Microsoft Face detection platform."""

    entities = []
    for camera in config[CONF_SOURCE]:
        entities.append(AwsFaceDetectEntity(
            camera[CONF_ENTITY_ID],camera.get(CONF_NAME)
        ))

    async_add_devices(entities)


class AwsFaceDetectEntity(ImageProcessingFaceEntity):
    """Microsoft Face API entity for identify."""

    def __init__(self, camera_entity, name=None):
        """Initialize Microsoft Face."""
        super().__init__()

        self._camera = camera_entity

        if name:
            self._name = name
        else:
            self._name = "MicrosoftFace {0}".format(
                split_entity_id(camera_entity)[1])

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @asyncio.coroutine
    def async_process_image(self, image):
        """Process image.

        This method is a coroutine.
        """
        face_data = None
        # _LOGGER.warning("image ==> %s" % image)
        try:
            response = client.index_faces(Image={'Bytes': image.read()})
            _LOGGER.warning("response => %s" % response)
        except HomeAssistantError as err:
            _LOGGER.error("Can't process image on microsoft face: %s", err)
            return

        # if face_data is None or len(face_data) < 1:
        #     return
        #
        # faces = []
        # for face in face_data:
        #     face_attr = {}
        #     for attr in self._attributes:
        #         if attr in face['faceAttributes']:
        #             face_attr[attr] = face['faceAttributes'][attr]
        #
        #     if face_attr:
        #         faces.append(face_attr)
        demo_data = [
            {
                ATTR_CONFIDENCE: 98.34,
                ATTR_NAME: 'Hans',
                ATTR_AGE: 16.0,
                ATTR_GENDER: 'male',
            },
            {
                ATTR_NAME: 'Helena',
                ATTR_AGE: 28.0,
                ATTR_GENDER: 'female',
            },
            {
                ATTR_CONFIDENCE: 62.53,
                ATTR_NAME: 'Luna',
            },
        ]

        self.async_process_faces(demo_data, len(demo_data))