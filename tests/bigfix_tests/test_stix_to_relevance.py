from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries):
    assert query['queries'] == queries


class TestStixToRelevance(unittest.TestCase, object):

    def test_process_query(self):

        stix_pattern = "[process:name = 'node' AND file:hashes.'SHA-256' = '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5']"

        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        # queries = '( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image file of it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes whose (name of it as lowercase = "node" as lowercase AND sha256 of image file of it as lowercase = "0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5" as lowercase )'

        queries = '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image file of it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes whose (name of it as lowercase = "node" as lowercase AND sha256 of image file of it as lowercase = "0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5" as lowercase )</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>'
        _test_query_assertions(query, queries)

    def test_file_query(self):

        stix_pattern = "[file:name = 'a' AND file:parent_directory_ref.path = '/root' OR file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d']"

        query = translation.translate('bigfix', 'query', '{}', stix_pattern)
        # queries = '("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files whose (name of it as lowercase = "a" as lowercase OR sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d" as lowercase) of folder ("/root")'

        queries = '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files whose (name of it as lowercase = "a" as lowercase OR sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d" as lowercase) of folder ("/root")</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>'
        _test_query_assertions(query, queries)
