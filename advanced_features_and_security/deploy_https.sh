#!/bin/bash

# Django HTTPS Deployment Script
# This script helps configure HTTPS for Django LibraryProject

set -e

echo "=================================="
echo "Django HTTPS Deployment Script"
echo "=================================="

# Configuration variables
PROJECT_NAME="LibraryProject"
DOMAIN=""
EMAIL=""
WEB_SERVER=""

# Function to display usage
usage() {
    echo "Usage: $0 -d DOMAIN -e EMAIL -s WEB_SERVER"
    echo "  -d DOMAIN     : Your domain name (e.g., example.com)"
    echo "  -e EMAIL      : Your email for Let's Encrypt"
    echo "  -s WEB_SERVER : Web server (nginx or apache)"
    echo "  -h            : Show this help message"
    exit 1
}

# Parse command line arguments
while getopts "d:e:s:h" opt; do
    case $opt in
        d)
            DOMAIN="$OPTARG"
            ;;
        e)
            EMAIL="$OPTARG"
            ;;
        s)
            WEB_SERVER="$OPTARG"
            ;;
        h)
            usage
            ;;
        \?)
            echo "Invalid option -$OPTARG" >&2
            usage
            ;;
    esac
done

# Check if all required parameters are provided
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ] || [ -z "$WEB_SERVER" ]; then
    echo "Error: Missing required parameters"
    usage
fi

# Validate web server choice
if [ "$WEB_SERVER" != "nginx" ] && [ "$WEB_SERVER" != "apache" ]; then
    echo "Error: Web server must be either 'nginx' or 'apache'"
    exit 1
fi

echo "Configuration:"
echo "  Domain: $DOMAIN"
echo "  Email: $EMAIL"
echo "  Web Server: $WEB_SERVER"
echo ""

# Function to install certbot
install_certbot() {
    echo "Installing Certbot..."
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update
        if [ "$WEB_SERVER" == "nginx" ]; then
            sudo apt-get install -y certbot python3-certbot-nginx
        else
            sudo apt-get install -y certbot python3-certbot-apache
        fi
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y epel-release
        sudo yum install -y certbot
        if [ "$WEB_SERVER" == "nginx" ]; then
            sudo yum install -y python3-certbot-nginx
        else
            sudo yum install -y python3-certbot-apache
        fi
    else
        echo "Error: Unsupported package manager. Please install certbot manually."
        exit 1
    fi
    
    echo "Certbot installed successfully!"
}

# Function to configure Nginx
configure_nginx() {
    echo "Configuring Nginx..."
    
    # Create Nginx configuration
    cat > "/tmp/${PROJECT_NAME}.conf" << EOF
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    return 301 https://\$server_name\$request_uri;
}

# HTTPS server configuration
server {
    listen 443 ssl http2;
    server_name ${DOMAIN} www.${DOMAIN};

    # SSL configuration will be handled by certbot
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "same-origin";

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Additional security headers for proxied content
        proxy_set_header X-Content-Type-Options nosniff;
        proxy_set_header X-Frame-Options DENY;
    }

    # Static files
    location /static/ {
        alias /var/www/${PROJECT_NAME}/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }

    # Media files
    location /media/ {
        alias /var/www/${PROJECT_NAME}/media/;
        expires 1y;
        add_header Cache-Control "public";
        add_header X-Content-Type-Options nosniff;
    }
    
    # Additional security configurations
    location ~ /\.ht {
        deny all;
    }
    
    # Prevent access to sensitive files
    location ~ \.(env|log|ini|conf)$ {
        deny all;
        return 404;
    }
}
EOF

    # Move configuration to sites-available
    sudo mv "/tmp/${PROJECT_NAME}.conf" "/etc/nginx/sites-available/${PROJECT_NAME}"
    
    # Enable the site
    sudo ln -sf "/etc/nginx/sites-available/${PROJECT_NAME}" "/etc/nginx/sites-enabled/"
    
    # Remove default site if it exists
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx configuration
    sudo nginx -t
    
    if [ $? -eq 0 ]; then
        sudo systemctl reload nginx
        echo "Nginx configured successfully!"
    else
        echo "Error: Nginx configuration test failed"
        exit 1
    fi
}

