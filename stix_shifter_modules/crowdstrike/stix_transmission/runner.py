import json
from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_transmission import stix_transmission

identity = "{\"type\": \"identity\", \"id\": \"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3\", \"name\": \"msatp\", \"identity_class\": \"events\"}"


def get_msatp_details():
    _connection = {
        'host': 'https://api.crowdstrike.com'
    }
    _configuration = {
        'auth': {
            'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzphNDdiNTc2MS0zYzk3LTQwMmItOTgzNi0wNmNhODI0NTViOTMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiI3MGViMDc0ODNlYzk0NzRmYmYxZThlODM4YzU3OGI0YiIsImV4cCI6MTYyMTg0NjIzNiwiZXh0Ijp7fSwiaWF0IjoxNjIxODQ0NDM2LCJpc3MiOiJodHRwczovL2FwaS5jcm93ZHN0cmlrZS5jb20vIiwianRpIjoiMTc5NWM4OTgtOWVmYy00YTlmLWI1Y2YtZmQyYTdmM2E3YTk1IiwibmJmIjoxNjIxODQ0NDM2LCJzY3AiOltdLCJzdWIiOiI3MGViMDc0ODNlYzk0NzRmYmYxZThlODM4YzU3OGI0YiJ9.StVQ58ugIbjrCvIO8bme-W4GarKUBvJyQ1HiBTKx5fp-Fu_lGUjrtPpmJLLeLR1hVGouwpchtjlqnJKI6_gh8fpPS5wyTMQeCS7QPOURZcayNjEuDtLwNRPYuogYJdlopzpZtAHc8vJh0Cm0vrwfLuomBqV5fM8HVOahU6E3jxtQTSv-Qtky0EnNgDaLnoblcPF40FsMuJnoKBNsEDY8Y0ixoeKH6hr0Xk-6O1TeNiwrv7Df7oeBoENXECftZGeWlAwtou6Pu9Imxzo_D1b3XML7Hf-KgDmkFuKd1iL2IMGJupNDgSLHaBQmNYXnXSfR0lV4o4I3Wq2LZP4jqaslPIr8zukithU9PkDb-6-yyR_hAY6HSSI64-BXlhG2zoqxOvqeYC2M-u40QKGBu7GRwajUVYyV8qZhlDnPhrWOPAOXN-L2hrTwefZM3bYPy1bcBOqQY51eI1_j2sjJf3MHIqV0zExhSqkuZiSj52-t6P3WAlX5ZojF5o4Gd39ri9a7LgsQ2i1l73fsfEu1qHbqJNubM3TRfLe5a9qFbBn6a6VLQJT76NRRrhzi0Ja7q32wA_48XvoYUQmEfNfOaN7p-6wkDDi8iduKeq6AKJbGU9_0EbBcrOEHB34YsziXEOs_nFSlE9YehvMfl1-EtchPUf0VhaqzITa9fCnJ6Gm2r4Y'
        }
    }
    return _connection, _configuration


if __name__ == '__main__':
    connection, configuration = get_msatp_details()
    # read patterns to test

    pattern = "[ipv4-addr:value = '9.147.31.113' AND process:name = 'python3']"

    #translation = stix_translation.StixTranslation()
    #queries = translation.translate(module='msatp', translate_type='query', data_source='', data=pattern)
    # print(queries)
    transmission = stix_transmission.StixTransmission(module='crowdstrike', connection=connection,
                                                      configuration=configuration)
    #query = queries['queries'][0]

    #print(query)

    translation = stix_translation.StixTranslation()


    response = transmission.results(0, 0, 9)
    if response['success']:
        data = response['data']
        results = translation.translate(module='msatp', translate_type='results', data_source=identity,
                                        data=json.dumps(data))
        print(results)
#
# def get_json(path):
#     with open(path, 'r') as f:
#         data = f.read()
#         j = json.loads(data)
#         d = "[" + json.dumps(j) + "]"
#         return d
#
#
# if __name__ == '__main__':
#     cbc_json = get_json('/Users/barha/Desktop/IBM/cp4s/lab/cb.json')
#     translation = stix_translation.StixTranslation()
#     response = translation.translate('cbcloud', 'results', "{\"type\": \"identity\", \"id\": \"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3\", \"name\": \"cbcloud\", \"identity_class\": \"events\"}", cbc_json)
#     print(response)
