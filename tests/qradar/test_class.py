from src import base_module


class TestStixToAql(object):
    def test_ipv4_query(self):
        interface = base_module.TranslationInterface()
        input_arguments = [
            "qradar", "sco", "[ipv4-addr:value = '9.21.122.83' or ipv4-addr:value = '9.21.122.83']"]
        query = interface.stix_to_datasource_query(input_arguments)
        assert query == "SELECT * FROM events WHERE destinationip='9.21.122.83' OR sourceip='9.21.122.83' OR destinationip='9.21.122.83' OR sourceip='9.21.122.83'"
