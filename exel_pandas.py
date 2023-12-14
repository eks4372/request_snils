import sys
import time
import pandas as pd
import os, pathlib

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.environ["PYMORPHY2_DICT_PATH"] = str(pathlib.Path(sys._MEIPASS).joinpath('pymorphy2_dicts_ru/data'))
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
        try:
            gender = row.пол
        except:
            if patronymic:
                gender = pymorphy2.MorphAnalyzer().parse(patronymic)[0].tag.gender
            else:
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
        if '-' not in birthday:
            birthday = f'{birthday[-4:]}-{birthday[3:5]}-{birthday[:2]}'
        print(birthday)
        if doc:
            try:
                doc_sn = row['Серия док. уд. личность'].replace(' ', '')
                m_id = ''
            except:
                print('не корректные паспортные данные')
                m_id = 'запрос с такими паспортными данными не будет отработан'
            doc_num = row['Номер док. уд. личность']
            # doc_num = f"{row['Номер док. уд. личность']:06}"  # чтоб не потерять нули вначале
            doc_date = row['Дата  док. уд. личность']
            print(f'паспорт {doc_sn} {doc_num} выдан {doc_date}')
        else:
            doc_sn = ''
            doc_num = ''
        if gender:
            try:
                if not m_id:
                    m_id = get_req(name, family, patronymic, gender, birthday, doc_sn, doc_num, doc_date)
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
    df['Номер док. уд. личность'] = df['Номер док. уд. личность'].apply(lambda x: str(x).zfill(3))
    df.to_excel(file_out, index=False)


def get_snils_from_smev(file, file_out='get.xlsx'):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        print(f'{index + 1} из {len(df)}')
        m_id = row.message_id
        print(m_id)
        if m_id == 'запрос с такими паспортными данными не будет отработан':
            df.at[index, 'СНИЛС'] = '-'
            continue
        try:
            snils = get_snils(m_id)
            print(snils)
            time.sleep(1)
            if snils:
                df.at[index, 'СНИЛС'] = snils
            else:
                df.at[index, 'СНИЛС'] = 'нет ответа'
        except:
            print(f'что-то пошло не так при запросе {index + 1} - {m_id}')
            df.to_excel('get_part.xlsx', index=False)
            sys.exit()
    df['Номер док. уд. личность'] = df['Номер док. уд. личность'].apply(lambda x: str(x).zfill(3))
    df.to_excel(file_out, index=False)


if __name__ == '__main__':
    # y = ['y', 'yes', 'д', 'да', 'ага']
    # input_file = input('введите имя входного файла: ')
    # output_file = input('введите имя выходного файла: ')
    # doc = input('передавать данные паспорта? (enter - по умолчанию - нет): ')
    # try:
    #     pause = int(input('пауза в секундах до обработки функции получения ответов (по умолчанию 1): '))
    # except:
    #     pause = 0
    # if '.xlsx' not in input_file:
    #     input_file = f'{input_file}.xlsx'
    # if '.xlsx' not in output_file:
    #     output_file = f'{output_file}.xlsx'
    # if doc.lower() in y:
    #     doc = True
    # else:
    #     doc = False
    #
    # send_request_to_smev(input_file, doc=doc)
    # if pause < 1 or not pause:
    #     pause = 1
    # for i in range(0, pause):
    #     print(f'ждем до приёма ответов {pause} секунд')
    #     time.sleep(1)
    #     pause -= 1
    # get_snils_from_smev('send.xlsx', output_file)

    # send_request_to_smev('1_doc.xlsx', doc=False, file_out='send_doc1.xlsx')
    # get_snils_from_smev('send_doc1.xlsx', file_out='get_doc1.xlsx')
    send_request_to_smev('merged_file.xlsx', doc=True, file_out='send.xlsx')
    time.sleep(10)
    get_snils_from_smev('send.xlsx', file_out='get_december.xlsx')
    # send_request_to_smev('2001 (933).xlsx', doc=False, file_out='send2_f.xlsx')
    # get_snils_from_smev('send2.xlsx', file_out='get2.xlsx')

    #  удаление совпадений

    # def filter_xlsx_files(file1_path, file2_path, output_path):
    #     # Чтение данных из файлов
    #     df1 = pd.read_excel(file1_path)
    #     df2 = pd.read_excel(file2_path)
    #
    #     # Удаление значений, которые есть во втором файле из столбца "Рег. № пр./огран."
    #     column_to_check = "Рег. № пр./огран."
    #     df_filtered = df1[~df1[column_to_check].isin(df2[column_to_check])]
    #
    #     # Запись отфильтрованных данных в новый файл
    #     df_filtered.to_excel(output_path, index=False)
    #
    #
    # file1_path = 'combined.xlsx'
    # file2_path = 'погашенные.xlsx'
    # output_path = 'путь_к_выходному_файлу.xlsx'
    # filter_xlsx_files(file1_path, file2_path, output_path)

    #  выбор совпадений

    # def filter_xlsx_files(file1_path, file2_path, output_path):
    #     # Чтение данных из файлов
    #     df1 = pd.read_excel(file1_path)
    #     df2 = pd.read_excel(file2_path)
    #
    #     # Фильтрация значений, которые присутствуют во втором файле в столбце "Рег. № пр./огран."
    #     column_to_check = "Рег. № пр./огран."
    #     df_filtered = df1[df1[column_to_check].isin(df2[column_to_check])]
    #
    #     # Запись отфильтрованных данных в новый файл
    #     df_filtered.to_excel(output_path, index=False)
    #
    #
    # # Пример использования функции
    # file1_path = 'combined_.xlsx'
    # file2_path = 'погашенные.xlsx'
    # output_path = 'путь_к_выходному_файлу_.xlsx'
    #
    # filter_xlsx_files(file1_path, file2_path, output_path)


    # def create_unique_values_file(input_file, column_name, output_file):
    #     # Чтение данных из входного файла
    #     df = pd.read_excel(input_file)
    #
    #     # Отфильтровываем уникальные значения указанного столбца
    #     filtered_df = df.drop_duplicates(subset=[column_name])
    #
    #     # Запись отфильтрованного DataFrame в новый файл
    #     filtered_df.to_excel(output_file, index=False)
    #
    #
    # # Пример использования функции
    # input_file = 'ввод(3745).xlsx'
    # column_name = 'Рег. № пр./огран.'
    # output_file = 'путь_к_выходному_файлу.xlsx'
    #
    # create_unique_values_file(input_file, column_name, output_file)