# triage2timesketch
Automated processing of host artifacts and ingestion in to timesketch using a durable Azure function.


The function input is a post request containing 3 parameters:

zipfile - actual zippied artifacts, base64 encoded
hostname - asset hostname
type - type of triage eg.  web, account


Zip file limit is 100mb due to Azure functions limitations.


