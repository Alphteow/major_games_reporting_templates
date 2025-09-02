import pandas as pd
import json
import numpy as np

def create_sports_templates_json():
    """
    Convert Excel data to JSON format for frontend-only sports template generator
    Reads all data dynamically from the Excel file without hardcoding
    """
    
    # Read the Excel file
    file_path = 'data/updated_all_sports.xlsx'
    
    try:
        # Read all necessary sheets
        sport_mapping_df = pd.read_excel(file_path, sheet_name='sport_result_mapping')
        round_mapping_df = pd.read_excel(file_path, sheet_name='round_template_mappings')
        
        # Try to read template sheets
        try:
            template_raw_df = pd.read_excel(file_path, sheet_name='template_raw')
        except:
            print("Warning: template_raw sheet not found, will create basic templates")
            template_raw_df = None
            
        try:
            template_type_df = pd.read_excel(file_path, sheet_name='template_type')
        except:
            print("Warning: template_type sheet not found")
            template_type_df = None
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
    # Process sport mappings - convert to list of dictionaries
    sport_mappings = []
    for _, row in sport_mapping_df.iterrows():
        sport_mappings.append({
            'sport': str(row['sport']) if pd.notna(row['sport']) else '',
            'event': str(row['value']) if pd.notna(row['value']) else '',
            'resultType': str(row['resultType']) if pd.notna(row['resultType']) else '',
            'team': str(row['team']) if pd.notna(row['team']) else 'no'
        })
    
    # Process round mappings - convert to list of dictionaries
    round_mappings = []
    for _, row in round_mapping_df.iterrows():
        round_mappings.append({
            'sport': str(row['sport']) if pd.notna(row['sport']) else '',
            'event': str(row['event']) if pd.notna(row['event']) else '',
            'round_type': str(row['round_type']) if pd.notna(row['round_type']) else '',
            'result_type': str(row['result_type']) if pd.notna(row['result_type']) else '',
            'is_team': str(row['is_team']) if pd.notna(row['is_team']) else 'no',
            'template_id': int(row['template_id']) if pd.notna(row['template_id']) else 1
        })
    
    # Create templates dictionary from template_raw or template_type
    templates = {}
    
    if template_type_df is not None and not template_type_df.empty:
        # Use template_type data
        for _, row in template_type_df.iterrows():
            if pd.notna(row.get('template')):
                template_id = str(row.get('id', len(templates) + 1))
                
                # Extract fields from template
                import re
                template_text = str(row['template'])
                fields = list(set(re.findall(r'\{([^}]+)\}', template_text)))
                
                templates[template_id] = {
                    'name': str(row.get('name', f'Template {template_id}')),
                    'template': template_text,
                    'fields': fields
                }
    
    # Get unique sports list
    sports_list = sorted(list(set(mapping['sport'] for mapping in sport_mappings if mapping['sport'])))
    
    # Get unique events list
    events_list = sorted(list(set(mapping['event'] for mapping in sport_mappings if mapping['event'])))
    
    # Get unique round types
    round_types_list = sorted(list(set(mapping['round_type'] for mapping in round_mappings if mapping['round_type'])))
    
    # Create the final JSON structure
    json_data = {
        'sport_mappings': sport_mappings,
        'round_mappings': round_mappings,
        'templates': templates,
        'sports_list': sports_list,
        'events_list': events_list,
        'round_types_list': round_types_list,
        'metadata': {
            'total_sports': len(sports_list),
            'total_events': len(sport_mappings),
            'total_round_mappings': len(round_mappings),
            'total_templates': len(templates),
            'generated_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0',
            'source_file': file_path
        }
    }
    
    # Create data directory if it doesn't exist
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Save to JSON file
    output_file = 'data/sports_templates.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON file created successfully: {output_file}")
    print(f"Total sports: {len(sports_list)}")
    print(f"Total sport-event combinations: {len(sport_mappings)}")
    print(f"Total round mappings: {len(round_mappings)}")
    print(f"Total templates: {len(templates)}")
    
    return json_data

