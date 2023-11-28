import requests
import xml.etree.ElementTree as ET


def get_snils(message_id):
    url = 'http://10.129.222.34:8090/rest/client/get'
    headers = {'Content-Type': 'application/json'}
    d = {"messageId": message_id, "typeMessage": "RESPONSE"}  # ответ
    # d = {"messageId":"41b5735b-2ae2-11ee-9d50-005056012da7","typeMessage":"REQUEST"} # запрос
    r = requests.post(url=url, json=d, headers=headers)
    if r.status_code == requests.codes.ok:
        try:
            # print(r.json()[0])
            x = r.json()[0]['xml']
            root_node = ET.fromstring(x)
            snils_value = root_node.find('.//{http://kvs.pfr.com/snils-by-additionalData/1.0.3}Snils').text
            # print(snils_value)
            return snils_value[:3] + '-' + snils_value[3:6] + '-' + snils_value[6:9] + ' ' + snils_value[9:]
        except:
            # print(r.text)
            # print(r.json())
            try:
                x = r.json()[0]['reject']['description']
            except:
                try:
                    x = r.json()[0]['error']
                except:
                    x = r.text
                    print('нет ответа')
            return x
        # print(x)
    else:
        return f'[ОШИБКА]!!! {r.raise_for_status()}'


if __name__ == '__main__':
    # 41b5735b-2ae2-11ee-9d50-005056012da7    5dbb290e-2ae8-11ee-9d50-005056012da7
    # messageId = "a7717adb-29dc-11ee-9d50-005056012da7"
    # messageId = "b9113655-2c51-11ee-9d50-005056012da7"  # valid
    # messageId = "ed334951-2c6e-11ee-94cc-005056012da7"  # valid
    messageId = "82739990-2c6f-11ee-94cc-005056012da7"  # valid
    # messageId = "b2acb4fc-2c51-11ee-9d50-005056012da7"
    # messageId = "b399ad0e-2c51-11ee-9d50-005056012da7"
    # messageId = "41b5735b-2ae2-11ee-9d50-005056012da7"  # не отработан
    print(get_snils(messageId))
