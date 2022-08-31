
# Ingest Pipeline Monitoring
Collect Elasticsearch ingest pipeline metrics and index them for monitoring

### Info
Until we get ingest monitoring built-in to stack monitoring, this is a temporary workaround


## *WARNING*

Prior to 7.17.4 and 8.2, there is a slight, but real, potential a **hung node could take down a cluster**. 

This was addressed by this [GH Issue](https://github.com/elastic/elasticsearch/issues/82337)

You are **strongly encouraged** to only run this in the 7x on versions 7.17.4+ or 8x 8.2+


## Running
python ./main.py

### Environment Variables that must be set
Monitoring Cluster
 - "es_mon_cloud_id":
 - "es_mon_cloud_user":    
 - "es_mon_cloud_pass":    

  Source Cluster
 
 - "es_cloud_id":   
 - "es_cloud_user":    
 -  "es_cloud_pass":



### Example Dashboard
<img width="2238" alt="Elastic Ingest Pipeline Monitoring Dashboard" src="https://user-images.githubusercontent.com/53237856/187766429-6a474a74-e87a-4182-89f5-a0e4b3c05a11.png">
