# TeleCRM to Brevo Integration

This project implements an integration between TeleCRM and Brevo mail system to allow for seamless lead data synchronization and email campaign management.

## Features

- Extract leads from TeleCRM segments
- Sync lead data to Brevo contacts
- Create and manage contact lists in Brevo
- Create email campaigns in Brevo targeting TeleCRM leads
- Webhook support for real-time updates
- Flexible filtering and segmentation options
- **Demo mode** for testing without real API keys

## Requirements

- Python 3.8 or higher
- Flask
- TeleCRM API access
- Brevo API access

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd telecrm-brevo-integration
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file based on the provided `env.example`:
```
cp env.example .env
```

4. Fill in your API keys in the `.env` file:
```
# For real API keys:
TELECRM_API_KEY=your_telecrm_api_key
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=your_brevo_api_key

# OR for demo mode:
TELECRM_API_KEY=demo_telecrm_api_key_12345
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=demo_brevo_api_key_12345
```

## Usage

### Demo Mode

This integration supports a demo mode that allows you to test the application without real API keys. To use demo mode:

1. Configure your `.env` file with demo keys (containing the word "demo"):
```
TELECRM_API_KEY=demo_telecrm_api_key_12345
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=demo_brevo_api_key_12345
```

2. Run the test script to verify demo functionality:
```
python test_demo.py
```

3. Start the application normally - it will automatically detect demo keys and use mock data.

For detailed documentation on demo mode, see [Demo Mode Documentation](docs/DEMO_MODE.md).

### Starting the Server

Run the Flask application:
```
python app.py
```

Or use Gunicorn for production:
```
gunicorn app:app
```

### API Endpoints

#### Sync Leads

```
POST /sync
```

Request body:
```json
{
  "segment_id": "your_telecrm_segment_id",
  "filter_criteria": {
    "status": "active",
    "created_after": "2023-01-01"
  }
}
```

#### Webhook Endpoint

Configure your TeleCRM webhook to point to:
```
POST /webhooks/telecrm
```

## Configuring TeleCRM

1. Log in to your TeleCRM account
2. Go to Settings > API & Webhooks
3. Create a new API key
4. Set up a webhook to notify this integration about lead changes

## Configuring Brevo

1. Log in to your Brevo account
2. Go to API Keys & Management > API Keys
3. Create a new API key with appropriate permissions
4. Use this key in your `.env` file

## Transitioning from Demo to Real Keys

When you're ready to use real API keys:

1. Update your `.env` file with actual API keys from TeleCRM and Brevo
2. Restart your application
3. Test basic operations to verify connectivity
4. Monitor logs for any API-related errors

See the [Demo Mode Documentation](docs/DEMO_MODE.md) for detailed instructions.

## Additional Integration Options

The integration can be further customized by modifying the mapping function in `services/lead_sync.py` to match your specific TeleCRM field structure and Brevo requirements.

## Troubleshooting

- Check the application logs for detailed error messages
- Ensure your API keys have the necessary permissions
- Verify that your TeleCRM segments contain valid lead data
- Check that the leads have valid email addresses for Brevo integration

## License

[MIT License](LICENSE) 