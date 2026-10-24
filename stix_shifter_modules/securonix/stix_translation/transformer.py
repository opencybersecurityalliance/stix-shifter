from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
from datetime import datetime, timezone
import json
import re
from typing import Any, Optional, Union


class SecuronixToStixTransformer(ValueTransformer):
    def __init__(self):
        self.logger = logger.set_logger(__name__)

    def transform(self, data: Any) -> Optional[Any]:
        """Transform Securonix data to STIX format"""
        if data is None:
            return None

        if isinstance(data, (int, float, bool)):
            return data

        if isinstance(data, str):
            return self.transform_string(data)

        if isinstance(data, dict):
            return self.transform_dict(data)

        if isinstance(data, list):
            return self.transform_list(data)

        return str(data)

    def transform_string(self, data: str) -> str:
        """Transform string values with special handling"""
        # Handle IP addresses
        if self._is_ip_address(data):
            return self.transform_ip(data)

        return data

    def transform_dict(self, data: dict) -> dict:
        """Transform dictionary values"""
        transformed_data = {k: self.transform(v) for k, v in data.items()}
        logger.debug(f"Transformed data: {transformed_data}")



        # Handle new mappings
        if 'client_ip_class' in transformed_data:
            transformed_data['client_ip_class'] = self.transform_ip(transformed_data['client_ip_class'])
        if 'client_referrer_host' in transformed_data:
            transformed_data['client_referrer_host'] = self.transform_ip(transformed_data['client_referrer_host'])
        if 'request_method' in transformed_data:
            transformed_data['request_method'] = self.transform_string(transformed_data['request_method'])
        if 'client_request_http_host' in transformed_data:
            transformed_data['client_request_http_host'] = self.transform_string(
                transformed_data['client_request_http_host'])
        if 'client_request_path' in transformed_data:
            transformed_data['client_request_path'] = self.transform_string(transformed_data['client_request_path'])
        if 'client_request_query' in transformed_data:
            transformed_data['client_request_query'] = self.transform_string(transformed_data['client_request_query'])
        if 'client_referrer_query' in transformed_data:
            transformed_data['client_referrer_query'] = self.transform_string(transformed_data['client_referrer_query'])
        if 'client_country_name' in transformed_data:
            transformed_data['client_country_name'] = self.transform_string(transformed_data['client_country_name'])
        if 'client_request_http_method_name' in transformed_data:
            transformed_data['client_request_http_method_name'] = self.transform_string(
                transformed_data['client_request_http_method_name'])
        if 'email_subject' in transformed_data:
            transformed_data['email_subject'] = self.transform_string(transformed_data['email_subject'])
        if 'emailsenderdomain' in transformed_data:
            transformed_data['emailsenderdomain'] = self.transform_string(transformed_data['emailsenderdomain'])
        if 'request_url' in transformed_data:
            transformed_data['request_url'] = self.transform_string(transformed_data['request_url'])

        return transformed_data

    def transform_list(self, data: list) -> list:
        """Transform list values"""
        return [self.transform(item) for item in data]

    @staticmethod
    def transform_ip(ip: str) -> str:
        """Normalize IP address format"""
        return ip.strip()

    @staticmethod
    def _is_ip_address(value: str) -> bool:
        """Check if string is an IP address"""
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ip_pattern, value.strip()))
