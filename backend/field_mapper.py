from field_config import FIELD_CONFIG
import re

def map_fields_to_labels(input_object):
    """
    Takes an object with FIELD_[number] keys and replaces them with the corresponding 
    labels from the field configuration.
    
    Args:
        input_object (dict): Dictionary containing keys like 'FIELD_7143', 'FIELD_20642', etc.
    
    Returns:
        dict: New dictionary with field keys replaced by their corresponding labels
    """
    
    # Create a mapping dictionary from field ID to label
    field_id_to_label = {}
    for field in FIELD_CONFIG:
        field_id_to_label[field['FieldID']] = field['Label']
    
    # Create a new dictionary to store the mapped results
    mapped_object = {}
    
    # Pattern to match FIELD_[number] keys
    field_pattern = re.compile(r'^FIELD_(\d+)$')
    
    for key, value in input_object.items():
        # Check if the key matches the FIELD_[number] pattern
        match = field_pattern.match(key)
        
        if match:
            # Extract the field ID number
            field_id = int(match.group(1))
            
            # Look up the corresponding label
            if field_id in field_id_to_label:
                # Use the label as the new key
                new_key = field_id_to_label[field_id]
                mapped_object[new_key] = value
            else:
                # If field ID not found in config, keep original key
                mapped_object[key] = value
        else:
            # If key doesn't match pattern, keep it as is
            mapped_object[key] = value
    
    return mapped_object

# Example usage:
if __name__ == "__main__":
    # Test with the example object you provided
    test_object = {
        'dynamicFieldMappings': '', 
        'recordName': 'P1332642429: Jane Doe [2 ACTIVE PSA]', 
        'datalistPath': '726~', 
        'recordPath': '215499', 
        'FIELD_7143': '1332642429', 
        'FIELD_20642': 'p1332642429', 
        'FIELD_SEARCHABLE_20642': 'p1332642429', 
        'FIELD_18471': 'draft', 
        'FIELD_7146': 'jane', 
        'FIELD_SEARCHABLE_7146': 'jane', 
        'FIELD_7145': 'doe', 
        'FIELD_SEARCHABLE_7145': 'doe', 
        'FIELD_12459': 'jane  doe', 
        'FIELD_20581': 'person', 
        'FIELD_20584': 'person', 
        'FIELD_28371': '[2 active psa]', 
        'DYNAMICFIELD_20410': '288546', 
        'FIELD_37926': 'alcorn', 
        'FIELD_SEARCHABLE_37926': 'alcorn', 
        'FIELD_20618': 'female', 
        'FIELD_SEARCHABLE_20618': 'female', 
        'FIELD_7148': 'female', 
        'DYNAMICFIELD_11977': '249128', 
        'DYNAMICFIELD_SEARCHABLE_11977': '249128', 
        'DYNAMICFIELD_20274': '245281', 
        'FIELD_20840': 'yes', 
        'FIELD_7149': '2020-11-01', 
        'FIELD_SEARCHABLE_7149': '2020-11-01', 
        'FIELD_48270': 'known', 
        'FIELD_SEARCHABLE_48270': 'known', 
        'FIELD_50387': 'jane doe', 
        'FIELD_SEARCHABLE_50387': 'jane doe'
    }
    
    result = map_fields_to_labels(test_object)
    
    print("Mapped object:")
    for key, value in result.items():
        print(f"  '{key}': '{value}'") 