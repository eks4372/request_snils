import sys
import time
import pandas as pd
import pymorphy2
from snils_post_request import get_req
from snils_post_response import get_snils


def send_request_to_smev(file, doc=False, file_out='send.xlsx'):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        print(f'{index + 1} из {len(df)}')
        fio = row.ФИО.split(maxsplit=2)
        family = fio[0]
        name = fio[1]
        try:
            patronymic = fio[2]
        except:
            patronymic = ''
        print(f'{family} {name} {patronymic}')
        gender = pymorphy2.MorphAnalyzer().parse(name)[0].tag.gender
        if gender == 'femn':
            gender = 'Female'
        elif gender == 'masc':
            gender = 'Male'
        else:
            gender = ''
        print(gender)
        df.at[index, 'пол'] = gender
        birthday = row.ДР
        birthday = f'{birthday[-4:]}-{birthday[3:5]}-{birthday[:2]}'
        print(birthday)
        if doc:
            doc_sn = row['Серия док. уд. личность']
            doc_num = row['Номер док. уд. личность']
            print(f'паспорт {doc_sn} {doc_num}')
        else:
            doc_sn = ''
            doc_num = ''
        if gender:
            try:
                m_id = get_req(name, family, patronymic, gender, birthday, doc_sn, doc_num)
                print(m_id)
                df.at[index, 'message_id'] = m_id
                time.sleep(1)
            except:
                print(f'что-то пошло не так при запросе {index + 1} - {fio}')
                df.to_excel('send_part.xlsx', index=False)
                sys.exit()
        else:
            df.at[index, 'message_id'] = 'нужно указать пол'
    # # print(df)
    df.to_excel(file_out, index=False)


def get_snils_from_smev(file, file_out='get.xlsx'):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        print(f'{index + 1} из {len(df)}')
        m_id = row.message_id
        print(m_id)
        try:
            snils = get_snils(m_id)
            print(snils)
            time.sleep(1)
            df.at[index, 'СНИЛС'] = snils
        except:
            print(f'что-то пошло не так при запросе {index + 1} - {m_id}')
            df.to_excel('get_part.xlsx', index=False)
            sys.exit()
    df.to_excel(file_out, index=False)


if __name__ == '__main__':
    y = ['y', 'yes', 'д', 'да', 'ага']
    input_file = input('введите имя входного файла: ')
    output_file = input('введите имя выходного файла: ')
    doc = input('передавать данные паспорта? (enter - по умолчанию - нет): ')
    if '.xlsx' not in input_file:
        input_file = f'{input_file}.xlsx'
    if '.xlsx' not in output_file:
        output_file = f'{output_file}.xlsx'
    if doc.lower() in y:
        doc = True
    else:
        doc = False

    send_request_to_smev(input_file, doc=doc)
    get_snils_from_smev('send.xlsx', output_file)

    # send_request_to_smev('2020.xlsx', doc=True, file_out='send2020.xlsx')
    # get_snils_from_smev('send2020.xlsx', file_out='get2020.xlsx')
    #
    # send_request_to_smev('2021.xlsx', doc=True, file_out='send2021.xlsx')
    # get_snils_from_smev('send2021.xlsx', file_out='get2021.xlsx')
    #
    # send_request_to_smev('2022.xlsx', doc=True, file_out='send2022.xlsx')
    # get_snils_from_smev('send2022.xlsx', file_out='get2022.xlsx')

    # pause = 3
    # for i in range(0, pause):
    #     print(f'ждем до приёма ответов {pause} секунд')
    #     time.sleep(1)
    #     pause -= 1
    # get_snils_from_smev('send.xlsx')
