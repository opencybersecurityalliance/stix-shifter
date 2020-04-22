import json
import os
import requests
import shutil
import subprocess
import time
import urllib3
from stix_shifter_utils.stix_translation.src.patterns.translator import DataModels

urllib3.disable_warnings()

# Seconds to wait before checking if a search platform indexed or deleted data.
SLEEP_INTERVAL = 0.1

docker_daemon_ip = "localhost"


try:
    if os.getenv("DOCKER_HOST", False):
        docker_daemon_ip = os.getenv("DOCKER_HOST")
    elif shutil.which("docker-machine"):
        tempAddr = subprocess.check_output(["docker-machine", "ip", "default"], stderr=subprocess.STDOUT).decode("utf-8", "strict")
        docker_daemon_ip = tempAddr.strip()
    else:
        docker_daemon_ip = '127.0.0.1'
except (subprocess.CalledProcessError, FileNotFoundError) as e:
    print("Error at docker-machine id is ", e)


print("the value of docker_daemon_ip is: ", docker_daemon_ip)


class SplunkConnector():

    SPLUNK_CONFIG = {
      'hostname': docker_daemon_ip,  # docker_daemon_ip is a variable for IP address
      'port': '8989',
      'user': 'admin',
      'pass': 'translator_test'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.verify = False
        self.auth = (self.SPLUNK_CONFIG['user'], self.SPLUNK_CONFIG['pass'])
        self.prep()

    def url(self, val):
        return "https://{}:{}/services/{}".format(self.SPLUNK_CONFIG['hostname'], self.SPLUNK_CONFIG['port'], val)

    def prep(self):
        for m in DataModels:
            # Delete the indexes
            dr = self.session.delete(self.url("data/indexes/{}".format(m.value.lower())), auth=(self.SPLUNK_CONFIG['user'], self.SPLUNK_CONFIG['pass']))
            # After deletion is complete, 404 will be returned.
            while self.session.get(self.url("data/indexes/{}".format(m.value.lower())),
                                   params={'summarize': True}, auth=(self.SPLUNK_CONFIG['user'],
                                                                     self.SPLUNK_CONFIG['pass'])).status_code != 404:
                time.sleep(SLEEP_INTERVAL)

            # Then create them. Raise an error if unable to create
            resp = self.session.post(self.url('data/indexes'), data={'name':m.value.lower()}, auth=(self.SPLUNK_CONFIG['user'], self.SPLUNK_CONFIG['pass']))
            # After index (re)creation is complete, 200 will be returned.
            while self.session.get(self.url("data/indexes/{}".format(m.value.lower())),
                                   params={'summarize': True}, auth=(self.SPLUNK_CONFIG['user'],
                                                                     self.SPLUNK_CONFIG['pass'])).status_code != 200:
                time.sleep(SLEEP_INTERVAL)


    def push(self, data_model, log_entries):
        if data_model == DataModels.CAR:
            car_events = ([self.car_to_splunk(e) for e in log_entries])

            for e in car_events:
                request = self.session.post(self.url('receivers/simple?sourcetype=json&source=converter&index=car'), data=json.dumps(e), auth=(self.SPLUNK_CONFIG['user'], self.SPLUNK_CONFIG['pass']))

            # Wait until all entries have been processed
            inserted_guids = {e.get('guid') for e in log_entries}
            queried_guids = set()
            while not inserted_guids.issubset(queried_guids):  # we should be able to find every inserted guid
                for guid in inserted_guids:
                    for found_guid in self.query('|where match(guid, "{}")'.format(guid), data_model, verbose=False):
                        queried_guids.add(found_guid)
                time.sleep(SLEEP_INTERVAL)
        elif data_model == DataModels.CIM:
            for e in log_entries:
                request = self.session.post(self.url('receivers/simple?sourcetype=json&source=converter&index=cim'), data=json.dumps(e), auth=(self.SPLUNK_CONFIG['user'], self.SPLUNK_CONFIG['pass']))
            # Wait until all entries have been processed
            inserted_guids = {e.get('guid') for e in log_entries}
            queried_guids = set()
            while not inserted_guids.issubset(queried_guids):  # we should be able to find every inserted guid
                for guid in inserted_guids:
                    for found_guid in self.query('|where match(guid, "{}")'.format(guid), data_model, verbose=False):
                        queried_guids.add(found_guid)
                time.sleep(SLEEP_INTERVAL)
        else:
            raise NotImplementedError("Data model not implemented: {}".format(data_model))

    def car_to_splunk(self, entry):
        event = entry['fields'].copy()
        event.update({
          'fake_tag': "dm-{}-{}".format(entry['object'], entry['action']),
          'guid': entry['guid']
        })
        return event

    def query(self, query, data_model, verbose=True):
        # Adding the GUID lets us correlate the results, need to replace tags so we don't need custom splunk configs
        formatted_query = "search index=" + data_model.value.lower() + " " + query.replace('tag', 'fake_tag') + " | fields + guid"
        if verbose:
            print("\n\nSearch: " + formatted_query)

        results = self.session.post(self.url('search/jobs'), data={
          'search': formatted_query,
          'output_mode': 'json',
          'exec_mode': 'oneshot'
        }, auth=(self.SPLUNK_CONFIG['user'], self.SPLUNK_CONFIG['pass']))
        if verbose:
            print("Results: " + str([r['_raw'] for r in results.json()['results']]))

        return [r['guid'] for r in results.json()['results']]

class ElasticConnector():

    ELASTIC_CONFIG = {
      'hostname': docker_daemon_ip,  # docker_daemon_ip is a variable for IP address
      'port': '9900',
      'user': 'elastic',
      'pass': 'changeme'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.verify = False
        self.auth = (self.ELASTIC_CONFIG['user'], self.ELASTIC_CONFIG['pass'])
        self.prep()

    def url(self, val):
        return "http://{}:{}/{}".format(self.ELASTIC_CONFIG['hostname'], self.ELASTIC_CONFIG['port'], val)

    def prep(self):
        for m in DataModels:
            # Delete the indexes
            dr = self.session.delete(self.url(m.value.lower()), auth=(self.ELASTIC_CONFIG['user'], self.ELASTIC_CONFIG['pass']))

            # Then create them. Raise an error if unable to create
            resp = self.session.put(self.url(m.value.lower()), auth=(self.ELASTIC_CONFIG['user'], self.ELASTIC_CONFIG['pass']))

    def push(self, data_model, log_entries):
        if data_model == DataModels.CAR:
            for e in log_entries:
                request = self.session.put(self.url("{}/event/{}".format(data_model.value.lower(), e['guid'])), data=json.dumps({'data_model': e}), auth=(self.ELASTIC_CONFIG['user'], self.ELASTIC_CONFIG['pass']))

            # Wait until all log entries have been indexed
            inserted_guids = {e.get('guid') for e in log_entries}
            queried_guids = set()
            while not inserted_guids.issubset(queried_guids):  # we should be able to find every inserted guid
                # TODO: convert to multi search
                for guid in inserted_guids:
                    for found_guid in self.query('data_model.guid:"{}"'.format(guid), data_model, verbose=False):
                        queried_guids.add(found_guid)
                time.sleep(SLEEP_INTERVAL)
        else:
            raise NotImplementedError("Data model not implemented: {}".format(data_model.value))

    def query(self, query, data_model, verbose=True):
        if verbose:
            print("\n\nSearch: " + query)

        results = self.session.get(self.url("{}/_search".format(data_model.value.lower())), params={
          'q': query
        }, auth=(self.ELASTIC_CONFIG['user'], self.ELASTIC_CONFIG['pass']))

        if verbose:
            print("Results: " + str(results.json()['hits']['hits']))

        return [r['_source']['data_model']['guid'] for r in results.json()['hits']['hits']]
