import csv
import camelot
import pandas as pd
import re
import os

def extract_PK(pdf_file, pages_range, output_filename, column_index=1):
    export_folder = "export"  # Директория экспорта .csv таблиц

    try:
        # Попытка чтения таблиц из указанного PDF и их объединения в датафрейм
        tables = camelot.read_pdf(pdf_file, pages=pages_range)
        
        if tables:
            # Конкатенация таблиц в датафрейм
            merged_df = pd.DataFrame()
            for table in tables:
                merged_df = pd.concat([merged_df, table.df], ignore_index=True)
            
            # Очистка первой колонки таблицы
            pk_col = merged_df.iloc[:, column_index]  # Выбор колонки таблицы
            clean_col = pk_col.str.replace(r'-?\n', '', regex=True).str.replace(r'\n', '', regex=True) # Очистка мусорных символов (regex)
            clean_col = clean_col.apply(lambda x: re.sub(r'\s+', ' ', x))  # Удаление лишних пробелов
            clean_col = clean_col.apply(lambda x: x.replace('.', ''))  # Удаление точек

            # Фильтрация строк, начинающихся с кода компетенции или строчной буквы (для переносов)
            clean_col = clean_col[clean_col.apply(lambda x: re.match(r'^УК|ОПК|ПК|[а-я]', x) is not None)]

            # Инициализация списка для хранения строк
            merged_table = []
            previous_row = None
            
            # Цикл для проверки строк на необходимость конкатенации с предыдущей строкой
            for row in clean_col:
                if previous_row is None:
                    merged_table.append(row)
                else:
                    # Проверка на перенесенные слова
                    if previous_row.endswith('-'):
                        merged_table[-1] = merged_table[-1][:-1] + row  # Удаление дефиса перед конкатенацией
                    else:
                        # Проверка на то, что строка НЕ начинается с кода компетенции
                        if not (row.startswith("УК") or row.startswith("ОПК") or row.startswith("ПК")):
                            merged_table[-1] += " " + row  # Конкатенация с предыдущей строкой
                        else:
                            merged_table.append(row)
                
                # Переход на следующую строку
                previous_row = row
            
            # Конвертация списка соединенных строк в датафрейм
            merged_df = pd.DataFrame(merged_table, columns=['Код и наименование компетенции'])

            # Удаление строк-дублей
            merged_df.drop_duplicates(inplace=True)
            
            # Создание директории для экспорта, если её нет
            if not os.path.exists(export_folder):
                os.makedirs(export_folder)
            
            # Полный путь для экспорта
            output_path = os.path.join(export_folder, output_filename)

            # Разделение строк на две колонки после первого пробела
            merged_df[['Код', 'Наименование']] = merged_df['Код и наименование компетенции'].str.split(n=1, expand=True)
            merged_df = merged_df[['Код', 'Наименование']]

            # Экспорт в csv
            merged_df.to_csv(output_path, index=False, encoding='windows-1251', quoting=csv.QUOTE_NONNUMERIC)
            # merged_df.to_csv(output_path, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)

            print(f"Сохранено в {output_path}")
        else:
            print("На указанных страницах таблиц не обнаружено.")
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

# Обработка файлов
extract_PK("pdf/26.05.06_oop_2023.pdf", '5-7',    "UK.csv",    column_index=1)
extract_PK("pdf/26.05.06_oop_2023.pdf", '8-9',    "OPK.csv",   column_index=1)
extract_PK("pdf/26.05.05_oop_2023.pdf", '8-20',   "05_PK.csv", column_index=0)
extract_PK("pdf/26.05.06_oop_2023.pdf", '14-34',  "06_PK.csv", column_index=1)
extract_PK("pdf/26.05.07_oop_2023.pdf", '13-end', "07_PK.csv", column_index=1)
