import re
import tldextract

# List of common phishing keywords
PHISHING_KEYWORDS = [
    "urgent", "verify your account", "account locked", "click here", 
    "sensitive information", "confirm your password", 
    "update your information", "verify your identity"
]

# List of trusted domain popular sites
TRUSTED_DOMAINS = [
    "facebook.com", "google.com", "amazon.com", "paypal.com", "microsoft.com",
    "apple.com", "twitter.com", "instagram.com", "linkedin.com", "youtube.com",
    "netflix.com", "spotify.com", "whatsapp.com", "tiktok.com", "dropbox.com",
    "github.com", "slack.com", "zoom.us", "yahoo.com", "icloud.com",
    "adobe.com", "oracle.com", "ibm.com", "salesforce.com", "snapchat.com",
    "bing.com", "wikipedia.org", "ebay.com", "reddit.com", "twitch.tv",
    "nytimes.com", "bbc.com", "cnn.com", "washingtonpost.com", "bloomberg.com",
    "walmart.com", "target.com", "bestbuy.com", "homedepot.com", "lowes.com",
    "bankofamerica.com", "chase.com", "wellsfargo.com", "citibank.com", "usbank.com",
    "capitolone.com", "americanexpress.com", "discover.com", "paypal.com", "squareup.com",
    "venmo.com", "zellepay.com", "amex.com", "navient.com", "fidelity.com",
    "vanguard.com", "etrade.com", "robinhood.com", "charles-schwab.com", "coinbase.com",
    "binance.com", "kraken.com", "okta.com", "godaddy.com", "bluehost.com",
    "shopify.com", "airbnb.com", "booking.com", "expedia.com", "tripadvisor.com",
    "uber.com", "lyft.com", "doordash.com", "grubhub.com", "postmates.com",
    "starbucks.com", "mcdonalds.com", "burgerking.com", "dominos.com", "subway.com",
    "nasa.gov", "whitehouse.gov", "irs.gov", "cdc.gov", "nih.gov",
    "npr.org", "ted.com", "kickstarter.com", "patreon.com", "medlineplus.gov"
]


# Function to scan email for phishing keywords
def check_phishing_keywords(email_content):
    found_keywords = []
    for keyword in PHISHING_KEYWORDS:
        if re.search(rf"\b{keyword}\b", email_content, re.IGNORECASE):
            found_keywords.append(keyword)
    return found_keywords

# function to extracts URLs from email
def extract_urls(email_content):
    url_pattern= r'(https?://[^\s]+)'
    urls= re.findall(url_pattern, email_content)
    return urls

# function to analyze URLs
def analyze_urls(urls):
    suspicious_urls= []
    for url in urls:
        # here we extract domain and subdomain from url
        domain_info= tldextract.extract(url)
        domain= f"{domain_info.domain}.{domain_info.suffix}"

        #here we check domain is similar to any trusted domains
        if domain not in TRUSTED_DOMAINS:
            suspicious_urls.append(url)
    return suspicious_urls


# read email content from the file
def read_email_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content= file.read()
        return email_content
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

# main function to check phishing keyword from the file and suspicious URLs
def main(file_path):
    email_content= read_email_from_file(file_path)
    if email_content:
        phishing_keywords_found = check_phishing_keywords(email_content)
        if phishing_keywords_found:
          print("Potential phishing keywords found:", phishing_keywords_found)
        else:
          print("No phishing keywords found.")

        # here we extract and analyze URLs
        urls= extract_urls(email_content)
        if urls:
            suspicious_urls= analyze_urls(urls)
            if suspicious_urls:
                print("Suspicious URLs found:", suspicious_urls)
            else:
                print("No suspicious URLs found.")
        else:
            print("No URLs found in the email")
    else:
        print("No content to check")

# rum main function with file path
if __name__ == "__main__":
    main("email_content.txt")