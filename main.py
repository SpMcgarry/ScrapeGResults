import csv
from bs4 import BeautifulSoup
import applescript
import time

#code is result of gpt discussion on how to extract links from results
#you will need bs4 and applescript , the only automation is clicking the next page button and extracting the content
#OSX will require that the IDE or terminal has permission to automate safari  pycharm worked for me Cursor did not. 

def get_safari_content():
    script = '''
    tell application "Safari"
        set pageSource to source of current tab of window 1
    end tell
    return pageSource
    '''
    scpt = applescript.AppleScript(script)
    return scpt.run()


def extract_google_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for item in soup.select('div.g'):
        link = item.find('a', href=True)
        description = item.find('div', class_='VwiC3b')
        if link and description:
            results.append((link['href'], description.text.strip()))
    return results


def click_next_page():
    script = '''
    tell application "Safari"
        do JavaScript "document.querySelector('#pnnext').click();" in current tab of window 1
    end tell
    '''
    scpt = applescript.AppleScript(script)
    scpt.run()


def main():
    results = []

    # Get initial results
    html = get_safari_content()
    results.extend(extract_google_results(html))

    # Ask user for number of additional pages
    num_pages = int(input("How many more pages do you want to scrape? "))

    # Scrape additional pages
    for _ in range(num_pages):
        click_next_page()
        time.sleep(2)  # Wait for page to load
        html = get_safari_content()
        results.extend(extract_google_results(html))

    # Save results to CSV
    with open('google_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Link', 'Description'])
        writer.writerows(results)

    print(f"Results saved to google_results.csv in the script's directory.")


if __name__ == "__main__":
    main()

