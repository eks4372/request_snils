import requests


def get_req(name, family, patronymic, gender, bday, series='', number='', doc_date='', issuer='-'):
    url = 'http://10.129.222.34:8090/rest/client/send'
    if patronymic:
        data = {
            "xml": f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><tns:SnilsByAdditionalDataRequest xmlns:tns=\"http://kvs.pfr.com/snils-by-additionalData/1.0.3\" xmlns:smev=\"urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.3\" xmlns:pfr=\"http://common.kvs.pfr.com/1.0.3\"><smev:FamilyName>{family}</smev:FamilyName><smev:FirstName>{name}</smev:FirstName><smev:Patronymic>{patronymic}</smev:Patronymic><tns:BirthDate>{bday}</tns:BirthDate><tns:Gender>{gender}</tns:Gender><smev:PassportRF><smev:Series>{series}</smev:Series><smev:Number>{number}</smev:Number><smev:IssueDate>{doc_date}</smev:IssueDate><smev:Issuer>{issuer}</smev:Issuer></smev:PassportRF></tns:SnilsByAdditionalDataRequest>",
            "typeMessage": "REQUEST"}
    else:
        data = {
            "xml": f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><tns:SnilsByAdditionalDataRequest xmlns:tns=\"http://kvs.pfr.com/snils-by-additionalData/1.0.3\" xmlns:smev=\"urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.3\" xmlns:pfr=\"http://common.kvs.pfr.com/1.0.3\"><smev:FamilyName>{family}</smev:FamilyName><smev:FirstName>{name}</smev:FirstName><tns:BirthDate>{bday}</tns:BirthDate><tns:Gender>{gender}</tns:Gender><smev:PassportRF><smev:Series>{series}</smev:Series><smev:Number>{number}</smev:Number><smev:IssueDate>{doc_date}</smev:IssueDate><smev:Issuer>{issuer}</smev:Issuer></smev:PassportRF></tns:SnilsByAdditionalDataRequest>",
            "typeMessage": "REQUEST"}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=url, json=data, headers=headers)
    # print(r.text)
    # print(r.json()['requestMessage']['messageId'])
    if r.status_code == requests.codes.ok:
        message_id = r.json()['requestMessage']['messageId']
        # print(f'MessageID: {message_id}')
        return message_id
    else:
        return f'[ОШИБКА]!!! {r.raise_for_status()}'


if __name__ == '__main__':
    name = 'Константин'
    family = 'Емельянов'
    patronymic = 'Сергеевич'
    gender = 'Male'
    bday = '1981-10-09'
    series = '3307'
    number = '801540'
    data = {
        "xml": f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><tns:SnilsByAdditionalDataRequest xmlns:tns=\"http://kvs.pfr.com/snils-by-additionalData/1.0.3\" xmlns:smev=\"urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.3\" xmlns:pfr=\"http://common.kvs.pfr.com/1.0.3\"><smev:FamilyName>{family}</smev:FamilyName><smev:FirstName>{name}</smev:FirstName><smev:Patronymic>{patronymic}</smev:Patronymic><tns:Gender>{gender}</tns:Gender><tns:BirthDate>{bday}</tns:BirthDate><smev:PassportRF><smev:Series>{series}</smev:Series><smev:Number>{number}</smev:Number></smev:PassportRF></tns:SnilsByAdditionalDataRequest>",
        "typeMessage": "REQUEST"}
    # print(data)
    headers = {'Content-Type': 'application/json'}

    print(get_req(name, family, patronymic, gender, bday, series, number))
