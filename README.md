# ingest_pipeline_metrics
Collect Elasticsearch ingest pipeline metrics and index them for monitoring

# Ingest Pipeline Monitoring

Jeff Vestal

### Info
Until we get ingest monitoring built-in to stack monitoring, this is a temporary workaround


## WARNING

Prior to 7.17.4 and 8.2, there is a slight, but real, potential a hung node could take down a cluster. This was addressed by this [GH Issue](https://github.com/elastic/elasticsearch/issues/82337)
#


### Environment Variables that must be set
Monitoring Cluster
 - "es_mon_cloud_id":
 - "es_mon_cloud_user":    
 - "es_mon_cloud_pass":    

  Source Cluster
 
 - "es_cloud_id":   
 - "es_cloud_user":    
 -  "es_cloud_pass":

### Running
python ./main.py
