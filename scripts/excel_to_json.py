import pandas as pd
import json

def convert_excel_to_json():
    # Read Excel file
    df = pd.read_excel('./sports_templates.xlsx', sheet_name='All Templates')
    
    # Convert fields column from string to array
    df['fields'] = df['fields'].apply(lambda x: eval(x) if pd.notna(x) else [])
    
    # Convert to JSON
    templates_data = df.to_dict('records')
    
    # Save as JSON
    with open('data/templates.json', 'w') as f:
        json.dump(templates_data, f, indent=2)
    
    print(f"Converted {len(templates_data)} templates to JSON")

if __name__ == "__main__":
    convert_excel_to_json()
