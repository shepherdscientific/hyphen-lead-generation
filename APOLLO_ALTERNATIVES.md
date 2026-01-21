# Apollo Alternatives: Free & Low-Cost Lead Generation

## Apollo Pricing Quick Ref

```
Free: 25 email credits/month, no API
Basic ($49/mo): 500 credits, no API
Professional ($99/mo): 1000 credits, API access ← What you'd need
Organization ($149/mo): 2000 credits, team features
```

**What you're paying for:**
- B2B contact database (275M contacts)
- Email/phone finder
- Company intelligence
- **The data**, not the technology

---

## Alternative Strategy: Build Your Own

**Core insight:** Apollo = Data aggregation + UI

**You can replicate:**
- ✅ LinkedIn scraping (free data source)
- ✅ Company website scraping (free)
- ✅ Email finding algorithms (pattern matching + verification)
- ✅ AI-powered enrichment (you have Ollama!)
- ✅ Lead scoring (your LLM)

**Cost:** $0-50/month vs Apollo's $99/month

---

## Option 1: Intelligent LinkedIn Scraper (FREE)

### What LinkedIn Provides

**Public data available:**
- Company names, sizes, locations
- Employee names, titles
- Company pages (industry, description)
- Job postings (hiring signals)
- Post activity (engagement signals)

**Challenge:** LinkedIn blocks scrapers aggressively

**Solution:** Smart, human-like scraping

---

### Implementation: Selenium with Stealth

