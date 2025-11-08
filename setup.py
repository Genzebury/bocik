#!/usr/bin/env python3
"""
Quick setup script for Bocik Discord Bot
This script helps you create the config.json file interactively
"""

import json
import os
import sys

def main():
    print("=" * 60)
    print("Bocik Discord Bot - Setup Wizard")
    print("=" * 60)
    print()
    
    # Check if config.json already exists
    if os.path.exists('config.json'):
        print("⚠️  config.json already exists!")
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Setup cancelled.")
            sys.exit(0)
        print()
    
    # Load example config
    try:
        with open('config.example.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.example.json not found!")
        sys.exit(1)
    
    print("Please provide the following information:")
    print()
    
    # Get bot token
    print("1. Bot Token")
    print("   Get this from: https://discord.com/developers/applications")
    print("   Navigate to: Your Application > Bot > Token")
    token = input("   Enter bot token: ").strip()
    if token:
        config['token'] = token
    else:
        print("   ⚠️  Warning: No token provided. You'll need to add it manually.")
    print()
    
    # Get webhook URL
    print("2. Webhook URL (optional)")
    print("   Get this from: Server Settings > Integrations > Webhooks")
    webhook_url = input("   Enter webhook URL (or press Enter to skip): ").strip()
    if webhook_url:
        config['webhook_url'] = webhook_url
    else:
        print("   ℹ️  Skipped. DM logs will only be saved locally.")
    print()
    
    # Get muted role name
    print("3. Muted Role Name")
    print(f"   Current: {config['muted_role_name']}")
    role_name = input("   Enter role name (or press Enter to keep default): ").strip()
    if role_name:
        config['muted_role_name'] = role_name
    print()
    
    # Response triggers
    print("4. Response Triggers")
    print("   Current triggers:")
    for trigger, response in config['response_triggers'].items():
        print(f"      '{trigger}' → '{response}'")
    modify = input("   Do you want to modify triggers? (yes/no): ").strip().lower()
    if modify in ['yes', 'y']:
        print("   (To keep current triggers, just press Enter)")
        new_triggers = {}
        while True:
            trigger = input("   Enter trigger word (or 'done' to finish): ").strip()
            if trigger.lower() == 'done':
                break
            if trigger:
                response = input(f"   Response for '{trigger}': ").strip()
                if response:
                    new_triggers[trigger] = response
        
        if new_triggers:
            config['response_triggers'] = new_triggers
    print()
    
    # Save config
    try:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("✅ Configuration saved to config.json")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the bot: python bot.py")
        print()
        print("For more information, see README.md")
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
