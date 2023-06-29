from typing import Optional
from fastapi import FastAPI,logger,responses
from configparser import ConfigParser
import torch, os, logging
import importlib
import os


global device
global processor
global models
global tokenizers
global logger
global default_question, default_context


chip_type = os.environ.get("CHIP_TYPE", "inf1")
if chip_type == "inf1":
    import torch_neuron
elif chip_type == "inf2"
    import torch_neuronx

logger = logging.getLogger()

# Read static configuration from config.properties
logger.warning("\nParsing configuration ...")

with open('config.properties') as f:
    config_lines = '[global]\n' + f.read()
    f.close()
config = ConfigParser()
config.read_string(config_lines)

compiled_model = config['global']['compiled_model']
num_models_per_server = int(config['global']['num_models_per_server'])

model_name = 'twmkn9/bert-base-uncased-squad2'
tokenizer_class_name = 'AutoTokenizer'
model_class_name = 'AutoModelForQuestionAnswering'
transformers = importlib.import_module("transformers")
tokenizer_class = getattr(transformers, tokenizer_class_name)


default_question = "What does the little engine say"
default_context = """In the childrens story about the little engine a small locomotive is pulling a large load up a mountain.
    Since the load is heavy and the engine is small it is not sure whether it will be able to do the job. This is a story 
    about how an optimistic attitude empowers everyone to achieve more. In the story the little engine says: 'I think I can' as it is 
    pulling the heavy load all the way to the top of the mountain. On the way down it says: I thought I could."""


env_var = os.getenv('NEURON_RT_VISIBLE_CORES')
neuron_core=int(env_var[0])

# FastAPI server
app = FastAPI()

# Server healthcheck
@app.get("/")
async def read_root():
    return {"Status": "Healthy"}

prediction_api_name = 'predictions_neuron_core_'+str(neuron_core)
postprocess = True
quiet = False

# Model inference API endpoint
@app.get("/{prediction_api_name}/{model_id}")
async def infer(model_id, seq_0: Optional[str] = default_question, seq_1: Optional[str] = default_context):
    question=seq_0
    context=seq_1
    status=200
    if model_id in models.keys():
        if not quiet:
            logger.warning(f"\nQuestion: {question}\n")
        tokenizer=tokenizers[model_id]
        encoded_input = tokenizer.encode_plus(question, context, return_tensors='pt', max_length=128, padding='max_length', truncation=True)
        model=models[model_id]
        model_input = (encoded_input['input_ids'],  encoded_input['attention_mask'])
        output=model(*model_input) # This is specific to Inferentia
        answer_text = str(output[0])
        if postprocess:
            answer_start = torch.argmax(output[0])
            answer_end = torch.argmax(output[1])+1
            if (answer_end > answer_start):
                answer_text = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(encoded_input["input_ids"][0][answer_start:answer_end]))
            else:
                answer_text = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(encoded_input["input_ids"][0][answer_start:]))
        if not quiet:
            logger.warning("\nAnswer: ")
            logger.warning(answer_text)
    else:
        status=404
        answer_text = f"Model {model_id} does not exist. Try a model name up to model{num_models-1}"
        if not quiet:
            logger.warning(answer_text)
    return responses.JSONResponse(status_code=status, content={"detail": answer_text})


tokenizers={}
models={}
# LOAD Models
print('Num of models to be loaded = '+str(num_models_per_server))
for i in range(num_models_per_server):
    model_id = 'model_' + str(i)
    # Load the compiled models
    print('Loading Model '+str(i)+'....')
    models[model_id] = torch.jit.load('/app/server/traced-models/'+compiled_model)
    tokenizers[model_id]=tokenizer_class.from_pretrained(model_name)
