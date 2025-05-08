# PowerShell script to switch between demo mode and real mode

function Print-Usage {
    Write-Host "Usage: .\switch_mode.ps1 [demo|real]"
    Write-Host ""
    Write-Host "  demo    Switch to demo mode using mock API keys"
    Write-Host "  real    Switch to real mode using your actual API keys"
    Write-Host ""
}

function Switch-ToDemo {
    Write-Host "Switching to DEMO mode..."
    
    # Create a backup of the current .env file if it exists
    if (Test-Path .env) {
        Copy-Item .env .env.backup
        Write-Host "Backed up existing .env to .env.backup"
    }
    
    # Create a new .env file with demo keys
    @"
TELECRM_API_KEY=demo_telecrm_api_key_12345
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=demo_brevo_api_key_12345
FLASK_APP=app.py
FLASK_ENV=development
"@ | Out-File -FilePath .env -Encoding ascii
    
    Write-Host "Created new .env file with demo keys"
    Write-Host "Demo mode activated. Run 'python test_demo.py' to verify functionality."
}

function Switch-ToReal {
    Write-Host "Switching to REAL mode..."
    
    # Check if .env.real exists (user-created file with real keys)
    if (Test-Path .env.real) {
        Copy-Item .env.real .env
        Write-Host "Copied .env.real to .env"
    } else {
        # Prompt user to enter real API keys
        Write-Host "Please enter your real API keys:"
        $telecrm_key = Read-Host "TeleCRM API Key"
        $brevo_key = Read-Host "Brevo API Key"
        
        # Create a new .env file with real keys
        @"
TELECRM_API_KEY=$telecrm_key
TELECRM_API_URL=https://app.telecrm.in/api/v1
BREVO_API_KEY=$brevo_key
FLASK_APP=app.py
FLASK_ENV=development
"@ | Out-File -FilePath .env -Encoding ascii
        
        # Save a copy for future use
        Copy-Item .env .env.real
        Write-Host "Created .env.real with your API keys for future use"
    }
    
    Write-Host "Real mode activated. API calls will now use real credentials."
}

# Main script logic
if ($args.Count -eq 0) {
    Print-Usage
    exit
}

switch ($args[0]) {
    "demo" { Switch-ToDemo }
    "real" { Switch-ToReal }
    default { Print-Usage }
} 