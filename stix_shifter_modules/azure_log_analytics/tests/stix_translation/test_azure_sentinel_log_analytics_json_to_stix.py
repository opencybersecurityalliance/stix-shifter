import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.azure_log_analytics.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "azure_sentinel"
options = {"api": "Log Analytics"}
entry_point = EntryPoint(options=options)
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "azure_sentinel",
    "identity_class": "events"
}

DATA1 = {
    'TenantId': 'e00daaf8-d6a4-4410-b50b-f5ef61c9cb45',
    'WorkspaceSubscriptionId': 'dc26ff57-0597-4cc8-8092-aa5b929f8f39', 'category': 'SuspiciousSVCHOSTRareGroup',
    'TimeGenerated': '2022-05-24T11:22:29.003Z',
    'ProductName': 'Azure Sentinel', "EventID": "4625",
    'EventTime': '2022-05-24T14:27:36.370Z', 'AlertName': 'AlertLog',
    'AlertSeverity': 'Medium', 'Status': 'New', 'ProviderName': 'ASI Scheduled Alerts'}

DATA2 = {
    "TenantId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45",
    "TimeGenerated": "2022-05-25 12:04:38.070000+00:00",
    "SourceSystem": "OpsManager",
    "Account": "",
    "AccountType": "",
    "Computer": "GslabCP4S",
    "EventSourceName": "Microsoft-Windows-Security-Auditing",
    "Channel": "Security",
    "Task": "1",
    "Level": "0",
    "EventID": "5379",
    "Activity": "5379",
    "PartitionKey": "",
    "LogonProcessName": "Advapi  ",
    "ProcessId": "0x2c0",
    "IpAddress": "80.66.76.145",
    "TargetUserName": "GS-2530"
}

DATA3 = {
    "TenantId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45",
    "TimeGenerated": "2022-05-07 12:27:10.171000+00:00",
    "IncidentName": "919158c6-4c3f-4273-a730-a37f75622350",
    "Title": "AlertLog",
    "Description": "",
    "Severity": "Medium",
    "Status": "New",
    "Classification": "",
    "ClassificationComment": "",
    "ClassificationReason": "",
    "Owner": "{\"objectId\":null,\"email\":null,\"assignedTo\":null,\"userPrincipalName\":null}",
    "ProviderName": "Azure Sentinel",
    "ProviderIncidentId": "1186",
    "FirstActivityTime": "2022-05-07 11:46:36.502000+00:00",
    "LastActivityTime": "2022-05-07 11:46:36.502000+00:00",
    "FirstModifiedTime": "None",
    "LastModifiedTime": "2022-05-07 12:27:10.171000+00:00",
    "CreatedTime": "2022-05-07 12:27:10.171000+00:00",
    "ClosedTime": "None",
    "IncidentNumber": "1186",
    "IncidentUrl": "https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350",
    "RelatedAnalyticRuleIds": "[\"9c4be437-b74c-440c-aa09-764367744a23\"]",
    "AlertIds": "[\"17bbb3bd-00fb-73f0-573b-f2039bd3b5c5\"]",
    "BookmarkIds": "[]",
    "Comments": "[]",
    "Labels": "[]",
    "ModifiedBy": "Incident created from alert",
    "SourceSystem": "Azure",
    "Type": "SecurityIncident"
}


class TestAzureSentinelResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for azure_sentinel translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestAzureSentinelResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        assert result_bundle_identity['id'] == data_source['id']
        assert result_bundle_identity['name'] == data_source['name']
        assert result_bundle_identity['identity_class'] == data_source['identity_class']

        observed_data = result_bundle_objects[1]
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    @staticmethod
    def test_x_oca_x_ibm_property():
        """
        to test the oca-ibm stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        # x_ibm_finding = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        x_oca_event = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        # assert x_ibm_finding['name'] == 'AlertLog'
        assert x_oca_event['provider'] == 'ASI Scheduled Alerts'
        assert x_oca_event['code'] == '4625'

    @staticmethod
    def test_x_alert_property():
        """
        to test the alert stix object properties
        """
        data = {
            "TenantId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45",
            "TimeGenerated": "2022-05-04 16:47:08.560000+00:00",
            "DisplayName": "AlertLog",
            "AlertName": "AlertLog",
            "AlertSeverity": "Medium",
            'EventTime': '2022-05-24T14:27:36.370Z',
            "Description": "",
            "ProviderName": "ASI Scheduled Alerts",
            "VendorName": "Microsoft",
            "VendorOriginalId": "f1303f5e-daae-407e-ab87-e1d8ec3651da",
            "SystemAlertId": "50396c5f-2cb6-9d2f-e601-9f430bf17869",
            "ResourceId": "",
            "SourceComputerId": "",
            "AlertType": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45_9c4be437-b74c-440c-aa09-764367744a23",
            "ConfidenceLevel": "",
            "ConfidenceScore": "None",
            "IsIncident": "False",
            "StartTime": "2022-05-04 16:08:32.180000+00:00",
            "EndTime": "2022-05-04 16:08:32.180000+00:00",
            "ProcessingEndTime": "2022-05-04 16:47:08.560000+00:00",
            "RemediationSteps": "",
            "Entities": "",
            "SourceSystem": "Detection",
            "WorkspaceSubscriptionId": "dc26ff57-0597-4cc8-8092-aa5b929f8f39",
            "WorkspaceResourceGroup": "newresource",
            "ExtendedLinks": "",
            "ProductName": "Azure Sentinel",
            "ProductComponentName": "Scheduled Alerts",
            "AlertLink": "",
            "Status": "New",
            "CompromisedEntity": "",
            "Tactics": "ResourceDevelopment",
            "Techniques": "",
            "Type": "SecurityAlert"
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        x_msazure_sentinel_alert = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(),
                                                                                    'x-msazure-sentinel-alert')

        assert x_msazure_sentinel_alert is not None, 'Custom object type not found'
        assert x_msazure_sentinel_alert['status'] == 'New'

    @staticmethod
    def test_x_incident_property():
        """
        to test incident stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA3], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        x_msazure_sentinel_incident = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(),
                                                                                       'x-msazure-sentinel-incident')
        assert x_msazure_sentinel_incident is not None, 'Custom object type not found'
        assert x_msazure_sentinel_incident['incident_name'] == '919158c6-4c3f-4273-a730-a37f75622350'
        assert x_msazure_sentinel_incident['severity'] == 'Medium'

    @staticmethod
    def test_x_event_property():
        """
        to test event stix object properties
        """

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        x_msazure_sentinel_event = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(),
                                                                                    'x-msazure-sentinel-event')
        assert x_msazure_sentinel_event is not None, 'Custom object type not found'
        assert x_msazure_sentinel_event['computer'] == 'GslabCP4S'
        assert x_msazure_sentinel_event['source'] == 'OpsManager'

    @staticmethod
    def test_process_json_to_stix():
        """
        to test process stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'process')

        assert process_obj is not None, 'process object type not found'
        assert process_obj['name'] == 'Advapi  '
        assert process_obj['pid'] == '0x2c0'

    @staticmethod
    def test_ipv4_addr_json_to_stix():
        """
        to test ipv4 stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        ip_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')

        assert ip_obj is not None, 'ip object type not found'
        assert ip_obj['value'] == '80.66.76.145'

    @staticmethod
    def test_url_json_to_stix():
        """
        to test url stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA3], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        url_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'url')

        assert url_obj is not None, 'url object type not found'
        assert url_obj['name'] == 'https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/dc26ff57-0597-4cc8-8092-aa5b929f8f39/resourceGroups/newresource/providers/Microsoft.OperationalInsights/workspaces/loganaly/providers/Microsoft.SecurityInsights/Incidents/919158c6-4c3f-4273-a730-a37f75622350'

    @staticmethod
    def test_user_account_json_to_stix():
        """
        to test url stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']

        user_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'user-account')

        assert user_obj is not None, 'user object type not found'
        assert user_obj['account_login'] == 'GS-2530'

    @staticmethod
    def test_unmapped_attribute_with_mapped_attribute():
        message = "\"GET /blog HTTP/1.1\" 200 2571"
        data = {"message": message, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
        curr_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'message')
        assert (curr_obj is None), 'url object type not found'

    @staticmethod
    def test_unmapped_attribute_alone():
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
