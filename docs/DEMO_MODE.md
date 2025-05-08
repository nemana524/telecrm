# Demo Mode Documentation

## Overview

The TeleCRM-Brevo Integration provides a demo mode that allows you to test and develop with the integration without requiring real API keys. This feature is useful for:

- Development and testing
- Demonstrations to stakeholders
- Training new team members
- Verifying functionality before deploying with real credentials

## How Demo Mode Works

The integration automatically detects when you're using demo API keys by checking if the string "demo" is present in your API key value. When detected, the system uses mock data and simulated responses instead of making real API calls to TeleCRM or Brevo.

## Using Demo Mode

### Setting Up Demo Keys

To use the demo mode, configure your environment with API keys that contain the word "demo":

```
TELECRM_API_KEY=demo_telecrm_api_key_12345
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=demo_brevo_api_key_12345
```

You can set these values:
1. In a `.env` file in your project root
2. As environment variables
3. Directly in your application code (for testing purposes only)

### Demo Data

When running in demo mode, the integration provides the following mock data:

#### TeleCRM Demo Data
- Two sample leads (John Doe and Jane Smith)
- Two segments (New Leads and Qualified Leads)
- Lead details including name, email, phone, etc.

#### Brevo Demo Data
- Two sample contact lists
- Mock contact creation/update functionality
- Mock list creation and contact addition

### Running the Demo

To verify the demo functionality is working properly, run the test script:

```
python test_demo.py
```

This will execute various operations using the demo clients and display the results.

## Features Available in Demo Mode

All major features of the integration are available in demo mode:

- **Lead Management**: View, create and update leads (simulated)
- **Segment Management**: View and access segments of leads
- **Contact Synchronization**: Sync leads from TeleCRM to Brevo
- **List Management**: Create and manage contact lists in Brevo
- **API Operations**: All API operations return realistic mock responses

## Transitioning to Real API Keys

When you're ready to transition from demo mode to using real API keys, follow these steps:

1. **Obtain Real API Keys**:
   - Get your TeleCRM API key from your TeleCRM account settings
   - Get your Brevo API key from your Brevo account settings

2. **Update Your Configuration**:
   - Replace the demo keys with real keys in your `.env` file or environment variables:
     ```
     TELECRM_API_KEY=your_actual_telecrm_api_key
     TELECRM_API_URL=https://app.telecrm.in/api/v1
     BREVO_API_KEY=your_actual_brevo_api_key
     ```

3. **Testing the Transition**:
   - Start with small operations to verify connectivity
   - Check that you can retrieve data from both services
   - Verify that lead syncing works correctly

4. **Monitoring**:
   - Monitor your application logs for any API errors
   - Check that rate limits are not being exceeded
   - Verify data is syncing correctly between systems

## API Rate Limits and Considerations

When moving from demo mode to real API keys, be aware of:

- **Rate Limits**: Both TeleCRM and Brevo impose rate limits on API calls
- **Data Validation**: Real APIs may have stricter validation than demo mode
- **Error Handling**: Real APIs may return different error responses

## Troubleshooting

If you encounter issues when transitioning from demo to real keys:

1. **Check Connectivity**: Ensure your application can reach the API endpoints
2. **Verify Credentials**: Double-check that your API keys are correct and active
3. **Inspect Logs**: Review application logs for detailed error messages
4. **API Documentation**: Consult the official TeleCRM and Brevo API documentation

## Best Practices

- Use demo mode for development and testing
- Never commit real API keys to version control
- Always use environment variables or secret management for real API keys
- Test thoroughly when transitioning from demo to real mode

## Support

If you need additional assistance with the demo mode or transitioning to real API keys, please contact our support team at cecezinemana524@gmail.com. 