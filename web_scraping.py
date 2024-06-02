import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import re
import configparser


# ログインマネージャ
class LoginManager():
    def __init__(self, login_url, headers):  
        self.login_url = login_url
        self.headers = headers

    # ログイン処理
    def login(self):
        # ログイン情報を読み込む
        self.load_login_info()

        # ログインのPOSTリクエストを送信
        response = requests.post(url=self.login_url, data=self.login_params, headers=self.headers)

        # セッションを開始し、CSRFトークンを取得する
        session = requests.session()

        # リトライ処理
        retries = Retry(total=5,  # リトライ回数
                    backoff_factor=1,  # リトライの間に適用される遅延の時間
                    status_forcelist=[500, 502, 503, 504])  # リトライを強制するHTTPステータスコードのリストを指定
         
        # http と https の両方で使用できるようにマウントする
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        login_page = session.get(self.login_url)
        soup = BeautifulSoup(login_page.content, 'html.parser')

        # セッションクッキーを取得する
        self.cookies = session.cookies
    
        # ログインを試みる
        response = session.post(self.login_url, data=self.login_params)

        # HTMLをBeautiful Soupオブジェクトに変換
        soup = BeautifulSoup(response.text, 'html.parser')

        # 指定された値を含むonmouseover属性を持つすべてのアンカー タグを検索
        anchor_tags = soup.find_all('a', onmouseover=re.compile(r"ezimg_change\('menu03','menu03_cur'\)"))

        # アンカータグからhref属性を抽出
        torihiki_url = [anchor['href'] for anchor in anchor_tags][0]

        # torihiki_urlからデータを取得
        response_torihiki = session.get("https://trade.smbcnikko.co.jp" + torihiki_url)

        # 取得したデータをBeautiful Soupオブジェクトに変換
        soup_torihiki = BeautifulSoup(response_torihiki.text, 'html.parser')

        # 新規新規売付のURL取得
        # 指定された div 内のすべてのアンカータグを検索します
        divs_with_anchors = soup_torihiki.find_all('div', class_='con_mrg03')

        # 'tku_odr/init'で終わる URL を抽出
        target_urls = []
        for div in divs_with_anchors:
            anchor_tag = div.find('a')
            if anchor_tag:
                href = anchor_tag.get('href')
                if href and href.endswith('tku_odr/init'):
                    target_urls.append(href)

        # 新規売付
        self.shinkibaitsuke_url = '\n'.join(target_urls).replace("init", "siji")
    
    # ログイン情報を読み込む（セキュリティのため設定ファイルから行う）
    def load_login_info(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.login_params = {
            'koza1': config['login']['shiten'],
            'koza2': config['login']['kouza'],
            'passwd': config['login']['login_pass'],
            'spHyojiMode': config['login']['spHyojiMode'],
            'syokiGamen': config['login']['syokiGamen'],
            'ntt': config['login']['ntt'],
            'logIn.x': config['login']['logIn.x'],
            'logIn.y': config['login']['logIn.y']
        }

    # 新規売付URLを渡す
    def get_shinkibaitsuke_url(self):
        return self.shinkibaitsuke_url

    # cookiesを渡す 
    def get_cookies(self):
        return self.cookies


# 注文マネージャ
class OrderManager():
    def __init__(self, order_url, submit_params, headers, cookies, meigara, stock_name, kabusu):
        self.order_url = order_url          # 注文URL
        self.submit_params = submit_params  # 注文入力パラメータ
        self.headers = headers              # ヘッダー情報
        self.cookies = cookies              # cookies情報
        self.meigara = meigara              # 銘柄情報
        self.stock_name = stock_name        # 銘柄名
        self.kabusu = kabusu                # 注文数

    # 注文情報入力処理
    def submit_order(self):
        # 注文情報入力のPOSTリクエストを送信
        response = requests.post(self.order_url, data=self.submit_params, headers=self.headers, cookies=self.cookies)
        
        # response_text = response.text

        soup = BeautifulSoup(response.text, 'html.parser')

        # span要素を取得し、クラス名が "txt_b01" のものを検索
        span_elements = soup.find_all('span', class_='txt_b01')

        # 2番目のspan要素のテキストを取得
        self.kakaku = span_elements[3].text

        print(f'[{self.meigara} {self.stock_name}] {self.kabusu}株 {self.kakaku}円')

        # 注文確認のURL取得
        form = soup.find("form", {"name": "frm_chart"})  # <form>要素を検索       
        action_url_parts = form["action"]                # <form>要素のaction属性からURLを取得
        self.action_url_parts = action_url_parts 

    # 注文確認処理
    def confirm_order(self):    
        # 注文確認のPOSTリクエストを送信
        response = requests.post(self.action_url, data=self.order_params, headers=self.headers, cookies=self.cookies)

        soup = BeautifulSoup(response.text, 'html.parser')

        #注文URL取得
        # <form> 要素の中から "exec" で終わる action 属性を持つ要素を検索
        exec_ending_forms = soup.find_all("form", action=re.compile(r"exec$"))

        # 各 <form> 要素の action 属性を出力　注文URL取得
        for form in exec_ending_forms:
            commit_url_parts = form["action"]
            self.commit_url_parts = commit_url_parts

        # <input>要素を検索してtokenIdのvalueを取得
        token_input = soup.find("input", {"name": "tokenId"})

        if token_input:
            # tokenId valueを取得
            token_id_value = token_input.get("value")
            self.token_id_value = token_id_value
        else:
            self.token_id_value = None
            print(f"[{self.meigara} {self.stock_name}] 一般信用売建可能数量がありませんでした。")
            return  # tokenIdの要素が見つからなかった場合に関数を終了
    
    # commit_url_paramsを渡す
    def get_commit_url_parts(self):
        return self.commit_url_parts
    
    # commit_urlをセットする
    def set_commit_url(self, commit_url):
        self.commit_url = commit_url
       
    # 注文確定処理
    def commit_order(self):
        # 注文確認POSTリクエストを送信
        response = requests.post(self.commit_url, data=self.commit_params, headers=self.headers, cookies=self.cookies)

        soup = BeautifulSoup(response.text, 'html.parser')
        order = soup.find('span', class_='txt_b01').get_text()

        return order

    # 価格を渡す    
    def get_kakaku(self):
        return self.kakaku

    # action_url_partsを渡す
    def get_action_url_parts(self):
        return self.action_url_parts

    # order_pramsをセットする
    def set_order_params(self, order_params):
        self.order_params = order_params

    # action_urlをセットする
    def set_action_url(self, action_url):
        self.action_url = action_url
        
    # token_idを渡す
    def get_token_id_values(self):
        return self.token_id_value
    
    # commit_paramsをセットする
    def set_commit_params(self, commit_params):
        self.commit_params = commit_params