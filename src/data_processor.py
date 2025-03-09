"""
European Train Routes Data Processor

This module processes raw train route data and prepares it for web visualization.
"""
import json
import os
import logging
from collections import defaultdict
from typing import Dict, List, Set, Tuple

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
ROUTES_FILE = os.path.join(DATA_DIR, 'train_routes.json')
WEB_DATA_FILE = os.path.join(DATA_DIR, 'web_data.json')


class TrainDataProcessor:
    """Process raw train route data for web visualization."""
    
    def __init__(self, input_file: str = ROUTES_FILE):
        """
        Initialize the train data processor.
        
        Args:
            input_file: Path to the input JSON file with train route data
        """
        self.input_file = input_file
        self.routes_data = self._load_data()
        
    def _load_data(self) -> List[Dict]:
        """Load train route data from JSON file."""
        if not os.path.exists(self.input_file):
            logger.warning(f"Input file {self.input_file} not found.")
            return []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_stations(self) -> List[Dict]:
        """
        Extract unique stations from routes data.
        
        Returns:
            List of unique station dictionaries with name, lat, lon
        """
        stations_dict = {}
        
        for route in self.routes_data:
            # Process origin station
            origin_key = route["origin"]
            if origin_key not in stations_dict:
                stations_dict[origin_key] = {
                    "name": route["origin"],
                    "latitude": route["origin_lat"],
                    "longitude": route["origin_lon"]
                }
            
            # Process destination station
            dest_key = route["destination"]
            if dest_key not in stations_dict:
                stations_dict[dest_key] = {
                    "name": route["destination"],
                    "latitude": route["destination_lat"],
                    "longitude": route["destination_lon"]
                }
        
        # Convert to list
        stations = list(stations_dict.values())
        logger.info(f"Extracted {len(stations)} unique stations")
        return stations
    
    def build_connections(self) -> Dict:
        """
        Build a connections dictionary for each station.
        
        Returns:
            Dictionary with station names as keys and lists of connected stations as values
        """
        connections = defaultdict(list)
        
        for route in self.routes_data:
            origin = route["origin"]
            destination = route["destination"]
            
            # Add connection to the origin station's list
            connections[origin].append({
                "name": destination,
                "latitude": route["destination_lat"],
                "longitude": route["destination_lon"],
                "operator": route["operator"],
                "country": route["country"]
            })
        
        logger.info(f"Built connections for {len(connections)} stations")
        return dict(connections)
    
    def process_data(self) -> Dict:
        """
        Process train route data for web visualization.
        
        Returns:
            Dictionary with processed data for web visualization
        """
        stations = self.extract_stations()
        connections = self.build_connections()
        
        processed_data = {
            "stations": stations,
            "connections": connections
        }
        
        # Save processed data to file for web use
        with open(WEB_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f)
        
        logger.info(f"Processed data saved to {WEB_DATA_FILE}")
        return processed_data
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics about the train route data.
        
        Returns:
            Dictionary with statistics
        """
        df = pd.DataFrame(self.routes_data)
        
        # Count routes by operator
        operator_counts = df['operator'].value_counts().to_dict()
        
        # Count routes by country
        country_counts = df['country'].value_counts().to_dict()
        
        # Find stations with most connections
        origin_counts = df['origin'].value_counts()
        top_origins = origin_counts.head(10).to_dict()
        
        # Calculate total number of unique stations
        unique_origins = set(df['origin'])
        unique_destinations = set(df['destination'])
        unique_stations = unique_origins.union(unique_destinations)
        
        stats = {
            "total_routes": len(df),
            "unique_stations": len(unique_stations),
            "operators": operator_counts,
            "countries": country_counts,
            "top_connected_stations": top_origins
        }
        
        return stats


def main():
    """Main function to process the data."""
    processor = TrainDataProcessor()
    processor.process_data()
    
    # Print statistics
    stats = processor.get_statistics()
    print(f"Total routes: {stats['total_routes']}")
    print(f"Unique stations: {stats['unique_stations']}")
    print(f"Top connected stations:")
    for station, count in stats['top_connected_stations'].items():
        print(f"  {station}: {count} connections")


if __name__ == "__main__":
    main()