#!/bin/bash -e

if [ ! -z $1 ];  then
   BRANCH=$1
   echo "Building $BRANCH"
   git checkout $BRANCH
else
   echo "Building current branch"
fi

rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install wheel

VERSION='7.0.7'

WHLS="stix_shifter-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_alertflex-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_arcsight-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_async_template-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_aws_athena-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_aws_cloud_watch_logs-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_aws_guardduty-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_azure_log_analytics-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_azure_sentinel-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_bigfix-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_carbonblack-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_cbcloud-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_cisco_secure_email-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_crowdstrike-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_crowdstrike_alerts-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_crowdstrike_logscale-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_cybereason-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_darktrace-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_datadog-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_demo_template-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_elastic_ecs-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_error_test-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_gcp_chronicle-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_guardium-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_ibm_security_verify-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_infoblox-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_msatp-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_mysql-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_nozomi_vantage-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_okta-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_onelogin-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_paloalto-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_proofpoint-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_proxy-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_qradar-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_qradar_perf_test-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_reaqta-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_reversinglabs-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_rhacs-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_secretserver-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_security_advisor-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_sentinelone-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_splunk-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_stix_bundle-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_sumologic-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_symantec_endpoint_security-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_synchronous_template-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_sysdig-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_stellarcyber-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_tanium-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_trellix_endpoint_security_hx-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_trendmicro_vision_one-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_vectra-${VERSION}-py2.py3-none-any.whl
stix_shifter_utils-${VERSION}-py2.py3-none-any.whl
stix_shifter_modules_securonix-${VERSION}-py2.py3-none-any.whl"

while IFS= read -r file; do
  rm -f dist/$file
done <<< "$WHLS"

MODE=N VERSION=${VERSION} python setup.py bdist_wheel

while IFS= read -r file; do
  ls dist/$file
done <<< "$WHLS"

echo "-----------------------------------------------"
echo "Wheel files created"
