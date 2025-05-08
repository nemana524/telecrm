import logging
from integrations.telecrm import TeleCRMClient
from integrations.brevo import BrevoClient
from services.lead_sync import LeadSyncService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_telecrm_client():
    # Initialize TeleCRM client with demo key
    telecrm_client = TeleCRMClient(
        api_key="demo_telecrm_api_key_12345",
        api_url="https://app.telecrm.in/api/v1"
    )
    
    # Test getting leads
    leads = telecrm_client.get_leads()
    print("\n=== TeleCRM Leads ===")
    print(f"Total leads: {len(leads.get('data', []))}")
    for lead in leads.get('data', []):
        print(f"Lead: {lead.get('name')} - {lead.get('email')}")
    
    # Test getting segments
    segments = telecrm_client.get_all_segments()
    print("\n=== TeleCRM Segments ===")
    for segment in segments:
        print(f"Segment: {segment.get('name')} (ID: {segment.get('id')})")
        
    # Test getting a specific lead
    lead_id = "lead1"
    lead = telecrm_client.get_lead_by_id(lead_id)
    print("\n=== TeleCRM Lead Details ===")
    print(f"Lead: {lead.get('name')} - {lead.get('email')}")
    
    return telecrm_client

def test_brevo_client():
    # Initialize Brevo client with demo key
    brevo_client = BrevoClient(
        api_key="demo_brevo_api_key_12345"
    )
    
    # Test getting all lists
    lists = brevo_client.get_all_lists()
    print("\n=== Brevo Lists ===")
    for lst in lists.get('lists', []):
        print(f"List: {lst.get('name')} (ID: {lst.get('id')}) - {lst.get('total_subscribers')} subscribers")
    
    # Test creating a contact
    contact_result = brevo_client.create_or_update_contact(
        email="test@example.com",
        attributes={
            "FIRSTNAME": "Test",
            "LASTNAME": "User",
            "COMPANY": "Test Company"
        }
    )
    print("\n=== Brevo Create Contact ===")
    print(f"Result: {contact_result.get('status')} - {contact_result.get('message')}")
    
    # Test creating a list
    list_result = brevo_client.create_contacts_list(name="Test List")
    print("\n=== Brevo Create List ===")
    print(f"Result: {list_result.get('status')} - {list_result.get('message')} (ID: {list_result.get('list_id')})")
    
    return brevo_client

def test_lead_sync():
    telecrm_client = TeleCRMClient(
        api_key="demo_telecrm_api_key_12345",
        api_url="https://app.telecrm.in/api/v1"
    )
    
    brevo_client = BrevoClient(
        api_key="demo_brevo_api_key_12345"
    )
    
    # Initialize lead sync service
    lead_sync_service = LeadSyncService(telecrm_client, brevo_client)
    
    # Test syncing leads from segment
    segment_id = "segment1"
    result = lead_sync_service.sync_leads_to_brevo(segment_id)
    
    print("\n=== Lead Sync Result ===")
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    print(f"Total leads: {result.get('total_leads')}")
    print(f"Successful syncs: {result.get('successful_syncs')}")
    print(f"Failed syncs: {result.get('failed_syncs')}")
    print(f"Skipped syncs: {result.get('skipped_syncs')}")
    print(f"List ID: {result.get('list_id')}")
    print(f"List name: {result.get('list_name')}")

if __name__ == "__main__":
    print("===== Testing TeleCRM Client with Demo Key =====")
    telecrm_client = test_telecrm_client()
    
    print("\n===== Testing Brevo Client with Demo Key =====")
    brevo_client = test_brevo_client()
    
    print("\n===== Testing Lead Sync Service with Demo Keys =====")
    test_lead_sync()
    
    print("\n===== All Tests Completed =====")
    print("Your demo integration is working properly!") 