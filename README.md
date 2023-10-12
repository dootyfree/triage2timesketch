# triage2timesketch
Automated processing of host artifacts and ingestion in to timesketch using a durable Azure function.


The function input is a post request containing 3 parameters:
<br />zipfile - actual zippied artifacts, base64 encoded
<br />hostname - asset hostname
<br />type - type of triage eg.  web, account


Zip file limit is 100mb due to Azure functions limitations.

<br />
Processing:
<br />The function will process the zipped artifacts with plaso and upload to timesketch application.
<br />The code will check timesketch for existing sketch mathing the hostname and add current timeline, if not found will create a sketch and add the timeline.


Return URL from Azure will provide processing status information.
