import os
import logging
from pprint import pprint
from elasticsearch import Elasticsearch, helpers
from elasticsearch.client import NodesClient 
from datetime import datetime

import time
starttime = time.time()



def esConnect(cid, user, passwd):
    '''Connect to Elastic Cloud cluster'''

    #TODO switch to API key?
    logging.info('Starting to create ES Connection')
    logging.debug('%s - %s - %s' % (cid, user, passwd))
    es = Elasticsearch(cloud_id=cid, http_auth=(user, passwd))
    
    logging.info('Finished creating ES Connection')
    return es

def esGetNodeStats(es):
    '''
    Pull node stats filtered for pipilines metrics
    GET /_nodes/stats/ingest?filter_path=nodes.*.ingest,nodes.*.timestamp
    '''

    filter_path = 'nodes.*.ingest,nodes.*.timestamp'
    metric = 'ingest'
    
    pipeline_stats = NodesClient.stats(es, metric=metric, filter_path=filter_path )
    return(pipeline_stats)

def parse_pipeline_stats(node_pipeline, cluster_name):
    bulk_load = []
    for node in node_pipeline['nodes']:
        node_ts = node_pipeline['nodes'][node]['timestamp']
        
        for pipeline in node_pipeline['nodes'][node]['ingest']['pipelines']:
            # Build total for each pipeline
    
            pipeline_stat_totals = {
                                'cluster' : {
                                    'name' : cluster_name
                                            },
                                '@timestamp' : node_ts,
                                'node' : {
                                    'name' : node
                                },
                                'pipeline' : {
                                    'name' : pipeline,
                                    'total' : {
                                        'count' : node_pipeline['nodes'][node]['ingest']['pipelines'][pipeline]['count'],
                                        'time_in_millis' : node_pipeline['nodes'][node]['ingest']['pipelines'][pipeline]['time_in_millis'],
                                        'current' : node_pipeline['nodes'][node]['ingest']['pipelines'][pipeline]['current'],
                                        'failed' : node_pipeline['nodes'][node]['ingest']['pipelines'][pipeline]['failed']
                                           }
                                    }
                                }
    
            #TODO build create/index(dataseaream) for bulk load
            bulk_load.append({"create": {"_index": "pipeline_metrics-pipeline_total"}})
            bulk_load.append(pipeline_stat_totals)
            
            # Build processor docs
            for processor in node_pipeline['nodes'][node]['ingest']['pipelines'][pipeline]['processors']:
                for name in processor:
                    processor_info = {
                                    'cluster' : {
                                        'name' : cluster_name
                                    },
                            '@timestamp' : node_ts,
                            'node' : {'name' : node
                                     },
                            'pipeline' : {
                                'name' : pipeline,
                                'processor' : {
                                    'name' : name,
                                    'type' : processor[name]['type'],
                                    'stats' : {
                                        'count' : processor[name]['stats']['count'],
                                        'time_in_millis' : processor[name]['stats']['time_in_millis'], 
                                        'current' : processor[name]['stats']['current'],
                                        'failed' : processor[name]['stats']['failed']
                                    }
                                }
                            }
                        }
                    
                    #TODO build create/index(dataseaream) for bulk load
                    bulk_load.append({"create": {"_index": "pipeline_metrics-pipeline_processors"}})
                    bulk_load.append(processor_info)
    
    #pprint(processor_info)
    
    #pprint(bulk_load)
    #pprint(pipeline_stat_totals)
    #pprint(processor_info)
    return(bulk_load)


def bulkLoad(es, payload):
    '''
    bulk load
    '''

    resp = es.bulk(body=payload)
    return resp

if __name__ == '__main__':
    
    # setup elastic cloud connection
    es_cloud_id = os.getenv('es_cloud_id')
    es_cloud_user = os.getenv('es_cloud_user')
    es_cloud_pass = os.getenv('es_cloud_pass')
    # es monitoring cluster
    es_mon_cloud_id = os.getenv('es_mon_cloud_id')
    es_mon_cloud_user = os.getenv('es_mon_cloud_user')
    es_mon_cloud_pass = os.getenv('es_mon_cloud_pass')

    
    logging.info('Calling esConnect')
    es = esConnect(es_cloud_id, es_cloud_user, es_cloud_pass)
    es_mon = esConnect(es_mon_cloud_id, es_mon_cloud_user, es_mon_cloud_pass)

    while True:
    
        #get metrics
        pipeline_stats = esGetNodeStats(es)
        cluster_name = 'Wonder Wharf'
        parsed_metrics = parse_pipeline_stats(pipeline_stats, cluster_name)
    
        #print('\n\n')
        #pprint(parsed_metrics[-2:])
    
        response = bulkLoad(es_mon, parsed_metrics)
        #print(response)
        print(response['took'])
        print(response['errors'])
        print(datetime.now())
        
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

