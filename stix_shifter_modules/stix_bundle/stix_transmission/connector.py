
from aiohttp import BasicAuth
import json
import re
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix2matcher.matcher import Pattern, MatchListener
from stix2matcher import matcher as stix2matcher_module
from stix_shifter_utils.utils.error_response import ErrorResponder


# ANTLR 4.13.2 Compatibility Patch for stix2-matcher
# stix2-matcher==3.0.0 has a bug where _literal_terminal_to_python_val() converts
# TimestampLiterals to datetime objects, but then the code tries to convert them
# again with _str_to_datetime(), causing "'datetime.datetime' object is not iterable".
# This patch fixes it by getting the raw text from the token instead.
# See: https://github.com/oasis-open/cti-pattern-matcher/issues
# Remove this patch when stix2-matcher is updated to fix this issue.
def _apply_stix2matcher_compatibility_patch():
    """Apply runtime compatibility patch for stix2-matcher with ANTLR 4.13.2."""
    # Check if not already patched
    if hasattr(stix2matcher_module, '_antlr_patched'):
        return

    def patched_exitStartStopQualifier(self, ctx):
        """Patched version that gets raw timestamp text instead of pre-converted datetime."""
        # For both STIX 2.0 and 2.1, get the raw text from the timestamp tokens
        # and convert them to datetime objects. The issue is that
        # _literal_terminal_to_python_val already converts TimestampLiterals,
        # so we need to get the raw text using .getText() instead.
        start_token = ctx.TimestampLiteral(0)
        stop_token = ctx.TimestampLiteral(1)

        # Get raw text and strip the t' prefix and ' suffix: t'2020-...' -> 2020-...
        start_text = start_token.getText()
        stop_text = stop_token.getText()
        start_str = start_text[2:-1] if start_text.startswith("t'") else start_text
        stop_str = stop_text[2:-1] if stop_text.startswith("t'") else stop_text

        # Convert timestamp strings to datetime objects
        try:
            start_dt = stix2matcher_module._str_to_datetime(start_str)
            stop_dt = stix2matcher_module._str_to_datetime(stop_str)
        except ValueError as e:
            # re-raise as MatcherException (Python 3 syntax)
            raise stix2matcher_module.MatcherException(*e.args) from e

        self._MatchListener__push((start_dt, stop_dt), u"exitStartStopQualifier")

    # Apply the patch
    stix2matcher_module.MatchListener.exitStartStopQualifier = patched_exitStartStopQualifier
    stix2matcher_module._antlr_patched = True


# Apply the patch when the module is loaded
_apply_stix2matcher_compatibility_patch()


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.connection = connection
        self.configuration = configuration
        self.timeout = connection['options'].get('timeout')
        self.bundle_url = self.connection.get('url')
        auth = None
        conf_auth = configuration.get('auth', {})
        if 'username' in conf_auth and 'password' in conf_auth:
            auth = BasicAuth(conf_auth['username'], conf_auth['password'])
        self.client = RestApiClientAsync(None,
                                    auth=auth,
                                    url_modifier_function=lambda host_port, endpoint, headers: f'{endpoint}')

    # We re-implement this method so we can fetch all the "bindings", as their method only
    # returns the first for some reason
    def match(self, pattern, observed_data_sdos, verbose=False, stix_version='2.0'):
        compiled_pattern = Pattern(pattern, stix_version=stix_version)
        matcher = MatchListener(observed_data_sdos, verbose, stix_version=stix_version)
        compiled_pattern.walk(matcher)

        found_bindings = matcher.matched()

        if found_bindings:
            matching_sdos = []
            for binding in found_bindings:
                matches = [match for match in matcher.get_sdos_from_binding(binding) if match not in matching_sdos]
                matching_sdos.extend(matches)
        else:
            matching_sdos = []

        return matching_sdos

    async def ping_connection(self):
        return_obj = dict()

        response = await self.client.call_api(self.bundle_url, 'head', timeout=self.timeout)
        response_txt = response.raise_for_status()

        if response.code == 200:
            return_obj['success'] = True
        elif response.code == 301:
            self.bundle_url = response.headers.get('Location')
            return await self.ping_connection()
        else:
            ErrorResponder.fill_error(return_obj, response_txt, ['message'], connector=self.connector)
        return return_obj

    async def create_results_connection(self, search_id, offset, length):
        observations = []
        return_obj = dict()
        is_stix_21 = self.connection.get('options', {}).get("stix_2.1")
        stix_version = '2.1' if is_stix_21 else '2.0'

        # NOTE: The 't' prefix in timestamp literals (t'2020-09-30T16:24:59.988Z') is required by
        # stix2-matcher for both STIX 2.0 and 2.1. Do not remove it.

        response = await self.client.call_api(self.bundle_url, 'get', timeout=self.timeout)

        if response.code != 200:
            response_txt = response.raise_for_status()
            if ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            elif ErrorResponder.is_json_string(response_txt):
                response_json = json.loads(response_txt)
                ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            else:
                raise UnexpectedResponseException
        else:
            try:
                response_txt = response.read().decode('utf-8')
                bundle = json.loads(response_txt)


                if is_stix_21:
                    observations = [bundle]
                else:
                    for obj in bundle["objects"]:
                        if obj["type"] == "observed-data":
                            observations.append(obj)

                # Pattern match
                try:
                    results = self.match(search_id, observations, False, stix_version)
                    if is_stix_21:
                        v21_results = []
                        v21_observed_data = []
                        v21_cboxes = {}
                        for obs_obj in results:
                            if "objects" in obs_obj:
                                for obj in obs_obj["objects"]:
                                    if obj['type'] == "observed-data":
                                        v21_observed_data.append(obj)
                                    elif obj['type'] != "identity":
                                        v21_cboxes[obj['id']] = obj

                        v21_observed_data = v21_observed_data[int(offset):int(offset + length)]
                        v21_results.extend(v21_observed_data)
                        for observed_data in v21_observed_data:
                            for ref in observed_data['object_refs']:
                                if ref in v21_cboxes:
                                    v21_results.append(v21_cboxes[ref])
                                    del v21_cboxes[ref]
                        
                        results = v21_results
                    else:
                        results = results[int(offset):int(offset + length)]

                    if len(results) != 0:
                        return_obj['success'] = True
                        return_obj['data'] = results
                    else:
                        return_obj['success'] = True
                        return_obj['data'] = []
                except Exception as ex:
                    ErrorResponder.fill_error(return_obj,  message='Object matching error: ' + str(ex), connector=self.connector)
            except Exception as ex:
                ErrorResponder.fill_error(return_obj,  message='Invalid STIX bundle. Malformed JSON: ' + str(ex), connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        return {'success': True}

    def test_START_STOP_format(self, query_string) -> bool:
        # Matches START t'1234-56-78T00:00:00.123Z' STOP t'1234-56-78T00:00:00.123Z'
        pattern = r"START\s(t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')\sSTOP"
        match = re.search(pattern, query_string)
        return bool(match)