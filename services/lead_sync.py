import logging
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class LeadSyncService:
    """
    Service for syncing leads from TeleCRM to Brevo
    """
    
    def __init__(self, telecrm_client, brevo_client):
        self.telecrm_client = telecrm_client
        self.brevo_client = brevo_client
    
    def map_telecrm_lead_to_brevo_contact(self, lead: Dict) -> Dict:
        """
        Map TeleCRM lead data to Brevo contact data format
        """
        # Extract basic contact information
        name = lead.get('name', '')
        first_name = ''
        last_name = ''
        
        # Split name into first and last name if available
        if name:
            name_parts = name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Map TeleCRM lead attributes to Brevo contact attributes
        attributes = {
            "FIRSTNAME": first_name,
            "LASTNAME": last_name,
            "COMPANY": lead.get('company', ''),
            "PHONE": lead.get('phone', ''),
            "ADDRESS": lead.get('address', ''),
            "CITY": lead.get('city', ''),
            "COUNTRY": lead.get('country', ''),
            "LEAD_SOURCE": lead.get('source', ''),
            "LEAD_STATUS": lead.get('status', ''),
            "LEAD_ID": lead.get('id', '')
        }
        
        # Add any custom fields that might be present
        custom_fields = lead.get('custom_fields', {})
        for field_name, value in custom_fields.items():
            # Convert field name to uppercase for Brevo compatibility
            brevo_field_name = field_name.upper().replace(' ', '_')
            attributes[brevo_field_name] = value
        
        return {
            "email": lead.get('email', ''),
            "attributes": attributes
        }
    
    def sync_lead_to_brevo(self, lead_id: str, list_ids: Optional[List[int]] = None) -> Dict:
        """
        Sync a single lead from TeleCRM to Brevo
        """
        try:
            # Get lead details from TeleCRM
            lead = self.telecrm_client.get_lead_by_id(lead_id)
            
            if not lead:
                return {"status": "error", "message": f"Lead with ID {lead_id} not found in TeleCRM"}
            
            # Skip leads without email
            if not lead.get('email'):
                return {"status": "error", "message": f"Lead with ID {lead_id} does not have an email address"}
            
            # Map lead data to Brevo contact format
            contact_data = self.map_telecrm_lead_to_brevo_contact(lead)
            
            # Create or update contact in Brevo
            result = self.brevo_client.create_or_update_contact(
                email=contact_data["email"],
                attributes=contact_data["attributes"],
                list_ids=list_ids
            )
            
            return {
                "status": result.get("status"),
                "message": result.get("message"),
                "lead_id": lead_id,
                "email": contact_data["email"]
            }
            
        except Exception as e:
            logger.error(f"Error syncing lead {lead_id} to Brevo: {str(e)}")
            return {"status": "error", "message": str(e), "lead_id": lead_id}
    
    def sync_leads_to_brevo(self, segment_id: str, filter_criteria: Optional[Dict] = None, 
                           create_list: bool = True, list_name: Optional[str] = None) -> Dict:
        """
        Sync leads from a TeleCRM segment to Brevo
        """
        try:
            # Get all leads from the specified segment
            leads = self.telecrm_client.get_all_leads_by_segment(segment_id, filter_criteria)
            
            if not leads:
                return {"status": "warning", "message": "No leads found in the specified segment"}
            
            # Create a new list in Brevo if requested
            brevo_list_id = None
            if create_list:
                # Use segment name as list name or use provided list name
                segment_info = self.telecrm_client.get_segment_by_id(segment_id)
                segment_name = segment_info.get('name', 'TeleCRM Segment')
                
                list_name = list_name or f"{segment_name} - {int(time.time())}"
                
                list_result = self.brevo_client.create_contacts_list(name=list_name)
                
                if list_result.get('status') == 'success':
                    brevo_list_id = list_result.get('list_id')
            
            # Process each lead
            successful_syncs = 0
            failed_syncs = 0
            skipped_syncs = 0
            contact_emails = []
            
            for lead in leads:
                if not lead.get('email'):
                    skipped_syncs += 1
                    continue
                
                # Map and sync the lead to Brevo
                contact_data = self.map_telecrm_lead_to_brevo_contact(lead)
                
                result = self.brevo_client.create_or_update_contact(
                    email=contact_data["email"],
                    attributes=contact_data["attributes"]
                )
                
                if result.get('status') == 'success':
                    successful_syncs += 1
                    contact_emails.append(contact_data["email"])
                else:
                    failed_syncs += 1
            
            # Add contacts to list if a list was created
            if brevo_list_id and contact_emails:
                self.brevo_client.add_contacts_to_list(brevo_list_id, contact_emails)
            
            return {
                "status": "success",
                "message": f"Sync completed: {successful_syncs} leads synced, {failed_syncs} failed, {skipped_syncs} skipped",
                "total_leads": len(leads),
                "successful_syncs": successful_syncs,
                "failed_syncs": failed_syncs,
                "skipped_syncs": skipped_syncs,
                "list_id": brevo_list_id,
                "list_name": list_name
            }
            
        except Exception as e:
            logger.error(f"Error syncing leads to Brevo: {str(e)}")
            return {"status": "error", "message": str(e)} 