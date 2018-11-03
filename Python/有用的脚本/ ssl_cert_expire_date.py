import ssl
import socket
import datetime
"""
验证ssl 的证书的有效期
"""


def ssl_expiry_datetime(domain, port=443):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        sock=socket.socket(socket.AF_INET), server_hostname=domain)
    conn.settimeout(2)
    try:
        conn.connect((domain, port))
        ssl_info = conn.getpeercert()
        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

    except Exception as e:
        return None
    finally:
        conn.close()


def ssl_expire_date_valid(hostname, port=443):
    """
        是否过期
        true 过期
    """
    expires = ssl_expiry_datetime(hostname, port)
    return datetime.datetime.utcnow() >= expires


if __name__ == '__main__':
    print(ssl_cert_date('test.1mi.cn', 8443))
