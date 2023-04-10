import torch
import os
import torch_neuron
import importlib

batch_size = 1

sequence_length = 128

model_name = 'twmkn9/bert-base-uncased-squad2'
tokenizer_class_name = 'AutoTokenizer'
model_class_name = 'AutoModelForQuestionAnswering'



# 2. LOAD PRE-TRAINED MODEL
print(f'\nLoading pre-trained model: {model_name}')
transformers = importlib.import_module("transformers")
tokenizer_class = getattr(transformers, tokenizer_class_name)
model_class = getattr(transformers, model_class_name)
tokenizer = tokenizer_class.from_pretrained(model_name)
model = model_class.from_pretrained(model_name, return_dict=False)


question = "Who ruled Macedonia"

context = """Macedonia was  an ancient kingdom on the periphery of Archaic and Classical Greece,
and later the dominant state of Hellenistic Greece. The kingdom was founded and initially ruled
by the Argead dynasty, followed by the Antipatrid and Antigonid dynasties. Home to the ancient
Macedonians, it originated on the northeastern part of the Greek peninsula. Before the 4th
century BC, it was a small kingdom outside of the area dominated by the city-states of Athens,
Sparta and Thebes, and briefly subordinate to Achaemenid Persia."""

# 1. TOKENIZE THE INPUT
# note: if you don't include return_tensors='pt' you'll get a list of lists which is easier for
# exploration but you cannot feed that into a model.
inputs = tokenizer.encode_plus(question,
                                context,
                                return_tensors="pt",
                                max_length=sequence_length,
                                padding='max_length',
                                truncation=True)


print('\nTracing model ...')
example_inputs = (
    torch.cat([inputs['input_ids']] * batch_size,0), 
    torch.cat([inputs['attention_mask']] * batch_size,0)
)

pipeline_cores = 1


model_traced = torch.neuron.trace(model, 
                                  example_inputs, 
                                  verbose=1, 
                                  compiler_workdir='./bert-bs-'+str(batch_size))


answer_logits = model_traced(*example_inputs)

model_traced.save('./compiled-model-bs-'+str(batch_size)+'.pt')

print('\n Model Traced and Saved')


