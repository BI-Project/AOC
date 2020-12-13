import re
import time

from goose3 import Goose
from selenium import webdriver


def crawl_news():
    start_date_2020 = {
        1: '1/1/2020',
        2: '2/1/2020',
        3: '3/1/2020',
        4: '4/1/2020',
        5: '5/1/2020',
        6: '6/1/2020',
        7: '7/1/2020',
        8: '8/1/2020',
        9: '9/1/2020',
        10: '10/1/2020',
        11: '11/1/2020',
        12: '12/1/2020',
    }
    end_date_2020 = {
        1: '1/31/2020',
        2: '2/28/2020',
        3: '3/31/2020',
        4: '4/30/2020',
        5: '5/31/2020',
        6: '6/30/2020',
        7: '7/31/2020',
        8: '8/31/2020',
        9: '9/30/2020',
        10: '10/31/2020',
        11: '11/30/2020',
        12: '12/31/2020',
    }

    start_date_2019 = {
        1: '1/1/2019',
        2: '2/1/2019',
        3: '3/1/2019',
        4: '4/1/2019',
        5: '5/1/2019',
        6: '6/1/2019',
        7: '7/1/2019',
        8: '8/1/2019',
        9: '9/1/2019',
        10: '10/1/2019',
        11: '11/1/2019',
        12: '12/1/2019',
    }
    end_date_2019 = {
        1: '1/31/2019',
        2: '2/28/2019',
        3: '3/31/2019',
        4: '4/30/2019',
        5: '5/31/2019',
        6: '6/30/2019',
        7: '7/31/2019',
        8: '8/31/2019',
        9: '9/30/2019',
        10: '10/31/2019',
        11: '11/30/2019',
        12: '12/31/2019',
    }
    start_date = [start_date_2020]
    end_date = [end_date_2020]
    end_month = [11]

    year_dict = {
        0: '2020'
    }

    regex = re.compile('[가-힣]+')

    driver = webdriver.Chrome('/home/junseok/jslee/nlp_project/chromedriver')
    driver.get('https://www.google.com/search?safe=active&biw=1533&bih=769&tbm=nws&sxsrf=ALeKk00u4ocQve3BmJSzaCLPbSiZ57KJvQ%3A1607159398449&ei=Zk7LX5D3GrOUr7wPseangAg&q=kpop&oq=kpop&gs_l=psy-ab.3..0l3.5772.6272.0.6757.4.4.0.0.0.0.316.526.2-1j1.2.0....0...1c.1.64.psy-ab..2.2.524....0.tUJdnYNI0zs')
    time.sleep(0.5)

    appbar = driver.find_element_by_class_name('appbar')
    appbar = appbar.find_element_by_id('extabar')
    appbar = appbar.find_element_by_tag_name('div')
    appbar = appbar.find_element_by_class_name('WE0UJf')
    appbar = appbar.find_element_by_id('Rzn5id')
    appbar = appbar.find_element_by_tag_name('div')
    button = appbar.find_element_by_xpath('//a[text()="Change to English"]')
    button.click()
    # search 'koera' and change it to english
    time.sleep(0.5)

    button = driver.find_element_by_xpath('//*[@id="hdtb-tls"]')
    button.click()
    button.click()
    button.click()
    time.sleep(0.5)

    g = Goose()

    for year_iter in range(1):
        #for i in range (3, end_month[year_iter] + 1)
        for i in range (1, 12):
            total_script = ''
            file_name = './' + year_dict[year_iter] + str(i) + '.txt'
            sem_dir = './' + year_dict[year_iter] + '_sem/'

            button = driver.find_element_by_xpath('//*[@id="hdtbMenus"]/div/span[1]/g-popup/div[1]/div/div')
            button.click()
            time.sleep(0.5)

            button = driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[8]/div/div/span')
            button.click()
            time.sleep(0.5)

            input1 = driver.find_element_by_xpath('//*[@id="OouJcb"]')
            input1.clear()
            input1.send_keys(start_date[year_iter][i])
            input2 = driver.find_element_by_xpath('//*[@id="rzG2be"]')
            input2.clear()
            input2.send_keys(end_date[year_iter][i])
            button = driver.find_element_by_xpath('//*[@id="T3kYXe"]/g-button')
            button.click()
            time.sleep(0.5)

            news_end = False
            news_cnt = 0
            news_amount = 200
            for k in range(30):
                data_box = driver.find_element_by_xpath('//*[@id="rso"]')
                class_elements = data_box.find_elements_by_tag_name('g-card')
                for class_element in class_elements:
                    element = class_element.find_element_by_class_name('dbsr')
                    element = element.find_element_by_tag_name('a')
                    url = element.get_attribute('href')
                    print(url)
                    if regex.search(element.text) == None:
                        try:
                            article = g.extract(url=url)
                            total_script += article.cleaned_text

                            file_name_sem = sem_dir + str(i) + '_' + str(news_cnt) + '.txt'
                            with open(file_name_sem, "w") as file:
                                file.write(article.cleaned_text)
                            news_cnt += 1
                        except Exception:
                            print("error!!")
                    if news_cnt == news_amount:
                        break
                if news_cnt == news_amount:
                    break
                foot = driver.find_element_by_id('foot')
                tbody = foot.find_element_by_tag_name('tbody')
                td = tbody.find_elements_by_tag_name('td')
                try:
                    button = td[len(td) - 1].find_element_by_xpath('//span[text()="Next"]')
                    button.click()
                    time.sleep(0.1)
                except Exception:
                    news_end = True
            with open(file_name, "w") as file:
                file.write(total_script)


if __name__ == "__main__":
    crawl_news()
