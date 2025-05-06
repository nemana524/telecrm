#!/usr/bin/env python
"""
Test script for TeleCRM to Brevo integration
"""
import os
import sys
import logging
import json
from dotenv import load_dotenv
from integrations.telecrm import TeleCRMClient
from integrations.brevo import BrevoClient
from services.lead_sync import LeadSyncService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_telecrm_connection(client):
    """Test the connection to TeleCRM API"""
    try:
        segments = client.get_all_segments()
        logger.info(f"Connected to TeleCRM API: Found {len(segments)} segments")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to TeleCRM API: {str(e)}")
        return False

def test_brevo_connection(client):
    """Test the connection to Brevo API"""
    try:
        lists = client.get_all_lists()
        list_count = len(lists.get('lists', []))
        logger.info(f"Connected to Brevo API: Found {list_count} lists")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Brevo API: {str(e)}")
        return False

def main():
    """Main test function"""
    load_dotenv()
    
    # Check if required environment variables are set
    missing_vars = []
    for var in ['TELECRM_API_KEY', 'TELECRM_API_URL', 'BREVO_API_KEY']:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file or environment.")
        sys.exit(1)
    
    # Initialize clients
    telecrm_client = TeleCRMClient(
        api_key=os.getenv('TELECRM_API_KEY'),
        api_url=os.getenv('TELECRM_API_URL')
    )
    
    brevo_client = BrevoClient(
        api_key=os.getenv('BREVO_API_KEY')
    )
    
    # Test connections
    telecrm_ok = test_telecrm_connection(telecrm_client)
    brevo_ok = test_brevo_connection(brevo_client)
    
    if not telecrm_ok or not brevo_ok:
        logger.error("Connection tests failed. Please check your API credentials.")
        sys.exit(1)
    
    # If a segment ID is provided as an argument, test syncing that segment
    if len(sys.argv) > 1:
        segment_id = sys.argv[1]
        logger.info(f"Testing sync with segment ID: {segment_id}")
        
        # Initialize sync service
        sync_service = LeadSyncService(telecrm_client, brevo_client)
        
        # Sync leads from segment to Brevo
        result = sync_service.sync_leads_to_brevo(
            segment_id=segment_id,
            create_list=True,
            list_name=f"Test Integration - Segment {segment_id}"
        )
        
        # Print result
        logger.info(f"Sync result: {json.dumps(result, indent=2)}")
    else:
        logger.info("All connection tests passed!")
        logger.info("To test lead syncing, provide a segment ID as a command line argument.")
        logger.info("Example: python test_integration.py YOUR_SEGMENT_ID")

if __name__ == "__main__":
    main() 