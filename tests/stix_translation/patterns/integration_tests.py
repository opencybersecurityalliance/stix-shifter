import unittest
import logging
from uuid import uuid4
import types
from collections import OrderedDict

from stix_shifter.stix_translation.src.patterns.translator import translate, SearchPlatforms, DataModels
from .helpers.input_file_helpers import input_files, collect_targets
from .helpers.connectors import SplunkConnector, ElasticConnector

class IntegrationTests(unittest.TestCase):
    test_type = None

    def setUp(self):
        # Todo make this less messy
        if self.test_type == SearchPlatforms.SPLUNK:
            self.splunk = SplunkConnector()
        elif self.test_type == SearchPlatforms.ELASTIC:
            self.elastic = ElasticConnector()
        else:
            self.splunk = SplunkConnector()
            self.elastic = ElasticConnector()

    @staticmethod
    def generate_tests():
        NOT_SUPPORTED = (DataModels.CIM.name.lower(), SearchPlatforms.ELASTIC.name.lower())
        test_classes = OrderedDict()
        for file_name, test_content in input_files().items():
            if 'matches' in test_content or 'nonmatches' in test_content:
                platforms, models = collect_targets(test_content)
                # Need to explode the platform and model combinations to do each
                for platform in platforms:
                    for model in models:
                        if ((model.value, platform.value) == (NOT_SUPPORTED)):
                            break

                        # Build a new TestCase class for each platform
                        class_key = (model.value.title(), platform.value.title())
                        if class_key not in test_classes:
                            new_class = types.new_class("Test{}".format(''.join(class_key)), bases=(IntegrationTests,))
                            new_class.__module__ = __name__
                            new_class.test_type = platform
                            test_classes[class_key] = new_class

                        # generate the test method
                        test_name = "test_integration_{}_{}_{}".format(file_name, model.value, platform.value)
                        test = IntegrationTests.integration_test_generator(model, platform, test_content)

                        # Add the generated test to the appropriate target class.
                        destination_class = test_classes.get(class_key, IntegrationTests)
                        setattr(destination_class, test_name, test)
        for _, dynamic_class in sorted(test_classes.items()):
            globals()[str(dynamic_class)] = dynamic_class
            pass

    @staticmethod
    def integration_test_generator(model, platform, data):
        """ Generates an integration test """
        def test(self):
            # Collect all of the events
            nonmatches = data['nonmatches'].get(model.value, [])
            matches = data['matches'].get(model.value, [])
            events = nonmatches + matches
            connector = None

            if platform == SearchPlatforms.SPLUNK:
                connector = self.splunk
            elif platform == SearchPlatforms.ELASTIC:
                connector = self.elastic

            # Add the GUID, which is how we line up the data after the search
            [e.update({'guid': str(uuid4())}) for e in events]

            # Then send them to all the search platforms. Need to include what data model because some platforms need to
            # format data per data model
            connector.push(model, events)

            # Then, run the tests. The GUIDs in "matches" should be in the results, the GUIDs in "nonmatches" should not.
            query = translate(data['stix-input'], platform, model)
            results = connector.query(query, model)

            # Perform the comparison of GUIDs
            self.assertEqual(set([e['guid'] for e in data['matches'][model.value]]), set(results))

        return test

IntegrationTests.generate_tests()
