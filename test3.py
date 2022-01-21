from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
response = translation.translate('qradar', 'query', '{}', "[ipv4-addr:value = '127.0.0.1']", {})

print(response)