def create_basic_template(mapping):
    """
    Create a basic template based on mapping data
    """
    sport = mapping['sport']
    event = mapping['event']
    round_type = mapping['round_type']
    result_type = mapping['result_type']
    is_team = mapping['is_team']
    
    if 'final' in round_type.lower():
        if is_team == 'yes':
            if result_type == 'time':
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_team}} - {{gold_time}}\nSilver: {{silver_team}} - {{silver_time}}\nBronze: {{bronze_team}} - {{bronze_time}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
            else:
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_team}} - {{gold_score}}\nSilver: {{silver_team}} - {{silver_score}}\nBronze: {{bronze_team}} - {{bronze_score}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
        else:
            if result_type == 'time':
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_athlete}} ({{gold_country}}) - {{gold_time}}\nSilver: {{silver_athlete}} ({{silver_country}}) - {{silver_time}}\nBronze: {{bronze_athlete}} ({{bronze_country}}) - {{bronze_time}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
            elif result_type == 'height':
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_athlete}} ({{gold_country}}) - {{gold_height}}\nSilver: {{silver_athlete}} ({{silver_country}}) - {{silver_height}}\nBronze: {{bronze_athlete}} ({{bronze_country}}) - {{bronze_height}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
            elif result_type == 'distance':
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_athlete}} ({{gold_country}}) - {{gold_distance}}\nSilver: {{silver_athlete}} ({{silver_country}}) - {{silver_distance}}\nBronze: {{bronze_athlete}} ({{bronze_country}}) - {{bronze_distance}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
            elif result_type == 'weight':
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_athlete}} ({{gold_country}}) - {{gold_weight}}\nSilver: {{silver_athlete}} ({{silver_country}}) - {{silver_weight}}\nBronze: {{bronze_athlete}} ({{bronze_country}}) - {{bronze_weight}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
            else:
                return f"{round_type.upper()} RESULTS - {sport} {event}\n\nGold: {{gold_athlete}} ({{gold_country}}) - {{gold_score}}\nSilver: {{silver_athlete}} ({{silver_country}}) - {{silver_score}}\nBronze: {{bronze_athlete}} ({{bronze_country}}) - {{bronze_score}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
    
    elif any(x in round_type.lower() for x in ['prelim', 'qualif', 'heat']):
        if result_type == 'time':
            return f"{round_type.upper()} - {sport} {event}\n\nHeat {{heat_number}}:\n1. {{athlete_1}} ({{country_1}}) - {{time_1}} Q\n2. {{athlete_2}} ({{country_2}}) - {{time_2}} Q\n3. {{athlete_3}} ({{country_3}}) - {{time_3}}\n4. {{athlete_4}} ({{country_4}}) - {{time_4}}\n\nQ = Qualified\nVenue: {{venue}}\nDate: {{date}}"
        else:
            return f"{round_type.upper()} - {sport} {event}\n\nResults:\n1. {{competitor_1}} - {{score_1}}\n2. {{competitor_2}} - {{score_2}}\n3. {{competitor_3}} - {{score_3}}\n4. {{competitor_4}} - {{score_4}}\n\nVenue: {{venue}}\nDate: {{date}}"
    
    elif 'round robin' in round_type.lower():
        return f"ROUND ROBIN STANDINGS - {sport} {event}\n\nStandings:\n1. {{team_1}} - {{points_1}} points\n2. {{team_2}} - {{points_2}} points\n3. {{team_3}} - {{points_3}} points\n4. {{team_4}} - {{points_4}} points\n\nVenue: {{venue}}\nDate: {{date}}"
    
    elif any(x in round_type.lower() for x in ['quarter', 'semi']):
        if is_team == 'yes':
            return f"{round_type.upper()} - {sport} {event}\n\n{{team_1}} {{score_1}} - {{score_2}} {{team_2}}\n\nWinner: {{winner}}\nAdvances to: {{next_round}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
        else:
            return f"{round_type.upper()} - {sport} {event}\n\n{{athlete_1}} ({{country_1}}) defeats {{athlete_2}} ({{country_2}})\nScore: {{score}}\n\nAdvances to: {{next_round}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"
    
    else:
        # Default template
        return f"{round_type.upper()} - {sport} {event}\n\nResults:\n{{competitor_1}} vs {{competitor_2}}\nResult: {{result}}\n\nVenue: {{venue}}\nDate: {{date}}\nTime: {{time}}"

# Run the function
if __name__ == "__main__":
    json_data = create_sports_templates_json()
    
    if json_data:
        print("\nJSON Structure Created Successfully!")
        print(f"- Sports: {len(json_data['sports_list'])}")
        print(f"- Sport-Event Mappings: {len(json_data['sport_mappings'])}")
        print(f"- Round Mappings: {len(json_data['round_mappings'])}")
        print(f"- Templates: {len(json_data['templates'])}")
        
        print("\nSample Sports:")
        for sport in json_data['sports_list'][:10]:
            print(f"  - {sport}")
        
        print("\nSample Templates:")
        for template_id, template_data in list(json_data['templates'].items())[:3]:
            print(f"  Template {template_id}: {template_data['name']}")
    else:
        print("Failed to create JSON file")
