"""
Example script demonstrating how to use the TeleCRM-Brevo integration programmatically
with both demo and real API keys.
"""

import os
import logging
from integrations.telecrm import TeleCRMClient
from integrations.brevo import BrevoClient
from services.lead_sync import LeadSyncService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_with_demo_keys():
    """
    Set up the integration with demo API keys
    """
    logger.info("Setting up integration with DEMO keys")
    
    # Initialize clients with demo keys
    telecrm_client = TeleCRMClient(
        api_key="demo_telecrm_api_key_12345",
        api_url="https://app.telecrm.in/api/v1"
    )
    
    brevo_client = BrevoClient(
        api_key="demo_brevo_api_key_12345"
    )
    
    # Create lead sync service
    lead_sync_service = LeadSyncService(telecrm_client, brevo_client)
    
    return telecrm_client, brevo_client, lead_sync_service

def setup_with_real_keys():
    """
    Set up the integration with real API keys from environment variables
    """
    logger.info("Setting up integration with REAL keys from environment variables")
    
    # Get API keys from environment variables
    telecrm_api_key = os.getenv('TELECRM_API_KEY')
    telecrm_api_url = os.getenv('TELECRM_API_URL', 'https://app.telecrm.in/api/v1')
    brevo_api_key = os.getenv('BREVO_API_KEY')
    
    # Validate API keys
    if not telecrm_api_key or not brevo_api_key:
        raise ValueError("API keys not found in environment variables. "
                         "Please set TELECRM_API_KEY and BREVO_API_KEY.")
    
    # Initialize clients with real keys
    telecrm_client = TeleCRMClient(
        api_key=telecrm_api_key,
        api_url=telecrm_api_url
    )
    
    brevo_client = BrevoClient(
        api_key=brevo_api_key
    )
    
    # Create lead sync service
    lead_sync_service = LeadSyncService(telecrm_client, brevo_client)
    
    return telecrm_client, brevo_client, lead_sync_service

def run_demo_example():
    """
    Example using demo keys
    """
    telecrm_client, brevo_client, lead_sync_service = setup_with_demo_keys()
    
    # Demonstrate TeleCRM functionality
    logger.info("Fetching leads from TeleCRM (demo)")
    leads = telecrm_client.get_leads()
    logger.info(f"Found {len(leads.get('data', []))} leads")
    
    # Demonstrate Brevo functionality
    logger.info("Creating contact in Brevo (demo)")
    result = brevo_client.create_or_update_contact(
        email="test@example.com",
        attributes={
            "FIRSTNAME": "Test",
            "LASTNAME": "User",
            "COMPANY": "Test Company"
        }
    )
    logger.info(f"Contact creation result: {result.get('status')} - {result.get('message')}")
    
    # Demonstrate lead sync
    logger.info("Syncing leads from segment to Brevo (demo)")
    sync_result = lead_sync_service.sync_leads_to_brevo("segment1")
    logger.info(f"Sync result: {sync_result.get('status')} - {sync_result.get('message')}")
    logger.info(f"Synced {sync_result.get('successful_syncs')} leads successfully")

def run_real_example():
    """
    Example using real keys (from environment variables)
    """
    try:
        telecrm_client, brevo_client, lead_sync_service = setup_with_real_keys()
        
        # Demonstrate TeleCRM functionality
        logger.info("Fetching segments from TeleCRM (real)")
        segments = telecrm_client.get_all_segments()
        logger.info(f"Found {len(segments)} segments")
        
        if segments:
            # Use the first segment for demonstration
            segment_id = segments[0].get('id')
            
            # Demonstrate lead sync with the first segment
            logger.info(f"Syncing leads from segment {segment_id} to Brevo (real)")
            sync_result = lead_sync_service.sync_leads_to_brevo(segment_id)
            logger.info(f"Sync result: {sync_result.get('status')} - {sync_result.get('message')}")
            logger.info(f"Synced {sync_result.get('successful_syncs')} leads successfully")
        else:
            logger.warning("No segments found to sync")
            
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Error in real example: {str(e)}")

if __name__ == "__main__":
    # Check if we should run with real or demo keys
    use_real_keys = os.getenv('USE_REAL_KEYS', '').lower() == 'true'
    
    if use_real_keys:
        logger.info("Running example with REAL API keys")
        run_real_example()
    else:
        logger.info("Running example with DEMO API keys")
        run_demo_example()
        
    logger.info("Example completed") 