# Function to configure Apache
configure_apache() {
    echo "Configuring Apache..."
    
    # Enable required modules
    sudo a2enmod ssl
    sudo a2enmod rewrite
    sudo a2enmod headers
    
    # Create Apache configuration
    cat > "/tmp/${PROJECT_NAME}.conf" << EOF
# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName ${DOMAIN}
    ServerAlias www.${DOMAIN}
    Redirect permanent / https://${DOMAIN}/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName ${DOMAIN}
    ServerAlias www.${DOMAIN}

    # SSL configuration will be handled by certbot
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "same-origin"

    # Django WSGI configuration
    WSGIDaemonProcess ${PROJECT_NAME} python-home=/var/www/${PROJECT_NAME}/venv python-path=/var/www/${PROJECT_NAME}
    WSGIProcessGroup ${PROJECT_NAME}
    WSGIScriptAlias / /var/www/${PROJECT_NAME}/LibraryProject/wsgi.py

    # Static files
    Alias /static/ /var/www/${PROJECT_NAME}/static/
    <Directory /var/www/${PROJECT_NAME}/static/>
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
        Header append Cache-Control "public, immutable"
    </Directory>

    # Media files
    Alias /media/ /var/www/${PROJECT_NAME}/media/
    <Directory /var/www/${PROJECT_NAME}/media/>
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
        Header append Cache-Control "public"
    </Directory>

    # Security configurations
    <Directory /var/www/${PROJECT_NAME}/>
        Require all granted
    </Directory>
    
    # Prevent access to sensitive files
    <Files ~ "\.(env|log|ini|conf)$">
        Require all denied
    </Files>
</VirtualHost>
EOF

    # Move configuration to sites-available
    sudo mv "/tmp/${PROJECT_NAME}.conf" "/etc/apache2/sites-available/${PROJECT_NAME}.conf"
    
    # Enable the site
    sudo a2ensite "${PROJECT_NAME}.conf"
    
    # Disable default site
    sudo a2dissite 000-default.conf
    
    # Test apache configuration
    sudo apache2ctl configtest
    
    if [ $? -eq 0 ]; then
        sudo systemctl reload apache2
        echo "Apache configured successfully!"
    else
        echo "Error: Apache configuration test failed"
        exit 1
    fi
}

# Function to obtain SSL certificate
obtain_ssl_certificate() {
    echo "Obtaining SSL certificate from Let's Encrypt..."
    
    if [ "$WEB_SERVER" == "nginx" ]; then
        sudo certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --email "$EMAIL" --agree-tos --no-eff-email
    else
        sudo certbot --apache -d "$DOMAIN" -d "www.$DOMAIN" --email "$EMAIL" --agree-tos --no-eff-email
    fi
    
    if [ $? -eq 0 ]; then
        echo "SSL certificate obtained successfully!"
    else
        echo "Error: Failed to obtain SSL certificate"
        exit 1
    fi
}

# Function to setup auto-renewal
setup_auto_renewal() {
    echo "Setting up automatic certificate renewal..."
    
    # Add cron job for automatic renewal
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --post-hook 'systemctl reload ${WEB_SERVER}'") | crontab -
    
    echo "Auto-renewal configured successfully!"
}

