import os
import sys
import transformers

def save_llm_from_llava(source_repo:str, target_repo:str):
    if not source_repo:
        raise ValueError("source_repo is unset!")
    if not target_repo:   
        raise ValueError("target_repo is unset!")

    tokenizer = transformers.AutoTokenizer.from_pretrained(source_repo)

    # NOTE: granite vision support was added to transformers very recently (4.49);
    # if you get size mismatches, your version is too old.
    # If you are running with an older version, set `ignore_mismatched_sizes=True`
    # as shown below; it won't be loaded correctly, but the LLM part of the model that
    # we are exporting will be loaded correctly.
    print(f"Loading model (AutoModelForImageTextToText) from: {source_repo}...")
    model = transformers.AutoModelForImageTextToText.from_pretrained(source_repo, ignore_mismatched_sizes=True)
    print(f"Saving pre-trained tokenizer to: {target_repo}...")
    tokenizer.save_pretrained(target_repo)
    print(f"Saving pre-trained mode to: {target_repo}...")    
    model.language_model.save_pretrained(target_repo)

if __name__ == "__main__":   
    arg_len = len(sys.argv)
    if arg_len < 3:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <source_repo> <target_repo>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]   
    source_repo = sys.argv[1]
    target_repo = sys.argv[2]   
    
    # Print input variables being used for this run
    print(f">> {fx_name}: source_repo='{source_repo}' target_repo='{target_repo}'")     
    
    # invoke fx
    save_llm_from_llava(source_repo=source_repo, target_repo=target_repo)  
   