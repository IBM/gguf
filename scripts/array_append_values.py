import sys
import json

def append_to_array(input_array, values_to_append):
    input_array.extend(values_to_append)
    return input_array

if __name__ == "__main__":
    try:
        input_array = json.loads(sys.argv[1])
        values_to_append = json.loads(sys.argv[2])
        print(f"input_array: {input_array}")
        print(f"values_to_append: {values_to_append}")
        result = append_to_array(input_array, values_to_append)
        print(json.dumps(result))
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Exit successfully
    sys.exit(0)