import os
import json
import paramiko
import requests

# 从环境变量中读取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS')
accounts = json.loads(accounts_json)

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_HEADERS = os.getenv('WEBHOOK_HEADERS')
WEBHOOK_DATA = os.getenv('WEBHOOK_DATA')
WEBHOOK_MESSAGE = os.getenv('WEBHOOK_MESSAGE')

SEND_TYPE = os.getenv('SEND_TYPE')


# 尝试通过SSH连接的函数
def ssh_connect(host, username, password, bark):
    transport = None
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        ssh_status = "SSH连接成功"
        print(f"SSH连接成功。")
        if SEND_TYPE == "bark":
            if bark:
                url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} SSH连接成功。"
                response = requests.get(url)
        else:
            send_webhook_request(f"Serv00自动登录账号 {username} SSH连接成功。")
    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(f"SSH连接失败: {e}")
        if SEND_TYPE == "bark":
            if bark:
                url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} SSH连接失败，请检查账号和密码是否正确。"
                response = requests.get(url)
        else:
            send_webhook_request(f"Serv00自动登录账号 {username} SSH连接失败，请检查账号和密码是否正确。")
    finally:
        if transport is not None:
            transport.close()


def send_webhook_request(message):
    url = WEBHOOK_URL
    headers = WEBHOOK_HEADERS
    data = WEBHOOK_DATA
    data[WEBHOOK_MESSAGE] = message
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到WebHook失败: {response.text}")
    except Exception as e:
        print(f"发送消息到WebHook时出错: {e}")


# 循环执行任务
for account in accounts:
    ssh_connect(account['host'], account['username'], account['password'], account["bark"])
