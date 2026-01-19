# analyzer.py
import requests
from bs4 import BeautifulSoup
import ssl
import time
from urllib.parse import urlparse
from typing import Dict, List, Optional
import json
import re
from datetime import datetime

class WebsiteAnalyzer:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Outdated technologies to flag
        self.outdated_tech = {
            'flash': 'Adobe Flash (deprecated)',
            'jquery_1': 'jQuery 1.x (outdated)',
            'angularjs': 'AngularJS (legacy)',
            'php_5': 'PHP 5.x (EOL)',
            'mysql_old': 'MySQL old version',
            'http': 'HTTP (not HTTPS)',
            'table_layout': 'Table-based layout',
            'frameset': 'Frames (deprecated)',
        }
        
        # Modern technologies
        self.modern_tech = {
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular 2+',
            'nextjs': 'Next.js',
            'nuxt': 'Nuxt.js',
            'tailwind': 'Tailwind CSS',
            'bootstrap_5': 'Bootstrap 5',
            'graphql': 'GraphQL',
            'pwa': 'Progressive Web App',
        }
    
    def analyze(self, url: str) -> Dict:
        """Comprehensive website analysis"""
        # Add scheme if missing
        if url and not url.startswith(('http://', 'https://', 'ftp://')):
            url = 'https://' + url
        
        analysis = {
            'url': url,
            'exists': False,
            'score': 0,
            'has_ssl': False,
            'mobile_friendly': False,
            'load_time': 0,
            'tech_stack': [],
            'issues': [],
            'recommendations': [],
            'needs_redesign': False,
            'has_contact_form': False,
            'analysis_date': datetime.now().isoformat()
        }
        
        if not url or not self._is_valid_url(url):
            analysis['issues'].append('Invalid URL')
            return analysis
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            end_time = time.time()
            
            analysis['load_time'] = round(end_time - start_time, 2)
            analysis['status_code'] = response.status_code
            analysis['exists'] = response.status_code == 200
            
            if response.status_code == 200:
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Run all checks
                self._check_ssl(url, analysis)
                self._check_mobile_friendly(soup, analysis)
                self._detect_tech_stack(soup, response, analysis)
                self._check_performance(response, analysis)
                self._check_contact_form(soup, analysis)
                self._check_modern_design(soup, analysis)
                self._check_seo(soup, analysis)
                self._check_accessibility(soup, analysis)
                
                # Calculate overall score
                analysis['score'] = self._calculate_score(analysis)
                analysis['needs_redesign'] = analysis['score'] < 50
                
            else:
                analysis['issues'].append(f'Website returned status code: {response.status_code}')
                
        except requests.exceptions.RequestException as e:
            analysis['issues'].append(f'Connection error: {str(e)}')
        except Exception as e:
            analysis['issues'].append(f'Analysis error: {str(e)}')
        
        return analysis
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        try:
            # Add scheme if missing
            if url and not url.startswith(('http://', 'https://', 'ftp://')):
                url = 'https://' + url
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _check_ssl(self, url: str, analysis: Dict):
        """Check if website uses SSL"""
        analysis['has_ssl'] = url.startswith('https://')
        if not analysis['has_ssl']:
            analysis['issues'].append('Website does not use HTTPS/SSL')
            analysis['recommendations'].append('Implement SSL certificate for security')
    
    def _check_mobile_friendly(self, soup: BeautifulSoup, analysis: Dict):
        """Check basic mobile responsiveness"""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        has_viewport = viewport is not None
        
        # Check for responsive CSS
        responsive_selectors = [
            '@media',
            'max-width',
            'min-width',
            'responsive'
        ]
        
        styles = soup.find_all('style')
        css_text = ' '.join([style.get_text() for style in styles])
        
        has_responsive_css = any(selector in css_text.lower() for selector in responsive_selectors)
        
        # Check for mobile-specific elements
        mobile_elements = soup.select('[class*="mobile"], [class*="phone"], [id*="mobile"]')
        
        analysis['mobile_friendly'] = has_viewport or has_responsive_css or len(mobile_elements) > 0
        
        if not analysis['mobile_friendly']:
            analysis['issues'].append('Website may not be mobile responsive')
            analysis['recommendations'].append('Implement responsive design for mobile devices')
    
    def _detect_tech_stack(self, soup: BeautifulSoup, response: requests.Response, analysis: Dict):
        """Detect technologies used on the website"""
        tech_stack = []
        html_text = str(soup).lower()
        headers = response.headers
        
        # Check for CMS
        if 'wp-content' in html_text or 'wordpress' in html_text:
            tech_stack.append('WordPress')
        
        if '/wp-json/' in html_text:
            tech_stack.append('WordPress REST API')
        
        # Check for JavaScript frameworks
        if 'react' in html_text:
            tech_stack.append('React')
        if 'vue' in html_text:
            tech_stack.append('Vue.js')
        if 'angular' in html_text:
            tech_stack.append('Angular')
        
        # Check for CSS frameworks
        if 'bootstrap' in html_text:
            tech_stack.append('Bootstrap')
        if 'tailwind' in html_text:
            tech_stack.append('Tailwind CSS')
        
        # Check server technology
        server = headers.get('Server', '').lower()
        if 'apache' in server:
            tech_stack.append('Apache')
        elif 'nginx' in server:
            tech_stack.append('Nginx')
        
        # Check for outdated tech
        outdated_found = []
        if 'flash' in html_text:
            outdated_found.append(self.outdated_tech['flash'])
        if 'jquery/1.' in html_text:
            outdated_found.append(self.outdated_tech['jquery_1'])
        
        if outdated_found:
            analysis['issues'].append(f'Outdated technologies detected: {", ".join(outdated_found)}')
            analysis['recommendations'].append(f'Update outdated technologies: {", ".join(outdated_found)}')
        
        analysis['tech_stack'] = list(set(tech_stack))
    
    def _check_performance(self, response: requests.Response, analysis: Dict):
        """Check basic performance metrics"""
        content_length = len(response.content)
        
        if content_length > 5 * 1024 * 1024:  # > 5MB
            analysis['issues'].append('Large page size may affect loading speed')
            analysis['recommendations'].append('Optimize images and minify assets')
        
        if analysis['load_time'] > 3:
            analysis['issues'].append(f'Slow load time: {analysis["load_time"]}s')
            analysis['recommendations'].append('Implement caching and optimize assets')
    
    def _check_contact_form(self, soup: BeautifulSoup, analysis: Dict):
        """Check if website has contact form"""
        contact_selectors = [
            'form[action*="contact"]',
            'form[id*="contact"]',
            'form[class*="contact"]',
            'a[href*="contact"]',
            'a[href*="mailto:"]'
        ]
        
        for selector in contact_selectors:
            if soup.select(selector):
                analysis['has_contact_form'] = True
                break
        
        if not analysis['has_contact_form']:
            analysis['issues'].append('No obvious contact form found')
            analysis['recommendations'].append('Add clear contact form or contact information')
    
    def _check_modern_design(self, soup: BeautifulSoup, analysis: Dict):
        """Check for modern design patterns"""
        modern_indicators = 0
        total_indicators = 7
        
        # 1. Hero section
        hero_selectors = ['.hero', '.banner', '.jumbotron', '[class*="hero"]']
        if any(soup.select(selector) for selector in hero_selectors):
            modern_indicators += 1
        
        # 2. Hamburger menu (mobile)
        if soup.select('.hamburger, .menu-toggle, [class*="nav-toggle"]'):
            modern_indicators += 1
        
        # 3. CSS Grid or Flexbox
        styles = soup.find_all('style')
        css_text = ' '.join([style.get_text() for style in styles])
        if 'display: grid' in css_text or 'display: flex' in css_text:
            modern_indicators += 1
        
        # 4. Modern typography
        font_selectors = [
            'font-family: -apple-system',
            'font-family: "Segoe UI"',
            'font-family: Roboto',
            'font-family: "Open Sans"'
        ]
        if any(font in css_text for font in font_selectors):
            modern_indicators += 1
        
        # 5. Call to action buttons
        cta_selectors = ['.btn', '.button', '[class*="cta"]', '[class*="action"]']
        if any(soup.select(selector) for selector in cta_selectors):
            modern_indicators += 1
        
        # 6. Social media icons
        social_selectors = ['.social', '[class*="social"]', '[href*="facebook.com"]', '[href*="twitter.com"]']
        if any(soup.select(selector) for selector in social_selectors):
            modern_indicators += 1
        
        # 7. Testimonials/carousel
        if soup.select('.testimonial, .carousel, .slider, [class*="testimonial"]'):
            modern_indicators += 1
        
        modern_percentage = (modern_indicators / total_indicators) * 100
        
        if modern_percentage < 50:
            analysis['issues'].append('Website design appears outdated')
            analysis['recommendations'].append('Consider modern redesign with current UI/UX trends')
    
    def _check_seo(self, soup: BeautifulSoup, analysis: Dict):
        """Check basic SEO factors"""
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content', '').strip():
            analysis['issues'].append('Missing meta description')
            analysis['recommendations'].append('Add descriptive meta tag for better SEO')
        
        # Title tag
        title = soup.find('title')
        if not title or not title.get_text().strip():
            analysis['issues'].append('Missing or empty title tag')
            analysis['recommendations'].append('Add descriptive title tag')
        
        # Heading structure
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            analysis['issues'].append('Missing H1 heading')
            analysis['recommendations'].append('Add a clear H1 heading for SEO')
        elif len(h1_tags) > 1:
            analysis['issues'].append('Multiple H1 headings (should have only one)')
            analysis['recommendations'].append('Use only one H1 tag per page')
    
    def _check_accessibility(self, soup: BeautifulSoup, analysis: Dict):
        """Check basic accessibility"""
        # Alt text for images
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        
        if images_without_alt:
            alt_percentage = (len(images_without_alt) / len(images)) * 100
            if alt_percentage > 50:
                analysis['issues'].append(f'Many images missing alt text ({int(alt_percentage)}%)')
                analysis['recommendations'].append('Add descriptive alt text to images for accessibility')
    
    def _calculate_score(self, analysis: Dict) -> int:
        """Calculate overall website score (0-100)"""
        score = 100
        
        # Deduct points for issues
        if not analysis['has_ssl']:
            score -= 25
        if not analysis['mobile_friendly']:
            score -= 20
        if analysis['load_time'] > 5:
            score -= 15
        elif analysis['load_time'] > 3:
            score -= 10
        
        # Deduct for each issue found
        score -= min(len(analysis['issues']) * 5, 30)
        
        # Bonus for modern tech
        modern_tech_count = len([tech for tech in analysis['tech_stack'] 
                               if tech in ['React', 'Vue.js', 'Angular', 'Tailwind CSS']])
        score += min(modern_tech_count * 5, 15)
        
        return max(0, min(100, score))
