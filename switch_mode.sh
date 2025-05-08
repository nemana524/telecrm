#!/bin/bash
# Script to switch between demo mode and real mode

function print_usage {
    echo "Usage: ./switch_mode.sh [demo|real]"
    echo ""
    echo "  demo    Switch to demo mode using mock API keys"
    echo "  real    Switch to real mode using your actual API keys"
    echo ""
}

function switch_to_demo {
    echo "Switching to DEMO mode..."
    
    # Create a backup of the current .env file if it exists
    if [ -f .env ]; then
        cp .env .env.backup
        echo "Backed up existing .env to .env.backup"
    fi
    
    # Create a new .env file with demo keys
    cat > .env << EOL
TELECRM_API_KEY=demo_telecrm_api_key_12345
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=demo_brevo_api_key_12345
FLASK_APP=app.py
FLASK_ENV=development
EOL
    
    echo "Created new .env file with demo keys"
    echo "Demo mode activated. Run 'python test_demo.py' to verify functionality."
}

function switch_to_real {
    echo "Switching to REAL mode..."
    
    # Check if .env.real exists (user-created file with real keys)
    if [ -f .env.real ]; then
        cp .env.real .env
        echo "Copied .env.real to .env"
    else
        # Prompt user to enter real API keys
        echo "Please enter your real API keys:"
        read -p "TeleCRM API Key: " telecrm_key
        read -p "Brevo API Key: " brevo_key
        
        # Create a new .env file with real keys
        cat > .env << EOL
TELECRM_API_KEY=$telecrm_key
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=$brevo_key
FLASK_APP=app.py
FLASK_ENV=development
EOL
        
        # Save a copy for future use
        cp .env .env.real
        echo "Created .env.real with your API keys for future use"
    fi
    
    echo "Real mode activated. API calls will now use real credentials."
}

# Main script logic
if [ "$1" = "demo" ]; then
    switch_to_demo
elif [ "$1" = "real" ]; then
    switch_to_real
else
    print_usage
fi 