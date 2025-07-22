#!/usr/bin/env python3
"""
Django Environment Management Script
Manages different Django settings configurations for development, staging, and production
"""

import os
import sys
import argparse
from pathlib import Path

class DjangoEnvironmentManager:
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.project_name = 'LibraryProject'
        self.settings_dir = Path(self.project_path) / self.project_name / self.project_name
        
    def list_environments(self):
        """List available environment configurations"""
        environments = []
        settings_files = self.settings_dir.glob('settings_*.py')
        
        for file in settings_files:
            env_name = file.stem.replace('settings_', '')
            environments.append(env_name)
        
        if (self.settings_dir / 'settings.py').exists():
            environments.append('default')
            
        return environments
    
    def switch_environment(self, environment):
        """Switch to a specific environment configuration"""
        settings_file = None
        
        if environment == 'dev' or environment == 'development':
            settings_file = 'settings_dev.py'
        elif environment == 'prod' or environment == 'production':
            settings_file = 'settings_prod.py'
        elif environment == 'staging':
            settings_file = 'settings_staging.py'
        elif environment == 'default':
            settings_file = 'settings.py'
        else:
            print(f"❌ Unknown environment: {environment}")
            return False
        
        source_path = self.settings_dir / settings_file
        if not source_path.exists():
            print(f"❌ Settings file not found: {settings_file}")
            return False
        
        # Set environment variable
        os.environ['DJANGO_SETTINGS_MODULE'] = f'{self.project_name}.{settings_file[:-3]}'
        
        print(f"✅ Switched to {environment} environment")
        print(f"📝 Using settings: {settings_file}")
        print(f"🔧 DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE')}")
        
        return True
    
    def validate_environment(self, environment):
        """Validate environment configuration"""
        try:
            os.environ['DJANGO_SETTINGS_MODULE'] = f'{self.project_name}.settings_{environment}'
            
            import django
            from django.conf import settings
            django.setup()
            
            print(f"✅ Environment '{environment}' is valid")
            print(f"🔐 DEBUG: {settings.DEBUG}")
            print(f"🌐 ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
            print(f"🔒 SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'Not set')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Environment validation failed: {e}")
            return False
    
    def create_environment_file(self):
        """Create .env file for environment variables"""
        env_file = Path(self.project_path) / '.env'
        
        env_content = """# Django Environment Configuration
# Copy this file to .env and configure for your environment

# Environment Selection (dev, prod, staging)
DJANGO_ENVIRONMENT=dev

# Security Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DB_NAME=libraryproject
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/1

# Production Domain
PRODUCTION_DOMAIN=yourdomain.com

# SSL Certificate Paths (for production)
SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
"""
        
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write(env_content)
            print(f"✅ Created environment file: {env_file}")
        else:
            print(f"📁 Environment file already exists: {env_file}")
    
    def run_management_command(self, command, environment=None):
        """Run Django management command with specified environment"""
        if environment:
            self.switch_environment(environment)
        
        os.system(f"python {Path(self.project_path) / 'manage.py'} {command}")

def main():
    parser = argparse.ArgumentParser(description='Django Environment Manager')
    parser.add_argument('action', choices=['list', 'switch', 'validate', 'init', 'run'], 
                       help='Action to perform')
    parser.add_argument('--env', '-e', help='Environment name (dev, prod, staging)')
    parser.add_argument('--command', '-c', help='Django management command to run')
    parser.add_argument('--project-path', '-p', help='Path to Django project')
    
    args = parser.parse_args()
    
    manager = DjangoEnvironmentManager(args.project_path)
    
    if args.action == 'list':
        environments = manager.list_environments()
        print("📋 Available environments:")
        for env in environments:
            print(f"  - {env}")
    
    elif args.action == 'switch':
        if not args.env:
            print("❌ Please specify environment with --env")
            sys.exit(1)
        manager.switch_environment(args.env)
    
    elif args.action == 'validate':
        if not args.env:
            print("❌ Please specify environment with --env")
            sys.exit(1)
        manager.validate_environment(args.env)
    
    elif args.action == 'init':
        manager.create_environment_file()
        print("🚀 Environment setup complete!")
        print("📝 Please edit .env file with your configuration")
    
    elif args.action == 'run':
        if not args.command:
            print("❌ Please specify command with --command")
            sys.exit(1)
        manager.run_management_command(args.command, args.env)

if __name__ == '__main__':
    main()
