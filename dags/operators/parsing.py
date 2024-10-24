from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from airflow.decorators import task
import pandas as pd
import logging
import chromedriver_autoinstaller

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений
    handlers=[
        logging.FileHandler('app.log'),  # Сохранение логов в файл
        logging.StreamHandler()          # Вывод логов в консоль
    ]
)

@task(multiple_outputs=True)
def fetch_arxiv_titles_with_safari(url: str) -> pd.DataFrame:
    logging.info("-------- open webdriver ----------")
    remote_webdriver = 'remote_chromedriver'
    driver = webdriver.Remote(
        command_executor=f'{remote_webdriver}:4444/wd/hub',
    )
    logging.info("-------- webdriver opened ----------")
    titles_list = []
    links_list = []
    authors_list = []
    abstract_list = []

    try:
        driver.get(url)
        # Получаем заголовки статей и ссылки для абстрактов
        links_for_abstract = WebDriverWait(driver, 4).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[title="Abstract"]'))
        )

        titles = WebDriverWait(driver, 4).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="list-title mathjax"]'))
        )

        authors = WebDriverWait(driver, 4).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="list-authors"]'))
        )

        if links_for_abstract:
            print(f'Count of titles finded: {len(links_for_abstract)}')
            for i in range(len(titles)):
                title_text = titles[i].text.strip()
                link = links_for_abstract[i].get_attribute('href')
                authors_text = authors[i].text.strip()

                titles_list.append(title_text)
                links_list.append(link)
                authors_list.append(authors_text)

                print(f'Title: {title_text}, Link: {link}\n Authors: {authors_text}')

                # Переход по ссылке на Abstract
                abstract_link = link
                driver.get(abstract_link)

                try:
                    # Ожидание загрузки страницы Abstract
                    abstracts = WebDriverWait(driver, 4).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'blockquote'))
                    )
                    for i in range(len(abstracts)):
                        abstract_text = abstracts[i].text.strip()

                    abstract_list.append(abstract_text)

                    for abstract in abstracts:
                        print(f'Abstract: {abstract.text.strip()}')


                except Exception as e:
                    print(f"Error then load Abstract: {e}")
                finally:
                    # Возвращаемся на страницу со списком заголовков
                    driver.back()

    except Exception as e:
        print(f"Error occured: {e}")

    finally:
        driver.quit()  # Закрываем драйвер после завершения работы

    # Создаем DataFrame из заголовков и ссылок
    df = pd.DataFrame({'Title': titles_list, 'Link': links_list, 'Authors': authors_list, 'Abstract': abstract_list})
    return df
