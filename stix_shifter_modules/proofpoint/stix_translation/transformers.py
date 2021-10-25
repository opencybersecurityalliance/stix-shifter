from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

class proofpoint_bodymultipart_transformer(ValueTransformer):
    @staticmethod
    def transform(multipart):

        # print("transformer multipart :", multipart)
        for part in multipart:
            part['content_type']=part.pop('contentType')
            # part['content_disposition'] = part.pop('disposition')

        return multipart

class proofpoint_emailid_transformer(ValueTransformer):
    @staticmethod
    def transform(emailid):
        if isinstance(emailid, list): emailid = emailid[0]
        if "<" in emailid and ">" in emailid:
            startindex = emailid.index('<') + 1
            endindex = emailid.index('>')
            emailid = emailid[startindex: endindex]

        return emailid