#!/usr/bin/python

from defusedxml.ElementTree import fromstring

from onelogin.api.models.mfa import MFA
from onelogin.api.models.saml_endpoint_response import SAMLEndpointResponse
from onelogin.api.models.session_token_info import SessionTokenInfo
from onelogin.api.models.session_token_mfa_info import SessionTokenMFAInfo


def get_resource_list(resource_cls, json_data, index, version_id):
    resources = []
    data = None
    if json_data:
        if version_id == 1 and isinstance(json_data, dict) and json_data.get('data', None):
            if index is not None:
                data = json_data['data'][index]
            else:
                data = json_data['data']
        elif version_id == 2:
            data = json_data

    if data:
        for data_item in data:
            if isinstance(data_item, dict):
                resources.append(resource_cls(data_item))

    return resources


def get_resource_or_id(resource_cls, json_data, version_id):
    data = resource = None

    if json_data:
        if version_id == 1 and isinstance(json_data, dict) and json_data.get('data', None):
            if isinstance(json_data['data'], list):
                data = json_data['data'][0]
            else:
                data = json_data['data']
        elif version_id == 2:
            if isinstance(json_data, list):
                data = json_data[0]
            else:
                data = json_data

        if data:
            if isinstance(data, dict):
                if list(data.keys()) == ["id"]:
                    resource = data["id"]
                else:
                    resource = resource_cls(data)
            else:
                resource = data
    return resource


def get_ids(json_data):
    ids = []
    if json_data:
        for data in json_data:
            if type(data) is dict and "id" in data.keys():
                ids.append(data["id"])
            else:
                ids.append(data)
    return ids


def extract_error_message_from_response(response):
    message = ''
    content = response.json()
    if content:
        if 'status' in content:
            status = content['status']
            if isinstance(status, dict):
                if 'message' in status:
                    if isinstance(status['message'], dict):
                        if 'description' in status['message']:
                            message = status['message']['description']
                    else:
                        message = status['message']
                elif 'type' in status:
                    message = status['type']
            elif 'description' in content:
                message = content['description']
        elif 'message' in content:
            message = content['message']
        elif 'messages' in content:
            message = " | ".join(content['messages'])
        elif 'name' in content:
            message = content['name']
    return message


def extract_error_attribute_from_response(response):
    attribute = None
    content = response.json()
    if content:
        if 'status' in content:
            status = content['status']
            if isinstance(status, dict) and 'message' in status:
                if isinstance(status['message'], dict):
                    if 'attribute' in status['message']:
                        attribute = status['message']['attribute']
        elif "message" in content and "unknown attribute" in content["message"]:
            attribute = content["message"].replace("unknown attribute: ", "")
        elif "message" in content and "errors" in content:
            errors = []
            for error in content["errors"]:
                if "field" in error and "message" in error:
                    field = error["field"]
                    error_detail = ". ".join(error["message"])
                    errors.append("Field: %s - %s" % (field, error_detail))
            attribute = ". ".join(errors)
        elif "message" in content and "field" in content:
            attribute = content["field"]
    return attribute


def get_after_cursor(response, version_id):
    after_cursor = None
    if version_id == 1:
        content = response.json()
        if content:
            if 'pagination' in content and 'after_cursor' in content['pagination']:
                after_cursor = content['pagination']['after_cursor']
            elif 'afterCursor' in content:
                after_cursor = content['afterCursor']
    else:
        headers = response.headers
        if headers and 'after-cursor' in headers:
            after_cursor = headers['after-cursor']
    return after_cursor


def get_before_cursor(response, version_id):
    before_cursor = None
    if version_id == 1:
        content = response.json()
        if content:
            if 'pagination' in content and 'before_cursor' in content['pagination']:
                before_cursor = content['pagination']['before_cursor']
            elif 'beforeCursor' in content:
                before_cursor = content['beforeCursor']
    else:
        headers = response.headers
        if headers and 'before-cursor' in headers:
            before_cursor = headers['before-cursor']
    return before_cursor


def extract_status_code_from_response(response):
    status_code = ''
    content = response.json()
    if content and 'statusCode' in content:
        status_code = content['statusCode']

    return status_code


def handle_operation_response(response):
    result = False
    try:
        content = response.json()
        if content and isinstance(content, dict):
            if 'status' in content and 'type' in content['status'] and content['status']['type'] == "success":
                result = True
            elif 'success' in content and content['success']:
                result = True
            elif 'name' in content and content['name'] == 'Success':
                result = True
    except Exception:
        pass
    return result


def handle_session_token_response(response):
    session_token = None
    content = response.json()
    if content and 'status' in content and 'message' in content['status'] and 'data' in content:
        if content['status']['message'] == "Success":
            session_token = SessionTokenInfo(content['data'][0])
        elif content['status']['message'] == "MFA is required for this user":
            session_token = SessionTokenMFAInfo(content['data'][0])
        else:
            raise Exception("Status Message type not recognized: %s" % content['status']['message'])
    return session_token


def handle_saml_endpoint_response(response, version_id):
    saml_endpoint_response = None
    try:
        content = response.json()
        if version_id == 1:
            if content and 'status' in content and 'message' in content['status'] and 'type' in content['status']:
                status_type = content['status']['type']
                status_message = content['status']['message']
                saml_endpoint_response = SAMLEndpointResponse(status_type, status_message)
                if 'data' in content:
                    if status_message == 'Success':
                        saml_endpoint_response.saml_response = str(content['data'])
                    else:
                        mfa = MFA(content['data'][0])
                        saml_endpoint_response.mfa = mfa
        elif version_id == 2:
            if 'message' in content:
                status_type = None
                if content['message'] == "Success" or "MFA is required" in content['message']:
                    status_type = "success"
                elif "pending" in content['message']:
                    status_type = "pending"
                status_message = content['message']
                saml_endpoint_response = SAMLEndpointResponse(status_type, status_message)
                if 'data' in content:
                    saml_endpoint_response.saml_response = str(content['data'])
                elif "state_token" in content:
                    mfa = MFA(content)
                    saml_endpoint_response.mfa = mfa
    except Exception:
        pass
    return saml_endpoint_response


def op_create_success(status_code):
    if status_code in [200, 201]:
        return True
    return False


def op_delete_success(status_code):
    if status_code in [200, 202, 204]:
        return True
    return False


def retrieve_apps_from_xml(cls_class, xml_content):
    root = fromstring(xml_content)
    node_list = root.findall("./app")
    attributes = {"id", "icon", "name", "provisioned", "extension_required", "personal", "login_id"}
    apps = []
    for node in node_list:
        app_data = {
            child.tag: child.text
            for child in node
            if child.tag in attributes
        }
        apps.append(cls_class(app_data))
    return apps