```python
"""
LinkedIn Intelligent Scraper
Mimics human behavior to avoid detection
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import random
from typing import List, Dict

class LinkedInScraper:
    """
    Scrape LinkedIn company pages and employee data
    Uses stealth mode and human-like behavior
    """
    
    def __init__(self, email: str, password: str):
        """Initialize with LinkedIn credentials"""
        
        # Setup Chrome with stealth
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        
        # Apply stealth settings
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        self.email = email
        self.password = password
        self.logged_in = False
    
    def login(self):
        """Login to LinkedIn"""
        print("🔐 Logging into LinkedIn...")
        
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(random.uniform(2, 4))  # Random delay
        
        # Enter credentials with human-like delays
        email_field = self.driver.find_element(By.ID, 'username')
        self._human_type(email_field, self.email)
        
        time.sleep(random.uniform(0.5, 1.5))
        
        password_field = self.driver.find_element(By.ID, 'password')
        self._human_type(password_field, self.password)
        
        time.sleep(random.uniform(0.5, 1.5))
        
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        )
        submit_button.click()
        
        time.sleep(random.uniform(3, 5))
        self.logged_in = True
        print("✅ Logged in successfully")
    
    def search_companies(
        self,
        keywords: str,
        location: str = "Nigeria",
        company_size: str = "11-50"
    ) -> List[Dict]:
        """
        Search for companies matching criteria
        
        Args:
            keywords: Search terms (e.g., "fintech")
            location: Company location
            company_size: Employee count range
        
        Returns:
            List of company data dicts
        """
        if not self.logged_in:
            self.login()
        
        print(f"🔍 Searching for: {keywords} in {location}")
        
        # Build search URL with filters
        search_url = f"https://www.linkedin.com/search/results/companies/"
        search_url += f"?keywords={keywords}"
        search_url += f"&origin=GLOBAL_SEARCH_HEADER"
        
        self.driver.get(search_url)
        self._random_sleep(3, 5)
        
        # Scroll to load more results (human-like)
        self._scroll_page()
        
        # Extract company cards
        companies = []
        company_elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            '.entity-result'
        )
        
        for elem in company_elements[:50]:  # Limit to 50 to avoid detection
            try:
                company = self._extract_company_data(elem)
                companies.append(company)
                
                # Random small delay between extractions
                time.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                print(f"Error extracting company: {e}")
                continue
        
        print(f"✅ Found {len(companies)} companies")
        return companies
    
    def get_company_employees(
        self,
        company_url: str,
        titles: List[str] = ["CTO", "CEO", "Founder"]
    ) -> List[Dict]:
        """
        Get employee data from company page
        
        Args:
            company_url: LinkedIn company page URL
            titles: Job titles to search for
        
        Returns:
            List of employee dicts
        """
        print(f"👥 Getting employees from: {company_url}")
        
        employees = []
        
        for title in titles:
            # Navigate to people search for this company + title
            search_url = f"{company_url}/people/"
            search_url += f"?keywords={title}"
            
            self.driver.get(search_url)
            self._random_sleep(2, 4)
            
            # Extract people
            people_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                '.org-people-profile-card'
            )
            
            for elem in people_elements[:10]:  # Limit per title
                try:
                    person = self._extract_person_data(elem)
                    person['company_url'] = company_url
                    employees.append(person)
                    
                    time.sleep(random.uniform(0.2, 0.5))
                    
                except Exception as e:
                    print(f"Error extracting person: {e}")
                    continue
        
        print(f"✅ Found {len(employees)} employees")
        return employees
    
    def _human_type(self, element, text: str):
        """Type like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def _random_sleep(self, min_sec: float, max_sec: float):
        """Random sleep to mimic human behavior"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def _scroll_page(self):
        """Scroll page like a human"""
        # Scroll down gradually
        scroll_pause = random.uniform(0.5, 1.5)
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )
        
        for _ in range(3):  # Scroll 3 times
            # Scroll down
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(scroll_pause)
            
            # Calculate new height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            
            if new_height == last_height:
                break
            
            last_height = new_height
    
    def _extract_company_data(self, element) -> Dict:
        """Extract data from company card element"""
        try:
            name = element.find_element(
                By.CSS_SELECTOR,
                '.entity-result__title-text a'
            ).text
            
            # Try to get other fields
            try:
                tagline = element.find_element(
                    By.CSS_SELECTOR,
                    '.entity-result__primary-subtitle'
                ).text
            except:
                tagline = None
            
            try:
                location = element.find_element(
                    By.CSS_SELECTOR,
                    '.entity-result__secondary-subtitle'
                ).text
            except:
                location = None
            
            try:
                url = element.find_element(
                    By.CSS_SELECTOR,
                    '.entity-result__title-text a'
                ).get_attribute('href')
            except:
                url = None
            
            return {
                'name': name,
                'tagline': tagline,
                'location': location,
                'linkedin_url': url
            }
            
        except Exception as e:
            print(f"Error in extraction: {e}")
            return {}
    
    def _extract_person_data(self, element) -> Dict:
        """Extract data from person card element"""
        try:
            name = element.find_element(
                By.CSS_SELECTOR,
                '.org-people-profile-card__profile-title'
            ).text
            
            title = element.find_element(
                By.CSS_SELECTOR,
                '.artdeco-entity-lockup__subtitle'
            ).text
            
            profile_url = element.find_element(
                By.CSS_SELECTOR,
                'a[data-control-name="people_profile_card_click"]'
            ).get_attribute('href')
            
            return {
                'name': name,
                'title': title,
                'linkedin_url': profile_url
            }
            
        except Exception as e:
            print(f"Error extracting person: {e}")
            return {}
    
    def quit(self):
        """Close browser"""
        self.driver.quit()


# Usage example
scraper = LinkedInScraper(
    email='your@email.com',
    password='your_password'
)

# Search for fintech companies in Nigeria
companies = scraper.search_companies(
    keywords='fintech',
    location='Nigeria',
    company_size='11-50'
)

# For each company, get decision makers
all_leads = []
for company in companies[:10]:  # Process first 10
    employees = scraper.get_company_employees(
        company['linkedin_url'],
        titles=['CEO', 'CTO', 'Founder', 'VP Engineering']
    )
    all_leads.extend(employees)
    
    # Be respectful - don't hammer LinkedIn
    time.sleep(random.uniform(5, 10))

scraper.quit()

print(f"✅ Extracted {len(all_leads)} leads")
```

**Pros:**
- ✅ Free (just your time)
- ✅ Fresh data (real-time)
- ✅ Flexible (any search criteria)
- ✅ No API limits

**Cons:**
- ❌ Slower than API
- ❌ Risk of account suspension (use fake account!)
- ❌ Maintenance needed (LinkedIn changes UI)
- ❌ Needs active LinkedIn account

**Best practices:**
- Use a separate LinkedIn account (not your main)
- Respect rate limits (max 100 searches/day)
- Add random delays (mimic human)
- Rotate user agents
- Use residential proxies if scraping at scale

---

## Option 2: Email Finding - Free Pattern Matching

### How Email Finding Works

**Most companies follow patterns:**
```
firstname@company.com
firstname.lastname@company.com
f.lastname@company.com
firstnamelastname@company.com
```

**Strategy:**
1. Generate possible email patterns
2. Verify which ones exist
3. Return verified email

---

### Implementation: Email Guesser + Verifier

