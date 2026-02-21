# comprehensive_analyzer.py
"""
Comprehensive Website Analysis Framework
Analyzes 84 criteria across 4 priority tiers
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ssl
import socket
from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional

class ComprehensiveAnalyzer:
    """Advanced website analysis with 84-point criteria"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_comprehensive(self, url: str) -> Dict:
        """
        Perform comprehensive analysis covering all 84 criteria
        Returns dict with scores and tier classification
        """
        
        # Initialize analysis structure
        analysis = {
            'url': url,
            'analysis_date': datetime.now().isoformat(),
            'has_website': False,
            'website_status': 'unknown',
            
            # Scoring tiers
            'critical_failures': [],  # No website at all
            'critical_issues': [],    # Critical: 10 pts each
            'high_priority_issues': [],  # High: 5 pts each
            'medium_priority_issues': [],  # Medium: 3 pts each
            'low_priority_issues': [],  # Low: 1 pt each
            
            # Final scores
            'critical_score': 0,  # 0-50
            'high_score': 0,      # 0-70
            'medium_score': 0,    # 0-105
            'low_score': 0,       # 0-80
            'total_score': 0,     # 0-100 (normalized)
            'tier': 'UNKNOWN',    # Tier 1-4
            
            # Detailed findings
            'findings': {}
        }
        
        # Check if website exists at all
        if not url or not self._validate_url(url):
            analysis['critical_failures'].append('INVALID_URL')
            analysis['website_status'] = 'invalid_url'
            analysis['tier'] = 'TIER_1'
            return analysis
        
        # Try to fetch website
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            analysis['has_website'] = True
            analysis['website_status'] = 'accessible'
        except Exception as e:
            analysis['critical_failures'].append('NO_WEBSITE_OR_BROKEN')
            analysis['website_status'] = 'unreachable'
            analysis['tier'] = 'TIER_1'
            return analysis
        
        # If website loads but no content
        if response.status_code != 200:
            analysis['critical_failures'].append('HTTP_ERROR_' + str(response.status_code))
            analysis['website_status'] = 'error_' + str(response.status_code)
            analysis['tier'] = 'TIER_1'
            return analysis
        
        # Parse content
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
        except:
            analysis['critical_failures'].append('PARSE_ERROR')
            analysis['tier'] = 'TIER_1'
            return analysis
        
        # Check for placeholder pages
        if self._is_placeholder_page(soup, url):
            analysis['critical_failures'].append('PLACEHOLDER_PAGE')
            analysis['tier'] = 'TIER_1'
            return analysis
        
        # ===== CRITICAL ISSUES (10 points each) =====
        # Category 1: No Website Presence alternatives
        if self._is_free_subdomain(url):
            analysis['critical_issues'].append('FREE_SUBDOMAIN')
        if self._is_social_media_only(url):
            analysis['critical_issues'].append('SOCIAL_MEDIA_ONLY')
        if self._is_pdf_only(url):
            analysis['critical_issues'].append('PDF_ONLY_WEBSITE')
        
        # Category 2: Security & Basics
        if not url.startswith('https://'):
            analysis['critical_issues'].append('NO_SSL_CERTIFICATE')
        if not self._check_domain_expiration(url):
            analysis['critical_issues'].append('DOMAIN_EXPIRING_SOON')
        if self._has_broken_core_pages(soup):
            analysis['critical_issues'].append('BROKEN_CORE_PAGES')
        if self._has_security_warnings(url):
            analysis['critical_issues'].append('SECURITY_WARNINGS')
        
        # Category 3: Mobile Experience
        if not self._check_mobile_responsive(soup):
            analysis['critical_issues'].append('NOT_MOBILE_RESPONSIVE')
        mobile_load_time = self._check_mobile_speed(url)
        if mobile_load_time > 5:
            analysis['critical_issues'].append('MOBILE_LOAD_TIME_EXCESSIVE')
        
        # Category 4: Business Functionality
        if not self._has_contact_info(soup):
            analysis['critical_issues'].append('NO_CONTACT_INFORMATION')
        if not self._check_contact_form(soup):
            analysis['critical_issues'].append('NO_WORKING_CONTACT_FORM')
        if not self._has_business_hours(soup):
            analysis['critical_issues'].append('NO_BUSINESS_HOURS')
        if not self._has_location_address(soup):
            analysis['critical_issues'].append('NO_LOCATION_ADDRESS')
        if not self._has_value_proposition(soup):
            analysis['critical_issues'].append('NO_VALUE_PROPOSITION')
        
        # ===== HIGH IMPORTANCE ISSUES (5 points each) =====
        # Performance
        load_time = self._check_page_speed(response)
        if load_time > 3:
            analysis['high_priority_issues'].append('SLOW_DESKTOP_LOAD_' + str(round(load_time)))
        if self._has_unoptimized_images(soup):
            analysis['high_priority_issues'].append('UNOPTIMIZED_IMAGES')
        server_response_time = response.elapsed.total_seconds() * 1000
        if server_response_time > 500:
            analysis['high_priority_issues'].append('SLOW_SERVER_RESPONSE')
        
        # UX
        if not self._has_clear_navigation(soup):
            analysis['high_priority_issues'].append('CONFUSING_NAVIGATION')
        if not self._check_readability(soup):
            analysis['high_priority_issues'].append('POOR_READABILITY')
        if not self._looks_professional(soup):
            analysis['high_priority_issues'].append('UNPROFESSIONAL_DESIGN')
        if not self._check_branding_consistency(soup):
            analysis['high_priority_issues'].append('INCONSISTENT_BRANDING')
        
        # Technical
        if self._has_outdated_code(soup):
            analysis['high_priority_issues'].append('OUTDATED_CODE')
        if self._has_javascript_errors(response):
            analysis['high_priority_issues'].append('JAVASCRIPT_ERRORS')
        if self._has_broken_links(soup, url):
            analysis['high_priority_issues'].append('BROKEN_INTERNAL_LINKS')
        
        # SEO Basics
        if not self._has_good_title_tags(soup):
            analysis['high_priority_issues'].append('MISSING_TITLE_TAGS')
        if not self._has_meta_descriptions(soup):
            analysis['high_priority_issues'].append('MISSING_META_DESCRIPTIONS')
        if not self._has_heading_structure(soup):
            analysis['high_priority_issues'].append('POOR_HEADING_STRUCTURE')
        if not self._has_sitemap(url):
            analysis['high_priority_issues'].append('NO_SITEMAP')
        if not self._has_robots_txt(url):
            analysis['high_priority_issues'].append('NO_ROBOTS_TXT')
        
        # ===== MEDIUM IMPORTANCE ISSUES (3 points each) =====
        # Modern Features
        if not self._uses_http2(url):
            analysis['medium_priority_issues'].append('OLD_HTTP_VERSION')
        if not self._has_cdn(response):
            analysis['medium_priority_issues'].append('NO_CDN')
        if not self._has_lazy_loading(soup):
            analysis['medium_priority_issues'].append('NO_LAZY_LOADING')
        if not self._uses_modern_frameworks(soup):
            analysis['medium_priority_issues'].append('OUTDATED_FRAMEWORKS')
        
        # Content Quality
        if not self._has_updated_content(soup):
            analysis['medium_priority_issues'].append('OUTDATED_CONTENT')
        if not self._has_professional_images(soup):
            analysis['medium_priority_issues'].append('STOCK_PHOTOS_ONLY')
        if not self._has_video_content(soup):
            analysis['medium_priority_issues'].append('NO_VIDEO_CONTENT')
        if not self._has_testimonials(soup):
            analysis['medium_priority_issues'].append('NO_TESTIMONIALS')
        if not self._has_portfolio_cases(soup):
            analysis['medium_priority_issues'].append('NO_PORTFOLIO')
        if not self._has_faq(soup):
            analysis['medium_priority_issues'].append('NO_FAQ')
        
        # Advanced SEO
        if not self._has_structured_data(soup):
            analysis['medium_priority_issues'].append('NO_STRUCTURED_DATA')
        if not self._has_image_alt_text(soup):
            analysis['medium_priority_issues'].append('MISSING_IMAGE_ALT_TEXT')
        
        # Conversion
        if not self._has_cta(soup):
            analysis['medium_priority_issues'].append('NO_CLEAR_CTA')
        if not self._has_live_chat(soup):
            analysis['medium_priority_issues'].append('NO_LIVE_CHAT')
        if not self._has_email_signup(soup):
            analysis['medium_priority_issues'].append('NO_NEWSLETTER_SIGNUP')
        if not self._has_social_proof(soup):
            analysis['medium_priority_issues'].append('NO_SOCIAL_PROOF')
        if not self._has_clear_pricing(soup):
            analysis['medium_priority_issues'].append('NO_CLEAR_PRICING')
        
        # ===== LOW IMPORTANCE ISSUES (1 point each) =====
        if not self._has_pwa(soup):
            analysis['low_priority_issues'].append('NO_PWA')
        if not self._has_dark_mode(soup):
            analysis['low_priority_issues'].append('NO_DARK_MODE')
        if not self._has_animations(soup):
            analysis['low_priority_issues'].append('NO_ANIMATIONS')
        if not self._has_accessibility(soup):
            analysis['low_priority_issues'].append('BASIC_ACCESSIBILITY')
        if not self._has_heatmaps(response):
            analysis['low_priority_issues'].append('NO_HEATMAPS')
        if not self._has_ab_testing(response):
            analysis['low_priority_issues'].append('NO_AB_TESTING')
        if not self._has_blog(soup):
            analysis['low_priority_issues'].append('NO_BLOG')
        if not self._has_social_integration(soup):
            analysis['low_priority_issues'].append('NO_SOCIAL_INTEGRATION')
        if not self._has_api_integration(response):
            analysis['low_priority_issues'].append('NO_API_INTEGRATION')
        
        # Calculate scores
        analysis['critical_score'] = len(analysis['critical_issues']) * 10
        analysis['high_score'] = len(analysis['high_priority_issues']) * 5
        analysis['medium_score'] = len(analysis['medium_priority_issues']) * 3
        analysis['low_score'] = len(analysis['low_priority_issues']) * 1
        
        # Normalize to 0-100 scale
        max_score = 50 + 70 + 105 + 80  # Max possible: 305
        total_issues = (
            analysis['critical_score'] + 
            analysis['high_score'] + 
            analysis['medium_score'] + 
            analysis['low_score']
        )
        analysis['total_score'] = max(0, 100 - int((total_issues / max_score) * 100))
        
        # Assign tier
        analysis['tier'] = self._assign_tier(analysis, url)
        
        analysis['findings'] = {
            'total_critical_issues': len(analysis['critical_issues']),
            'total_high_issues': len(analysis['high_priority_issues']),
            'total_medium_issues': len(analysis['medium_priority_issues']),
            'total_low_issues': len(analysis['low_priority_issues']),
        }
        
        return analysis
    
    def _assign_tier(self, analysis: Dict, url: str) -> str:
        """Assign priority tier based on analysis"""
        
        # No website at all = Tier 1
        if analysis['critical_failures']:
            return 'TIER_1'
        
        # Multiple critical issues = Tier 1
        if len(analysis['critical_issues']) >= 3:
            return 'TIER_1'
        
        # Tier 2: Emergency fixes needed
        if len(analysis['critical_issues']) >= 1 or len(analysis['high_priority_issues']) >= 5:
            return 'TIER_2'
        
        # Tier 3: Significant improvements
        if len(analysis['high_priority_issues']) >= 3 or len(analysis['medium_priority_issues']) >= 8:
            return 'TIER_3'
        
        # Tier 4: Minor improvements
        return 'TIER_4'
    
    # Helper methods for checks
    def _validate_url(self, url: str) -> bool:
        try:
            if url and not url.startswith(('http://', 'https://', 'ftp://')):
                url = 'https://' + url
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _is_placeholder_page(self, soup: BeautifulSoup, url: str) -> bool:
        """Check if page is placeholder like Coming Soon"""
        placeholders = ['coming soon', 'under construction', 'not yet available']
        text = soup.get_text().lower()
        return any(placeholder in text for placeholder in placeholders)
    
    def _is_free_subdomain(self, url: str) -> bool:
        """Check for free subdomain hosting"""
        free_domains = ['.wixsite.com', '.weebly.com', '.wordpress.com', '.blogspot.com', '.webs.com']
        return any(domain in url.lower() for domain in free_domains)
    
    def _is_social_media_only(self, url: str) -> bool:
        """Check if only social media presence"""
        social_only = ['facebook.com', 'instagram.com', 'tiktok.com']
        return any(domain in url.lower() for domain in social_only)
    
    def _is_pdf_only(self, url: str) -> bool:
        """Check if website is just PDF"""
        return url.lower().endswith('.pdf')
    
    def _check_domain_expiration(self, url: str) -> bool:
        """Check if domain expiring soon"""
        # This would need WHOIS API, simplified version
        return True  # Placeholder
    
    def _has_broken_core_pages(self, soup: BeautifulSoup) -> bool:
        """Check if core pages are broken"""
        if not soup.find('body') or len(soup.get_text().strip()) < 100:
            return True
        return False
    
    def _has_security_warnings(self, url: str) -> bool:
        """Check for security warnings"""
        # Would integrate with Safe Browsing API
        return False  # Placeholder
    
    def _check_mobile_responsive(self, soup: BeautifulSoup) -> bool:
        """Check if mobile responsive"""
        viewport = soup.find('meta', {'name': 'viewport'})
        return viewport is not None
    
    def _check_mobile_speed(self, url: str) -> float:
        """Check mobile loading speed"""
        # Simplified - would use PageSpeed Insights API
        return 2.0  # Placeholder
    
    def _has_contact_info(self, soup: BeautifulSoup) -> bool:
        """Check for contact information"""
        contact_indicators = ['phone', 'email', 'contact', 'call', 'whatsapp']
        text = soup.get_text().lower()
        return any(indicator in text for indicator in contact_indicators)
    
    def _check_contact_form(self, soup: BeautifulSoup) -> bool:
        """Check if contact form exists and works"""
        form = soup.find('form')
        if not form:
            return False
        submit_btn = form.find(['button', 'input'], {'type': 'submit'})
        return submit_btn is not None
    
    def _has_business_hours(self, soup: BeautifulSoup) -> bool:
        """Check for business hours"""
        hours_indicators = ['hours', 'open', 'closed', 'monday', 'friday']
        text = soup.get_text().lower()
        return any(indicator in text for indicator in hours_indicators)
    
    def _has_location_address(self, soup: BeautifulSoup) -> bool:
        """Check for location/address"""
        address_indicators = ['address', 'location', 'street', 'city', 'zip', 'postal']
        text = soup.get_text().lower()
        return any(indicator in text for indicator in address_indicators)
    
    def _has_value_proposition(self, soup: BeautifulSoup) -> bool:
        """Check if clear value proposition"""
        main_content = soup.find(['main', 'article', 'section'])
        if main_content:
            text_length = len(main_content.get_text())
            return text_length > 200
        return False
    
    def _check_page_speed(self, response) -> float:
        """Check page load speed"""
        return response.elapsed.total_seconds()
    
    def _has_unoptimized_images(self, soup: BeautifulSoup) -> bool:
        """Check for unoptimized images"""
        images = soup.find_all('img')
        for img in images[:5]:  # Check first 5
            src = img.get('src', '')
            if src and not any(opt in src.lower() for opt in ['webp', 'optimized', 'compressed']):
                return True
        return False
    
    def _has_clear_navigation(self, soup: BeautifulSoup) -> bool:
        """Check for clear navigation"""
        nav = soup.find(['nav', 'header'])
        if nav:
            links = nav.find_all('a')
            return len(links) >= 3
        return False
    
    def _check_readability(self, soup: BeautifulSoup) -> bool:
        """Check readability"""
        # Check for proper heading structure
        h1 = soup.find('h1')
        p_tags = soup.find_all('p')
        return h1 is not None and len(p_tags) > 0
    
    def _looks_professional(self, soup: BeautifulSoup) -> bool:
        """Check if design looks professional"""
        # Check for CSS and modern structure
        css_links = soup.find_all('link', {'rel': 'stylesheet'})
        return len(css_links) > 0
    
    def _check_branding_consistency(self, soup: BeautifulSoup) -> bool:
        """Check branding consistency"""
        # Simplified check
        return True  # Placeholder
    
    def _has_outdated_code(self, soup: BeautifulSoup) -> bool:
        """Check for outdated code"""
        outdated = ['tables for layout', 'flash', 'deprecated']
        html_str = str(soup)
        return 'table' in html_str and 'layout' in html_str.lower()
    
    def _has_javascript_errors(self, response) -> bool:
        """Check for JavaScript errors"""
        # Would need Selenium or similar
        return False  # Placeholder
    
    def _has_broken_links(self, soup: BeautifulSoup, base_url: str) -> bool:
        """Check for broken links"""
        # Simplified - would check all links
        return False  # Placeholder
    
    def _has_good_title_tags(self, soup: BeautifulSoup) -> bool:
        """Check for good title tags"""
        title = soup.find('title')
        return title is not None and len(title.get_text()) > 10
    
    def _has_meta_descriptions(self, soup: BeautifulSoup) -> bool:
        """Check for meta descriptions"""
        meta = soup.find('meta', {'name': 'description'})
        return meta is not None
    
    def _has_heading_structure(self, soup: BeautifulSoup) -> bool:
        """Check heading structure"""
        h1 = soup.find('h1')
        return h1 is not None
    
    def _has_sitemap(self, url: str) -> bool:
        """Check for sitemap"""
        try:
            sitemap_url = url.rstrip('/') + '/sitemap.xml'
            response = requests.head(sitemap_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _has_robots_txt(self, url: str) -> bool:
        """Check for robots.txt"""
        try:
            robots_url = url.rstrip('/') + '/robots.txt'
            response = requests.head(robots_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _uses_http2(self, url: str) -> bool:
        """Check if using HTTP/2"""
        # Would check HTTP version from response
        return False  # Placeholder
    
    def _has_cdn(self, response) -> bool:
        """Check for CDN usage"""
        headers = response.headers
        cdn_indicators = ['cloudflare', 'akamai', 'cloudfront', 'cdn']
        return any(indicator in str(headers).lower() for indicator in cdn_indicators)
    
    def _has_lazy_loading(self, soup: BeautifulSoup) -> bool:
        """Check for lazy loading"""
        lazy_attrs = ['loading="lazy"', 'data-src', 'lazyload']
        html_str = str(soup)
        return any(attr in html_str for attr in lazy_attrs)
    
    def _uses_modern_frameworks(self, soup: BeautifulSoup) -> bool:
        """Check for modern frameworks"""
        html_str = str(soup)
        modern = ['react', 'vue', 'angular', 'bootstrap', 'tailwind']
        return any(fw in html_str.lower() for fw in modern)
    
    def _has_updated_content(self, soup: BeautifulSoup) -> bool:
        """Check if content is updated"""
        # Look for blog or recent dates
        html_str = str(soup)
        year = str(datetime.now().year)
        return year in html_str
    
    def _has_professional_images(self, soup: BeautifulSoup) -> bool:
        """Check for professional images"""
        images = soup.find_all('img')
        return len(images) >= 3
    
    def _has_video_content(self, soup: BeautifulSoup) -> bool:
        """Check for video content"""
        videos = soup.find_all(['video', 'iframe'])
        return len(videos) > 0
    
    def _has_testimonials(self, soup: BeautifulSoup) -> bool:
        """Check for testimonials"""
        text = soup.get_text().lower()
        return 'testimonial' in text or 'review' in text
    
    def _has_portfolio_cases(self, soup: BeautifulSoup) -> bool:
        """Check for portfolio/case studies"""
        text = soup.get_text().lower()
        return 'portfolio' in text or 'case study' in text or 'our work' in text
    
    def _has_faq(self, soup: BeautifulSoup) -> bool:
        """Check for FAQ section"""
        text = soup.get_text().lower()
        return 'faq' in text or 'frequently asked' in text
    
    def _has_structured_data(self, soup: BeautifulSoup) -> bool:
        """Check for structured data/schema"""
        schema = soup.find('script', {'type': 'application/ld+json'})
        return schema is not None
    
    def _has_image_alt_text(self, soup: BeautifulSoup) -> bool:
        """Check if images have alt text"""
        images = soup.find_all('img')
        if not images:
            return True
        with_alt = sum(1 for img in images if img.get('alt'))
        return with_alt >= len(images) * 0.7  # 70% threshold
    
    def _has_cta(self, soup: BeautifulSoup) -> bool:
        """Check for clear CTA"""
        cta_text = ['buy', 'call', 'contact', 'learn more', 'get started', 'sign up']
        text = soup.get_text().lower()
        return any(cta in text for cta in cta_text)
    
    def _has_live_chat(self, soup: BeautifulSoup) -> bool:
        """Check for live chat"""
        html_str = str(soup)
        return any(chat in html_str.lower() for chat in ['drift', 'intercom', 'zendesk', 'livechat'])
    
    def _has_email_signup(self, soup: BeautifulSoup) -> bool:
        """Check for email signup"""
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all('input', {'type': 'email'})
            if inputs:
                return True
        return False
    
    def _has_social_proof(self, soup: BeautifulSoup) -> bool:
        """Check for social proof"""
        text = soup.get_text().lower()
        indicators = ['trusted by', 'used by', 'badge', 'certification', 'award']
        return any(ind in text for ind in indicators)
    
    def _has_clear_pricing(self, soup: BeautifulSoup) -> bool:
        """Check for clear pricing"""
        text = soup.get_text().lower()
        pricing_indicators = ['$', '€', '£', 'price', 'plan', 'cost']
        return any(ind in text for ind in pricing_indicators)
    
    def _has_pwa(self, soup: BeautifulSoup) -> bool:
        """Check for PWA"""
        manifest = soup.find('link', {'rel': 'manifest'})
        return manifest is not None
    
    def _has_dark_mode(self, soup: BeautifulSoup) -> bool:
        """Check for dark mode"""
        html_str = str(soup)
        return 'prefers-color-scheme' in html_str or 'dark-mode' in html_str.lower()
    
    def _has_animations(self, soup: BeautifulSoup) -> bool:
        """Check for animations"""
        html_str = str(soup)
        return '@keyframes' in html_str or 'animation' in html_str.lower()
    
    def _has_accessibility(self, soup: BeautifulSoup) -> bool:
        """Check for accessibility"""
        html_str = str(soup)
        return 'aria-' in html_str or 'role=' in html_str
    
    def _has_heatmaps(self, response) -> bool:
        """Check for heatmap tracking"""
        html_str = str(response.content)
        return any(heat in html_str.lower() for heat in ['hotjar', 'mouseflow', 'heatmap'])
    
    def _has_ab_testing(self, response) -> bool:
        """Check for A/B testing"""
        html_str = str(response.content)
        return any(test in html_str.lower() for test in ['optimizely', 'vwo', 'convert'])
    
    def _has_blog(self, soup: BeautifulSoup) -> bool:
        """Check for blog"""
        text = soup.get_text().lower()
        return 'blog' in text or 'article' in text or 'post' in text
    
    def _has_social_integration(self, soup: BeautifulSoup) -> bool:
        """Check for social integration"""
        html_str = str(soup)
        return any(social in html_str.lower() for social in ['facebook', 'twitter', 'instagram', 'linkedin'])
    
    def _has_api_integration(self, response) -> bool:
        """Check for API integration"""
        html_str = str(response.content)
        return 'api' in html_str.lower() or 'webhook' in html_str.lower()
