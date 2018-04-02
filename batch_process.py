from selenium import webdriver
from price_finder import price_finder,BS
def get_prices(links):
    try:
        opts = webdriver.chrome.options.Options()
        opts.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options = opts,headless= True)
        results = []
        for link in links:
            driver.get(link)
            try:
                results.append(
                    price_finder(
                        url = link,bs=BS(driver.page_source,'lxml')
                        )
                    )
            except AttributeError:
                results.append(price_finder(link))
        driver.quit()
        return results
    except Exception as excpt:
        driver.quit()
        raise excpt
if __name__ == "__main__":
    
    import saveto
    links  = saveto.load('quad_links')
    products = get_prices(links)
