import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
def scrape_and_save():
    amazonURL = 'https://www.wantedly.com/projects?new=true&page=1&occupationTypes=jp__engineering&hiringTypes=internship&areas=kyoto&order=mixed'

    amazonPage = requests.get(amazonURL)
    soup = BeautifulSoup(amazonPage.text, "html.parser")
    data = []
    spots = soup.find_all('li', class_='ProjectListJobPostsLaptop__ProjectListItem-sc-79m74y-12 irQOzL')
    for spot in spots:
        title = spot.find('h2', class_='ProjectListJobPostItem__TitleText-sc-bjcnhh-5 gCpJyB wui-reset wui-text wui-text-headline2').text
        company = spot.find('p', class_='JobPostCompanyWithWorkingConnectedUser__CompanyNameText-sc-1nded7v-5 hIALDA wui-reset wui-text wui-text-body2').text
        places = soup.find_all('ul', class_="ListWithMore__Ul-sc-1968quv-1 eKMonf")
        # place = places('li', class_="ListItem__Li-sc-1ty6hrk-0 ListItem__SelectableLi-sc-1ty6hrk-3 cTnFUW bcGmGW wui-reaction-by-color wui-reaction-overlay-black wui-text-body2 wui-listItem wui-listItem-dence")
        place = places[1].find('li', {'aria-selected': 'true'}).text
        
        # print(title)
        # print(company)
        # print(place)
        detum = {
            'title': title,
            'company': company,
            'place': place,
        }
        data.append(detum)
    # print(data[0]['title'])
    print(data)


    # 共通レイアウトここまで
    # 個別レイアウトここから
    # for spot in spots:
    #     spot_name = spot.find(class_='u_title col s12')
    #     spot_name.find('span').extract()
    #     spot_name = spot_name.text.replace('\n','')
    #     rank = float(spot.find(class_='evaluateNumber').text )


    #     categoryItems = spot.find(class_='u_categoryTipsItem col s12')
    #     categoryItems = categoryItems.find_all('dl')

    #     details = {}
    #     for categoryItem in categoryItems:
    #         rank = float(categoryItem.dd.text)
    #         category = categoryItem.dt.text
    #         details[category] = rank

    #     detum = details
    #     detum['観光地名'] = spot_name
    #     detum['評点'] = rank
    #     data.append(detum)
    #     # print(details['楽しさ'])
    #     # jobs = Job.objects.create(spot = detum['観光地名'], rank = detum['評点'], acucess = detum['アクセス'], fun = detum['楽しさ'], many = detum['人混みの多さ'], view = detum['景色'])
 
    # # return data
    # # print(data[0]['楽しさ'])
    # print(data[0])



def scrape_jobs(url):
    amazonURL = url
    amazonPage = requests.get(amazonURL)
    soup = BeautifulSoup(amazonPage.text, "html.parser")
    data = []
    spots = soup.find_all('li', class_='ProjectListJobPostsLaptop__ProjectListItem-sc-79m74y-12 irQOzL')
    for spot in spots:
        title = spot.find('h2', class_='ProjectListJobPostItem__TitleText-sc-bjcnhh-5 gCpJyB wui-reset wui-text wui-text-headline2').text
        company = spot.find('p', class_='JobPostCompanyWithWorkingConnectedUser__CompanyNameText-sc-1nded7v-5 hIALDA wui-reset wui-text wui-text-body2').text
        places = soup.find_all('ul', class_="ListWithMore__Ul-sc-1968quv-1 eKMonf")
        # place = places('li', class_="ListItem__Li-sc-1ty6hrk-0 ListItem__SelectableLi-sc-1ty6hrk-3 cTnFUW bcGmGW wui-reaction-by-color wui-reaction-overlay-black wui-text-body2 wui-listItem wui-listItem-dence")
        place = places[1].find('li', {'aria-selected': 'true'}).text
        
        # print(title)
        # print(company)
        # print(place)
        detum = {
            'title': title,
            'company': company,
            'place': place,
        }
        data.append(detum)
    # print(data[0]['title'])
    print(data)

def scrape_all_amazon_jobs(url):
    driver = webdriver.Chrome()  # または他のブラウザのWebDriver
    driver.get(url)
    time.sleep(3)  # ページの読み込みを待機

    all_jobs = []
    page_num = 1
    max_clicks = 20  # 最大クリック回数（無限ループ防止）
    click_count = 0

    while click_count < max_clicks:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        spots = soup.find_all('li', class_='ProjectListJobPostsLaptop__ProjectListItem-sc-79m74y-12 irQOzL')

        for spot in spots:
            try:
                title = spot.find('h2', class_='ProjectListJobPostItem__TitleText-sc-bjcnhh-5 gCpJyB wui-reset wui-text wui-text-headline2').text
                company = spot.find('p', class_='JobPostCompanyWithWorkingConnectedUser__CompanyNameText-sc-1nded7v-5 hIALDA wui-reset wui-text wui-text-body2').text
                places = soup.find_all('ul', class_="ListWithMore__Ul-sc-1968quv-1 eKMonf")
                place = places[1].find('li', {'aria-selected': 'true'}).text

                job_data = {
                    'title': title,
                    'company': company,
                    'place': place,
                }
                if job_data not in all_jobs: #重複を防ぐため追加する前に確認する。
                    all_jobs.append(job_data)
            except AttributeError as e:
                print(f"要素が見つかりませんでした: {e}")

        try:
            # "Go to next page" ボタンを取得
            next_page_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")

            # disabled 属性の有無で次のページが存在するか判定
            if next_page_button.get_attribute('disabled'):
                print("最後のページです。スクレイピング終了")
                break

            # 次のページへ移動
            next_page_button.click()
            time.sleep(3)  # 次のページの読み込みを待機
            page_num += 1
            click_count += 1
            print(f"ページ {page_num} をスクレイピング中...")

        except NoSuchElementException:
            print("次のページボタンが見つかりません。スクレイピング終了")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            break

    driver.quit()
    return all_jobs



url = 'https://www.wantedly.com/projects?new=true&page=1&occupationTypes=jp__engineering&hiringTypes=internship&areas=kyoto&order=mixed'

jobs = scrape_all_amazon_jobs(url)

for job in jobs:
    print(job)
