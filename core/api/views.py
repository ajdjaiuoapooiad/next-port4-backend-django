from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import DeviceSerializer

from ..models import Post, Job
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time



class TaskCreateListAPIView(views.APIView):
  """ Taskモデルの登録API """
  def get(self, request, *args, **kwargs):
     """ Taskモデルの一覧取得API """
     # 複数のobjectの場合、many=Trueを指定します
    #  scrape_createJob()
     serializer = DeviceSerializer(instance=Job.objects.all(), many=True)
     return Response(serializer.data, status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    # JSON文字列をレスポンスとして返す
    serializer = DeviceSerializer(data=request.data)
    # バリデーション実行
    serializer.is_valid(raise_exception=True)
    # モデルオブジェクトを登録
    serializer.save()
    # JSON文字列をレスポンスとして返す
    return Response(serializer.data, status.HTTP_201_CREATED)




@csrf_exempt
def JobsPage(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            jobs = scrape_jobs(url)
            data = {'jobs': jobs}
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
            return JsonResponse({'error': 'POSTリクエストのみ受け付けます'}, status=405)
    
@csrf_exempt
def CreateJobsPage(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            jobs = scrape_createJob(url)
            # jobs = Job.objects.all()
            data = {'jobs': jobs}
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
            return JsonResponse({'error': 'POSTリクエストのみ受け付けます'}, status=405)



class TaskRetrieveUpdataDestroyAPIView(views.APIView):
  """ Taskモデルのpk APIクラス """

  def get(self, request, pk, *args, **kwargs):
    """ Taskモデルの詳細取得API """
    # モデルオブジェクトを取得
    task = get_object_or_404(Job, pk=pk)
    serializer = DeviceSerializer(instance=task)
    return Response(serializer.data, status.HTTP_200_OK)

  def put(self, request, pk, *args, **kwargs):
    """ Taskモデルの更新API """
    task = get_object_or_404(Job, pk=pk)
    serializer = DeviceSerializer(instance=task, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)

  def patch(self, request, pk, *args, **kwargs):
    """ Taskモデルの更新API """
    task = get_object_or_404(Job, pk=pk)
    # partial=Trueにより、request.dataで指定したデータのみ更新される
    serializer = DeviceSerializer(instance=task, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)

  def delete(self, request, pk, *args, **kwargs):
    """ Taskモデルの削除API """
    task = get_object_or_404(Job, pk=pk)
    task.delete()
    return Response(status.HTTP_200_OK)
  




def scrape_jobs2(url):
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
    return  data

def scrape_jobs(url):
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






def scrape_createJob(url):
    amazonURL = url
    amazonPage = requests.get(amazonURL)
    soup = BeautifulSoup(amazonPage.text, "html.parser")
    data = []
    spots = soup.find_all('li', class_='ProjectListJobPostsLaptop__ProjectListItem-sc-79m74y-12 irQOzL')
    for spot in spots:
        status = '応募中'
        company = spot.find('p', class_='JobPostCompanyWithWorkingConnectedUser__CompanyNameText-sc-1nded7v-5 hIALDA wui-reset wui-text wui-text-body2').text
        places = soup.find_all('ul', class_="ListWithMore__Ul-sc-1968quv-1 eKMonf")
        # place = places('li', class_="ListItem__Li-sc-1ty6hrk-0 ListItem__SelectableLi-sc-1ty6hrk-3 cTnFUW bcGmGW wui-reaction-by-color wui-reaction-overlay-black wui-text-body2 wui-listItem wui-listItem-dence")
        place = places[1].find('li', {'aria-selected': 'true'}).text
        
        # print(title)
        # print(company)
        # print(place)
        # detum = {
        #     'title': title,
        #     'company': company,
        #     'place': place,
        # }
        detum = {}
        detum['status'] = status
        detum['company'] = company
        detum['place'] = place
        data.append(detum)
        Job.objects.create(status=detum['status'], company=detum['company'], place=detum['place'])
    # print(data[0]['title'])
    return data

