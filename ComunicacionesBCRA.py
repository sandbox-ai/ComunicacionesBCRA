import os, re
import requests
from bs4 import BeautifulSoup
import logging
import urllib3
from time import sleep

# Disable warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ScrapperBCRA:
    base_url = "https://www.bcra.gob.ar/SistemasFinancierosYdePagos/Buscador_por_tipo.asp"
    
    def __init__(self, max_retries=3):
        self.pdf_urls = []
        self.max_retries = max_retries

    def scrape_urls(self, tipo, stop_at_existing=False):
        page = 1
        params = {
            'tipo': tipo,
            'tamanopagina': 50,
            'paginaabsoluta': 1
        }
        existing_urls = set()
        
        # Load existing URLs if the file exists
        filename = f'BCRA_{tipo}.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                existing_urls = set(file.read().splitlines())
        
        while True:
            logging.info(f"Scraping page {page} for tipo {.tipo}")
            response = requests.get(self.base_url, params=params, verify=False)
            
            if response.status_code != 200:
                logging.error(f"Failed to retrieve page {page}")
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.select('.table tr > td:nth-of-type(2) > a')

            if not links:
                logging.info("No more links found, stopping.")
                logging.debug(soup.text)
                break

            for link in links:
                url = link['href']
                if stop_at_existing and url in existing_urls:
                    logging.info(f"Existing URL {url} found, stopping.")
                    return
                self.pdf_urls.append(url)
                logging.info(f"Found PDF URL: {url}")

            params['paginaabsoluta'] += 1
            page += 1
        logging.info(f"Scraped {len(self.pdf_urls)} new PDF URLs for tipo {tipo}.")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for url in self.pdf_urls:
                file.write(f"{url}\n")
        logging.info(f"Saved {len(self.pdf_urls)} PDF URLs to {filename}")

    def scrape_pdfs_naive(self, tipo):
        if not os.path.exists(f'{tipo}'):
            os.makedirs(f'{tipo}')
        
        params = {
            'tipo': tipo,
            'tamanopagina': 50,
            'paginaabsoluta': 1
        }
        response = requests.get(self.base_url, params=params, verify=False)
            
        if response.status_code != 200:
            logging.error(f"Failed to retrieve page")
            
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.table tr > td:nth-of-type(2) > a')
        latest_url = links[0]['href']
        match = re.search(r'\b[A-Z]\d+\b', latest_url)
        latest = match.group(0)[1:]
        retries = 0
        for n in range(int(latest), 0, -1):
                try:
                    file_path = f'{tipo}/{tipo}{str(n).zfill(4)}.pdf'
                    if os.path.exists(file_path):
                        logging.info(f"PDF {file_path} already exists, skipping...")
                        continue
                    url = f'https://www.bcra.gob.ar/Pdfs/comytexord/{tipo}{str(n).zfill(4)}.pdf'
                    response = requests.get(url, verify=False)
                    if response.status_code == 200:
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                    else:
                        retries += 1
                        logging.warning(f"Failed to download {url}, retry {retries}/{self.max_retries}")
                        sleep(2)
                except requests.exceptions.RequestException as e:
                    retries += 1
                    logging.error(f"Request exception: {e}, retry {retries}/{self.max_retries}")
                    sleep(2)
        
def main():
    tipos = ['A', 'B', 'C', 'P']
    for tipo in tipos:
        scrapper = ScrapperBCRA()
        scrapper.scrap_pdfs_naive(tipo)

if __name__ == "__main__":
    main()
