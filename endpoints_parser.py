from dotenv import load_dotenv
import os
import json
import re

def load_environment():
    """Load environment variables from .env file and merge with process.env"""
    load_dotenv()
    return dict(os.environ)

def replace_env_vars(value, env_vars):
    """Replace ${VAR} with environment variable values in a string"""
    if not isinstance(value, str):
        return value
    
    def replace_match(match):
        var_name = match.group(1)
        return env_vars.get(var_name, f"${{{var_name}}}")  # Keep original if not found
    
    return re.sub(r'\${([^}]+)}', replace_match, value)

def process_object(obj, env_vars):
    """Recursively process an object and replace environment variables"""
    if isinstance(obj, dict):
        return {k: process_object(v, env_vars) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_object(item, env_vars) for item in obj]
    elif isinstance(obj, str):
        return replace_env_vars(obj, env_vars)
    return obj

def parse_endpoints():
    """Load endpoints.json and replace environment variables"""
    try:
        # Load environment variables
        env_vars = load_environment()
        
        # Read endpoints.json
        with open('endpoints.json', 'r') as f:
            endpoints = json.load(f)
        
        # Process and replace environment variables
        processed_endpoints = process_object(endpoints, env_vars)
        
        return processed_endpoints
    except FileNotFoundError:
        print("Error: endpoints.json not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in endpoints.json")
        return None
    except Exception as e:
        print(f"Error processing endpoints: {str(e)}")
        return None