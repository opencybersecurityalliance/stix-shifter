from stix_shifter.stix_translation import stix_translation
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern = r'\"\d{2}\s[a-zA-Z]{3}\s\d{4}\s(\d{2}\:){2}(\d{2})\s(\+|\-){1}\d{4}\"'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestStixToRelevance(unittest.TestCase):
    """
    class to perform unit test case bigfix translate query
    """

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    maxDiff = None

    def test_one_obser_eq_operator_file(self):
        """
        to test single observation with '=' operator
        """
        stix_pattern = "[file:name = '.bashrc'] START t'2013-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  '
            '"sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  '
            '(modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((name of it as '
            'string = ".bashrc" as string)) AND (modification time of it is greater than or equal to "10 Jan 2013 '
            '08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 '
            '+0000" as time)) of  (system folder; folders of system '
            'folder)</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_obser_ne_operator_process(self):
        """
        to test single observation with '!=' operator
        """
        stix_pattern = "[process:name != 'cron'] START t'2019-08-01T08:43:10.003Z' STOP t'2019-08-31T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("process", name of it | "n/a",  pid of it as string | "n/a",  '
            '"sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", '
            'md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  '
            '(if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string '
            '| "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | '
            '"01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time '
            'of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of '
            'processes whose (((name of it as lowercase != "cron" as lowercase)) AND (if (windows of operating '
            'system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "01 '
            'Aug 2019 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less '
            'than or equal to "31 Aug 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 '
            '+0000" as time is greater than or equal to "01 Aug 2019 08:43:10 +0000" as time AND start time of it | '
            '"01 Jan 1970 00:00:00 +0000" as time is less than or equal to "31 Aug 2019 10:43:10 +0000" as '
            'time)))</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_obser_in_operator_process(self):
        """
        to test single observation with 'IN' operator
        """
        stix_pattern = "[process:creator_user_ref.user_id IN ('root','rpc')] START " \
                       "t'2013-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("process", name of it | "n/a",  pid of it as string | "n/a",  '
            '"sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", '
            'md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  '
            '(if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string '
            '| "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | '
            ' as time -   as time)/second else  (start time of it |  as time -   as time)/second))  of processes '
            'whose (((if (windows of operating system) then (user of it as lowercase = "root" as lowercase OR user of '
            'it as lowercase = "rpc" as lowercase) else (name of user of it as lowercase = "root" as lowercase OR '
            'name of user of it as lowercase = "rpc" as lowercase))) AND (if (windows of operating system) then ('
            'creation time of it |  as time is greater than or equal to  as time AND creation time of it |  as time '
            'is less than or equal to  as time) else (start time of it |  as time is greater than or equal to  as '
            'time AND start time of it |  as time is less than or equal to  as '
            'time)))</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_obser_in_operator_mac(self):
        """
        to test single observation with 'LIKE' operator
        """
        stix_pattern = "[network-traffic:src_ref.value IN ('0a-65-a4-7f-ad-65','0a-d0-c4-a0-e4-b4')] START " \
                       "t'2013-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("Address", address of it as string | "n/a",  mac address of it as '
            'string | "n/a") of adapters whose (((mac address of it as string = "0a-65-a4-7f-ad-65" as string) OR ('
            'mac address of it as string = "0a-d0-c4-a0-e4-b4" as string)) AND (loopback of it = false AND address of '
            'it != "0.0.0.0")) of network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target'
            '></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_obser_like_operator_network(self):
        """
        to test single observation with 'LIKE' operator
        """
        stix_pattern = "[ipv4-addr:value LIKE '169.254']"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("Local Address", local address of it as string | "n/a",  '
            '"Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  '
            '"remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it '
            'as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image '
            'files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of '
            'image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of '
            'operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it '
            'as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then '
            ' (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" '
            'as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan '
            '1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local '
            'address of it as string contains "169.254" as string OR remote address of it as string contains '
            '"169.254" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 '
            'Jan 1970 00:00:00 +0000" as time is greater than or equal to "04 Sep 2019 11:38:50 +0000" as time AND '
            'creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "04 Sep '
            '2019 11:43:50 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time '
            'is greater than or equal to "04 Sep 2019 11:38:50 +0000" as time AND start time of process of it | "01 '
            'Jan 1970 00:00:00 +0000" as time is less than or equal to "04 Sep 2019 11:43:50 +0000" as time))) of '
            'network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_obser_not_operator_file(self):
        """
        to test single observation with 'LIKE' operator
        """
        stix_pattern = "[ipv4-addr:value NOT LIKE '169.254']"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("Local Address", local address of it as string | "n/a",  '
            '"Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  '
            '"remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it '
            'as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image '
            'files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of '
            'image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of '
            'operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it '
            'as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then '
            ' (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" '
            'as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan '
            '1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose ((NOT (('
            'local address of it as string contains "169.254" as string OR remote address of it as string contains '
            '"169.254" as string))) AND (if (windows of operating system) then (creation time of process of it | "01 '
            'Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND '
            'creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct '
            '2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time '
            'is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 '
            'Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of '
            'network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_obser_match_operator_file(self):
        """
        to test single observation with 'MATCH' operator
        """
        stix_pattern = "[file:name MATCHES  '^bash\\w+']"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  '
            '"sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  '
            '(modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((exist '
            'matches(regex"(^bash&#92;w+)") of (name of it as string))) AND (modification time of it is greater than '
            'or equal to "29 Aug 2019 15:27:20 +0000" as time AND modification time of it is less than or equal to '
            '"29 Aug 2019 15:32:20 +0000" as time)) of  (system folder; folders of system '
            'folder)</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_one_combined_comparision_mac_ipv4(self):
        """
        to test single observation with 'LIKE' operator
        """
        stix_pattern = "[mac-addr:value LIKE '0a-fb-a0-5a' AND ipv4-addr:value = '127.0.0.1'] START " \
                       "t'2013-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("Local Address", local address of it as string | "n/a",  '
            '"Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  '
            '"remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it '
            'as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image '
            'files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of '
            'image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of '
            'operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it '
            'as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then '
            ' (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" '
            'as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan '
            '1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local '
            'address of it as string = "127.0.0.1" as string OR remote address of it as string = "127.0.0.1" as '
            'string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 '
            '00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation '
            'time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 '
            '10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is '
            'greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 Jan '
            '1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of '
            'network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>',
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("Address", address of it as string | "n/a",  mac address of it as '
            'string | "n/a") of adapters whose ((mac address of it as string contains "0a-fb-a0-5a" as string) AND ('
            'loopback of it = false AND address of it != "0.0.0.0")) of '
            'network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_two_combined_obser_expression(self):
        """
        to test 2 observation expression
        """
        stix_pattern = "([file:name =  'udf.conf' and file:parent_directory_ref.path='/root'] AND [process:name = " \
                       "'rpciod']) START t'2013-01-01T08:43:10.003Z' " \
                       "STOP t'2019-07-25T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  '
            '"sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  '
            '(modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((name of it as '
            'string = "udf.conf" as string)) AND (modification time of it is greater than or equal to "01 Jan 2013 '
            '08:43:10 +0000" as time AND modification time of it is less than or equal to "25 Jul 2019 10:43:10 '
            '+0000" as time)) of  (system folder; folders of system '
            'folder)</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>',
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("process", name of it | "n/a",  pid of it as string | "n/a",  '
            '"sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", '
            'md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  '
            '(if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string '
            '| "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | '
            '"01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time '
            'of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of '
            'processes whose (((name of it as lowercase = "rpciod" as lowercase)) AND (if (windows of operating '
            'system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "01 '
            'Jan 2013 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less '
            'than or equal to "25 Jul 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 '
            '+0000" as time is greater than or equal to "01 Jan 2013 08:43:10 +0000" as time AND start time of it | '
            '"01 Jan 1970 00:00:00 +0000" as time is less than or equal to "25 Jul 2019 10:43:10 +0000" as '
            'time)))</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_three_combined_obser_expression(self):
        """
        to test 3 observation expression
        """
        stix_pattern = "([process:name = 'systemd' AND process:binary_ref.hashes.'SHA-256' = " \
                       "'2f2f74f4083b95654a742a56a6c7318f3ab378c94b69009ceffc200fbc22d4d8'] AND [file:name LIKE " \
                       "'rc.status' AND file:parent_directory_ref.path = '/etc'] OR [ipv4-addr:value LIKE '169.254'])" \
                       "START t'2012-04-10T08:43:10.003Z' STOP t'2020-04-23T10:43:10.003Z'"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = [
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("process", name of it | "n/a",  pid of it as string | "n/a",  '
            '"sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", '
            'md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  '
            '(if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string '
            '| "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | '
            '"01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time '
            'of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of '
            'processes whose (((sha256 of image file of it as string = '
            '"2f2f74f4083b95654a742a56a6c7318f3ab378c94b69009ceffc200fbc22d4d8" as string) AND (name of it as '
            'lowercase = "systemd" as lowercase)) AND (if (windows of operating system) then (creation time of it | '
            '"01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Apr 2012 08:43:10 +0000" as time '
            'AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Apr 2020 '
            '10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than '
            'or equal to "10 Apr 2012 08:43:10 +0000" as time AND start time of it | "01 Jan 1970 00:00:00 +0000" as '
            'time is less than or equal to "23 Apr 2020 10:43:10 +0000" as '
            'time)))</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>',
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  '
            '"sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  '
            '(modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((name of it as '
            'string contains "rc.status" as string)) AND (modification time of it is greater than or equal to "10 Apr '
            '2012 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Apr 2020 10:43:10 '
            '+0000" as time)) of folder "/etc"</QueryText><Target><CustomRelevance>true</CustomRelevance></Target'
            '></ClientQuery></BESAPI>',
            '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true'
            '</ApplicabilityRelevance><QueryText>("Local Address", local address of it as string | "n/a",  '
            '"Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  '
            '"remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it '
            'as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image '
            'files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of '
            'image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of '
            'operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it '
            'as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then '
            ' (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" '
            'as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan '
            '1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local '
            'address of it as string contains "169.254" as string OR remote address of it as string contains '
            '"169.254" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 '
            'Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Apr 2012 08:43:10 +0000" as time AND '
            'creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Apr '
            '2020 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time '
            'is greater than or equal to "10 Apr 2012 08:43:10 +0000" as time AND start time of process of it | "01 '
            'Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Apr 2020 10:43:10 +0000" as time))) of '
            'network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>']

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    @staticmethod
    def test_one_obser_is_super_set_operator_network():
        """
        to test single observation with an un-supported operator
        """
        stix_pattern = "([ipv4-addr:value ISSUPERSET '172.217.0.0/24'] " \
                       "START t'2019-04-10T08:43:10.003Z' STOP t'2019-04-23T10:43:10.003Z')"
        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        assert query['success'] is False
        assert query['code'] == 'not_implemented'
        assert query['error'] == 'wrong parameter : Comparison operator IsSuperSet unsupported for BigFix adapter'
