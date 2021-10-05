from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

class prrofpoint_bodymultipart_transformer(ValueTransformer):
    @staticmethod
    def transform(multipart):

        # print("transformer multipart :", multipart)
        for part in multipart:
            part['content_type']=part.pop('contentType')
            part['content_disposition'] = part.pop('disposition')

        return multipart