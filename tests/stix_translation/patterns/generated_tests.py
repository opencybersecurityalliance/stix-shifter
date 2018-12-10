
import unittest
from stix_shifter.stix_translation.src.patterns.translator import translate, DataModels, SearchPlatforms
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class TextStix2PatterningInput(unittest.TestCase):
    def test_anded_obs_expressi_car_elastic(self):
        res = translate("[ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_anded_obs_expressi_cim_elastic(self):
        res = translate("[ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_anded_obs_expressi_car_splunk(self):
        res = translate("[ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_anded_obs_expressi_cim_splunk(self):
        res = translate("[ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5'] AND [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_anded_one_regex_car_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_one_regex_cim_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_one_regex_car_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_one_regex_cim_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_two_regex_car_elastic(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_two_regex_cim_elastic(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_two_regex_car_splunk(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_anded_two_regex_cim_splunk(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' AND process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_and_not_in_set_car_elastic(self):
        res = translate("[process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']    TO   ", res)
    
    def test_and_not_in_set_cim_elastic(self):
        res = translate("[process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']    TO   ", res)
    
    def test_and_not_in_set_car_splunk(self):
        res = translate("[process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']    TO   ", res)
    
    def test_and_not_in_set_cim_splunk(self):
        res = translate("[process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3) AND process:name = 'wsmprovhost.exe']    TO   ", res)
    
    def test_and_not_like_car_elastic(self):
        res = translate("[process:name NOT LIKE '%.exe' AND process:pid >= 4]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name NOT LIKE '%.exe' AND process:pid >= 4]    TO   ", res)
    
    def test_and_not_like_cim_elastic(self):
        res = translate("[process:name NOT LIKE '%.exe' AND process:pid >= 4]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name NOT LIKE '%.exe' AND process:pid >= 4]    TO   ", res)
    
    def test_and_not_like_car_splunk(self):
        res = translate("[process:name NOT LIKE '%.exe' AND process:pid >= 4]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name NOT LIKE '%.exe' AND process:pid >= 4]    TO   ", res)
    
    def test_and_not_like_cim_splunk(self):
        res = translate("[process:name NOT LIKE '%.exe' AND process:pid >= 4]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name NOT LIKE '%.exe' AND process:pid >= 4]    TO   ", res)
    
    def test_car_2013_03_001_car_elastic(self):
        res = translate("[process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']    TO   ", res)
    
    def test_car_2013_03_001_cim_elastic(self):
        res = translate("[process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']    TO   ", res)
    
    def test_car_2013_03_001_car_splunk(self):
        res = translate("[process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']    TO   ", res)
    
    def test_car_2013_03_001_cim_splunk(self):
        res = translate("[process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'reg.exe' AND process:parent_ref.name = 'cmd.exe' AND process:parent_ref.parent_ref.name != 'explorer.exe']    TO   ", res)
    
    def test_car_2013_05_002_car_elastic(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_car_2013_05_002_cim_elastic(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_car_2013_05_002_car_splunk(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_car_2013_05_002_cim_splunk(self):
        res = translate("[process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:binary_ref.parent_directory_ref.path MATCHES ':\\\\RECYCLER' OR process:binary_ref.parent_directory_ref.path MATCHES ':\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_car_2014_11_004_car_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']    TO   ", res)
    
    def test_car_2014_11_004_cim_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']    TO   ", res)
    
    def test_car_2014_11_004_car_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']    TO   ", res)
    
    def test_car_2014_11_004_cim_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:parent_ref.name = 'svchost.exe']    TO   ", res)
    
    def test_followedby_obs_expressi_car_elastic(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_followedby_obs_expressi_cim_elastic(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_followedby_obs_expressi_car_splunk(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_followedby_obs_expressi_cim_splunk(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_gt_car_elastic(self):
        res = translate("[process:pid > 4]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid > 4]    TO   ", res)
    
    def test_gt_cim_elastic(self):
        res = translate("[process:pid > 4]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid > 4]    TO   ", res)
    
    def test_gt_car_splunk(self):
        res = translate("[process:pid > 4]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid > 4]    TO   ", res)
    
    def test_gt_cim_splunk(self):
        res = translate("[process:pid > 4]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid > 4]    TO   ", res)
    
    def test_gte_car_elastic(self):
        res = translate("[process:pid >= 4]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid >= 4]    TO   ", res)
    
    def test_gte_cim_elastic(self):
        res = translate("[process:pid >= 4]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid >= 4]    TO   ", res)
    
    def test_gte_car_splunk(self):
        res = translate("[process:pid >= 4]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid >= 4]    TO   ", res)
    
    def test_gte_cim_splunk(self):
        res = translate("[process:pid >= 4]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid >= 4]    TO   ", res)
    
    def test_gt_and_car_elastic(self):
        res = translate("[process:pid > 512 AND process:parent_ref.pid > 7]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid > 512 AND process:parent_ref.pid > 7]    TO   ", res)
    
    def test_gt_and_cim_elastic(self):
        res = translate("[process:pid > 512 AND process:parent_ref.pid > 7]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid > 512 AND process:parent_ref.pid > 7]    TO   ", res)
    
    def test_gt_and_car_splunk(self):
        res = translate("[process:pid > 512 AND process:parent_ref.pid > 7]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid > 512 AND process:parent_ref.pid > 7]    TO   ", res)
    
    def test_gt_and_cim_splunk(self):
        res = translate("[process:pid > 512 AND process:parent_ref.pid > 7]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid > 512 AND process:parent_ref.pid > 7]    TO   ", res)
    
    def test_gt_and_gte_car_elastic(self):
        res = translate("[process:pid > 4 AND process:pid >= 512]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid > 4 AND process:pid >= 512]    TO   ", res)
    
    def test_gt_and_gte_cim_elastic(self):
        res = translate("[process:pid > 4 AND process:pid >= 512]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid > 4 AND process:pid >= 512]    TO   ", res)
    
    def test_gt_and_gte_car_splunk(self):
        res = translate("[process:pid > 4 AND process:pid >= 512]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid > 4 AND process:pid >= 512]    TO   ", res)
    
    def test_gt_and_gte_cim_splunk(self):
        res = translate("[process:pid > 4 AND process:pid >= 512]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid > 4 AND process:pid >= 512]    TO   ", res)
    
    def test_gt_and_is_equal_car_elastic(self):
        res = translate("[process:pid > 4 AND process:binary_ref.name = 'cmd.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid > 4 AND process:binary_ref.name = 'cmd.exe']    TO   ", res)
    
    def test_gt_and_is_equal_cim_elastic(self):
        res = translate("[process:pid > 4 AND process:binary_ref.name = 'cmd.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid > 4 AND process:binary_ref.name = 'cmd.exe']    TO   ", res)
    
    def test_gt_and_is_equal_car_splunk(self):
        res = translate("[process:pid > 4 AND process:binary_ref.name = 'cmd.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid > 4 AND process:binary_ref.name = 'cmd.exe']    TO   ", res)
    
    def test_gt_and_is_equal_cim_splunk(self):
        res = translate("[process:pid > 4 AND process:binary_ref.name = 'cmd.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid > 4 AND process:binary_ref.name = 'cmd.exe']    TO   ", res)
    
    def test_in_set_car_elastic(self):
        res = translate("[process:pid IN (1, 2, 3)]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid IN (1, 2, 3)]    TO   ", res)
    
    def test_in_set_cim_elastic(self):
        res = translate("[process:pid IN (1, 2, 3)]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid IN (1, 2, 3)]    TO   ", res)
    
    def test_in_set_car_splunk(self):
        res = translate("[process:pid IN (1, 2, 3)]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid IN (1, 2, 3)]    TO   ", res)
    
    def test_in_set_cim_splunk(self):
        res = translate("[process:pid IN (1, 2, 3)]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid IN (1, 2, 3)]    TO   ", res)
    
    def test_like_car_elastic(self):
        res = translate("[file:name LIKE '%.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [file:name LIKE '%.exe']    TO   ", res)
    
    def test_like_cim_elastic(self):
        res = translate("[file:name LIKE '%.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [file:name LIKE '%.exe']    TO   ", res)
    
    def test_like_car_splunk(self):
        res = translate("[file:name LIKE '%.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [file:name LIKE '%.exe']    TO   ", res)
    
    def test_like_cim_splunk(self):
        res = translate("[file:name LIKE '%.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [file:name LIKE '%.exe']    TO   ", res)
    
    def test_like_single_char_car_elastic(self):
        res = translate("[file:name LIKE 'file_.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [file:name LIKE 'file_.exe']    TO   ", res)
    
    def test_like_single_char_cim_elastic(self):
        res = translate("[file:name LIKE 'file_.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [file:name LIKE 'file_.exe']    TO   ", res)
    
    def test_like_single_char_car_splunk(self):
        res = translate("[file:name LIKE 'file_.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [file:name LIKE 'file_.exe']    TO   ", res)
    
    def test_like_single_char_cim_splunk(self):
        res = translate("[file:name LIKE 'file_.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [file:name LIKE 'file_.exe']    TO   ", res)
    
    def test_lt_car_elastic(self):
        res = translate("[process:pid < 5]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid < 5]    TO   ", res)
    
    def test_lt_cim_elastic(self):
        res = translate("[process:pid < 5]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid < 5]    TO   ", res)
    
    def test_lt_car_splunk(self):
        res = translate("[process:pid < 5]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid < 5]    TO   ", res)
    
    def test_lt_cim_splunk(self):
        res = translate("[process:pid < 5]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid < 5]    TO   ", res)
    
    def test_lte_car_elastic(self):
        res = translate("[process:pid <= 5]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid <= 5]    TO   ", res)
    
    def test_lte_cim_elastic(self):
        res = translate("[process:pid <= 5]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid <= 5]    TO   ", res)
    
    def test_lte_car_splunk(self):
        res = translate("[process:pid <= 5]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid <= 5]    TO   ", res)
    
    def test_lte_cim_splunk(self):
        res = translate("[process:pid <= 5]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid <= 5]    TO   ", res)
    
    def test_md5_hash_car_elastic(self):
        res = translate("[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']    TO   ", res)
    
    def test_md5_hash_cim_elastic(self):
        res = translate("[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']    TO   ", res)
    
    def test_md5_hash_car_splunk(self):
        res = translate("[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']    TO   ", res)
    
    def test_md5_hash_cim_splunk(self):
        res = translate("[file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [file:hashes.MD5 ='79054025255fb1a26e4bc422aef54eb4']    TO   ", res)
    
    def test_negated_compari_car_elastic(self):
        res = translate("[process:name NOT = 'wsmprovhost.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name NOT = 'wsmprovhost.exe']    TO   ", res)
    
    def test_negated_compari_cim_elastic(self):
        res = translate("[process:name NOT = 'wsmprovhost.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name NOT = 'wsmprovhost.exe']    TO   ", res)
    
    def test_negated_compari_car_splunk(self):
        res = translate("[process:name NOT = 'wsmprovhost.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name NOT = 'wsmprovhost.exe']    TO   ", res)
    
    def test_negated_compari_cim_splunk(self):
        res = translate("[process:name NOT = 'wsmprovhost.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name NOT = 'wsmprovhost.exe']    TO   ", res)
    
    def test_neq_car_elastic(self):
        res = translate("[process:name != 'wsmprovhost.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name != 'wsmprovhost.exe']    TO   ", res)
    
    def test_neq_cim_elastic(self):
        res = translate("[process:name != 'wsmprovhost.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name != 'wsmprovhost.exe']    TO   ", res)
    
    def test_neq_car_splunk(self):
        res = translate("[process:name != 'wsmprovhost.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name != 'wsmprovhost.exe']    TO   ", res)
    
    def test_neq_cim_splunk(self):
        res = translate("[process:name != 'wsmprovhost.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name != 'wsmprovhost.exe']    TO   ", res)
    
    def test_not_in_set_car_elastic(self):
        res = translate("[process:pid NOT IN (1, 2, 3)]", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3)]    TO   ", res)
    
    def test_not_in_set_cim_elastic(self):
        res = translate("[process:pid NOT IN (1, 2, 3)]", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3)]    TO   ", res)
    
    def test_not_in_set_car_splunk(self):
        res = translate("[process:pid NOT IN (1, 2, 3)]", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3)]    TO   ", res)
    
    def test_not_in_set_cim_splunk(self):
        res = translate("[process:pid NOT IN (1, 2, 3)]", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:pid NOT IN (1, 2, 3)]    TO   ", res)
    
    def test_not_like_car_elastic(self):
        res = translate("[file:name NOT LIKE '%.exe']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [file:name NOT LIKE '%.exe']    TO   ", res)
    
    def test_not_like_cim_elastic(self):
        res = translate("[file:name NOT LIKE '%.exe']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [file:name NOT LIKE '%.exe']    TO   ", res)
    
    def test_not_like_car_splunk(self):
        res = translate("[file:name NOT LIKE '%.exe']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [file:name NOT LIKE '%.exe']    TO   ", res)
    
    def test_not_like_cim_splunk(self):
        res = translate("[file:name NOT LIKE '%.exe']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [file:name NOT LIKE '%.exe']    TO   ", res)
    
    def test_ored_obs_expressi_car_elastic(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_ored_obs_expressi_cim_elastic(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_ored_obs_expressi_car_splunk(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_ored_obs_expressi_cim_splunk(self):
        res = translate("[ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [ipv4-addr:value = '198.51.100.5' ] OR [ipv4-addr:value = '198.51.100.10']    TO   ", res)
    
    def test_regex_car_elastic(self):
        res = translate("[file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']    TO   ", res)
    
    def test_regex_cim_elastic(self):
        res = translate("[file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']    TO   ", res)
    
    def test_regex_car_splunk(self):
        res = translate("[file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']    TO   ", res)
    
    def test_regex_cim_splunk(self):
        res = translate("[file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [file:parent_directory_ref.path MATCHES '^C:\\\\Windows\\\\w+$']    TO   ", res)
    
    def test_regex_anchor_car_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_anchor_cim_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_anchor_car_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_anchor_cim_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_back_anchor_car_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_back_anchor_cim_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_back_anchor_car_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_back_anchor_cim_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation$']    TO   ", res)
    
    def test_regex_front_anchor_car_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_front_anchor_cim_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_front_anchor_car_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_front_anchor_cim_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '^\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_no_anchor_car_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_no_anchor_cim_elastic(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_no_anchor_car_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_regex_no_anchor_cim_splunk(self):
        res = translate("[process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [process:name = 'wsmprovhost.exe' AND process:binary_ref.parent_directory_ref.path MATCHES '\\\\SystemVolumeInformation']    TO   ", res)
    
    def test_timestamp_car_elastic(self):
        res = translate("[file:created = t'2014-01-13T07:03:17Z']", SearchPlatforms.ELASTIC, DataModels.CAR)
        print("CONVERTED: [file:created = t'2014-01-13T07:03:17Z']    TO   ", res)
    
    def test_timestamp_cim_elastic(self):
        res = translate("[file:created = t'2014-01-13T07:03:17Z']", SearchPlatforms.ELASTIC, DataModels.CIM)
        print("CONVERTED: [file:created = t'2014-01-13T07:03:17Z']    TO   ", res)
    
    def test_timestamp_car_splunk(self):
        res = translate("[file:created = t'2014-01-13T07:03:17Z']", SearchPlatforms.SPLUNK, DataModels.CAR)
        print("CONVERTED: [file:created = t'2014-01-13T07:03:17Z']    TO   ", res)
    
    def test_timestamp_cim_splunk(self):
        res = translate("[file:created = t'2014-01-13T07:03:17Z']", SearchPlatforms.SPLUNK, DataModels.CIM)
        print("CONVERTED: [file:created = t'2014-01-13T07:03:17Z']    TO   ", res)
    