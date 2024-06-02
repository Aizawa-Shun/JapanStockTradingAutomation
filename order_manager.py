import configparser
import dates

# Manager to store information
class Manager():
    def __init__(self):
        # Login URL
        self.login_url = "https://trade.smbcnikko.co.jp/Login/0/login/ipan_web/exec"

        # Set trading password
        self.set_trading_password()
        
        # Header information
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',  # Specifies the content types the client can accept (HTML, XML, images, etc.)
            'Accept-Encoding': 'gzip, deflate, br',  # Specifies the compression methods the client can understand (gzip, deflate, br)
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8,es;q=0.7,ko;q=0.6,zh-TW;q=0.5,zh;q=0.4',  # Specifies the languages the client can understand (in order of priority: Japanese, English, Spanish, etc.)
            'Cache-Control': 'no-cache',       # Controls cache behavior. Here it indicates not to use cache.
            'Connection': 'keep-alive',        # Indicates to keep the network connection alive.
            'Content-Type': 'application/x-www-form-urlencoded',  # Specifies the content type of the request (URL-encoded form).
            'Host': 'trade.smbcnikko.co.jp',            # Specifies the host name of the server to which the request is being sent.
            'Origin': 'https://trade.smbcnikko.co.jp',  # Specifies the origin (source) of the request.
            'Pragma': 'no-cache',              # An old form of cache control header, here also indicating not to use cache.
            'Referer': 'https://trade.smbcnikko.co.jp/Etc/1/webtoppage/',  # Specifies the URL of the page from which the request originated.
            'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',  # Provides information about the browser brand and version.
            'Sec-Ch-Ua-Mobile': '?0',          # Indicates whether the client is a mobile device (here it is not a mobile device).
            'Sec-Ch-Ua-Platform': '"macOS"',   # Specifies the platform (OS) of the client (here it is macOS).
            'Sec-Fetch-Dest': 'document',      # Specifies the purpose of the request (here it is to fetch a document).
            'Sec-Fetch-Mode': 'navigate',      # Specifies the mode of the request (here it is normal navigation).
            'Sec-Fetch-Site': 'same-origin',   # Indicates whether the request is from the same origin (here it is the same origin).
            'Sec-Fetch-User': '?1',            # Indicates whether the request was triggered by user intervention (here there was user intervention).
            'Upgrade-Insecure-Requests': '1',  # Requests to upgrade insecure connections to secure connections.
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'  # Specifies the browser and version (here Chrome version 115 on macOS).
        }
    
    # Set order information input parameters
    def set_submit_params(self):
        self.submit_params = {
            'odrJoken': 1,                 # Order condition: specific condition flag (1 may indicate a specific state or requirement).
            'execCnd': 0,                  # Execution condition: specifies how or when the order should be executed (0 may mean default or no special condition).
            'ippanSinyoTriKanoFlg': 1,     # General margin trading flag: indicates whether general margin trading is possible (1 means possible).
            'kakunin': 1,                  # Confirmation: a step that requires user confirmation.
            'odrExecYmd': '',              # Order execution date: specifies the date the order should be executed (blank means unspecified).
            'dispChk': 0,                  # Display check: a flag to check some display state (0 may mean no specific check).
            'honjituIjiRitu': 89.54,       # Today's maintenance rate: indicates the maintenance rate for a specific financial transaction on the day.
            'shintategaku': '1,782,900',   # New position amount: indicates the amount of new positions being established (enclosed in quotes).
            'specifyMeig': '',             # Specify stock: specifies a specific stock (blank means unspecified).
            'meigCd': self.meigara,        # Stock code: specifies the code of the stock.
            'sinkbShitei': 0,              # Credit designation: indicates the designation for margin trading (0 may mean no specific designation).
            'sijyoKbn': 1,                 # Market classification: indicates the classification of the market (1 may refer to a specific market).
            'sinyoToriKbn': 1,             # Margin trading classification: specifies the classification of margin trading (1 may indicate a specific classification).
            'suryo': self.kabusu,          # Quantity: specifies the quantity for the transaction.
            'kakaku': '',                  # Price: specifies the price for the transaction (blank may mean market price or unspecified).
            'yukokigenDate': '',           # Expiration date: specifies the expiration date for the transaction (blank means unspecified).
            'kozaKbnSinyo': 1,             # Margin account classification: specifies the classification for margin trading accounts (1 may indicate a specific classification).
            'kozaKyakKbn': 1,              # Account customer classification: indicates the classification of the account's customer (1 may indicate a specific customer classification).
            'execUrl.x': 130,              # Execution URL X-coordinate: specifies the X-coordinate for the execution URL.
            'execUrl.y': 22                # Execution URL Y-coordinate: specifies the Y-coordinate for the execution URL.
        }

    # Set order confirmation parameters
    def set_order_params(self):
        # Parameters to be sent
        self.order_params = {
            'odrJoken': 1,                # Order condition (probably indicates a specific type of order).
            'execCnd': 0,                 # Execution condition (probably specifies immediate or conditional execution).
            'ippanSinyoTriKanoFlg': 1,    # General margin trading flag (indicates whether general margin trading is possible).
            'kakunin': 1,                 # Confirmation (a flag for order confirmation).
            'odrExecYmd': '',             # Order execution date (blank may indicate immediate execution).
            'dispChk': 0,                 # Display check (probably a flag related to UI display).
            'honjituIjiRitu': 89.54,      # Today's fluctuation rate (current stock price fluctuation rate).
            'shintategaku': '1,782,900',  # New position amount (total amount of the new order).
            'specifyMeig': '',            # Specify stock (stock name if specified).
            'meigCd': self.meigara,       # Stock code (code of the stock to be ordered).
            'sinkbShitei': 0,             # Credit buy designation (for margin buy orders).
            'sijyoKbn': 1,                # Market classification (specifies which market to trade in).
            'sinyoToriKbn': 1,            # Margin trading classification (specifies the type of margin trading).
            'suryo': self.kabusu,         # Quantity (quantity of the stock to be ordered).
            'nariSasiKbn': 1,             # Market order designation (specifies whether it is a market or limit order).
            'kakaku': self.kakaku,        # Price (price for limit orders).
            'cnd14': 3,                   # Condition 14 (specifies a specific order condition).
            'yukokikan': 1,               # Validity period (specifies the validity period of the order).
            'yukokigenDate': '',          # Expiration date (for orders valid until a specific date).
            'kozaKbnSinyo': 1,            # Margin account classification (specifies the classification for margin trading accounts).
            'kozaKyakKbn': 1,             # Account customer classification (specifies the type of account).
            'execUrl.x': 46,              # Execution URL X-coordinate: specifies the X-coordinate for the execution URL.
            'execUrl.y': 23               # Execution URL Y-coordinate: specifies the Y-coordinate for the execution URL.
        }
            
    # Set parameters for confirmation
    def set_commit_params(self):
        self.commit_params = {
            'specifyMeig': '',                            # Specify stock (for specifying a particular stock).
            'sinkbShitei': 0,                             # Credit buy designation (for margin buy orders).
            'meigCd': self.meigara,                       # Stock code (code of the stock to be ordered).
            'bbaiKbn': 1,                                 # Trading classification (specifies the type of trade).
            'sijyoKbn': 1,                                # Market classification (specifies which market to trade in).
            'execCnd': 3,                                 # Execution condition (specifies the condition for order execution).
            'nariSasiKbn': 1,                             # Market order designation (specifies whether it is a market or limit order).
            'kakaku': self.kakaku,                        # Price (price for limit orders).
            'suryo': self.kabusu,                         # Quantity (quantity of the stock to be ordered).
            'odrExecYmd': dates.get_next_business_day(),  # Order execution date (automatically gets the next business day).
            'expcheck': 0,                                # Expiration check (specifies whether there is an expiration date).
            'yukoSiteDate': 1,                            # Effective start date (specifies the start date of the order validity).
            'yukokigenDate': '',                          # Expiration date (specifies the expiration date of the order).
            'nyuKeroKbn': '',                             # Deposit classification (specifies the method of stock deposit).
            'execCndKbn': '',                             # Execution condition classification (specifies details of the execution condition).
            'kanriKesaiKbn': '',                          # Management settlement classification (specifies the type of management settlement).
            'jreit': '',                                  # J-REIT designation (related to J-REIT).
            'etf': '',                                    # ETF designation (related to ETF).
            'kozaKbnSinyo': 1,                            # Margin account classification (specifies the classification for margin trading accounts).
            'kozaKyakKbn': 1,                             # Account customer classification (specifies the type of account).
            'tokenId': self.token_id_value,               # Token ID (value of the security token).
            'toriPasswd': self.trading_password,          # Trading password (password used for trading).
            'funcId': '01',                               # Function ID (specifies a particular function).
            # X,Y coordinates (specifies the position of a specific button or link on the webpage).
            'x': 161,
            'y': 17,
            'shintategaku': '1,782,900',                  # New position amount (total amount of the new order).
            'odrJoken': 1,                                # Order condition (specifies a particular condition).
            # Various conditions (specifies particular order conditions).
            'cnd11': '',
            'cnd12': '',
            'cnd13': '',
            'cnd14': 'checked',
            'cnd15': '',
            'cnd16': '',
            'cnd17': '',
            #################################
            'dosokuKehai': '',                            # Dosoku series (specifies a particular condition).
            'oya': '',                                    # Parent (specifies the parent order).
            'sinyoToriKbn': 1,                            # Margin trading classification (specifies the type of margin trading).
            'ippanSinyoTriKanoFlg': 1,                    # General margin trading flag (indicates whether general margin trading is possible).
            # Trigger related (specifies orders triggered by particular conditions).
            'trgKbn': '',
            'trgKBkakaku': '',
            'trgKbnHZ': '',
            'trgKbnPM': '',
            'trgHZkakaku': '',
            'trgKbnJouge': '',
            #####################################################
            'nyuKeroKbn2': 'pcw00'                        # Deposit classification 2 (specifies the method of stock deposit).
        }
    
    # Store the information of the stock to be traded
    def set_stock_infos(self, meigara, kabusu):
        self.meigara = meigara
        self.kabusu = kabusu
        self.set_submit_params()
    
    # Set order information input URL
    def set_order_url(self, order_url):
        self.order_url = "https://trade.smbcnikko.co.jp" + order_url
    
    # Set order execution URL
    def set_action_url(self, action_url):
        self.action_url = "https://trade.smbcnikko.co.jp" + action_url
    
    # Set order confirmation URL
    def set_commit_url(self, commit_url):
        self.commit_url = "https://trade.smbcnikko.co.jp" + commit_url

    # Set token ID
    def set_token_id(self, token_id_value):
        self.token_id_value = token_id_value
    
    # Get trading password from config.ini
    def set_trading_password(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.trading_password = config['trading']['password']  # Store the trading password

    # Set price
    def set_price(self, price):
        self.price = price     # Set the price
        self.set_order_params()  # Set order_params
