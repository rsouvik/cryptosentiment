import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "hft"
org = "ddnusers"
token = "Y68gLteW69vpkdz3f15BFnvK6cVcAvwpUSx-e5kG8S3izH5DDSGDbd39zIneFuBUcumPeaXRUCMF3KG3Q7wh4w=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Delhi").field("temperature", 45.3)
write_api.write(bucket=bucket, org=org, record=p)