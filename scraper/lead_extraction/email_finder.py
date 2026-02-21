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
        if website_url and not website_url.startswith(('http://', 'https://', 'ftp://')):
            website_url = 'https://' + website_url
        emails = []
        scraped_emails = self._scrape_website_emails(website_url)
        emails.extend(scraped_emails)
        domain_emails = self._generate_common_emails(website_url)
        emails.extend(domain_emails)
        unique_emails = list(set(emails))
        valid_emails = [email for email in unique_emails if self._validate_email(email)]
        return valid_emails
    
    def _scrape_website_emails(self, website_url: str) -> List[str]:
        emails = []
        if website_url and not website_url.startswith(('http://', 'https://', 'ftp://')):
            website_url = 'https://' + website_url
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code == 200:
                mailto_pattern = r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
                mailto_emails = re.findall(mailto_pattern, response.text, re.IGNORECASE)
                emails.extend(mailto_emails)
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                text_emails = re.findall(email_pattern, response.text, re.IGNORECASE)
                emails.extend(text_emails)
        except Exception as e:
            print(f"Error scraping website for emails: {e}")
        return list(set(emails))
    
    def _generate_common_emails(self, website_url: str) -> List[str]:
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
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
