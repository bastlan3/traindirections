# European Train Routes Explorer

A web application that visualizes train routes across Europe, allowing users to explore possible train connections from any major European city.

## Project Overview

This project consists of two main parts:
1. **Data Scraper**: Python scripts to collect train route data from various European railway operators.
2. **Web Interface**: An interactive web map showing train connections between cities.

The web interface is designed to be hosted on GitHub Pages, making it accessible to anyone interested in exploring European train routes.

## Features

- 🚄 View regular train routes between European cities
- 🔍 Search for specific cities/stations
- 🗺️ Interactive map visualization using Leaflet.js
- 📊 See all possible connections from a selected city
- 🌐 Works on desktop and mobile devices

## Project Structure

```
euro-train-routes/
├── data/                # Stores scraped and processed data
├── src/                 # Python source code for data collection
│   ├── __init__.py      
│   ├── scraper.py       # Train routes scraper
│   └── data_processor.py # Data processing for the web interface
└── web/                 # Web interface files (for GitHub Pages)
    ├── index.html       # Main HTML page
    ├── style.css        # CSS styles
    └── script.js        # JavaScript for the interactive map
```

## Installation and Setup

### Prerequisites

- Python 3.8+ 
- Git
- Web browser

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/euro-train-routes.git
cd euro-train-routes
```

2. **Create and activate a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the required Python packages**

```bash
pip install -r requirements.txt
```

## Data Collection

To collect train route data, run the scraper:

```bash
cd src
python -m scraper
```

The scraper currently includes placeholder data for:
- Deutsche Bahn (Germany)
- SNCF (France)
- Trenitalia (Italy)
- International routes

After scraping, process the data for the web interface:

```bash
python -m data_processor
```

This will create a `web_data.json` file in the `data/` directory which is used by the web interface.

## Running the Web Interface Locally

To test the web interface locally:

```bash
cd web
# Start a simple Python HTTP server
python -m http.server 8000
```

Then open your browser and navigate to `http://localhost:8000`.

## Deploying to GitHub Pages

1. Create a GitHub repository for your project
2. Push your code to GitHub:

```bash
git remote set-url origin https://github.com/yourusername/euro-train-routes.git
git push -u origin main
```

3. Configure GitHub Pages:
   - Go to your repository on GitHub
   - Navigate to Settings > Pages
   - Select the branch you want to deploy (usually `main`)
   - Set the folder to `/docs` or `/web`
   - Save the settings

4. Your site will be published at `https://yourusername.github.io/euro-train-routes/`

## Extending the Project

### Adding More Railway Operators

To add data from additional railway operators, extend the `RailwayDataScraper` class in `scraper.py` with new methods following the pattern of existing ones.

### Improving the Web Interface

The web interface can be enhanced with:
- Route filtering by operator or country
- Journey planning functionality
- Travel time information
- Platform information
- Transfer suggestions

## License

[MIT License](LICENSE)

## Acknowledgments

- [Leaflet.js](https://leafletjs.com/) for the interactive mapping functionality
- [OpenStreetMap](https://www.openstreetmap.org/) for the map tiles# traindirections