```python
"""
Email Finder - Pattern Matching + Verification
Free alternative to Hunter.io
"""

import smtplib
import dns.resolver
import re
from typing import List, Optional
import requests
from email_validator import validate_email, EmailNotValidError

class EmailFinder:
    """
    Find and verify email addresses using pattern matching
    """
    
    # Common email patterns
    PATTERNS = [
        '{first}@{domain}',
        '{first}.{last}@{domain}',
        '{f}{last}@{domain}',
        '{first}{last}@{domain}',
        '{last}.{first}@{domain}',
        '{first}_{last}@{domain}',
        '{f}.{last}@{domain}',
        '{first}{l}@{domain}'
    ]
    
    def find_email(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> Optional[str]:
        """
        Find email address for person at company
        
        Args:
            first_name: First name
            last_name: Last name
            domain: Company domain (e.g., "company.com")
        
        Returns:
            Verified email or None
        """
        first = first_name.lower().strip()
        last = last_name.lower().strip()
        f = first[0] if first else ''
        l = last[0] if last else ''
        
        # Generate possible emails
        candidates = []
        for pattern in self.PATTERNS:
            try:
                email = pattern.format(
                    first=first,
                    last=last,
                    f=f,
                    l=l,
                    domain=domain
                )
                candidates.append(email)
            except:
                continue
        
        # Remove duplicates
        candidates = list(set(candidates))
        
        print(f"🔍 Testing {len(candidates)} email patterns for {first} {last}")
        
        # Verify each candidate
        for email in candidates:
            if self.verify_email(email):
                print(f"✅ Found: {email}")
                return email
        
        print(f"❌ No valid email found")
        return None
    
    def verify_email(self, email: str) -> bool:
        """
        Verify if email exists
        Uses MX record check + SMTP verification
        """
        
        # Step 1: Validate format
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            return False
        
        # Step 2: Check MX records
        domain = email.split('@')[1]
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                return False
            
            mx_host = str(mx_records[0].exchange)
        except:
            return False
        
        # Step 3: SMTP verification (careful - can be detected!)
        try:
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_host)
            server.helo('example.com')
            server.mail('test@example.com')
            code, message = server.rcpt(email)
            server.quit()
            
            # Code 250 = email exists
            # Code 550 = email doesn't exist
            return code == 250
            
        except Exception as e:
            # If SMTP verification fails, assume email exists
            # (Many servers block SMTP verification)
            return True
    
    def find_emails_from_company_website(self, domain: str) -> List[str]:
        """
        Scrape company website for email addresses
        """
        emails = set()
        
        try:
            # Get website content
            response = requests.get(
                f'https://{domain}',
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            # Extract emails using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found = re.findall(email_pattern, response.text)
            
            # Filter to domain only
            for email in found:
                if domain in email.lower():
                    emails.add(email.lower())
            
        except Exception as e:
            print(f"Error scraping website: {e}")
        
        return list(emails)


# Usage
finder = EmailFinder()

# Find email for person
email = finder.find_email(
    first_name='John',
    last_name='Doe',
    domain='example.com'
)

# Or scrape website for any emails
emails = finder.find_emails_from_company_website('example.com')
```

**Pros:**
- ✅ Free (no API costs)
- ✅ Works for most companies
- ✅ High accuracy if pattern is correct

**Cons:**
- ❌ SMTP verification can be blocked
- ❌ Slower than API (one-by-one checking)
- ❌ May trigger spam filters if overdone

**Best practices:**
- Limit SMTP verification (100/day max)
- Use MX check only for initial validation
- Cache results to avoid re-verification
- Combine with website scraping for context

---

## Option 3: Paid Alternatives (Cheaper than Apollo)

### Hunter.io - Best Value

**Pricing:**
```
Free: 25 searches/month
Starter ($49/mo): 500 searches
Growth ($99/mo): 2,500 searches
Pro ($199/mo): 10,000 searches
```

**What you get:**
- Email finder (pattern detection)
- Email verifier
- Domain search (find all emails at domain)
- API access (even free tier!)
- Bulk operations

**Accuracy:** 95%+  
**Coverage:** 100M+ emails

**Best for:** Email finding specifically

**Use case:** Combine with free LinkedIn scraping:
1. LinkedIn → Get names + companies
2. Hunter.io → Find emails
3. Your LLM → Score leads
4. HubSpot → Store

**Cost:** $49-99/month (vs Apollo $99 for less)

---

### RocketReach

**Pricing:**
```
Free: 5 lookups/month
Essentials ($49/mo): 170 lookups
Pro ($99/mo): 400 lookups
Ultimate ($249/mo): 1,000 lookups
```

