import os
import transformers

MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")    
print(f"MODEL_PATH={MODEL_PATH}")

if not MODEL_PATH:
    raise ValueError("LOCAL_MODEL_PATH is unset!")

ENCODER_PATH = os.getenv("LLM_EXPORT_PATH")
print(f"ENCODER_PATH={MODEL_PATH}") 

if not ENCODER_PATH:   
    raise ValueError("ENCODER_PATH is unset!")

tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_PATH)

# NOTE: granite vision support was added to transformers very recently (4.49);
# if you get size mismatches, your version is too old.
# If you are running with an older version, set `ignore_mismatched_sizes=True`
# as shown below; it won't be loaded correctly, but the LLM part of the model that
# we are exporting will be loaded correctly.
model = transformers.AutoModelForImageTextToText.from_pretrained(MODEL_PATH, ignore_mismatched_sizes=True)

tokenizer.save_pretrained(ENCODER_PATH)
model.language_model.save_pretrained(ENCODER_PATH)