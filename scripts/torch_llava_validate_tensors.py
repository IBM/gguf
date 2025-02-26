import os
import sys
import torch

def validate_llava_tensors(file_llava_clip:str, file_llava_projector:str, projector_keys_file:str="projector_keys.txt") -> None:
    if not file_llava_clip:
        raise ValueError(f"invalid: file_llava_clip: {file_llava_clip}")
    if not file_llava_projector:
        raise ValueError(f"invalid: file_llava_projector: {file_llava_projector}")    

    encoder_tensors = torch.load(file_llava_clip)
    projector_tensors = torch.load(file_llava_projector)

    assert len(encoder_tensors) > 0
    assert len(projector_tensors) > 0

    keys_projector = projector_tensors.keys()
    print("encoder keys: len: \n", len(encoder_tensors.keys()))
    print("projector keys: type: ", type(keys_projector))
    
    import json
    with open("projector_keys.txt", "w") as projector_file:
      for key in keys_projector:
        projector_file.write(">> " + str(key) + "\n")
    
if __name__ == "__main__":   
    arg_len = len(sys.argv)
    if arg_len < 3:   
        script_name = os.path.basename(__file__)
        print(f"Usage: python {script_name} <file_llava_clip> <file_llava_projector>")
        print(f"Actual: sys.argv[]: '{sys.argv}'")
        sys.exit(1)
       
    # Parse input arguments into named params.   
    fx_name = sys.argv[0]   
    file_llava_clip = sys.argv[1]
    file_llava_projector = sys.argv[2]   
    
    if arg_len == 4:
        key_file = sys.argv[3]
    
    # Print input variables being used for this run
    print(f">> {fx_name}: file_llava_clip='{file_llava_clip}' file_llava_projector='{file_llava_projector}'")     
    
    # invoke fx
    validate_llava_tensors(file_llava_clip=file_llava_clip, file_llava_projector=file_llava_projector, projector_keys_file=key_file)  
    