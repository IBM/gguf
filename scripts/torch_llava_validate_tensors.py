import os
import sys
import torch

def validate_llava_tensors(file_llava_clip:str, file_llava_projector:str) -> None:
    if not file_llava_clip:
        raise ValueError(f"invalid: file_llava_clip: {file_llava_clip}")
    if not file_llava_projector:
        raise ValueError(f"invalid: file_llava_projector: {file_llava_projector}")    

    encoder_tensors = torch.load(file_llava_clip)
    projector_tensors = torch.load(file_llava_projector)

    assert len(encoder_tensors) > 0
    assert len(projector_tensors) > 0

    keys_projector = projector_tensors.keys()
    print("encoder keys: \n", encoder_tensors.keys())
    print("projector keys: type: \n", type(keys_projector))
    
    import json
    with open("projector_keys.txt", "w") as projector_file:
        json.dump(keys_projector, projector_file, sort_keys=True, indent=2)
    
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
    
    # Print input variables being used for this run
    print(f">> {fx_name}: file_llava_clip='{file_llava_clip}' file_llava_projector='{file_llava_projector}'")     
    
    # invoke fx
    validate_llava_tensors(file_llava_clip=file_llava_clip, file_llava_projector=file_llava_projector)  
    