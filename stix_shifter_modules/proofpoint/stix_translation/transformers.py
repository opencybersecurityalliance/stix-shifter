from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

class proofpoint_bodymultipart_transformer(ValueTransformer):
    @staticmethod
    def transform(multipart):
        for part in multipart:
            part['content_type']=part.pop('contentType')
            part['content_disposition'] = part.pop('disposition')
            if part['content_type'] == 'text/plain':
                part['body'] = part['filename'][:-4]
            if 'filename' in part:
                del part['filename']
                if 'md5' in part: del part['md5']
                if 'sha256' in part: del part['sha256']

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