**What you get:**
- Emails AND phone numbers
- Social profiles
- Job history
- API access

**Best for:** When you need phone numbers too

---

### Clearbit

**Pricing:**
- Pay-per-lookup: ~$0.50-2.00 per enrichment
- No monthly fee
- Only pay for successful enrichments

**What you get:**
- Company data (size, revenue, tech stack)
- Person data (title, seniority)
- Social profiles
- Technographics

**Best for:** Enriching existing leads, not finding new ones

---

### Snov.io

**Pricing:**
```
Trial: 50 credits free
Starter ($39/mo): 1,000 credits
Pro ($99/mo): 5,000 credits
```

**What you get:**
- Email finder
- Email verifier
- LinkedIn automation
- Drip campaigns
- Chrome extension

**Best for:** All-in-one cheaper alternative

---

## Option 4: AI-Powered Web Scraper (Recommended!)

### Using Your Local LLM for Intelligent Scraping

**Concept:** Traditional scrapers break when websites change. AI-powered scrapers adapt.

```python
"""
AI-Powered Web Scraper
Uses local LLM to understand page structure and extract data
Self-healing - adapts when HTML changes
"""

from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import requests
from bs4 import BeautifulSoup
import json

class AIWebScraper:
    """
    Scrape websites using LLM for intelligent extraction
    """
    
    def __init__(self):
        self.llm = Ollama(
            model='qwen2.5-coder:32b',
            temperature=0.1
        )
        
        self.extraction_prompt = PromptTemplate(
            input_variables=['html', 'target'],
            template="""
Extract {target} from this HTML.

HTML:
{html}

Return JSON array of objects with relevant fields.
If no data found, return empty array [].

Output only valid JSON, no explanation.
"""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.extraction_prompt)
    
    def scrape_company_page(self, url: str) -> dict:
        """
        Scrape company website for contact information
        """
        print(f"🌐 Scraping: {url}")
        
        # Get page content
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            html = response.text
        except Exception as e:
            print(f"Error fetching page: {e}")
            return {}
        
        # Use BeautifulSoup to clean HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts, styles
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        
        # Get main content (limit to 5000 chars for LLM)
        clean_html = str(soup.body)[:5000] if soup.body else str(soup)[:5000]
        
        # Extract emails
        emails = self._extract_with_ai(clean_html, 'email addresses')
        
        # Extract phone numbers
        phones = self._extract_with_ai(clean_html, 'phone numbers')
        
        # Extract team members
        team = self._extract_with_ai(clean_html, 'team members with names and titles')
        
        return {
            'url': url,
            'emails': emails,
            'phones': phones,
            'team': team
        }
    
    def _extract_with_ai(self, html: str, target: str) -> list:
        """Use LLM to extract specific data"""
        try:
            result = self.chain.run(html=html, target=target)
            
            # Clean response
            result = result.strip()
            if result.startswith('```'):
                result = result.split('```')[1]
                if result.startswith('json'):
                    result = result[4:]
            
            # Parse JSON
            data = json.loads(result)
            return data if isinstance(data, list) else [data]
            
        except Exception as e:
            print(f"AI extraction error: {e}")
            return []


# Usage
scraper = AIWebScraper()

# Scrape company website
data = scraper.scrape_company_page('https://example.com')

print(json.dumps(data, indent=2))
# {
#   "url": "https://example.com",
#   "emails": ["info@example.com", "sales@example.com"],
#   "phones": ["+234 803 123 4567"],
#   "team": [
#     {"name": "John Doe", "title": "CEO"},
#     {"name": "Jane Smith", "title": "CTO"}
#   ]
# }
```

**Why this is powerful:**
- ✅ Adapts to any website structure
- ✅ No brittle CSS selectors
- ✅ Understands context ("CEO" vs "CEO email")
- ✅ Self-healing (website changes → still works)
- ✅ Uses your local LLM (free!)

**Limitations:**
- ⚠️ Slower than traditional scraping
- ⚠️ Uses LLM tokens (but free with Ollama)
- ⚠️ Need good HTML cleaning (reduce token usage)

---

## Recommended Combo Strategy

### Free Tier Approach

**Month 1 (Proving Concept):**
```
1. LinkedIn scraping (free)
   → Get 100 company names + employee names
   
2. AI web scraper (free)
   → Scrape company websites for emails
   
3. Email pattern matcher (free)
   → Guess/verify emails if not found on website
   
