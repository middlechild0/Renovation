# email_finder.py
import requests
import re
from typing import List, Optional
from urllib.parse import urlparse
import time

class EmailFinder:
    def __init__(self, hunter_api_key: str = ""):
        self.hunter_api_key = hunter_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def find_emails(self, website_url: str) -> List[str]:
        """Find email addresses associated with a website"""
        # Add scheme if missing
        if website_url and not website_url.startswith(('http://', 'https://', 'ftp://')):
            website_url = 'https://' + website_url
        
        emails = []
        
        # Method 1: Hunter.io API (if key provided)
        if self.hunter_api_key:
            hunter_emails = self._hunter_find_emails(website_url)
            emails.extend(hunter_emails)
        
        # Method 2: Scrape website for emails
        scraped_emails = self._scrape_website_emails(website_url)
        emails.extend(scraped_emails)
        
        # Method 3: Common email patterns
        domain_emails = self._generate_common_emails(website_url)
        emails.extend(domain_emails)
        
        # Remove duplicates and validate
        unique_emails = list(set(emails))
        valid_emails = [email for email in unique_emails if self._validate_email(email)]
        
        return valid_emails
    
    def _hunter_find_emails(self, website_url: str) -> List[str]:
        """Use Hunter.io API to find emails"""
        if not self.hunter_api_key:
            return []
        
        # Add scheme if missing
        if website_url and not website_url.startswith(('http://', 'https://', 'ftp://')):
            website_url = 'https://' + website_url
        
        domain = urlparse(website_url).netloc
        
        url = "https://api.hunter.io/v2/domain-search"
        params = {
            'domain': domain,
            'api_key': self.hunter_api_key,
            'limit': 10
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            emails = []
            if data.get('data', {}).get('emails'):
                for email_data in data['data']['emails']:
                    email = email_data.get('value')
                    if email and email_data.get('confidence') > 70:  # Only high confidence
                        emails.append(email)
            
            return emails
            
        except Exception as e:
            print(f"Hunter.io API error: {e}")
            return []
    
    def _scrape_website_emails(self, website_url: str) -> List[str]:
        """Scrape website for email addresses"""
        emails = []
        
        # Add scheme if missing
        if website_url and not website_url.startswith(('http://', 'https://', 'ftp://')):
            website_url = 'https://' + website_url
        
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code == 200:
                # Look for mailto links
                mailto_pattern = r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
                mailto_emails = re.findall(mailto_pattern, response.text, re.IGNORECASE)
                emails.extend(mailto_emails)
                
                # Look for email patterns in text
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                text_emails = re.findall(email_pattern, response.text, re.IGNORECASE)
                emails.extend(text_emails)
                
                # Look for contact page
                contact_page_emails = self._find_contact_page_emails(website_url, response.text)
                emails.extend(contact_page_emails)
        
        except Exception as e:
            print(f"Error scraping website for emails: {e}")
        
        return list(set(emails))
    
    def _find_contact_page_emails(self, base_url: str, html_content: str) -> List[str]:
        """Find emails on contact/contact-us pages"""
        emails = []
        
        # Common contact page patterns
        contact_patterns = [
            r'href=["\']([^"\']*contact[^"\']*)["\']',
            r'href=["\']([^"\']*about[^"\']*)["\']',
            r'href=["\']([^"\']*connect[^"\']*)["\']'
        ]
        
        for pattern in contact_patterns:
            contact_links = re.findall(pattern, html_content, re.IGNORECASE)
            for link in contact_links:
                if link.startswith('/'):
                    link = base_url.rstrip('/') + link
                elif not link.startswith('http'):
                    link = base_url.rstrip('/') + '/' + link
                
                try:
                    response = self.session.get(link, timeout=5)
                    if response.status_code == 200:
                        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                        page_emails = re.findall(email_pattern, response.text, re.IGNORECASE)
                        emails.extend(page_emails)
                except:
                    continue
        
        return list(set(emails))
    
    def _generate_common_emails(self, website_url: str) -> List[str]:
        """Generate common email addresses for a domain"""
        # Add scheme if missing
        if website_url and not website_url.startswith(('http://', 'https://', 'ftp://')):
            website_url = 'https://' + website_url
            
        domain = urlparse(website_url).netloc
        
        if not domain:
            return []
        
        common_prefixes = [
            'contact', 'info', 'hello', 'support', 'sales',
            'admin', 'office', 'business', 'service',
            'team', 'help', 'inquiry', 'questions'
        ]
        
        emails = [f"{prefix}@{domain}" for prefix in common_prefixes]
        return emails
    
    def _validate_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
