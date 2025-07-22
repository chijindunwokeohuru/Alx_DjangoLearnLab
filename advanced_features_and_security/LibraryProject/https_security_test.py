#!/usr/bin/env python3
"""
HTTPS Security Testing Script for Django Applications
Tests HTTPS configuration, security headers, SSL certificates, and overall security posture
"""

import requests
import ssl
import socket
import subprocess
import json
import sys
from urllib.parse import urlparse
from datetime import datetime, timedelta
import warnings

# Suppress SSL warnings for testing purposes
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class HTTPSSecurityTester:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.hostname = self.parsed_url.hostname
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
        self.results = {}
        
    def test_https_redirect(self):
        """Test if HTTP requests are redirected to HTTPS"""
        http_url = self.url.replace('https://', 'http://').replace(':443', ':80')
        
        try:
            response = requests.get(http_url, allow_redirects=False, timeout=10)
            
            if response.status_code in [301, 302, 307, 308]:
                location = response.headers.get('Location', '')
                if location.startswith('https://'):
                    self.results['https_redirect'] = {
                        'status': 'PASS',
                        'message': f'HTTP redirects to HTTPS ({response.status_code})',
                        'redirect_url': location
                    }
                else:
                    self.results['https_redirect'] = {
                        'status': 'FAIL',
                        'message': f'HTTP redirects but not to HTTPS: {location}'
                    }
            else:
                self.results['https_redirect'] = {
                    'status': 'FAIL',
                    'message': f'No HTTPS redirect (status: {response.status_code})'
                }
        except Exception as e:
            self.results['https_redirect'] = {
                'status': 'ERROR',
                'message': f'Error testing redirect: {str(e)}'
            }
    
    def test_ssl_certificate(self):
        """Test SSL certificate validity and configuration"""
        try:
            context = ssl.create_default_context()
            
            with socket.create_connection((self.hostname, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    # Check certificate validity
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    now = datetime.utcnow()
                    
                    days_until_expiry = (not_after - now).days
                    
                    status = 'PASS'
                    messages = []
                    
                    if now < not_before:
                        status = 'FAIL'
                        messages.append('Certificate not yet valid')
                    elif now > not_after:
                        status = 'FAIL'
                        messages.append('Certificate expired')
                    elif days_until_expiry < 30:
                        status = 'WARN'
                        messages.append(f'Certificate expires in {days_until_expiry} days')
                    else:
                        messages.append(f'Certificate valid for {days_until_expiry} more days')
                    
                    # Check cipher strength
                    if cipher and len(cipher) >= 3:
                        cipher_name = cipher[0]
                        if 'AES256' in cipher_name or 'CHACHA20' in cipher_name:
                            messages.append(f'Strong cipher: {cipher_name}')
                        else:
                            messages.append(f'Cipher: {cipher_name}')
                    
                    self.results['ssl_certificate'] = {
                        'status': status,
                        'message': '; '.join(messages),
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'expires': not_after.isoformat(),
                        'cipher': cipher[0] if cipher else 'Unknown'
                    }
                    
        except ssl.SSLError as e:
            self.results['ssl_certificate'] = {
                'status': 'FAIL',
                'message': f'SSL Error: {str(e)}'
            }
        except Exception as e:
            self.results['ssl_certificate'] = {
                'status': 'ERROR',
                'message': f'Error checking certificate: {str(e)}'
            }
    
    def test_security_headers(self):
        """Test security headers configuration"""
        try:
            response = requests.get(self.url, timeout=10, verify=False)
            headers = response.headers
            
            security_checks = {
                'Strict-Transport-Security': {
                    'present': 'Strict-Transport-Security' in headers,
                    'value': headers.get('Strict-Transport-Security', ''),
                    'required': True,
                    'description': 'HSTS header enforces HTTPS'
                },
                'Content-Security-Policy': {
                    'present': 'Content-Security-Policy' in headers,
                    'value': headers.get('Content-Security-Policy', ''),
                    'required': True,
                    'description': 'CSP prevents XSS attacks'
                },
                'X-Content-Type-Options': {
                    'present': 'X-Content-Type-Options' in headers,
                    'value': headers.get('X-Content-Type-Options', ''),
                    'required': True,
                    'description': 'Prevents MIME type sniffing'
                },
                'X-Frame-Options': {
                    'present': 'X-Frame-Options' in headers,
                    'value': headers.get('X-Frame-Options', ''),
                    'required': True,
                    'description': 'Prevents clickjacking'
                },
                'X-XSS-Protection': {
                    'present': 'X-XSS-Protection' in headers,
                    'value': headers.get('X-XSS-Protection', ''),
                    'required': False,
                    'description': 'Browser XSS protection (legacy)'
                },
                'Referrer-Policy': {
                    'present': 'Referrer-Policy' in headers,
                    'value': headers.get('Referrer-Policy', ''),
                    'required': True,
                    'description': 'Controls referrer information'
                }
            }
            
            passed = 0
            total = len([k for k, v in security_checks.items() if v['required']])
            
            header_details = {}
            for header_name, check in security_checks.items():
                if check['present']:
                    passed += 1 if check['required'] else 0
                    header_details[header_name] = {
                        'status': 'PASS',
                        'value': check['value']
                    }
                else:
                    header_details[header_name] = {
                        'status': 'FAIL' if check['required'] else 'MISSING',
                        'value': 'Not present'
                    }
            
            overall_status = 'PASS' if passed == total else 'FAIL'
            
            self.results['security_headers'] = {
                'status': overall_status,
                'message': f'{passed}/{total} required security headers present',
                'details': header_details
            }
            
        except Exception as e:
            self.results['security_headers'] = {
                'status': 'ERROR',
                'message': f'Error checking headers: {str(e)}'
            }
    
    def test_hsts_configuration(self):
        """Test HSTS configuration specifically"""
        try:
            response = requests.get(self.url, timeout=10, verify=False)
            hsts_header = response.headers.get('Strict-Transport-Security', '')
            
            if not hsts_header:
                self.results['hsts'] = {
                    'status': 'FAIL',
                    'message': 'HSTS header not present'
                }
                return
            
            # Parse HSTS header
            hsts_parts = [part.strip() for part in hsts_header.split(';')]
            max_age = None
            include_subdomains = False
            preload = False
            
            for part in hsts_parts:
                if part.startswith('max-age='):
                    max_age = int(part.split('=')[1])
                elif part == 'includeSubDomains':
                    include_subdomains = True
                elif part == 'preload':
                    preload = True
            
            messages = []
            status = 'PASS'
            
            if max_age is None:
                status = 'FAIL'
                messages.append('No max-age specified')
            elif max_age < 31536000:  # 1 year
                status = 'WARN'
                messages.append(f'max-age is {max_age} seconds (less than 1 year)')
            else:
                messages.append(f'max-age: {max_age} seconds ({max_age//86400} days)')
            
            if include_subdomains:
                messages.append('includeSubDomains: enabled')
            else:
                messages.append('includeSubDomains: disabled')
            
            if preload:
                messages.append('preload: enabled')
            
            self.results['hsts'] = {
                'status': status,
                'message': '; '.join(messages),
                'max_age': max_age,
                'include_subdomains': include_subdomains,
                'preload': preload
            }
            
        except Exception as e:
            self.results['hsts'] = {
                'status': 'ERROR',
                'message': f'Error checking HSTS: {str(e)}'
            }
    
    def test_cookie_security(self):
        """Test cookie security configuration"""
        try:
            response = requests.get(self.url, timeout=10, verify=False)
            cookies = response.cookies
            
            secure_cookies = 0
            httponly_cookies = 0
            total_cookies = len(cookies)
            
            cookie_details = {}
            for cookie in cookies:
                cookie_details[cookie.name] = {
                    'secure': cookie.secure,
                    'httponly': cookie.has_nonstandard_attr('HttpOnly'),
                    'samesite': cookie.get_nonstandard_attr('SameSite')
                }
                
                if cookie.secure:
                    secure_cookies += 1
                if cookie.has_nonstandard_attr('HttpOnly'):
                    httponly_cookies += 1
            
            if total_cookies == 0:
                self.results['cookie_security'] = {
                    'status': 'INFO',
                    'message': 'No cookies found to test'
                }
            else:
                status = 'PASS' if secure_cookies == total_cookies else 'FAIL'
                self.results['cookie_security'] = {
                    'status': status,
                    'message': f'{secure_cookies}/{total_cookies} cookies secure, {httponly_cookies}/{total_cookies} HttpOnly',
                    'details': cookie_details
                }
                
        except Exception as e:
            self.results['cookie_security'] = {
                'status': 'ERROR',
                'message': f'Error checking cookies: {str(e)}'
            }
    
    def test_tls_configuration(self):
        """Test TLS configuration using external tools"""
        try:
            # Try to use testssl.sh if available
            result = subprocess.run(
                ['testssl.sh', '--quiet', '--jsonfile-pretty', '/tmp/testssl.json', self.url],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                try:
                    with open('/tmp/testssl.json', 'r') as f:
                        testssl_data = json.load(f)
                    
                    self.results['tls_configuration'] = {
                        'status': 'PASS',
                        'message': 'TLS configuration analyzed with testssl.sh',
                        'details': testssl_data
                    }
                except:
                    self.results['tls_configuration'] = {
                        'status': 'INFO',
                        'message': 'testssl.sh completed but results not parsed'
                    }
            else:
                raise Exception('testssl.sh failed')
                
        except FileNotFoundError:
            self.results['tls_configuration'] = {
                'status': 'INFO',
                'message': 'testssl.sh not available for detailed TLS testing'
            }
        except Exception as e:
            self.results['tls_configuration'] = {
                'status': 'INFO',
                'message': f'Advanced TLS testing not available: {str(e)}'
            }
    
    def run_all_tests(self):
        """Run all security tests"""
        print(f"🔍 Testing HTTPS security for: {self.url}")
        print("=" * 60)
        
        tests = [
            ('HTTPS Redirect', self.test_https_redirect),
            ('SSL Certificate', self.test_ssl_certificate),
            ('Security Headers', self.test_security_headers),
            ('HSTS Configuration', self.test_hsts_configuration),
            ('Cookie Security', self.test_cookie_security),
            ('TLS Configuration', self.test_tls_configuration)
        ]
        
        for test_name, test_func in tests:
            print(f"🔧 Running: {test_name}")
            test_func()
        
        return self.results
    
    def print_results(self):
        """Print formatted test results"""
        print("\n" + "=" * 60)
        print("🔒 HTTPS Security Test Results")
        print("=" * 60)
        
        status_symbols = {
            'PASS': '✅',
            'FAIL': '❌',
            'WARN': '⚠️',
            'ERROR': '🔥',
            'INFO': 'ℹ️'
        }
        
        for test_name, result in self.results.items():
            status = result.get('status', 'UNKNOWN')
            message = result.get('message', 'No message')
            symbol = status_symbols.get(status, '❓')
            
            print(f"\n{symbol} {test_name.replace('_', ' ').title()}")
            print(f"   Status: {status}")
            print(f"   Details: {message}")
            
            if 'details' in result:
                print("   Additional Info:")
                details = result['details']
                if isinstance(details, dict):
                    for key, value in details.items():
                        if isinstance(value, dict) and 'status' in value:
                            detail_symbol = status_symbols.get(value['status'], '❓')
                            print(f"     {detail_symbol} {key}: {value.get('value', 'N/A')}")
                        else:
                            print(f"     • {key}: {value}")
        
        # Overall assessment
        print("\n" + "=" * 60)
        passed_tests = len([r for r in self.results.values() if r.get('status') == 'PASS'])
        total_tests = len([r for r in self.results.values() if r.get('status') in ['PASS', 'FAIL']])
        
        if total_tests > 0:
            pass_rate = (passed_tests / total_tests) * 100
            print(f"📊 Overall Score: {passed_tests}/{total_tests} tests passed ({pass_rate:.1f}%)")
            
            if pass_rate >= 80:
                print("🎉 Excellent HTTPS security configuration!")
            elif pass_rate >= 60:
                print("👍 Good HTTPS security, minor improvements needed")
            else:
                print("⚠️ HTTPS security needs significant improvement")
        
        print("=" * 60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python https_security_test.py <URL>")
        print("Example: python https_security_test.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    tester = HTTPSSecurityTester(url)
    tester.run_all_tests()
    tester.print_results()
    
    # Return appropriate exit code
    failed_tests = len([r for r in tester.results.values() if r.get('status') == 'FAIL'])
    sys.exit(1 if failed_tests > 0 else 0)

if __name__ == '__main__':
    main()