4. Your LLM scoring (free)
   → Score leads
   
5. HubSpot sync (free)
   → Store leads

Cost: $0/month
Time: ~10 hours to build
Leads: ~50-100/month (manual effort)
```

---

### Low-Cost Approach

**Month 2+ (Scaling Up):**
```
1. LinkedIn scraping (free)
   → Get 200 company names + employee names
   
2. Hunter.io Starter ($49/mo)
   → 500 email searches
   → High accuracy
   → API automation
   
3. Your LLM scoring (free)
   → Score leads
   
4. HubSpot sync (free)
   → Store leads

Cost: $49/month
Time: Mostly automated
Leads: ~200-500/month
```

---

### Best ROI Approach

**Month 3+ (Proven Value):**
```
1. Apollo Professional ($99/mo) OR Hunter Growth ($99/mo)
   → 1,000-2,500 credits
   → Full API access
   → High-quality data
   
2. Your LLM enrichment (free)
   → Add custom scoring
   → Generate outreach copy
   
3. HubSpot sync (free)
   → Store leads

Cost: $99/month
Time: Fully automated
Leads: 500-1,000/month
Quality: High
```

---

## DIY Stack Comparison

| Method | Cost/Month | Setup Time | Leads/Month | Quality | Maintenance |
|--------|------------|------------|-------------|---------|-------------|
| **LinkedIn Scraper** | $0 | 8 hours | 50-100 | Medium | High |
| **Email Pattern Matcher** | $0 | 4 hours | N/A | Medium | Low |
| **AI Web Scraper** | $0 | 6 hours | 50-100 | Medium | Low |
| **Hunter.io Starter** | $49 | 2 hours | 200-500 | High | Low |
| **Apollo Professional** | $99 | 1 hour | 500-1000 | High | None |
| **DIY Full Stack** | $0 | 20 hours | 100-200 | Medium | Medium |
| **Hybrid (Scrape + Hunter)** | $49 | 10 hours | 300-600 | High | Low |

---

## My Recommendation

### For You (Hyphen Partners):

**Phase 1 (This Month):**
```
Build the free DIY stack:
✅ LinkedIn scraper
✅ Email pattern matcher
✅ AI web scraper (using your M4 Pro)
✅ LLM scoring

Investment: 20 hours of development
Cost: $0/month
Output: 100-200 leads/month
Purpose: Prove the concept works
```

**Phase 2 (Next Month):**
```
Add Hunter.io Starter ($49/mo):
✅ 500 email searches via API
✅ Keep free LinkedIn scraping
✅ Keep LLM scoring

Investment: 2 hours integration
Cost: $49/month
Output: 300-600 leads/month
Purpose: Scale up quality
```

**Phase 3 (When Proven):**
```
Evaluate Apollo Pro ($99/mo):
✅ If your leads generate >$1000/month value
✅ If time saved > $99 value
✅ If data quality significantly better

Purpose: Maximize efficiency
```

---

## Code to Build This Week

**Priority 1:** LinkedIn scraper (8 hours)
- Most valuable free data source
- Reusable for all B2B lead gen
- Works for Nigeria, US, anywhere

**Priority 2:** AI web scraper (6 hours)
- Leverages your M4 Pro
- Self-healing
- Very flexible

**Priority 3:** Email pattern matcher (4 hours)
- Simple but effective
- Complements scrapers well
- 60-70% success rate

**Total: 18 hours = 1 weekend of work**

---

## Legal & Ethical Notes

**LinkedIn scraping:**
- ⚠️ Against LinkedIn TOS
- Use separate account (not your main)
- Don't sell the data
- Respect rate limits
- Use for B2B outreach only

**Email verification:**
- ✅ Legal to verify emails
- ⚠️ Don't spam them
- ✅ Use for B2B only
- ⚠️ Respect CAN-SPAM, GDPR

**Web scraping:**
- ✅ Public websites are fair game
- ⚠️ Respect robots.txt
- ✅ Use for business intelligence
- ⚠️ Don't overload servers

**General principle:**
- Use data for legitimate B2B outreach
- Provide opt-out mechanisms
- Don't sell/share the data
- Respect privacy requests

---

## Want Me To Build Any of These?

**I can create:**
1. ✅ LinkedIn scraper (production-ready)
2. ✅ Email finder + verifier
3. ✅ AI web scraper
4. ✅ Integration with your lead system
5. ✅ Complete DIY alternative to Apollo

**Just let me know which you want first!** 🚀
