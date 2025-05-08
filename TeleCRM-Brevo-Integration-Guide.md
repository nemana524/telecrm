# TeleCRM to Brevo Integration Guide

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Webhook Setup](#webhook-setup)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [FAQs](#faqs)

## Overview

This integration allows you to sync lead data from TeleCRM to Brevo (formerly Sendinblue) for email marketing purposes. Key features include:

- Lead synchronization from TeleCRM segments to Brevo contacts
- Real-time updates via webhooks
- Custom field mapping
- Automatic list creation in Brevo
- Email campaign support

## Prerequisites

Before beginning the integration, ensure you have:

1. **TeleCRM Account**
   - Admin access to create API keys
   - Access to segments and lead data

2. **Brevo Account**
   - API access enabled
   - Permission to create contacts and lists

3. **Technical Requirements**
   - Python 3.8 or higher
   - Ability to run a Python web server (locally or on a server)
   - Basic understanding of API concepts

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-organization/telecrm-brevo-integration.git
   cd telecrm-brevo-integration
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Obtain API Keys**

   **TeleCRM API Key:**
   - Log in to your TeleCRM account
   - Navigate to Settings > API & Webhooks
   - Create a new API key with appropriate permissions
   - Note down the API key and URL

   **Brevo API Key:**
   - Log in to your Brevo account
   - Go to API Keys & Management > API Keys
   - Create a new API key with permissions for contacts and email campaigns
   - Note down the API key

2. **Configure Environment Variables**

   Create a `.env` file in the project root by copying the provided template:
   ```bash
   cp env.example .env
   ```

   Edit the `.env` file with your actual API keys:
   ```
   TELECRM_API_KEY=your_telecrm_api_key
   TELECRM_API_URL=https://app.telecrm.in/api/v1
   BREVO_API_KEY=your_brevo_api_key
   ```

## Usage

### Starting the Server

1. **Run the Flask Application**
   ```bash
   python app.py
   ```

   This will start a local server at `http://127.0.0.1:5000`

2. **For Production Deployment**
   
   For production environments, consider using Gunicorn:
   ```bash
   gunicorn app:app
   ```

   Or a service like Heroku, AWS, or similar cloud platforms.

### Manually Triggering a Sync

1. **Sync a Segment**

   To manually sync a segment from TeleCRM to Brevo, make a POST request to the `/sync` endpoint:

   ```bash
   curl -X POST http://127.0.0.1:5000/sync \
     -H "Content-Type: application/json" \
     -d '{"segment_id": "your_telecrm_segment_id"}'
   ```

   Or use a tool like Postman with the following configuration:
   - Method: POST
   - URL: http://127.0.0.1:5000/sync
   - Headers: Content-Type: application/json
   - Body (raw JSON):
     ```json
     {
       "segment_id": "your_telecrm_segment_id",
       "filter_criteria": {
         "status": "active",
         "created_after": "2023-01-01"
       }
     }
     ```

2. **Response Example**

   Successful response:
   ```json
   {
     "status": "success",
     "message": "Sync completed: 42 leads synced, 0 failed, 3 skipped",
     "total_leads": 45,
     "successful_syncs": 42,
     "failed_syncs": 0,
     "skipped_syncs": 3,
     "list_id": 123,
     "list_name": "My TeleCRM Segment - 1688997654"
   }
   ```

## Webhook Setup

Webhooks allow for real-time updates when leads are created or updated in TeleCRM.

1. **Configure TeleCRM Webhook**

   - Log in to TeleCRM
   - Go to Settings > API & Webhooks
   - Create a new webhook
   - Set the webhook URL to your integration endpoint: `https://your-server.com/webhooks/telecrm`
   - Select events: Lead Created, Lead Updated
   - Save the webhook configuration

2. **Testing the Webhook**

   After configuration, create or update a lead in TeleCRM to test the webhook. Check your integration logs to verify the webhook was received.

   Sample webhook payload from TeleCRM:
   ```json
   {
     "event": "lead_created",
     "lead_id": "12345",
     "timestamp": "2023-07-15T14:30:45Z"
   }
   ```

## Testing

### Test Connection to TeleCRM and Brevo

Use the provided test script to verify your API connections:

```bash
python test_integration.py
```

### Test Lead Syncing with a Specific Segment

```bash
python test_integration.py your_segment_id
```

## Troubleshooting

### Common Issues

1. **API Connection Failures**
   
   - Verify API keys are correct in your `.env` file
   - Check if TeleCRM or Brevo services are experiencing outages
   - Ensure your server has internet access

2. **Missing Leads**

   - Check if leads in the segment have valid email addresses (required for Brevo)
   - Verify filter criteria isn't excluding leads
   - Check TeleCRM API response for errors

3. **Webhook Not Working**

   - Verify the webhook URL is accessible from TeleCRM servers
   - Check server logs for incoming webhook requests
   - Ensure your server's firewall allows incoming connections

4. **Email Delivery Issues**

   - Check Brevo's sending logs for errors
   - Verify test email addresses are valid
   - Check if emails are being marked as spam

### Logging

The integration logs information to help with troubleshooting:

- Check the console output when running the application
- For production, configure proper logging to a file

## FAQs

**Q: Are there any costs associated with this integration?**  
A: The integration software itself is free, but you need active subscriptions to both TeleCRM and Brevo. Brevo may charge based on the number of contacts or emails sent, depending on your plan.

**Q: Can I customize the contact fields mapping?**  
A: Yes, you can modify the mapping in `services/lead_sync.py` in the `map_telecrm_lead_to_brevo_contact` function.

**Q: Does this integration support two-way sync?**  
A: No, this integration is one-way from TeleCRM to Brevo. It does not sync data back from Brevo to TeleCRM.

**Q: What happens if a lead doesn't have an email address?**  
A: Leads without email addresses will be skipped during sync, as Brevo requires an email address for each contact.

**Q: Is there a limit to how many leads can be synced?**  
A: The integration handles pagination to sync large segments, but be aware of Brevo's API rate limits and your plan's contact limits.

**Q: Do I need an MT license for this integration?**  
A: "MT" typically refers to Brevo's Marketing Automation features. The base integration works with standard Brevo plans, but some advanced features may require higher-tier plans.

**Q: How often should I sync my leads?**  
A: With the webhook configuration, leads will sync in real-time when created or updated. Manual syncs can be run as needed for initial data loading or verification.

**Q: Can I use this integration in demo mode?**  
A: Yes, the integration supports a demo mode for testing without real API keys. See the README.md for details. 