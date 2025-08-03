from flask import Flask, request, make_response
import hashlib
import time
import xml.etree.ElementTree as ET
import random

app = Flask(__name__)

# 这里就是你的 Token，自己随便设置，改成你喜欢的字符串
TOKEN = "my_wechat_token_123"

@app.route("/", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        # 微信服务器验证URL有效性
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")

        hashlist = [TOKEN, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join(hashlist).encode('utf-8')
        hashcode = hashlib.sha1(hashstr).hexdigest()

        if hashcode == signature:
            return echostr
        else:
            return "error"

    elif request.method == "POST":
        # 处理用户发送的消息，回复验证码
        xml_data = request.data
        xml = ET.fromstring(xml_data)
        to_user = xml.find("FromUserName").text
        from_user = xml.find("ToUserName").text
        content = xml.find("Content").text.strip()

        # 生成6位随机数字验证码
        code = ''.join(random.choices("0123456789", k=6))
        print(f"[生成验证码] 用户 {to_user} -> {code}")

        reply = f"""
        <xml>
          <ToUserName><![CDATA[{to_user}]]></ToUserName>
          <FromUserName><![CDATA[{from_user}]]></FromUserName>
          <CreateTime>{int(time.time())}</CreateTime>
          <MsgType><![CDATA[text]]></MsgType>
          <Content><![CDATA[您的验证码是：{code}]]></Content>
        </xml>
        """
        return make_response(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
