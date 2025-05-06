from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from integrations.telecrm import TeleCRMClient
from integrations.brevo import BrevoClient
from services.lead_sync import LeadSyncService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize clients
telecrm_client = TeleCRMClient(
    api_key=os.getenv('TELECRM_API_KEY'),
    api_url=os.getenv('TELECRM_API_URL')
)
brevo_client = BrevoClient(
    api_key=os.getenv('BREVO_API_KEY')
)

# Initialize services
lead_sync_service = LeadSyncService(telecrm_client, brevo_client)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "TeleCRM-Brevo Integration API is running"
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
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False) 