# Function to create monitoring script
create_monitoring_script() {
    echo "Creating SSL monitoring script..."
    
    cat > "/usr/local/bin/ssl-monitor.sh" << EOF
#!/bin/bash

DOMAIN="${DOMAIN}"
DAYS_THRESHOLD=30

EXPIRY_DATE=\$(echo | openssl s_client -connect \$DOMAIN:443 -servername \$DOMAIN 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_TIMESTAMP=\$(date -d "\$EXPIRY_DATE" +%s)
CURRENT_TIMESTAMP=\$(date +%s)
DAYS_UNTIL_EXPIRY=\$(( (\$EXPIRY_TIMESTAMP - \$CURRENT_TIMESTAMP) / 86400 ))

if [ \$DAYS_UNTIL_EXPIRY -lt \$DAYS_THRESHOLD ]; then
    echo "WARNING: SSL certificate for \$DOMAIN expires in \$DAYS_UNTIL_EXPIRY days!"
    # Add notification logic here (email, Slack, etc.)
fi
EOF

    sudo chmod +x /usr/local/bin/ssl-monitor.sh
    
    # Add to cron for daily monitoring
    (crontab -l 2>/dev/null; echo "0 9 * * * /usr/local/bin/ssl-monitor.sh") | crontab -
    
    echo "SSL monitoring script created!"
}

# Function to test HTTPS configuration
test_https_configuration() {
    echo "Testing HTTPS configuration..."
    
    # Wait for services to fully restart
    sleep 5
    
    # Test HTTP to HTTPS redirect
    echo "Testing HTTP to HTTPS redirect..."
    REDIRECT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://$DOMAIN" --max-time 10)
    
    if [ "$REDIRECT_STATUS" == "301" ] || [ "$REDIRECT_STATUS" == "302" ]; then
        echo "✅ HTTP to HTTPS redirect working"
    else
        echo "❌ HTTP to HTTPS redirect failed (Status: $REDIRECT_STATUS)"
    fi
    
    # Test HTTPS connection
    echo "Testing HTTPS connection..."
    HTTPS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" --max-time 10)
    
    if [ "$HTTPS_STATUS" == "200" ]; then
        echo "✅ HTTPS connection working"
    else
        echo "❌ HTTPS connection failed (Status: $HTTPS_STATUS)"
    fi
    
    # Test security headers
    echo "Testing security headers..."
    HEADERS=$(curl -s -I "https://$DOMAIN" --max-time 10)
    
    if echo "$HEADERS" | grep -q "Strict-Transport-Security"; then
        echo "✅ HSTS header present"
    else
        echo "❌ HSTS header missing"
    fi
    
    if echo "$HEADERS" | grep -q "X-Frame-Options"; then
        echo "✅ X-Frame-Options header present"
    else
        echo "❌ X-Frame-Options header missing"
    fi
    
    if echo "$HEADERS" | grep -q "X-Content-Type-Options"; then
        echo "✅ X-Content-Type-Options header present"
    else
        echo "❌ X-Content-Type-Options header missing"
    fi
    
    echo ""
    echo "HTTPS configuration test completed!"
}

# Function to display summary
display_summary() {
    echo ""
    echo "=================================="
    echo "HTTPS Deployment Summary"
    echo "=================================="
    echo "✅ Web server configured: $WEB_SERVER"
    echo "✅ SSL certificate obtained from Let's Encrypt"
    echo "✅ HTTPS redirection enabled"
    echo "✅ Security headers configured"
    echo "✅ Auto-renewal setup complete"
    echo "✅ Monitoring script created"
    echo ""
    echo "Your Django application is now secured with HTTPS!"
    echo ""
    echo "Next steps:"
    echo "1. Update your Django settings.py ALLOWED_HOSTS to include '$DOMAIN'"
    echo "2. Deploy your Django application to /var/www/${PROJECT_NAME}/"
    echo "3. Collect static files: python manage.py collectstatic"
    echo "4. Test your application at: https://$DOMAIN"
    echo ""
    echo "Monitoring:"
    echo "- Certificate expiry check: /usr/local/bin/ssl-monitor.sh"
    echo "- Auto-renewal: Configured via cron (12:00 daily)"
    echo ""
    echo "Security testing tools:"
    echo "- SSL Labs: https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
    echo "- Security Headers: https://securityheaders.com/?q=$DOMAIN"
    echo "- Mozilla Observatory: https://observatory.mozilla.org/analyze/$DOMAIN"
}

# Main execution
main() {
    echo "Starting HTTPS deployment process..."
    echo ""
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        echo "This script needs to be run with sudo privileges"
        echo "Please run: sudo $0 $@"
        exit 1
    fi
    
    # Install certbot
    install_certbot
    
    # Configure web server
    if [ "$WEB_SERVER" == "nginx" ]; then
        configure_nginx
    else
        configure_apache
    fi
    
    # Obtain SSL certificate
    obtain_ssl_certificate
    
    # Setup auto-renewal
    setup_auto_renewal
    
    # Create monitoring script
    create_monitoring_script
    
    # Test configuration
    test_https_configuration
    
    # Display summary
    display_summary
}

# Run main function
main
