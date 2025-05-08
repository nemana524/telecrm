from flask import Flask, request, jsonify
from flask_cors import CORS
import os
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

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Use demo API keys
telecrm_api_key = 'demo_telecrm_api_key_12345'
telecrm_api_url = 'https://app.telecrm.in/api/v1'
brevo_api_key = 'demo_brevo_api_key_12345'

logger.info(f"Using TeleCRM API key: {telecrm_api_key[:5]}...")
logger.info(f"Using TeleCRM API URL: {telecrm_api_url}")
logger.info(f"Using Brevo API key: {brevo_api_key[:5]}...")

# Initialize clients
telecrm_client = TeleCRMClient(
    api_key=telecrm_api_key,
    api_url=telecrm_api_url
)
brevo_client = BrevoClient(
    api_key=brevo_api_key
)

# Initialize services
lead_sync_service = LeadSyncService(telecrm_client, brevo_client)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "TeleCRM-Brevo Integration API is running",
        "demo_mode": "demo" in telecrm_api_key.lower()
    })

@app.route('/sync', methods=['POST'])
def sync_leads():
    """
    Endpoint to manually trigger lead sync from TeleCRM to Brevo
    """
    try:
        segment_id = request.json.get('segment_id')
        filter_criteria = request.json.get('filter_criteria', {})
        
        if not segment_id:
            return jsonify({
                "status": "error",
                "message": "segment_id is required"
            }), 400
            
        result = lead_sync_service.sync_leads_to_brevo(segment_id, filter_criteria)
        return jsonify({
            "status": "success",
            "message": "Lead sync triggered successfully",
            "data": result
        })
    except Exception as e:
        logger.error(f"Error during sync: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to sync leads: {str(e)}"
        }), 500

@app.route('/webhooks/telecrm', methods=['POST'])
def telecrm_webhook():
    """
    Webhook to receive updates from TeleCRM
    """
    try:
        webhook_data = request.json
        event_type = webhook_data.get('event')
        
        if event_type == 'lead_created' or event_type == 'lead_updated':
            lead_id = webhook_data.get('lead_id')
            lead_sync_service.sync_lead_to_brevo(lead_id)
            return jsonify({"status": "success", "message": f"Lead {lead_id} synced to Brevo"})
        
        return jsonify({"status": "success", "message": "Webhook received but no action taken"})
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to process webhook: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Use 127.0.0.1 instead of 0.0.0.0 to avoid socket issues on Windows
    app.run(host='127.0.0.1', port=5000, debug=True) 