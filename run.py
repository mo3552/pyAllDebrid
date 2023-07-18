import urllib.request
import json
from tqdm import tqdm
from colorama import init, Fore
import os

# colorama init
init()

# clear screen at download start
os.system('cls')

while True:

    # enter download link
    link = input("다운로드 링크 "+Fore.CYAN +
                 "(종료는 Q 입력)"+Fore.RESET+" : ")

    # exit the program by typing 'q' key
    if link.lower() == "q":
        print('Exit the program.')
        break

        # check the download link
    if not link.startswith(("http://", "https://")):
        print(
            Fore.RED + "잘못된 링크 입니다. http:// 또는 https:// 는 필수로 입력되어야 합니다." + Fore.RESET+"\n")
        continue

    apiEndpoint = "https://api.alldebrid.com/v4/link/unlock?agent=MYAGENT&apikey=APIKEY=" + \
        urllib.parse.quote(link)
    apiEndpointWithPassword = "https://api.alldebrid.com/v4/link/unlock?agent=MYAGENT&apikey=APIKEY&link=" + \
        urllib.parse.quote(link) + "&password=" + \
        urllib.parse.quote('MY PASSWORD')

    try:
        response = urllib.request.urlopen(apiEndpoint)
        if response.status == 400:
            print("잘못된 요청입니다. 다른 링크를 입력하세요.")
            continue

        data = response.read().decode('utf-8')
        response = json.loads(data)

        # response download file
        download_url = response['data']['link']
        file_name = response['data']['filename']  # 다운로드 받을 파일 이름과 확장자

        # show download progress
        os.system('cls')
        response = urllib.request.urlopen(download_url)
        total_size = int(response.headers['Content-Length'])
        progress_bar = tqdm(total=total_size, unit='B',
                            unit_scale=True, desc='다운로드 진행 중', ncols=80)

        with open(file_name, 'wb') as file:
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                file.write(chunk)
                progress_bar.update(len(chunk))

        progress_bar.close()
        print("파일 다운로드가 완료되었습니다.\n")

    # handling link exceptions
    except urllib.error.HTTPError as e:
        print(
            Fore.RED + f"HTTP 오류가 발생했습니다: {e.code} {e.reason}\n" + Fore.RESET)
    except urllib.error.URLError as e:
        print(Fore.RED + f"URL 오류가 발생했습니다: {e.reason}\n" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"링크에 파일이 없거나 존재 하지 않는 링크입니다.\n" + Fore.RESET)
