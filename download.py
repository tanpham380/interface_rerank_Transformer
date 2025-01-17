from transformers import AutoModel, AutoTokenizer
import os
import sys

model_dir = './models/model'
model_name = os.getenv('MODEL_NAME') # Model name is passed in when you build the container, the bash script for this is in the readme
if model_name is None or model_name == "":
    print("Fatal: MODEL_NAME is required")
    sys.exit(1)

print("Downloading model {} from Hugging Face model hub".format(model_name))

# Download and save the model and tokenizer
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model.save_pretrained(model_dir)
tokenizer.save_pretrained(model_dir)

print("Success")