import time
import json
import re
from datetime import datetime
start_time = time.time()

# Function to transform values based on type information
def transform_value(value):
    if 'S' in value:  # String type
        val = value['S'].strip()
        if not val:  # Omit empty strings
            return None
        # Check if it's a valid RFC3339 date format and convert to Unix Epoch
        try:
            return int(datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ').timestamp())
        except ValueError:
            return val  # Return as string if not a date
    elif 'N' in value:  # Number type
        val = value['N'].strip()
        # Check for valid numeric value
        try:
            return int(val.lstrip("0")) if '.' not in val else float(val.lstrip("0"))
        except ValueError:
            return None
    elif 'BOOL' in value:  # Boolean type
        val = value['BOOL'].strip().lower()
        if val in ['1', 't', 'true']:
            return True
        elif val in ['0', 'f', 'false']:
            return False
        else:
            return None
    elif 'NULL' in value:  # Null type
        val = value['NULL'].strip().lower()
        if val in ['1', 't', 'true']:
            return None  # Return None for null
        elif val in ['0', 'f', 'false']:
            return None  # Omit
        else:
            return None
    elif 'L' in value:  # List type
        transformed_list = []
        if isinstance(value['L'], list):
            for item in value['L']:
                transformed_item = transform_value(item)
                if transformed_item is not None:
                    transformed_list.append(transformed_item)
        return transformed_list if transformed_list else None
    elif 'M' in value:  # Map type
        return transform_map(value['M'])

# Function to transform the map (dictionary)
def transform_map(data):
    transformed_data = {}
    for key, value in data.items():
        key = key.strip()  # Sanitize key
        if not key:  # Skip empty keys
            continue
        transformed_value = transform_value(value)
        if transformed_value is not None:  # Omit empty or invalid values
            transformed_data[key] = transformed_value
    return transformed_data if transformed_data else None

# Main function
def json_transformer(input_data):
    transformed_output = []
    # Transform the top-level map
    transformed_data = transform_map(input_data)
    if transformed_data:
        transformed_output.append(transformed_data)
    return transformed_output

# Input JSON (as a string)
input_json = '''
{
  "number_1": {
    "N": "1.50"
  },
  "string_1": {
    "S": "784498 "
  },
  "string_2": {
    "S": "2014-07-16T20:55:46Z"
  },
  "map_1": {
    "M": {
      "bool_1": {
        "BOOL": "truthy"
      },
      "null_1": {
        "NULL ": "true"
      },
      "list_1": {
        "L": [
          {
            "S": ""
          },
          {
            "N": "011"
          },
          {
            "N": "5215s"
          },
          {
            "BOOL": "f"
          },
          {
            "NULL": "0"
          }
        ]
      }
    }
  },
  "list_2": {
    "L": "noop"
  },
  "list_3": {
    "L": [
      "noop"
    ]
  },
  "": {
    "S": "noop"
  }
}
'''

# Parse input JSON
input_data = json.loads(input_json)

# Get the transformed output
output = json_transformer(input_data)

# Print the transformed output to stdout
print(json.dumps(output, indent=2))
end_time = time.time()
execution_time = end_time - start_time
print(f"\nThe program processes the input in approximately {execution_time:.4f} seconds.")
