from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
import json
from urllib.parse import quote_plus
import vt
import time
import sys
from datetime import datetime

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        auth_values = configuration.get('auth')
        virustotal_key = auth_values['key']
        # remove protocol from hostname and retriving hostname from connection not giving statically 
        self.client = vt.Client(virustotal_key)
        self.connection = connection
        self.virustotal_key = virustotal_key
        self.namespace = connection.get('namespace')

    async def ping_virus_total(self):
        # implement this
        ping_endpoint = '/users/%s' % self.virustotal_key
        try:
            ping_return = await self.client.get_json_async(ping_endpoint, 'GET')
        finally:
            await self.client.close_async()
        return ping_return

    async def get_search_results(self, query_expression, range_start=None, range_end=None):
        # Queries the data source
        # extract the data        
        data_type = query_expression['dataType']
        data = query_expression['data']
        query_data = dict()    
        query_data["code"] = 200
        enrichment_info = None

        if (data_type == "domain" or data_type == "fqdn"):
            try:
                enrichment_info = await self.client.get_json_async("/domains/{}", data)
                detected_urls = {}
                detected_urls['scan_date'] = str(datetime.fromtimestamp(enrichment_info['data']['attributes']['last_modification_date']))
                detected_urls['positives'] = enrichment_info['data']['attributes']['last_analysis_stats']['malicious'] + enrichment_info['data']['attributes']['last_analysis_stats']['suspicious']
                detected_urls['total'] = detected_urls['positives'] + enrichment_info['data']['attributes']['last_analysis_stats']['harmless'] + enrichment_info['data']['attributes']['last_analysis_stats']['undetected']
                enrichment_info['data']['info'] = {}
                enrichment_info['data']['info']['detected_urls'] = detected_urls
                enrichment_info['data']['info']['permalink'] = f"https://www.virustotal.com/gui/domain/{enrichment_info['data']['id']}"
            except Exception as e:
                if e.code == 'NotFoundError': query_data["code"] = 200
                else: 
                    query_data["code"] = 400
                    return {'code': 400, 'error': e}, self.namespace
            await self.client.close_async()
        elif data_type == "ip":
            try:
                enrichment_info = await self.client.get_json_async("/ip_addresses/{}", data)
                detected_urls = {}
                detected_urls['scan_date'] = str(datetime.fromtimestamp(enrichment_info['data']['attributes']['last_modification_date'])) if enrichment_info.get('data').get('attributes').get('last_modification_date') else None
                detected_urls['positives'] = enrichment_info['data']['attributes']['last_analysis_stats']['malicious'] + enrichment_info['data']['attributes']['last_analysis_stats']['suspicious']
                detected_urls['total'] = detected_urls['positives'] + enrichment_info['data']['attributes']['last_analysis_stats']['harmless'] + enrichment_info['data']['attributes']['last_analysis_stats']['undetected']
                enrichment_info['data']['info'] = {}
                print(('abc'))
                enrichment_info['data']['info']['detected_urls'] = detected_urls
                enrichment_info['data']['info']['permalink'] = f"https://www.virustotal.com/gui/ip-address/{enrichment_info['data']['id']}"
            except Exception as e:
                if e.code == 'NotFoundError': query_data["code"] = 200
                else: 
                    query_data["code"] = 400
                    return {'code': 400, 'error': e}, self.namespace
            await self.client.close_async()
        elif data_type == "url":
            try:
                url_id = vt.url_id(data)
                enrichment_info = await self.client.get_json_async("/urls/{}", url_id)
                info = {}
                info['positives'] = enrichment_info['data']['attributes']['last_analysis_stats']['malicious'] + enrichment_info['data']['attributes']['last_analysis_stats']['suspicious']
                info['resource'] = enrichment_info['data']['attributes']['url']
                info['scan_id'] = f"{enrichment_info['data']['id']}"
                info['scan_date'] = str(datetime.fromtimestamp(enrichment_info['data']['attributes']['last_analysis_date']))
                info['total'] = info['positives'] + enrichment_info['data']['attributes']['last_analysis_stats']['harmless'] + enrichment_info['data']['attributes']['last_analysis_stats']['undetected']
                info['permalink'] = f"https://www.virustotal.com/gui/url/{info['scan_id']}"
                enrichment_info['data']['info'] = info
            except:
                try:
                    analysis = await self.client.scan_url_async(data)
                    while True:
                        analysis = await self.client.get_object_async("/analyses/{}", analysis.id)
                        if analysis.status == "completed":
                            url_id = vt.url_id(data)
                            enrichment_info = await self.client.get_json_async("/urls/{}", url_id)
                            break
                        time.sleep(10)
                except Exception as e:
                    if e.code == 'NotFoundError': query_data["code"] = 200
                    else: 
                        query_data["code"] = 400
                        return {'code': 400, 'error': e}, self.namespace
            await self.client.close_async()
        elif data_type == "hash":
            try:
                enrichment_info = await self.client.get_json_async("/files/{}", data)
                info = {}
                info['positives'] = enrichment_info['data']['attributes']['last_analysis_stats']['malicious'] + enrichment_info['data']['attributes']['last_analysis_stats']['suspicious']
                info['resource'] = enrichment_info['data']['attributes']['md5']
                info['scan_id'] = f"{enrichment_info['data']['attributes']['sha256']}-{enrichment_info['data']['attributes']['last_analysis_date']}"
                info['sha256'] = enrichment_info['data']['attributes']['sha256']
                info['sha1'] = enrichment_info['data']['attributes']['sha1']
                info['md5'] = enrichment_info['data']['attributes']['md5']
                info['scan_date'] = str(datetime.fromtimestamp(enrichment_info['data']['attributes']['last_analysis_date']))
                info['total'] = info['positives'] + enrichment_info['data']['attributes']['last_analysis_stats']['harmless'] + enrichment_info['data']['attributes']['last_analysis_stats']['undetected']
                info['permalink'] = f"https://www.virustotal.com/gui/file/{info['sha256']}"
                enrichment_info['data']['info'] = info
            except Exception as e:
                if e.code == 'NotFoundError': query_data["code"] = 200
                else: 
                    query_data["code"] = 400
                    return {'code': 400, 'error': e}, self.namespace
            await self.client.close_async()

        query_data["data"] = dict()
        query_data["data"]["success"] = True
        if enrichment_info is None: 
            query_data["data"]["full"] = {
                "message": "IOC Not Found."
            }
        else:
            query_data["data"]["full"] = enrichment_info
        return query_data, self.namespace


    async def delete_search(self, search_id):
        # Delete the search - Optional since this may not be supported by the data source API
        return {"code": 200, "success": True} 