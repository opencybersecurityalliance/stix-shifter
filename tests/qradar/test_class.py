from src import base_module


class TestStixToAql(object):
    def test_ipv4_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"]
        query = interface.stix_to_datasource_query(input_arguments)
        selections = "SELECT QIDNAME(qid) as qidname, qid as qid, CATEGORYNAME(category) as categoryname,\
    category as categoryid, CATEGORYNAME(highlevelcategory) as high_level_category_name,\
    highlevelcategory as high_level_category_id, LOGSOURCETYPENAME(logsourceid) as logsourcename, starttime as starttime,\
    endtime as endtime, devicetime as devicetime, sourceip as sourceip, sourceport as sourceport, sourcemac as sourcemac,\
    destinationip as destinationip, destinationport as destinationport, destinationmac as destinationmac,\
    username as username, eventdirection as direction, identityip as identityip, identityhostname as identity_host_name,\
    eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol"
        assert query == selections + " FROM events WHERE destinationip='192.168.122.84' OR sourceip='192.168.122.84' OR destinationip='192.168.122.83' OR sourceip='192.168.122.83'"
