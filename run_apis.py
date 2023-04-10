import requests
import os
from configparser import ConfigParser
from concurrent import futures


with open('config.properties') as f:
    config_lines = '[global]\n' + f.read()
f.close()

config = ConfigParser()
config.read_string(config_lines)

num_cores = int(config['global']['num_cores'])
num_models_per_server = int(config['global']['num_models_per_server'])

num_models = num_cores*num_models_per_server

COUNT = 1000

url_template = "http://localhost:%i/predictions_neuron_core_%i/model_%i"

# Neuron Core 0
def api_nc_0_model_0(url_template, COUNT):
    for _ in range(COUNT):
        response = requests.get(url_template % (8081,0,0))

# Neuron Core 1
def api_nc_1_model_0(url_template, COUNT):
    for _ in range(COUNT):
        response = requests.get(url_template % (8082,1,0))

# Neuron Core 2
def api_nc_2_model_0(url_template, COUNT):
    for _ in range(COUNT):
        response = requests.get(url_template % (8083,2,0))

# Neuron Core 3
def api_nc_3_model_0(url_template, COUNT):
    for _ in range(COUNT):
        response = requests.get(url_template % (8084,3,0))

# Neuron Core 4
def api_nc_4_model_0(url_template, COUNT):
    for _ in range(COUNT):
        response = requests.get(url_template % (8085,4,0))

# Neuron Core 5
def api_nc_5_model_0(url_template, COUNT):
    for _ in range(COUNT):
        response = requests.get(url_template % (8086,5,0))



with futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
    executor.submit(api_nc_0_model_0,url_template, COUNT)
    executor.submit(api_nc_1_model_0,url_template, COUNT)
    executor.submit(api_nc_2_model_0,url_template, COUNT)
    executor.submit(api_nc_3_model_0,url_template, COUNT)
    executor.submit(api_nc_4_model_0,url_template, COUNT)
    executor.submit(api_nc_5_model_0,url_template, COUNT)






