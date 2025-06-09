import subprocess
import sys
import importlib
import importlib.util
import random
import os

def install_deps():
    deps = ['requests', 'cryptography>=42.0.0', 'pytz']
    if not all(importlib.util.find_spec(dep.split('>=')[0]) for dep in deps):
        subprocess.check_call([sys.executable, "-m", "pip", "install", *deps])

def main():
    install_deps()
    req = importlib.import_module('requests')
    b64 = importlib.import_module('base64').b64encode
    x = importlib.import_module('cryptography.hazmat.primitives.asymmetric.x25519')
    ser = importlib.import_module('cryptography.hazmat.primitives.serialization')
    dt = importlib.import_module('datetime').datetime
    tz = importlib.import_module('pytz')

    ua_list = [
        "okhttp/4.9.3 Android/10; SM-G973F",
        "okhttp/4.10.0 Android/11; Pixel 5",
        "okhttp/4.8.1 Android/9; ONEPLUS A6003",
        "okhttp/4.9.2 Android/12; SM-A525F"
    ]
    
    def gen_keys():
        priv = x.X25519PrivateKey.generate()
        pub = priv.public_key()
        priv_b = priv.private_bytes(ser.Encoding.Raw, ser.PrivateFormat.Raw, ser.NoEncryption())
        pub_b = pub.public_bytes(ser.Encoding.Raw, ser.PublicFormat.Raw)
        return b64(priv_b).decode('utf-8'), b64(pub_b).decode('utf-8')

    def reg_client():
        priv, pub = gen_keys()
        url = "https://api.cloudflareclient.com/v0a1922/reg"
        headers = {"Content-Type": "application/json; charset=UTF-8", "User-Agent": random.choice(ua_list)}
        payload = {"key": pub, "install_id": "", "fcm_token": "", "tos": dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "model": "Android", "serial_number": f"SN{random.randint(1000000, 9999999)}", "locale": "en_US"}
        for _ in range(3):
            try:
                r = req.post(url, headers=headers, json=payload, timeout=10)
                r.raise_for_status()
                d = r.json()
                return {"priv": priv, "ipv4": d["config"]["interface"]["addresses"]["v4"], "ipv6": d["config"]["interface"]["addresses"]["v6"], "peer_pub": d["config"]["peers"][0]["public_key"]}
            except req.exceptions.RequestException as e:
                print(f"Ошибка API: {e}")
                continue
        return None

    data = reg_client()
    if not data:
        print("Не удалось зарегистрировать клиента после 3 попыток")
        return

    try:
        msk = dt.now(tz.timezone('Europe/Moscow')).strftime('%Y%m%d%H%M')
        fn = f"WARP{msk}.conf"
        i = 1
        while os.path.exists(fn):
            fn = f"WARP{msk}_{i}.conf"
            i += 1
        with open(fn, 'w') as f:
            f.write(f"""[Interface]
PrivateKey = {data['priv']}
S1 = 0
S2 = 0
Jc = 120
Jmin = 23
Jmax = 911
H1 = 1
H2 = 2
H3 = 3
H4 = 4
MTU = 1280
Address = {data['ipv4']}, {data['ipv6']}
DNS = 1.1.1.1, 2606:4700:4700::1111, 1.0.0.1, 2606:4700:4700::1001

[Peer]
PublicKey = {data['peer_pub']}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = engage.cloudflareclient.com:2408""")
        print(f"Конфигурация сохранена в {fn}")
    except IOError as e:
        print(f"Ошибка записи файла: {e}")

if __name__ == "__main__":
    main()