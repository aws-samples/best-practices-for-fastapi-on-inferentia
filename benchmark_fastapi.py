import requests
import os
from time import time
from configparser import ConfigParser
import pandas as pd

from multiprocessing import Pool

def process_one_api(input_list):
    """process a single api"""
    count_api = input_list[0]
    api_port = input_list[1]
    api_core = input_list[2]
    api_model_num = input_list[3]

    url_template = "http://localhost:%i/predictions_neuron_core_%i/model_%i"

    # fetch the data
    for _ in range(count_api):
        response = requests.get(url_template % (api_port,api_core,api_model_num))
    
    
    return None

def run_apis_in_parallel(COUNT,num_cores,num_models_per_server):

    num_apis = num_cores*num_models_per_server
    count_api = int(COUNT/num_apis)

    input_list = []
    for nc in range(num_cores):
        for i in range(num_models_per_server):
            input_list.append([count_api,8080+nc+1,nc,i])
    
    pool = Pool(processes=num_apis)
    pool.map(process_one_api, input_list)


# BENCHMARK
if __name__ == "__main__":

    print('RUNNING BENCHMARK....')

    with open('config.properties') as f:
        config_lines = '[global]\n' + f.read()
    f.close()
    config = ConfigParser()
    config.read_string(config_lines)

    num_cores = int(config['global']['num_cores'])
    num_models_per_server = int(config['global']['num_models_per_server'])
    
    COUNT = 1000

    url_template = "http://localhost:%i/predictions_neuron_core_%i/model_%i"
    
    start = time()

    run_apis_in_parallel(COUNT,num_cores,num_models_per_server)

    end = time()

    throughput = COUNT/(end-start)
    latency_ms = (end-start)*1000/COUNT

    print(f"avg. throughput (Inf1): {COUNT/(end-start):.2f} requests/sec ")
    print(f"avg. latency (Inf1)   : {(end-start)*1000/COUNT:.2f} ms\n")

    column_names = ['num_cores','num_models_per_server','avg_throughput','avg_latency_ms']
    df = pd.DataFrame([[num_cores,num_models_per_server,throughput,latency_ms]],columns = column_names)

    # if file does not exist write header
    results_filename = 'benchmark_results.csv'
    if not os.path.isfile(results_filename):
        df.to_csv(results_filename, header=column_names,index = None)
    else: # else it exists so append without writing the header
        df.to_csv(results_filename, mode='a', header=False,index = None)


