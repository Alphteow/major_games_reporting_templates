import pandas as pd
import json
import os
import ast
from typing import Dict, List, Optional

class TemplateJSONGenerator:
    def __init__(self, file_path: str):
        # Load all data
        self.template_raw = pd.read_excel(file_path, sheet_name='template_raw')
        self.template_type = pd.read_excel(file_path, sheet_name='template_type')
        self.all_sports = pd.read_excel(file_path, sheet_name='all_sports_raw')
        self.sport_result_mapping = pd.read_excel(file_path, sheet_name='sport_result_mapping')
        
        # Initialize the mapping system
        self.sport_map = self._build_sport_map()
        self.round_map = self._build_round_map()
        
    def _build_sport_map(self) -> Dict[str, str]:
        """Build comprehensive sport mapping"""
        sport_map = {}
        
        # Get all unique sports
        template_sports = set(self.template_raw['sport'].dropna().unique())
        all_sports_sports = set(self.all_sports['Sports'].dropna().unique())
        result_mapping_sports = set(self.sport_result_mapping['sport'].dropna().unique())
        unique_sports = template_sports | all_sports_sports | result_mapping_sports
        
        # Hardcoded mappings for all sports
        hardcoded_mappings = {
            'AQUATHLON': 'AQUATHLON',
            'DUATHLON': 'DUATHLON', 
            'TRIATHLON': 'TRIATHLON',
            'ARTISTIC SWIMMING': 'ARTISTIC SWIMMING',
            'ATHLETICS': 'ATHLETICS',
            'BADMINTON': 'BADMINTON',
            'BASEBALL': 'BASEBALL',
            'BASKETBALL': 'BASKETBALL',
            'BOWLING': 'BOWLING',
            'BOXING': 'BOXING',
            'CANOEING': 'CANOEING',
            'CHESS': 'CHESS',
            'CRICKET': 'CRICKET',
            'CUESPORTS': 'CUESPORTS',
            'BILLIARDS SPORTS': 'CUESPORTS',
            'CYCLING ROAD RACE': 'CYCLING',
            'CYCLING': 'CYCLING',
            'CYCLING MOUNTAIN BIKING': 'CYCLING',
            'DIVING': 'DIVING',
            'AQUATICS DIVING': 'DIVING',
            'DRAGON BOAT': 'TRADITIONAL BOAT RACE',
            'TRADITIONAL BOAT RACING': 'TRADITIONAL BOAT RACE',
            'EQUESTRIAN': 'EQUESTRIAN',
            'ESPORTS': 'ESPORTS',
            'E-SPORTS': 'ESPORTS',
            'FENCING': 'FENCING',
            'FLOORBALL': 'FLOORBALL',
            'FLOORBALL -': 'FLOORBALL',
            'FLYING DISC': 'FLYING DISC',
            'FOOTBALL': 'FOOTBALL',
            'GOLF': 'GOLF',
            'GOLF -': 'GOLF',
            'GYMNASTICS': 'GYMNASTICS',
            'HANDBALL': 'HANDBALL',
            'HOCKEY': 'HOCKEY',
            'HOCKEY FIELD': 'HOCKEY FIELD',
            'FIELD HOCKEY': 'HOCKEY FIELD',
            'HOCKEY INDOOR': 'HOCKEY INDOOR',
            'INDOOR HOCKEY': 'HOCKEY INDOOR',
            'ICE HOCKEY': 'ICE HOCKEY',
            'ICE SKATING': 'ICE SKATING',
            'JET SKI': 'JET SKI',
            'JUDO': 'JUDO',
            'JU-JITSU': 'JU-JITSU',
            'KABADDI': 'KABADDI',
            'KARATE': 'KARATE',
            'KICKBOXING': 'KICKBOXING',
            'MODERN PENTATHLON': 'MODERN PENTATHLON',
            'MUAY THAI': 'MUAY THAI',
            'NETBALL': 'NETBALL',
            'OPEN WATER SWIMMING': 'OPEN WATER SWIMMING',
            'PARAGLIDING': 'PARAGLIDING',
            'PENCAK SILAT': 'PENCAK SILAT',
            'PETANQUE': 'PETANQUE',
            'POLO': 'POLO',
            'ROLLER SPORTS': 'ROLLER SPORTS',
            'ROWING': 'ROWING',
            'RUGBY': 'RUGBY',
            'SAILING': 'SAILING',
            'SEPAKTAKRAW': 'SEPAKTAKRAW',
            'SEPAK TAKRAW': 'SEPAKTAKRAW',
            'SHOOTING': 'SHOOTING',
            'SOFTBALL': 'SOFTBALL',
            'SPORT CLIMBING': 'SPORT CLIMBING',
            'SQUASH': 'SQUASH',
            'SWIMMING': 'SWIMMING',
            'AQUATICS SWIMMING': 'SWIMMING',
            'TABLE TENNIS': 'TABLE TENNIS',
            'TAEKWONDO': 'TAEKWONDO',
            'TENNIS': 'TENNIS',
            'TENNIS -': 'TENNIS',
            'TEQBALL': 'TEQBALL',
            'TUG OF WAR': 'TUG OF WAR',
            'VOLLEYBALL': 'VOLLEYBALL',
            'VOLLEYBALL BEACH': 'VOLLEYBALL BEACH',
            'BEACH VOLLEYBALL': 'VOLLEYBALL BEACH',
            'VOLLEYBALL INDOOR': 'VOLLEYBALL INDOOR',
            'INDOOR VOLLEYBALL': 'VOLLEYBALL INDOOR',
            'WATER POLO': 'WATER POLO',
            'AQUATICS WATERPOLO': 'WATER POLO',
            'WATERSKI & WAKEBOARD': 'WATERSKI & WAKEBOARD',
            'WEIGHTLIFTING': 'WEIGHTLIFTING',
            'WOODBALL': 'WOODBALL',
            'WRESTLING': 'WRESTLING',
            'ARCHERY': 'ARCHERY',
            'FLAG FOOTBALL': 'FLAG FOOTBALL',
            'LACROSSE': 'LACROSSE',
            'SURFING': 'SURFING',
            'WUSHU': 'WUSHU',
            'WUSHU -': 'WUSHU',
            'FINSWIMMING': 'FINSWIMMING',
            'XIANGQI': 'XIANGQI'
        }
        
        # Apply hardcoded mappings first
        for original, normalized in hardcoded_mappings.items():
            sport_map[original] = normalized
            
        # Handle any remaining sports with basic normalization
        for sport in unique_sports:
            if pd.isna(sport):
                continue
            sport_upper = sport.upper().strip()
            if sport_upper not in sport_map:
                sport_map[sport_upper] = sport_upper
                
        return sport_map
    
    def _build_round_map(self) -> Dict[str, str]:
        """Build round normalization mapping"""
        return {
            'Qualification': 'QUALIFICATION',
            'Final': 'FINALS',
            'Team Final': 'FINALS',
            'Round Robin': 'ROUND ROBIN',
            'Team Round Robin': 'ROUND ROBIN',
            '3rd/4th Placing Match': 'BRONZE MEDAL PLAYOFF',
            'Bronze Medal Playoff': 'BRONZE MEDAL PLAYOFF',
            'Semi Finals': 'SEMI FINALS',
            'Semi Final': 'SEMI FINALS',
            'Quarter Finals': 'QUARTER FINALS',
            'Quarter Final': 'QUARTER FINALS',
            'Preliminary Round': 'PRELIMINARY ROUND',
            'Preliminaries': 'PRELIMINARY ROUND',
            'Group Stage': 'GROUP STAGE',
            'Pool Stage': 'POOL STAGE',
            'Pool': 'POOL',
            'Heat': 'HEAT',
            'Heats': 'HEAT',
            'Grand Final': 'GRAND FINAL',
            'Round of 32': 'ROUND OF 32',
            'Round of 16': 'ROUND OF 16',
            'Table of 16': 'TABLE OF 16',
            'Elimination Round': 'ELIMINATION ROUND',
            'Upper Bracket': 'UPPER BRACKET',
            'Fleet Racing': 'FLEET RACING DAY',
            'Open Fleet Racing': 'FLEET RACING DAY',
            'Individual Final': 'FINALS',
            'Relay Final': 'FINALS',
            'Finals': 'FINALS',
            'Round': 'ROUND ROBIN',
            'Round One': 'ROUND ONE'
        }
    
    def _get_result_type(self, sport_norm: str, event_norm: str) -> str:
        """Get result type from sport_result_mapping"""
        # Try exact match first
        match = self.sport_result_mapping[
            (self.sport_result_mapping['sport'].str.upper() == sport_norm) & 
            (self.sport_result_mapping['value'].str.upper() == event_norm.upper())
        ]
        
        if not match.empty:
            return match.iloc[0]['resultType']
        
        # Try partial match on sport
        sport_matches = self.sport_result_mapping[
            self.sport_result_mapping['sport'].str.upper() == sport_norm
        ]
        
        if not sport_matches.empty:
            return sport_matches.iloc[0]['resultType']
        
        # Default fallback
        return 'score'
    
    def create_enhanced_templates_json(self):
        """Create enhanced JSON with mapping information"""
        templates_data = []
        
        for _, row in self.template_raw.iterrows():
            # Normalize sport
            sport_norm = self.sport_map.get(row['sport'], row['sport'])
            
            # Parse fields
            fields_str = row.get('fields', '[]')
            try:
                if pd.isna(fields_str):
                    fields = []
                elif isinstance(fields_str, str):
                    fields = ast.literal_eval(fields_str)
                else:
                    fields = []
            except:
                fields = []
            
            # Get result type
            event_name = row.get('event_name', '') or ''
            result_type = self._get_result_type(sport_norm, event_name)
            
            # Normalize round
            event_type = row.get('event_type', '') or ''
            round_norm = self.round_map.get(event_type, event_type)
            
            template_entry = {
                'id': f"TEMPLATE_{len(templates_data) + 1:03d}",
                'sport': row['sport'],
                'sport_normalized': sport_norm,
                'event_category': row.get('event_category', ''),
                'gender': row['gender'],
                'event_name': event_name,
                'event_type': event_type,
                'event_type_normalized': round_norm,
                'template': row['template'],
                'fields': fields,
                'sample_data': row.get('sample_data', ''),
                'result_type': result_type,
                'is_team': self._infer_team_flag(event_name, row['template'], fields),
                'competition_flow': self._get_competition_flow(sport_norm)
            }
            
            templates_data.append(template_entry)
        
        # Create organized structure
        organized_data = {
            'templates': templates_data,
            'sports_list': sorted(list(set([t['sport_normalized'] for t in templates_data]))),
            'sport_mappings': {k: v for k, v in self.sport_map.items()},
            'round_mappings': self.round_map,
            'competition_flows': self._generate_competition_flows(),
            'metadata': {
                'total_templates': len(templates_data),
                'total_sports': len(set([t['sport_normalized'] for t in templates_data])),
                'generated_at': pd.Timestamp.now().isoformat()
            }
        }
        
        return organized_data
    
    def _infer_team_flag(self, event_name: str, template_text: str, fields: List[str]) -> bool:
        """Infer if this is a team event"""
        if pd.isna(event_name):
            event_name = ""
        if pd.isna(template_text):
            template_text = ""
            
        team_indicators = [
            'TEAM', 'RELAY', 'DOUBLES', 'PAIRS', 'CREW', 'TOURNAMENT',
            'TEAM_MEMBERS', 'PLAYER_NAMES', 'REGU', 'DUILIAN'
        ]
        
        text_to_check = f"{event_name} {template_text} {' '.join(fields) if fields else ''}".upper()
        
        for indicator in team_indicators:
            if indicator in text_to_check:
                return True
                
        return False
    
    def _get_competition_flow(self, sport_norm: str) -> List[str]:
        """Get typical competition flow for a sport"""
        flows = {
            'SWIMMING': ['HEAT', 'FINALS'],
            'ATHLETICS': ['HEAT', 'FINALS'],
            'DIVING': ['FINALS'],
            'BASKETBALL': ['PRELIMINARY ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'FOOTBALL': ['GROUP STAGE', 'QUARTER FINALS', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'VOLLEYBALL': ['GROUP STAGE', 'QUARTER FINALS', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'WATER POLO': ['ROUND ROBIN', 'FINALS'],
            'BADMINTON': ['ROUND OF 32', 'ROUND OF 16', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'TABLE TENNIS': ['PRELIMINARY ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'TENNIS': ['ROUND ONE', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'BOXING': ['ELIMINATION ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'JUDO': ['ELIMINATION ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'WRESTLING': ['ROUND ROBIN', 'FINALS'],
            'SAILING': ['FLEET RACING DAY'],
            'TRADITIONAL BOAT RACE': ['HEAT', 'SEMI FINALS', 'GRAND FINAL'],
            'SEPAKTAKRAW': ['ROUND ROBIN', 'SEMI FINALS', 'FINALS'],
            'FENCING': ['POOL', 'TABLE OF 16', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS']
        }
        return flows.get(sport_norm, ['PRELIMINARY ROUND', 'FINALS'])
    
    def _generate_competition_flows(self) -> Dict[str, List[str]]:
        """Generate all competition flows"""
        return {
            'SWIMMING': ['HEAT', 'FINALS'],
            'ATHLETICS': ['HEAT', 'FINALS'],
            'DIVING': ['FINALS'],
            'BASKETBALL': ['PRELIMINARY ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'FOOTBALL': ['GROUP STAGE', 'QUARTER FINALS', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'VOLLEYBALL': ['GROUP STAGE', 'QUARTER FINALS', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'VOLLEYBALL BEACH': ['PRELIMINARY ROUND', 'ROUND OF 12', 'SEMI FINALS', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'VOLLEYBALL INDOOR': ['GROUP STAGE', '5TH TO 8TH PLACING PLAYOFFS', 'FINALS'],
            'WATER POLO': ['ROUND ROBIN', 'FINALS'],
            'BADMINTON': ['ROUND OF 32', 'ROUND OF 16', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'TABLE TENNIS': ['PRELIMINARY ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'TENNIS': ['ROUND ONE', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'BOXING': ['ELIMINATION ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'JUDO': ['ELIMINATION ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'WRESTLING': ['ROUND ROBIN', 'FINALS'],
            'SAILING': ['FLEET RACING DAY'],
            'TRADITIONAL BOAT RACE': ['HEAT', 'SEMI FINALS', 'GRAND FINAL'],
            'SEPAKTAKRAW': ['ROUND ROBIN', 'SEMI FINALS', 'FINALS'],
            'FENCING': ['POOL', 'TABLE OF 16', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'GOLF': ['ROUND', 'FINALS'],
            'CYCLING': ['FINALS'],
            'ESPORTS': ['GROUP STAGE', 'UPPER BRACKET', 'SEMI FINALS', 'FINALS'],
            'CUESPORTS': ['PRELIMINARY ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'FLOORBALL': ['GROUP STAGE', '3RD PLACING MATCH', 'FINALS'],
            'HOCKEY FIELD': ['POOL STAGE', 'FINALS'],
            'HOCKEY INDOOR': ['GROUP STAGE', 'FINALS'],
            'CRICKET': ['ROUND ROBIN', 'BRONZE MEDAL PLAYOFF', 'FINALS'],
            'TRIATHLON': ['INDIVIDUAL FINAL', 'RELAY FINAL'],
            'WUSHU': ['FINALS'],
            'TAEKWONDO': ['ELIMINATION ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'KICKBOXING': ['PRELIMINARY ROUND', 'QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'PENCAK SILAT': ['QUARTER FINALS', 'SEMI FINALS', 'FINALS'],
            'PETANQUE': ['ROUND ROBIN', 'SEMI FINALS', 'FINALS'],
            'TEQBALL': ['GROUP STAGE', 'SEMI FINALS', 'FINALS'],
            'XIANGQI': ['ROUND'],
            'FINSWIMMING': ['HEAT', 'FINALS'],
            'JU-JITSU': ['ROUND ROBIN', 'FINALS']
        }

def main():
    generator = TemplateJSONGenerator('data/all_sports.xlsx')
    
    # Generate enhanced JSON
    organized_data = generator.create_enhanced_templates_json()
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save comprehensive JSON
    with open('data/sports_templates.json', 'w', encoding='utf-8') as f:
        json.dump(organized_data, f, indent=2, ensure_ascii=False)
    
    # Save simplified templates for the web interface
    with open('data/templates.json', 'w', encoding='utf-8') as f:
        json.dump(organized_data['templates'], f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated enhanced JSON with {len(organized_data['templates'])} templates")
    print(f"✅ Mapped {len(organized_data['sports_list'])} unique sports")
    print(f"✅ Created competition flows for {len(organized_data['competition_flows'])} sports")
    
    return organized_data

if __name__ == "__main__":
    main()
