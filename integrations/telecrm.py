import requests
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class TeleCRMClient:
    """
    Client for interacting with TeleCRM API
    """
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Helper method to make requests to TeleCRM API
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when calling TeleCRM API: {e}")
            if response.text:
                logger.error(f"Response content: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling TeleCRM API: {e}")
            raise
    
    def get_leads(self, filter_criteria: Optional[Dict] = None, page: int = 1, per_page: int = 100) -> Dict:
        """
        Get leads from TeleCRM with optional filtering
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        # Add filter criteria to params if provided
        if filter_criteria:
            for key, value in filter_criteria.items():
                params[key] = value
        
        return self._make_request("GET", "/leads", params=params)
    
    def get_lead_by_id(self, lead_id: str) -> Dict:
        """
        Get a specific lead by ID
        """
        return self._make_request("GET", f"/leads/{lead_id}")
    
    def get_leads_by_segment(self, segment_id: str, page: int = 1, per_page: int = 100) -> Dict:
        """
        Get leads that belong to a specific segment
        """
        params = {
            "segment_id": segment_id,
            "page": page,
            "per_page": per_page
        }
        
        return self._make_request("GET", "/leads", params=params)
    
    def get_all_segments(self) -> List[Dict]:
        """
        Get all segments defined in TeleCRM
        """
        return self._make_request("GET", "/segments")
    
    def get_segment_by_id(self, segment_id: str) -> Dict:
        """
        Get a specific segment by ID
        """
        return self._make_request("GET", f"/segments/{segment_id}")
    
    def get_all_leads_by_segment(self, segment_id: str, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Get all leads in a segment with pagination handling
        """
        all_leads = []
        page = 1
        per_page = 100
        
        while True:
            response = self.get_leads_by_segment(segment_id, page, per_page)
            leads = response.get("data", [])
            
            if not leads:
                break
                
            all_leads.extend(leads)
            
            # Check if we've reached the last page
            if len(leads) < per_page:
                break
                
            page += 1
            
        return all_leads 