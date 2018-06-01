from src import base_module

selections = "SELECT QIDNAME(qid) as qidname, qid as qid, CATEGORYNAME(category) as categoryname, \
category as categoryid, CATEGORYNAME(highlevelcategory) as high_level_category_name, \
highlevelcategory as high_level_category_id, LOGSOURCETYPENAME(logsourceid) as logsourcename, starttime as starttime, \
endtime as endtime, devicetime as devicetime, sourceip as sourceip, sourceport as sourceport, sourcemac as sourcemac, \
destinationip as destinationip, destinationport as destinationport, destinationmac as destinationmac, \
username as username, eventdirection as direction, identityip as identityip, identityhostname as identity_host_name, \
eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol"


class TestStixToAql(object):

    def test_ipv4_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"]
        query = interface.stix_to_datasource_query(input_arguments)
        assert query == selections + " FROM events WHERE sourceip='192.168.122.84' OR destinationip='192.168.122.84' OR sourceip='192.168.122.83' OR destinationip='192.168.122.83'"

    def test_ipv6_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[ipv6-addr:value = '192.168.122.83']"]
        query = interface.stix_to_datasource_query(input_arguments)
        assert query == selections + \
            " FROM events WHERE sourceip='192.168.122.83' OR destinationip='192.168.122.83'"

    def test_url_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[url:value = 'http://www.testaddress.com']"]
        query = interface.stix_to_datasource_query(input_arguments)
        assert query == selections + \
            " FROM events WHERE url='http://www.testaddress.com'"

    def test_mac_address_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[mac-addr:value = '00-00-5E-00-53-00']"]
        query = interface.stix_to_datasource_query(input_arguments)
        assert query == selections + \
            " FROM events WHERE sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00'"

    def test_domain_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[domain-name:value = 'example.com']"]
        query = interface.stix_to_datasource_query(input_arguments)
        assert query == selections + \
            " FROM events WHERE domainname='example.com'"

    def test_query_from_multiple_observation_expressions(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[domain-name:value = 'example.com'] and [mac-addr:value = '00-00-5E-00-53-00']"]
        query = interface.stix_to_datasource_query(input_arguments)
        # Expect the STIX and to be converted to an AQL or.
        assert query == selections + \
            " FROM events WHERE domainname='example.com' OR sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00'"
