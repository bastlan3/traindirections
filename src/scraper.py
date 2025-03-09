"""
European Train Routes Scraper

This module scrapes train routes information from various European railway websites.
"""
import json
import logging
import os
import time
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
CACHE_FILE = os.path.join(DATA_DIR, 'railway_cache.json')
ROUTES_FILE = os.path.join(DATA_DIR, 'train_routes.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class RailwayDataScraper:
    """Scraper for collecting European railway routes data."""
    
    def __init__(self, use_cache: bool = True):
        """
        Initialize the railway data scraper.
        
        Args:
            use_cache: Whether to use cached data if available
        """
        self.use_cache = use_cache
        self.cache = self._load_cache() if use_cache else {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def _load_cache(self) -> Dict:
        """Load cached data if it exists."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Cache file corrupted, creating new cache")
                return {}
        return {}
    
    def _save_cache(self):
        """Save current cache to file."""
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f)
    
    def get_page(self, url: str) -> str:
        """
        Get page content with caching.
        
        Args:
            url: URL to fetch
            
        Returns:
            Page HTML content
        """
        if self.use_cache and url in self.cache:
            return self.cache[url]
        
        logger.info(f"Fetching {url}")
        response = self.session.get(url)
        response.raise_for_status()
        
        # Add delay to be respectful to servers
        time.sleep(2)
        
        if self.use_cache:
            self.cache[url] = response.text
            self._save_cache()
        
        return response.text
    
    def scrape_dbahn(self) -> List[Dict]:
        """
        Scrape German railway (Deutsche Bahn) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        # In a real implementation, we would parse actual DB website
        # For demonstration, we're generating sample data
        
        logger.info("Scraping German railway routes")
        
        main_stations = [
            {"name": "Berlin Hauptbahnhof", "latitude": 52.5250, "longitude": 13.3690},
            {"name": "München Hauptbahnhof", "latitude": 48.1402, "longitude": 11.5600},
            {"name": "Frankfurt Hauptbahnhof", "latitude": 50.1071, "longitude": 8.6636},
            {"name": "Hamburg Hauptbahnhof", "latitude": 53.5533, "longitude": 10.0064},
            {"name": "Köln Hauptbahnhof", "latitude": 50.9432, "longitude": 6.9587},
            # Adding more German stations
            {"name": "Stuttgart Hauptbahnhof", "latitude": 48.7841, "longitude": 9.1817},
            {"name": "Düsseldorf Hauptbahnhof", "latitude": 51.2198, "longitude": 6.7942},
            {"name": "Dresden Hauptbahnhof", "latitude": 51.0404, "longitude": 13.7315},
            {"name": "Hannover Hauptbahnhof", "latitude": 52.3772, "longitude": 9.7420},
            {"name": "Leipzig Hauptbahnhof", "latitude": 51.3455, "longitude": 12.3819},
            {"name": "Nürnberg Hauptbahnhof", "latitude": 49.4450, "longitude": 11.0825}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    # Add direct routes
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "Deutsche Bahn",
                        "country": "Germany",
                        "route_type": "direct"
                    })
        
        return routes
    
    def scrape_sncf(self) -> List[Dict]:
        """
        Scrape French railway (SNCF) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        # In a real implementation, we would parse actual SNCF website
        
        logger.info("Scraping French railway routes")
        
        main_stations = [
            {"name": "Paris Gare du Nord", "latitude": 48.8809, "longitude": 2.3553},
            {"name": "Lyon Part-Dieu", "latitude": 45.7601, "longitude": 4.8591},
            {"name": "Marseille Saint-Charles", "latitude": 43.3036, "longitude": 5.3831},
            {"name": "Bordeaux Saint-Jean", "latitude": 44.8263, "longitude": -0.5553},
            {"name": "Lille Europe", "latitude": 50.6392, "longitude": 3.0728},
            # Adding more French stations
            {"name": "Paris Gare de Lyon", "latitude": 48.8449, "longitude": 2.3743},
            {"name": "Nice Ville", "latitude": 43.7049, "longitude": 7.2619},
            {"name": "Strasbourg Gare Centrale", "latitude": 48.5855, "longitude": 7.7348},
            {"name": "Nantes", "latitude": 47.2173, "longitude": -1.5419},
            {"name": "Toulouse Matabiau", "latitude": 43.6112, "longitude": 1.4567},
            {"name": "Rennes", "latitude": 48.1043, "longitude": -1.6726},
            {"name": "Montpellier Saint-Roch", "latitude": 43.6034, "longitude": 3.8798}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "SNCF",
                        "country": "France",
                        "route_type": "direct"
                    })
        
        return routes
    
    def scrape_trenitalia(self) -> List[Dict]:
        """
        Scrape Italian railway (Trenitalia) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        
        logger.info("Scraping Italian railway routes")
        
        main_stations = [
            {"name": "Roma Termini", "latitude": 41.9010, "longitude": 12.5011},
            {"name": "Milano Centrale", "latitude": 45.4862, "longitude": 9.2050},
            {"name": "Firenze Santa Maria Novella", "latitude": 43.7764, "longitude": 11.2481},
            {"name": "Venezia Santa Lucia", "latitude": 45.4416, "longitude": 12.3254},
            {"name": "Napoli Centrale", "latitude": 40.8518, "longitude": 14.2720},
            # Adding more Italian stations
            {"name": "Torino Porta Nuova", "latitude": 45.0601, "longitude": 7.6764},
            {"name": "Bologna Centrale", "latitude": 44.5075, "longitude": 11.3514},
            {"name": "Genova Piazza Principe", "latitude": 44.4185, "longitude": 8.9221},
            {"name": "Verona Porta Nuova", "latitude": 45.4287, "longitude": 10.9819},
            {"name": "Bari Centrale", "latitude": 41.1175, "longitude": 16.8716},
            {"name": "Palermo Centrale", "latitude": 38.1056, "longitude": 13.3623}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "Trenitalia",
                        "country": "Italy",
                        "route_type": "direct"
                    })
        
        return routes
    
    def scrape_renfe(self) -> List[Dict]:
        """
        Scrape Spanish railway (Renfe) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        
        logger.info("Scraping Spanish railway routes")
        
        main_stations = [
            {"name": "Madrid Atocha", "latitude": 40.4065, "longitude": -3.6891},
            {"name": "Barcelona Sants", "latitude": 41.3793, "longitude": 2.1400},
            {"name": "Valencia Joaquín Sorolla", "latitude": 39.4668, "longitude": -0.3764},
            {"name": "Sevilla Santa Justa", "latitude": 37.3917, "longitude": -5.9756},
            {"name": "Málaga María Zambrano", "latitude": 36.7124, "longitude": -4.4291},
            {"name": "Zaragoza Delicias", "latitude": 41.6585, "longitude": -0.9127},
            {"name": "Alicante Terminal", "latitude": 38.3440, "longitude": -0.4930},
            {"name": "Bilbao Abando", "latitude": 43.2613, "longitude": -2.9243},
            {"name": "Santiago de Compostela", "latitude": 42.8763, "longitude": -8.5452},
            {"name": "Granada", "latitude": 37.1712, "longitude": -3.6125}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "Renfe",
                        "country": "Spain",
                        "route_type": "direct"
                    })
        
        return routes
    
    def scrape_sbb(self) -> List[Dict]:
        """
        Scrape Swiss railway (SBB) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        
        logger.info("Scraping Swiss railway routes")
        
        main_stations = [
            {"name": "Zürich Hauptbahnhof", "latitude": 47.3783, "longitude": 8.5403},
            {"name": "Bern", "latitude": 46.9490, "longitude": 7.4397},
            {"name": "Basel SBB", "latitude": 47.5476, "longitude": 7.5905},
            {"name": "Genève Cornavin", "latitude": 46.2100, "longitude": 6.1418},
            {"name": "Lausanne", "latitude": 46.5168, "longitude": 6.6290},
            {"name": "Luzern", "latitude": 47.0504, "longitude": 8.3093},
            {"name": "Winterthur", "latitude": 47.5007, "longitude": 8.7242},
            {"name": "Lugano", "latitude": 46.0050, "longitude": 8.9471},
            {"name": "St. Gallen", "latitude": 47.4237, "longitude": 9.3718},
            {"name": "Interlaken", "latitude": 46.6863, "longitude": 7.8632}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "SBB",
                        "country": "Switzerland",
                        "route_type": "direct"
                    })
        
        return routes
    
    def scrape_obb(self) -> List[Dict]:
        """
        Scrape Austrian railway (ÖBB) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        
        logger.info("Scraping Austrian railway routes")
        
        main_stations = [
            {"name": "Wien Hauptbahnhof", "latitude": 48.1855, "longitude": 16.3798},
            {"name": "Salzburg Hauptbahnhof", "latitude": 47.8126, "longitude": 13.0465},
            {"name": "Graz Hauptbahnhof", "latitude": 47.0728, "longitude": 15.4160},
            {"name": "Innsbruck Hauptbahnhof", "latitude": 47.2632, "longitude": 11.4011},
            {"name": "Linz Hauptbahnhof", "latitude": 48.2914, "longitude": 14.2919},
            {"name": "Klagenfurt Hauptbahnhof", "latitude": 46.6168, "longitude": 14.3104},
            {"name": "Bregenz", "latitude": 47.5031, "longitude": 9.7471},
            {"name": "St. Pölten Hauptbahnhof", "latitude": 48.2048, "longitude": 15.6230}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "ÖBB",
                        "country": "Austria",
                        "route_type": "direct"
                    })
        
        return routes
    
    def scrape_ns(self) -> List[Dict]:
        """
        Scrape Dutch railway (NS) routes.
        
        Returns:
            List of route dictionaries
        """
        # This is a placeholder implementation
        
        logger.info("Scraping Dutch railway routes")
        
        main_stations = [
            {"name": "Amsterdam Centraal", "latitude": 52.3789, "longitude": 4.9003},
            {"name": "Utrecht Centraal", "latitude": 52.0894, "longitude": 5.1100},
            {"name": "Rotterdam Centraal", "latitude": 51.9245, "longitude": 4.4699},
            {"name": "Den Haag Centraal", "latitude": 52.0809, "longitude": 4.3241},
            {"name": "Eindhoven Centraal", "latitude": 51.4433, "longitude": 5.4812},
            {"name": "Groningen", "latitude": 53.2114, "longitude": 6.5654},
            {"name": "Maastricht", "latitude": 50.8493, "longitude": 5.7056},
            {"name": "Arnhem Centraal", "latitude": 51.9850, "longitude": 5.9010},
            {"name": "Leeuwarden", "latitude": 53.1962, "longitude": 5.7867},
            {"name": "Zwolle", "latitude": 52.5047, "longitude": 6.0914}
        ]
        
        routes = []
        
        # Generate connections between these stations
        for i, origin in enumerate(main_stations):
            for j, destination in enumerate(main_stations):
                if i != j:  # Don't connect a station to itself
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "NS",
                        "country": "Netherlands",
                        "route_type": "direct"
                    })
        
        return routes
    
    def combine_international_routes(self) -> List[Dict]:
        """
        Create international connections between major cities.
        
        Returns:
            List of international route dictionaries
        """
        logger.info("Creating international railway connections")
        
        international_hubs = [
            {"name": "Paris Gare du Nord", "latitude": 48.8809, "longitude": 2.3553, "country": "France"},
            {"name": "Brussels Midi", "latitude": 50.8357, "longitude": 4.3356, "country": "Belgium"},
            {"name": "Amsterdam Centraal", "latitude": 52.3789, "longitude": 4.9003, "country": "Netherlands"},
            {"name": "London St Pancras", "latitude": 51.5322, "longitude": -0.1271, "country": "United Kingdom"},
            {"name": "Frankfurt Hauptbahnhof", "latitude": 50.1071, "longitude": 8.6636, "country": "Germany"},
            {"name": "Zürich Hauptbahnhof", "latitude": 47.3783, "longitude": 8.5403, "country": "Switzerland"},
            {"name": "Wien Hauptbahnhof", "latitude": 48.1855, "longitude": 16.3798, "country": "Austria"},
            {"name": "Milano Centrale", "latitude": 45.4862, "longitude": 9.2050, "country": "Italy"},
            {"name": "Barcelona Sants", "latitude": 41.3793, "longitude": 2.1400, "country": "Spain"},
            {"name": "Copenhagen Central", "latitude": 55.6726, "longitude": 12.5645, "country": "Denmark"},
            {"name": "Prague Main Station", "latitude": 50.0831, "longitude": 14.4353, "country": "Czech Republic"},
            {"name": "Budapest Keleti", "latitude": 47.5006, "longitude": 19.0840, "country": "Hungary"},
            {"name": "Stockholm Central", "latitude": 59.3307, "longitude": 18.0580, "country": "Sweden"}
        ]
        
        routes = []
        
        # Generate connections between international hubs
        for i, origin in enumerate(international_hubs):
            for j, destination in enumerate(international_hubs):
                if i != j and ((i + j) % 2 != 0):  # Create a more connected network than before
                    routes.append({
                        "origin": origin["name"],
                        "origin_lat": origin["latitude"],
                        "origin_lon": origin["longitude"],
                        "destination": destination["name"],
                        "destination_lat": destination["latitude"],
                        "destination_lon": destination["longitude"],
                        "operator": "International",
                        "country": f"{origin['country']}-{destination['country']}",
                        "route_type": "direct"
                    })
        
        return routes
    
    def generate_multi_stop_routes(self, all_routes: List[Dict], num_stops: int = 1) -> List[Dict]:
        """
        Generate routes with multiple stops using existing direct routes.
        
        Args:
            all_routes: List of all direct routes
            num_stops: Number of intermediate stops to include
        
        Returns:
            List of multi-stop routes
        """
        logger.info(f"Generating routes with {num_stops} intermediate stop(s)")
        
        # Create a lookup dictionary of direct routes for faster searching
        direct_routes_lookup = {}
        for route in all_routes:
            if route.get("route_type") == "direct":
                origin = route["origin"]
                if origin not in direct_routes_lookup:
                    direct_routes_lookup[origin] = []
                direct_routes_lookup[origin].append(route)
        
        multi_stop_routes = []
        
        # For simplicity, we'll just generate routes with 1 intermediate stop
        if num_stops == 1:
            for origin_station, origin_routes in direct_routes_lookup.items():
                for first_leg in origin_routes:
                    intermediate_stop = first_leg["destination"]
                    
                    # Find routes that start from this intermediate stop
                    if intermediate_stop in direct_routes_lookup:
                        for second_leg in direct_routes_lookup[intermediate_stop]:
                            final_destination = second_leg["destination"]
                            
                            # Avoid routes that circle back to the origin
                            if final_destination != origin_station:
                                # Create a new multi-stop route
                                multi_stop_route = {
                                    "origin": origin_station,
                                    "origin_lat": first_leg["origin_lat"],
                                    "origin_lon": first_leg["origin_lon"],
                                    "destination": final_destination,
                                    "destination_lat": second_leg["destination_lat"],
                                    "destination_lon": second_leg["destination_lon"],
                                    "stops": [
                                        {
                                            "name": intermediate_stop,
                                            "lat": first_leg["destination_lat"],
                                            "lon": first_leg["destination_lon"],
                                        }
                                    ],
                                    "operator": f"{first_leg['operator']}-{second_leg['operator']}",
                                    "country": f"{first_leg['country']}-{second_leg['country']}",
                                    "route_type": "multi-stop"
                                }
                                
                                multi_stop_routes.append(multi_stop_route)
        
        # For multi-hop routes (more than 1 intermediate stop)
        elif num_stops > 1:
            # Build on the 1-stop routes and add more stops
            one_stop_routes = self.generate_multi_stop_routes(all_routes, num_stops=1)
            
            # Use recursive approach for simplicity with limited number of stops
            for route in one_stop_routes:
                final_stop = route["destination"]
                
                if final_stop in direct_routes_lookup:
                    for next_leg in direct_routes_lookup[final_stop]:
                        next_destination = next_leg["destination"]
                        
                        # Avoid loops in the route
                        if next_destination != route["origin"] and next_destination not in [stop["name"] for stop in route["stops"]]:
                            # Create a new multi-stop route with additional stop
                            new_multi_stop_route = route.copy()
                            new_multi_stop_route["destination"] = next_destination
                            new_multi_stop_route["destination_lat"] = next_leg["destination_lat"]
                            new_multi_stop_route["destination_lon"] = next_leg["destination_lon"]
                            new_multi_stop_route["stops"] = route["stops"] + [
                                {
                                    "name": final_stop,
                                    "lat": route["destination_lat"],
                                    "lon": route["destination_lon"],
                                }
                            ]
                            new_multi_stop_route["operator"] = f"{route['operator']}-{next_leg['operator']}"
                            new_multi_stop_route["country"] = f"{route['country']}-{next_leg['country']}"
                            
                            multi_stop_routes.append(new_multi_stop_route)
        
        logger.info(f"Generated {len(multi_stop_routes)} multi-stop routes")
        return multi_stop_routes
    
    def scrape_all(self) -> List[Dict]:
        """
        Scrape train routes from all supported railway operators.
        
        Returns:
            Combined list of all train routes
        """
        routes = []
        
        # Scrape each railway operator
        routes.extend(self.scrape_dbahn())
        routes.extend(self.scrape_sncf())
        routes.extend(self.scrape_trenitalia())
        routes.extend(self.scrape_renfe())
        routes.extend(self.scrape_sbb())
        routes.extend(self.scrape_obb())
        routes.extend(self.scrape_ns())
        routes.extend(self.combine_international_routes())
        
        logger.info(f"Scraped {len(routes)} direct train routes")
        
        # Add route_type to international routes if missing
        for route in routes:
            if "route_type" not in route:
                route["route_type"] = "direct"
        
        # Generate multi-stop routes with 1 intermediate stop
        one_stop_routes = self.generate_multi_stop_routes(routes, num_stops=1)
        routes.extend(one_stop_routes)
        
        # Generate multi-stop routes with 2 intermediate stops
        # Limiting to a small subset to avoid too many routes
        if one_stop_routes:
            two_stop_routes = self.generate_multi_stop_routes(
                routes, 
                num_stops=2
            )
            routes.extend(two_stop_routes[:min(500, len(two_stop_routes))])  # Limit to 500 routes to avoid overwhelming
        
        # Save all routes to a file
        with open(ROUTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(routes, f, indent=2)
        
        # Calculate the number of direct and multi-stop routes
        direct_routes = [r for r in routes if r.get("route_type") == "direct"]
        one_stop_count = len(one_stop_routes)
        two_stop_count = min(500, len(two_stop_routes)) if 'two_stop_routes' in locals() else 0
        
        logger.info(f"Scraped a total of {len(routes)} train routes")
        logger.info(f"  - Direct routes: {len(direct_routes)}")
        logger.info(f"  - 1-stop routes: {one_stop_count}")
        logger.info(f"  - 2-stop routes: {two_stop_count}")
        
        return routes


def main():
    """Main function to run the scraper."""
    scraper = RailwayDataScraper(use_cache=True)
    routes = scraper.scrape_all()
    
    # Print summary
    df = pd.DataFrame(routes)
    print(f"Total routes: {len(routes)}")
    print(f"Routes by operator:\n{df['operator'].value_counts()}")
    print(f"Routes by country:\n{df['country'].value_counts()}")
    
    print(f"Routes saved to {ROUTES_FILE}")


if __name__ == "__main__":
    main()