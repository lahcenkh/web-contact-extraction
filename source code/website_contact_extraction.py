import httpx
from selectolax.parser import HTMLParser
import argparse
import os
import csv
from urllib.parse import urlparse
import re

parser = argparse.ArgumentParser(description='This Script is for getting contact from websites')
parser.add_argument('-f', '--file', type=str, help='list of urls csv file')
args = parser.parse_args()

## get file name to porcess
URLS_LIST = args.file

## check file existance
try:
    if not os.path.exists(URLS_LIST):
        raise FileExistsError("File does not exist")
except FileExistsError:
    print(f"The Filename {URLS_LIST} Does Not Exist!")
    exit()

def filter_email(email):
    try:
        
        email_address = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email).group()
        
        return email_address
    except :
        return "Not Found"
    
def get_html(url):
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    try:
        response = httpx.get(url=url, headers=headers, follow_redirects=True, timeout=10.0)
        html = HTMLParser(response.text)
        return html

    except Exception as exc:
        print(f"Error response {exc}")
        return False

  

def get_contact(html, css_selector):
    try:
        contact = html.css_first(css_selector).attributes.get("href")
        return contact
    except:
        return "Not Found"
        
def get_contact_email(html, css_selector):
    try:
        contact = html.css_first(css_selector).attributes.get("href")
        return contact
    except:
        try:
            ctr_email = filter_email(email=html.text())
            return ctr_email
        except:
            return "Not Found"
    

def main():
    contact_list = []
    with open(URLS_LIST, "r") as file_urls:
        website_urls = csv.reader(file_urls)
    
        for url in website_urls:
            print(f"|-------------url: {url[0]}")
            domain = urlparse(url[0]).netloc
            page_html = get_html(url=url[0])
            
            if page_html == False:
                continue
            

            site_contact = {
                str(domain) : {
            "facebook" : get_contact(html=page_html, css_selector="a[href*='facebook.com']"),
            "twitter" : get_contact(html=page_html, css_selector="a[href*='twitter.com']"),
            "email" : filter_email(email=str(get_contact_email(html=page_html, css_selector="a[href^='mailto:']"))),
            "telephone" : get_contact(html=page_html, css_selector="a[href^='tel:']").replace("tel:", ""),
            "linkedin" : get_contact(html=page_html, css_selector="a[href*='linkedin.com']" ),
            "instagram" : get_contact(html=page_html, css_selector="a[href*='instagram.com']"),
            "whatsapp" : get_contact(html=page_html, css_selector="a[href*='wa.me']"),
            "pinterest": get_contact(html=page_html, css_selector="a[href*='pinterest.com']"),
            "youtube": get_contact(html=page_html, css_selector="a[href*='youtube.com']"),
            "tiktok": get_contact(html=page_html, css_selector="a[href*='tiktok.com']"),
            "youtube": get_contact(html=page_html, css_selector="a[href*='youtube.com']"),
            "yelp": get_contact(html=page_html, css_selector="a[href*='yelp.com']"),
            }}

            
            contact_list.append(site_contact)
        
    with open("Report_Contact_website.csv", "w") as report:
        report.write("domain,facebook,twitter,email,telephone,whatsapp,instagram,linkedin,pinterest,youtube,tiktok,yelp\n")
        for cont in contact_list:
            for i in cont.keys():
                report.write(f"{i},{cont[i]['facebook']},{cont[i]['twitter']},{cont[i]['email']},{cont[i]['telephone']},{cont[i]['whatsapp']},{cont[i]['instagram']},{cont[i]['linkedin']},{cont[i]['pinterest']},{cont[i]['youtube']},{cont[i]['tiktok']},{cont[i]['yelp']}\n")


if __name__ == "__main__":
    main()