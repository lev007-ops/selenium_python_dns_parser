from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

domen = 'www.dns-shop.ru'


def get_text(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()


def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument(
        'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    sleep(1)
    generated_html = driver.page_source
    driver.quit()
    return generated_html


def parse():
    src = get_html('https://www.dns-shop.ru/search/?q=%D0%9A%D0%9E%D0%9D%D0%A1%D0%9E%D0%9B%D0%98&stock=soft&category=17a8978216404e77-17a893cd16404e77-17a9f95d16404e77')

    soup = BeautifulSoup(src, 'lxml')

    items = soup.find_all('div', class_='catalog-product')

    result = {'products': []}

    for item in items:
        cart_text = item.find('a', class_='catalog-product__name')
        title = cart_text.text.strip()
        link = domen + cart_text.get('href')
        price = get_text(item.find('div', class_='product-buy__price'))

        result['products'].append({
            'title': title,
            'price': price,
            'link': link
        })
    return result


def main():
    # with open('site.html', 'w', encoding='utf-8') as file:
    #     file.write(get_html(
    #         'https://www.dns-shop.ru/search/?q=%D0%9A%D0%9E%D0%9D%D0%A1%D0%9E%D0%9B%D0%98&stock=soft&category=17a8978216404e77-17a893cd16404e77-17a9f95d16404e77'))

    print(parse())


if __name__ == '__main__':
    main()
