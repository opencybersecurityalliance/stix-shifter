from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = 'mysql'
TRANSFORMERS = get_module_transformers(MODULE)
epoch_to_timestamp_class = TRANSFORMERS.get('EpochToTimestamp')
timestamp_to_epoch_class = TRANSFORMERS.get('TimestampToMilliseconds')
EPOCH = 1634657528000
TIMESTAMP = "2021-10-19T15:32:08.000Z"

class TestTransform(object):

    def test_epoch_to_timestamp_conversion(self):
        conversion = epoch_to_timestamp_class.transform(EPOCH)
        assert conversion == TIMESTAMP

    def test_timestamp_to_epoch_conversion(self):
        conversion = timestamp_to_epoch_class.transform(TIMESTAMP)
        assert conversion == EPOCH

