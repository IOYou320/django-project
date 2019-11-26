import base64
from Crypto.Cipher import AES

class AesEcb():

    def __init__(self):
        self.key = '1234567890123456'  # 密钥长度必须为16,分别对应AES-128/ 初始化密钥
        self.aes = AES.new(str.encode(self.key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式

    # 补足字符串长度为16的倍数
    def format_str(self, str_point):
        while len(str_point) % 16 != 0:
            str_point += '\0'
        # 返回bytes
        str_out = str_point.encode()
        return str_out

    def encryption(self, str_point):
        enc = self.format_str(str_point)
        # self.aes.encrypt(enc) 加密字符
        # base64.encodebytes base64 编码方式
        # str （str_point ,encoding='ust-8'）转变类型 str格式 utf-8

        res_encrypt = str(base64.encodebytes(self.aes.encrypt(enc)), encoding='utf8').replace('\n', '')  # 加密
        return res_encrypt

    def unencryption(self, str_in):
        uncrypted = str(
            self.aes.decrypt(base64.decodebytes(bytes(str_in, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
        return uncrypted