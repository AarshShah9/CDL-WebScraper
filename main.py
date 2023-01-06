from bs4 import BeautifulSoup
import requests


def main():

    # go to base website
    # find all company sub links by navigating to every div with class "unit"
    # go to each sub link
    # find company name and website link from the sublink

    values = []
    loop_counter = 0

    locations = ['vancouver', 'rockies', 'toronto']
    streams = ['artificial-intelligence', 'blockchain', 'energy', 'crypto', 'fintech', 'health',
               'prime', 'quantum', 'supply-chain', 'space']

    base_url = "https://creativedestructionlab.com/companies/"

    for stream in streams:

        for location in locations:

            if stream == '' and location == '':
                url = base_url

            elif stream == '':
                url = base_url + f"?location={location}"

            elif location == '':
                url = base_url + f"?stream={stream}"

            elif stream != '' and location != '':
                url = base_url + f"?stream={stream}&location={location}"

            source = requests.get(url).text

            soup = BeautifulSoup(source, 'lxml')
            mydivs = soup.find_all("div", {"class": "unit"})

            for div in mydivs:
                loop_counter += 1
                cdlcompany_url = div.find('a')

                if (
                    (cdlcompany_url is not None)
                    and (cdlcompany_url['href'] is not None)
                    and cdlcompany_url['href'].startswith(
                        'https://creativedestructionlab.com/companies/'
                    )
                ):
                    cdlcompany_url = cdlcompany_url['href']
                    company_source = requests.get(cdlcompany_url).text

                    company_soup = BeautifulSoup(company_source, 'lxml')
                    company_website = company_soup.find(
                        'a', {'class': 'company-website-link'})
                    company_name = company_soup.find(
                        'h2', {'class': 'c-primary'})

                    if (company_website is not None) and (company_name is not None):
                        print(
                            f"{company_website['href']} - {company_name.text} - Counter: {loop_counter}\n")

                        values.append(
                            f"{company_name.text} - {company_website['href']}")

    with open('output.txt', 'w') as f:
        for item in values:
            f.write(f"{item}\n")


if __name__ == '__main__':
    main()
