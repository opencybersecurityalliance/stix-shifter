# -*- coding: utf-8 -*-
import json
import unittest
import uuid
from datetime import datetime

from stix_shifter_modules.infoblox.entry_point import EntryPoint
from stix_shifter.stix_translation.stix_translation import StixTranslation
from . import utils

translation = StixTranslation()

class TestResultTranslatorMixin:

    @staticmethod
    def get_dialect():
        raise NotImplementedError()

    @property
    def data_source(self):
        now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
        return {
            "id": "identity--" + str(uuid.uuid4()),
            "name": "name",
            "type": "identity",
            "identity_class": "individual",
            "created": now,
            "modified": now
        }

    @staticmethod
    def _find_by_type(objects, obj_type):
        return next((obj for obj in objects if obj["type"] == obj_type), None)

    @staticmethod
    def _find_object_by_type(objects: dict, obj_type):
        return next(((key, obj) for key, obj in objects.items() if obj["type"] == obj_type), None)

    @staticmethod
    def _find_objects_by_type(objects: dict, obj_type):
        return [(key, obj) for key, obj in objects.items() if obj["type"] == obj_type]

    @staticmethod
    def _find_object(objects: dict, obj_type, obj_value):
        return next(((key, obj) for key, obj in objects.items() if obj["type"] == obj_type and obj["value"] == obj_value), None)

    def _get_observed_objects(self, data):
        objects = self._get_objects(data)
        ob_data = self._find_by_type(objects, "observed-data")
        return ob_data["objects"]

    def translate_results(self, data):
        result = self.results_translator.translate_results(json.dumps(self.data_source), json.dumps(data))
        return result

    def _get_objects(self, data):
        result = self.translate_results(data)
        objects = result["objects"]
        return objects

class TestStixParsingMixin:

    @staticmethod
    def get_dialect():
        raise NotImplementedError()

    @staticmethod
    def _parse_query(stix_pattern, dialect):
        query = translation.translate(f'infoblox:{dialect}', 'query', '{}', stix_pattern)
        return query

    def _retrieve_query(self, stix_pattern):
        queries: dict = self._parse_query(stix_pattern, self.get_dialect())
        self.assertIn("queries", queries)
        query = json.loads(queries["queries"][0])
        return query

    def _test_time_range(self, stix_pattern, expectation):
        query = self._retrieve_query(stix_pattern)
        self.assertEqual(expectation, query["to"] - query["from"])

    def _test_pattern(self, pattern, expectation):
        query = self._retrieve_query(pattern)
        self.assertEqual(expectation, query["query"])

    def _test_regex_timestamp(self, pattern, expectation):
        query = self._retrieve_query(pattern)
        self.assertRegex(query["query"], r'^t0=\d{10}&t1=\d{10}&' + expectation)
