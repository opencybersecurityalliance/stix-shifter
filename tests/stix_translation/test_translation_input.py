from stix_shifter.stix_translation import stix_translation
import json

data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "unsupportedDataSource",
    "identity_class": "events"
}

data = {"key": "value"}

data_source_string = json.dumps(data_source)
data_string = json.dumps(data)
translation = stix_translation.StixTranslation()


class TestTranslation(object):

    def test_unsupported_datasource_for_results(self):
        result = translation.translate('unsupportedDataSource', 'results', data_source_string, data_string)
        assert result == {'code': 'not_implemented', 'error': 'unsupported datasource : unsupportedDataSource is an unsupported data source.', 'success': False}

    def test_unsupported_datasource_for_query(self):
        result = translation.translate('unsupportedDataSource', 'query', '{}', "[ipv4-addr:value = '333.333.333.0']")
        assert result == {'code': 'not_implemented', 'error': 'unsupported datasource : unsupportedDataSource is an unsupported data source.', 'success': False}
