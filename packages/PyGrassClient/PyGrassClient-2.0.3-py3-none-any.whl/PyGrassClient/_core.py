import asyncio
import json
import pathlib
import ssl
import sys
import threading
import time
import uuid

import websocket
from faker import Faker
from loguru import logger
from playwright.sync_api import sync_playwright
from websocket import setdefaulttimeout

from PyGrassClient._async_core import AsyncGrassWs
from PyGrassClient.utils import parse_proxy_url, new_session, Status

logger.remove()  # 移除默认的控制台输出处理器

logger.add(sys.stdout, level="INFO")  # 添加新的控制台输出处理器


class GrassWs:
    def __init__(self, user_id, proxy_url=None):
        self.user_id = user_id
        self.is_online = False
        self.reconnect_times = 0
        self.user_agent = Faker().chrome()
        self.device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, proxy_url or ""))
        self.proxy_url = proxy_url
        self.ping_thread = None
        self.ws = self.init_ws()

    def init_ws(self):
        return websocket.WebSocketApp(
            "wss://proxy.wynd.network:4650/",
            header=[
                f"User-Agent: {self.user_agent}"],
            on_error=self.on_error,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close
        )

    def info(self, message):
        return f'\n------\n[{message}]\n[user_id: {self.user_id}]\n[proxy_url: {self.proxy_url}]\n[device_id: {self.device_id}]\n------\n'

    def send_ping(self, wsapp):
        while self.is_online:
            time.sleep(20)
            try:
                send_message = json.dumps(
                    {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                wsapp.send(send_message)
                logger.debug(f'send {send_message}')
            except Exception as e:
                logger.error(f'[user_id: {self.user_id}] [proxy_url: {self.proxy_url}] ping error: {e}')
                self.ws.close()
                break
        self.is_online = False
        self.ping_thread = None

    def on_open(self, wsapp):
        self.reconnect_times += 1
        logger.debug(self.info(f'Connect open'))

    def on_close(self, wsapp, close_status_code, close_msg):
        self.is_online = False
        logger.error(self.info(f'Connect close: {close_msg}'))

    def on_error(self, wsapp, err):
        self.is_online = False
        logger.error(self.info(f'Connect error: {err}'))

    def on_message(self, wsapp, message):
        message = json.loads(message)
        logger.debug(f'recv {message}')
        if message.get("action") == "AUTH":
            auth_response = {
                "id": message["id"],
                "origin_action": "AUTH",
                "result": {
                    "browser_id": self.device_id,
                    "user_id": self.user_id,
                    "user_agent": self.user_agent,
                    "timestamp": int(time.time()),
                    "device_type": "extension",
                    "version": "3.3.0"
                }
            }
            logger.debug(f'send {auth_response}')
            wsapp.send(json.dumps(auth_response))
            self.is_online = True
            logger.info(self.info(f"连接成功 连接次数: {self.reconnect_times}"))
            self.ping_thread = threading.Thread(target=self.send_ping, args=(self.ws,), daemon=True)
            self.ping_thread.start()
        elif message.get("action") == "PONG":
            pong_response = {"id": message["id"], "origin_action": "PONG"}
            logger.debug(f'send {pong_response}')
            wsapp.send(json.dumps(pong_response))

    def run(self):
        setdefaulttimeout(30)
        if self.proxy_url:
            proxy_type, http_proxy_host, http_proxy_port, http_proxy_auth = parse_proxy_url(self.proxy_url)
        else:
            proxy_type = http_proxy_host = http_proxy_port = http_proxy_auth = None
        logger.info(self.info('Run start'))
        while True:
            self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, proxy_type=proxy_type,
                                http_proxy_host=http_proxy_host,
                                http_proxy_port=http_proxy_port, http_proxy_auth=http_proxy_auth,
                                reconnect=5)
            self.is_online = False
            while self.ping_thread is not None:
                time.sleep(1)
            self.ws = self.init_ws()


class PyGrassClient:
    def __init__(self, *, user_name=None, password=None, user_id=None, proxy_url=None):
        assert user_id or (user_name and password), Exception('must set user_name and password or set user_id!')
        self.user_name = user_name
        self.password = password
        self.user_id = user_id
        self.proxy_url = proxy_url
        self.session = new_session(self.proxy_url)
        self.ws = AsyncGrassWs(self.user_id, self.proxy_url)
        self.dashboard = {}
        # self.is_login = False

    def login(self):
        assert (self.user_name and self.password), Exception('must set user_name and password!')
        json_data = {
            'user': self.user_name,
            'password': self.password,
        }
        response = self.session.post('https://api.getgrass.io/auth/login', json=json_data).json()
        if response["status"] == "success":
            self.user_id = response["data"]["id"]
        else:
            raise Exception(f'login fail, [{self.user_name}, {self.password}]')

    def get_dash_data(self):
        logger.info('Logining...')
        playwright = sync_playwright().start()
        browser_proxy = None
        if self.proxy_url:
            scheme, host, port, auth = parse_proxy_url(self.proxy_url)
            browser_proxy = {
                "server": f"{scheme}://{host}:{port}"
            }
            if auth:
                browser_proxy.update({
                    "username": auth[0],
                    "password": auth[1]
                })
        browser = playwright.firefox.launch(proxy=browser_proxy, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60 * 1000)
        page.goto('https://app.getgrass.io/', wait_until='networkidle')
        # 如果有缓存
        if pathlib.Path(f'cookies/{self.user_name}.json').exists():
            # 将cookies保存为文件
            with open(f'cookies/{self.user_name}.json', 'r') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            # 从文件中读取 localStorage 数据
            with open(f'cookies/localStorage—{self.user_name}.json', 'r') as f:
                localStorage = json.load(f)

            # 将 localStorage 数据加载到网页中
            page.evaluate(
                f"localStorageData => {{ for (let item in localStorageData) localStorage.setItem(item, localStorageData[item]) }}",
                localStorage)

            page.goto('https://app.getgrass.io/dashboard')

        if page.url == 'https://app.getgrass.io/':
            page.get_by_placeholder('Username or Email').fill(self.user_name)
            page.get_by_placeholder('Password').fill(self.password)
            page.get_by_text("ACCESS MY ACCOUNT").click()

        page.wait_for_url('https://app.getgrass.io/dashboard', wait_until='networkidle')
        logger.info('Login Success!')

        self.user_id = page.evaluate("() => localStorage.userId").replace('"', '')

        # 保存登陆信息
        cookies = context.cookies()
        # 将cookies保存为文件
        with open(f'cookies/{self.user_name}.json', 'w') as f:
            json.dump(cookies, f)

        # 获取 localStorage 数据
        localStorage = page.evaluate("() => JSON.stringify(localStorage)")
        # 将 localStorage 数据保存为文件
        with open(f'cookies/localStorage—{self.user_name}.json', 'w') as f:
            f.write(localStorage)

        # score
        box = page.locator(
            'xpath=/html/body/div[1]/div[2]/main/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[1]').bounding_box()
        page.mouse.move(box["x"] + box["width"] / 3 * 2, box["y"] + box["height"] / 2)
        score_text = page.locator('xpath=/html/body/div[3]/div').text_content()
        total_score = float(score_text.split(':')[1].replace(',', ''))
        self.dashboard['total_score'] = total_score
        browser.close()
        return self.dashboard

    async def connect_ws(self):
        if not self.user_id:
            self.login()
        self.ws.user_id = self.user_id
        await self.ws.run()


def run_by_file(acc_file_path):
    asyncio.run(aio_run_by_file(acc_file_path))


async def aio_run_by_file(acc_file_path):
    all_clients = load_account_by_file(acc_file_path)
    for client in all_clients:
        asyncio.create_task(client.connect_ws())
        await asyncio.sleep(1)
    n = 0
    while n < 60 * 60 * 4:
        if n % 10 == 0:
            logger.info(
                f'online: {len(list(filter(lambda x: x.ws.status == Status.connected, all_clients)))} all: {len(all_clients)}')
        n += 1
        await asyncio.sleep(1)


def load_account_by_file(acc_file_path):
    all_clients = []
    index = 0
    with open(acc_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "==" in line:
                user_id, proxy_url = line.split('==')
            else:
                user_id, proxy_url = line, None
            if "---" in user_id:
                user_name, password = user_id.split('---')
                user_id = None
            else:
                user_name = password = None
            proxy_url = proxy_url or None
            index += 1
            client = PyGrassClient(user_id=user_id, user_name=user_name, password=password, proxy_url=proxy_url)
            logger.info(f'[{index}] [user_id: {user_id}] [proxy: {proxy_url}]')
            all_clients.append(client)
    return all_clients
