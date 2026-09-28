"""lecture 7-10: USGS Seismic API Client (განახლებული ფართო ძებნით)."""
import requests
from typing import List, Dict, Any

class SeismicAPIError(Exception):
    """USGS API-სთან დაკავშირებული შეცდომა."""

class SeismicClient:
    BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def get_recent_events(self, start_date: str, end_date: str, min_magnitude: float = 0.0) -> List[Dict[str, Any]]:
        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": min_magnitude,
            # მოვხსნათ მკაცრი გეოგრაფიული შეზღუდვა, რომ მსოფლიო მასშტაბით წამოიღოს მონაცემები ტესტირებისთვის
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            events = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                geom = feature.get("geometry", {})
                coords = geom.get("coordinates", [0.0, 0.0, 0.0])
                
                events.append({
                    "event_id": feature.get("id"),
                    "magnitude": props.get("mag", 0.0),
                    "place": props.get("place", "Unknown"),
                    "latitude": coords[1],
                    "longitude": coords[0],
                    "depth_km": coords[2],
                })
            return events
        except requests.RequestException as exc:
            raise SeismicAPIError(f"USGS API მოთხოვნა ჩავარდა: {exc}") from exc
