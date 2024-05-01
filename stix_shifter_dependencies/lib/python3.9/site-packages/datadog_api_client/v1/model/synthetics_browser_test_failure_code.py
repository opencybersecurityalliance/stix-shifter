# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsBrowserTestFailureCode(ModelSimple):
    """
    Error code that can be returned by a Synthetic test.

    :param value: Must be one of ["API_REQUEST_FAILURE", "ASSERTION_FAILURE", "DOWNLOAD_FILE_TOO_LARGE", "ELEMENT_NOT_INTERACTABLE", "EMAIL_VARIABLE_NOT_DEFINED", "EVALUATE_JAVASCRIPT", "EVALUATE_JAVASCRIPT_CONTEXT", "EXTRACT_VARIABLE", "FORBIDDEN_URL", "FRAME_DETACHED", "INCONSISTENCIES", "INTERNAL_ERROR", "INVALID_TYPE_TEXT_DELAY", "INVALID_URL", "INVALID_VARIABLE_PATTERN", "INVISIBLE_ELEMENT", "LOCATE_ELEMENT", "NAVIGATE_TO_LINK", "OPEN_URL", "PRESS_KEY", "SERVER_CERTIFICATE", "SELECT_OPTION", "STEP_TIMEOUT", "SUB_TEST_NOT_PASSED", "TEST_TIMEOUT", "TOO_MANY_HTTP_REQUESTS", "UNAVAILABLE_BROWSER", "UNKNOWN", "UNSUPPORTED_AUTH_SCHEMA", "UPLOAD_FILES_ELEMENT_TYPE", "UPLOAD_FILES_DIALOG", "UPLOAD_FILES_DYNAMIC_ELEMENT", "UPLOAD_FILES_NAME"].
    :type value: str
    """

    allowed_values = {
        "API_REQUEST_FAILURE",
        "ASSERTION_FAILURE",
        "DOWNLOAD_FILE_TOO_LARGE",
        "ELEMENT_NOT_INTERACTABLE",
        "EMAIL_VARIABLE_NOT_DEFINED",
        "EVALUATE_JAVASCRIPT",
        "EVALUATE_JAVASCRIPT_CONTEXT",
        "EXTRACT_VARIABLE",
        "FORBIDDEN_URL",
        "FRAME_DETACHED",
        "INCONSISTENCIES",
        "INTERNAL_ERROR",
        "INVALID_TYPE_TEXT_DELAY",
        "INVALID_URL",
        "INVALID_VARIABLE_PATTERN",
        "INVISIBLE_ELEMENT",
        "LOCATE_ELEMENT",
        "NAVIGATE_TO_LINK",
        "OPEN_URL",
        "PRESS_KEY",
        "SERVER_CERTIFICATE",
        "SELECT_OPTION",
        "STEP_TIMEOUT",
        "SUB_TEST_NOT_PASSED",
        "TEST_TIMEOUT",
        "TOO_MANY_HTTP_REQUESTS",
        "UNAVAILABLE_BROWSER",
        "UNKNOWN",
        "UNSUPPORTED_AUTH_SCHEMA",
        "UPLOAD_FILES_ELEMENT_TYPE",
        "UPLOAD_FILES_DIALOG",
        "UPLOAD_FILES_DYNAMIC_ELEMENT",
        "UPLOAD_FILES_NAME",
    }
    API_REQUEST_FAILURE: ClassVar["SyntheticsBrowserTestFailureCode"]
    ASSERTION_FAILURE: ClassVar["SyntheticsBrowserTestFailureCode"]
    DOWNLOAD_FILE_TOO_LARGE: ClassVar["SyntheticsBrowserTestFailureCode"]
    ELEMENT_NOT_INTERACTABLE: ClassVar["SyntheticsBrowserTestFailureCode"]
    EMAIL_VARIABLE_NOT_DEFINED: ClassVar["SyntheticsBrowserTestFailureCode"]
    EVALUATE_JAVASCRIPT: ClassVar["SyntheticsBrowserTestFailureCode"]
    EVALUATE_JAVASCRIPT_CONTEXT: ClassVar["SyntheticsBrowserTestFailureCode"]
    EXTRACT_VARIABLE: ClassVar["SyntheticsBrowserTestFailureCode"]
    FORBIDDEN_URL: ClassVar["SyntheticsBrowserTestFailureCode"]
    FRAME_DETACHED: ClassVar["SyntheticsBrowserTestFailureCode"]
    INCONSISTENCIES: ClassVar["SyntheticsBrowserTestFailureCode"]
    INTERNAL_ERROR: ClassVar["SyntheticsBrowserTestFailureCode"]
    INVALID_TYPE_TEXT_DELAY: ClassVar["SyntheticsBrowserTestFailureCode"]
    INVALID_URL: ClassVar["SyntheticsBrowserTestFailureCode"]
    INVALID_VARIABLE_PATTERN: ClassVar["SyntheticsBrowserTestFailureCode"]
    INVISIBLE_ELEMENT: ClassVar["SyntheticsBrowserTestFailureCode"]
    LOCATE_ELEMENT: ClassVar["SyntheticsBrowserTestFailureCode"]
    NAVIGATE_TO_LINK: ClassVar["SyntheticsBrowserTestFailureCode"]
    OPEN_URL: ClassVar["SyntheticsBrowserTestFailureCode"]
    PRESS_KEY: ClassVar["SyntheticsBrowserTestFailureCode"]
    SERVER_CERTIFICATE: ClassVar["SyntheticsBrowserTestFailureCode"]
    SELECT_OPTION: ClassVar["SyntheticsBrowserTestFailureCode"]
    STEP_TIMEOUT: ClassVar["SyntheticsBrowserTestFailureCode"]
    SUB_TEST_NOT_PASSED: ClassVar["SyntheticsBrowserTestFailureCode"]
    TEST_TIMEOUT: ClassVar["SyntheticsBrowserTestFailureCode"]
    TOO_MANY_HTTP_REQUESTS: ClassVar["SyntheticsBrowserTestFailureCode"]
    UNAVAILABLE_BROWSER: ClassVar["SyntheticsBrowserTestFailureCode"]
    UNKNOWN: ClassVar["SyntheticsBrowserTestFailureCode"]
    UNSUPPORTED_AUTH_SCHEMA: ClassVar["SyntheticsBrowserTestFailureCode"]
    UPLOAD_FILES_ELEMENT_TYPE: ClassVar["SyntheticsBrowserTestFailureCode"]
    UPLOAD_FILES_DIALOG: ClassVar["SyntheticsBrowserTestFailureCode"]
    UPLOAD_FILES_DYNAMIC_ELEMENT: ClassVar["SyntheticsBrowserTestFailureCode"]
    UPLOAD_FILES_NAME: ClassVar["SyntheticsBrowserTestFailureCode"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsBrowserTestFailureCode.API_REQUEST_FAILURE = SyntheticsBrowserTestFailureCode("API_REQUEST_FAILURE")
SyntheticsBrowserTestFailureCode.ASSERTION_FAILURE = SyntheticsBrowserTestFailureCode("ASSERTION_FAILURE")
SyntheticsBrowserTestFailureCode.DOWNLOAD_FILE_TOO_LARGE = SyntheticsBrowserTestFailureCode("DOWNLOAD_FILE_TOO_LARGE")
SyntheticsBrowserTestFailureCode.ELEMENT_NOT_INTERACTABLE = SyntheticsBrowserTestFailureCode("ELEMENT_NOT_INTERACTABLE")
SyntheticsBrowserTestFailureCode.EMAIL_VARIABLE_NOT_DEFINED = SyntheticsBrowserTestFailureCode(
    "EMAIL_VARIABLE_NOT_DEFINED"
)
SyntheticsBrowserTestFailureCode.EVALUATE_JAVASCRIPT = SyntheticsBrowserTestFailureCode("EVALUATE_JAVASCRIPT")
SyntheticsBrowserTestFailureCode.EVALUATE_JAVASCRIPT_CONTEXT = SyntheticsBrowserTestFailureCode(
    "EVALUATE_JAVASCRIPT_CONTEXT"
)
SyntheticsBrowserTestFailureCode.EXTRACT_VARIABLE = SyntheticsBrowserTestFailureCode("EXTRACT_VARIABLE")
SyntheticsBrowserTestFailureCode.FORBIDDEN_URL = SyntheticsBrowserTestFailureCode("FORBIDDEN_URL")
SyntheticsBrowserTestFailureCode.FRAME_DETACHED = SyntheticsBrowserTestFailureCode("FRAME_DETACHED")
SyntheticsBrowserTestFailureCode.INCONSISTENCIES = SyntheticsBrowserTestFailureCode("INCONSISTENCIES")
SyntheticsBrowserTestFailureCode.INTERNAL_ERROR = SyntheticsBrowserTestFailureCode("INTERNAL_ERROR")
SyntheticsBrowserTestFailureCode.INVALID_TYPE_TEXT_DELAY = SyntheticsBrowserTestFailureCode("INVALID_TYPE_TEXT_DELAY")
SyntheticsBrowserTestFailureCode.INVALID_URL = SyntheticsBrowserTestFailureCode("INVALID_URL")
SyntheticsBrowserTestFailureCode.INVALID_VARIABLE_PATTERN = SyntheticsBrowserTestFailureCode("INVALID_VARIABLE_PATTERN")
SyntheticsBrowserTestFailureCode.INVISIBLE_ELEMENT = SyntheticsBrowserTestFailureCode("INVISIBLE_ELEMENT")
SyntheticsBrowserTestFailureCode.LOCATE_ELEMENT = SyntheticsBrowserTestFailureCode("LOCATE_ELEMENT")
SyntheticsBrowserTestFailureCode.NAVIGATE_TO_LINK = SyntheticsBrowserTestFailureCode("NAVIGATE_TO_LINK")
SyntheticsBrowserTestFailureCode.OPEN_URL = SyntheticsBrowserTestFailureCode("OPEN_URL")
SyntheticsBrowserTestFailureCode.PRESS_KEY = SyntheticsBrowserTestFailureCode("PRESS_KEY")
SyntheticsBrowserTestFailureCode.SERVER_CERTIFICATE = SyntheticsBrowserTestFailureCode("SERVER_CERTIFICATE")
SyntheticsBrowserTestFailureCode.SELECT_OPTION = SyntheticsBrowserTestFailureCode("SELECT_OPTION")
SyntheticsBrowserTestFailureCode.STEP_TIMEOUT = SyntheticsBrowserTestFailureCode("STEP_TIMEOUT")
SyntheticsBrowserTestFailureCode.SUB_TEST_NOT_PASSED = SyntheticsBrowserTestFailureCode("SUB_TEST_NOT_PASSED")
SyntheticsBrowserTestFailureCode.TEST_TIMEOUT = SyntheticsBrowserTestFailureCode("TEST_TIMEOUT")
SyntheticsBrowserTestFailureCode.TOO_MANY_HTTP_REQUESTS = SyntheticsBrowserTestFailureCode("TOO_MANY_HTTP_REQUESTS")
SyntheticsBrowserTestFailureCode.UNAVAILABLE_BROWSER = SyntheticsBrowserTestFailureCode("UNAVAILABLE_BROWSER")
SyntheticsBrowserTestFailureCode.UNKNOWN = SyntheticsBrowserTestFailureCode("UNKNOWN")
SyntheticsBrowserTestFailureCode.UNSUPPORTED_AUTH_SCHEMA = SyntheticsBrowserTestFailureCode("UNSUPPORTED_AUTH_SCHEMA")
SyntheticsBrowserTestFailureCode.UPLOAD_FILES_ELEMENT_TYPE = SyntheticsBrowserTestFailureCode(
    "UPLOAD_FILES_ELEMENT_TYPE"
)
SyntheticsBrowserTestFailureCode.UPLOAD_FILES_DIALOG = SyntheticsBrowserTestFailureCode("UPLOAD_FILES_DIALOG")
SyntheticsBrowserTestFailureCode.UPLOAD_FILES_DYNAMIC_ELEMENT = SyntheticsBrowserTestFailureCode(
    "UPLOAD_FILES_DYNAMIC_ELEMENT"
)
SyntheticsBrowserTestFailureCode.UPLOAD_FILES_NAME = SyntheticsBrowserTestFailureCode("UPLOAD_FILES_NAME")
