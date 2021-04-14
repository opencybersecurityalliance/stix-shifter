from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
import re

START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"

ERROR_TYPE_PARSE_EXCEPTION = 'parse_exception'
ERROR_TYPE_TRANSFORM_EXCEPTION = 'transform_exception'

class QueryTranslator(EmptyQueryTranslator):

    # def parse_query(self, data):
    #     # TODO: replicate parse query from superclass
    #     pass

    def parse_query(self, data):
        print('**IN PARSE QUERY')
        print(self.options.get('error_type'))
        if self.options.get('error_type') == ERROR_TYPE_PARSE_EXCEPTION:
            print('** triggering parse exception')
            raise Exception('test exception in parse query')
        return super().parse_query(data)
        # if self.options.get('validate_pattern'):
        #     self._validate_pattern(data)
        # antlr_parsing = generate_query(data)
        # # Extract pattern elements into parsed stix object
        # parsed_stix_dictionary = parse_stix(antlr_parsing, self.options['time_range'])
        # parsed_stix = parsed_stix_dictionary['parsed_stix']
        # start_time = parsed_stix_dictionary['start_time']
        # end_time = parsed_stix_dictionary['end_time']
        # return {'parsed_stix': parsed_stix, 'start_time': start_time, 'end_time': end_time}


    def transform_query(self, data):
        print('*** IN TRANSFORM QUERY OF NEW CONNECTOR')
        print(self.options.get('error_type'))
        if self.options.get('error_type') == ERROR_TYPE_TRANSFORM_EXCEPTION:
            print('** triggering transform exception')
            raise Exception('test exception in transform query')
        # Data is a STIX pattern.
        # stix2-matcher will break on START STOP qualifiers so remove before returning pattern.
        # Remove this when ever stix2-matcher supports proper qualifier timestamps
        data = re.sub(START_STOP_PATTERN, " ", data)
        return {'queries': [data]}
