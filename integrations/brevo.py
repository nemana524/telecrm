import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class BrevoClient:
    """
    Client for interacting with Brevo API
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Check if we're using a demo key
        self.is_demo = "demo" in api_key.lower()
        
        if not self.is_demo:
            self.configure_api()
        
    def configure_api(self):
        """
        Configure the Brevo API client
        """
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = self.api_key
        self.api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
        self.list_api_instance = sib_api_v3_sdk.ListsApi(sib_api_v3_sdk.ApiClient(configuration))
        self.email_api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
        
    def create_or_update_contact(self, email: str, attributes: Dict, list_ids: Optional[List[int]] = None) -> Dict:
        """
        Create or update a contact in Brevo
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info(f"DEMO MODE: Creating/updating contact with email {email}")
            return {"status": "success", "message": "Contact created or updated successfully in demo mode"}
            
        try:
            create_contact = sib_api_v3_sdk.CreateContact(
                email=email,
                attributes=attributes,
                list_ids=list_ids
            )
            
            result = self.api_instance.create_contact(create_contact)
            return {"status": "success", "message": "Contact created or updated successfully"}
        except ApiException as e:
            logger.error(f"Exception when calling ContactsApi->create_contact: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_contacts_list(self, name: str, folder_id: Optional[int] = None) -> Dict:
        """
        Create a new contacts list in Brevo
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info(f"DEMO MODE: Creating contact list with name {name}")
            # Generate a fake ID between 1-100
            import random
            list_id = random.randint(1, 100)
            return {"status": "success", "list_id": list_id, "message": "List created successfully in demo mode"}
            
        try:
            create_list = sib_api_v3_sdk.CreateList(
                name=name,
                folder_id=folder_id
            )
            
            result = self.list_api_instance.create_list(create_list)
            return {"status": "success", "list_id": result.id, "message": "List created successfully"}
        except ApiException as e:
            logger.error(f"Exception when calling ListsApi->create_list: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_all_lists(self) -> Dict:
        """
        Get all contact lists from Brevo
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info("DEMO MODE: Getting all contact lists")
            return {
                "status": "success", 
                "lists": [
                    {"id": 1, "name": "Demo List 1", "total_subscribers": 42},
                    {"id": 2, "name": "Demo List 2", "total_subscribers": 18}
                ]
            }
            
        try:
            result = self.list_api_instance.get_lists(limit=50)
            return {"status": "success", "lists": result.lists}
        except ApiException as e:
            logger.error(f"Exception when calling ListsApi->get_lists: {e}")
            return {"status": "error", "message": str(e)}
    
    def add_contacts_to_list(self, list_id: int, contact_emails: List[str]) -> Dict:
        """
        Add multiple contacts to a list in Brevo
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info(f"DEMO MODE: Adding {len(contact_emails)} contacts to list {list_id}")
            return {"status": "success", "message": f"Added {len(contact_emails)} contacts to list {list_id} in demo mode"}
            
        try:
            add_contacts_to_list = sib_api_v3_sdk.AddContactToList(
                emails=contact_emails
            )
            
            result = self.list_api_instance.add_contacts_to_list(list_id, add_contacts_to_list)
            return {"status": "success", "message": "Contacts added to list successfully"}
        except ApiException as e:
            logger.error(f"Exception when calling ListsApi->add_contacts_to_list: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_email_campaign(self, name: str, subject: str, sender: Dict, 
                             content: Dict, recipients: Dict) -> Dict:
        """
        Create an email campaign in Brevo
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info(f"DEMO MODE: Creating email campaign with name {name}")
            # Generate a fake campaign ID
            import random
            campaign_id = random.randint(1000, 9999)
            return {
                "status": "success", 
                "campaign_id": campaign_id,
                "message": "Email campaign created successfully in demo mode"
            }
            
        try:
            email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(
                name=name,
                subject=subject,
                sender=sender,
                html_content=content.get("html"),
                recipients=recipients
            )
            
            result = self.email_api_instance.create_email_campaign(email_campaigns)
            return {
                "status": "success", 
                "campaign_id": result.id,
                "message": "Email campaign created successfully"
            }
        except ApiException as e:
            logger.error(f"Exception when calling EmailCampaignsApi->create_email_campaign: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_contact(self, email: str) -> Dict:
        """
        Get contact information by email
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info(f"DEMO MODE: Getting contact info for {email}")
            # Generate fake contact data
            return {
                "status": "success", 
                "contact": {
                    "email": email,
                    "id": hash(email) % 10000,  # Generate a stable fake ID
                    "attributes": {
                        "FIRSTNAME": "Demo",
                        "LASTNAME": "User",
                        "SMS": None,
                        "COMPANY": "Demo Company"
                    },
                    "listIds": [1, 2],
                    "createdAt": "2023-01-01T00:00:00Z",
                    "modifiedAt": "2023-06-15T00:00:00Z"
                }
            }
            
        try:
            result = self.api_instance.get_contact_info(email)
            return {"status": "success", "contact": result}
        except ApiException as e:
            logger.error(f"Exception when calling ContactsApi->get_contact_info: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_webhook(self, url: str, events: List[str], description: str) -> Dict:
        """
        Create a webhook in Brevo to receive real-time updates
        """
        # Return mock response for demo mode
        if self.is_demo:
            logger.info(f"DEMO MODE: Creating webhook with URL {url}")
            # Generate a fake webhook ID
            import random
            webhook_id = random.randint(1, 100)
            return {"status": "success", "webhook_id": webhook_id, "message": "Webhook created successfully in demo mode"}
            
        try:
            # Initialize the WebhooksApi instance
            webhook_api = sib_api_v3_sdk.WebhooksApi(sib_api_v3_sdk.ApiClient(sib_api_v3_sdk.Configuration()))
            webhook_api.api_client.configuration.api_key['api-key'] = self.api_key
            
            create_webhook = sib_api_v3_sdk.CreateWebhook(
                url=url,
                description=description,
                events=events,
                type="marketing"
            )
            
            result = webhook_api.create_webhook(create_webhook)
            return {"status": "success", "webhook_id": result.id, "message": "Webhook created successfully"}
        except ApiException as e:
            logger.error(f"Exception when calling WebhooksApi->create_webhook: {e}")
            return {"status": "error", "message": str(e)} 