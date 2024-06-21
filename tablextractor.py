import csv
import camelot
import pandas as pd
import re

try:
    # Попытка чтения таблиц из указанного PDF и их объединения в датафрейм
    tables = camelot.read_pdf("pdf/26.05.05_oop_2023.pdf", pages='8-20')
    if tables:
        # Конкатенация таблиц в датафрейм
        combined_df = pd.DataFrame()
        for table in tables:
            combined_df = pd.concat([combined_df, table.df], ignore_index=True)
        
        # Очистка первой колонки таблицы
        firstCol = combined_df.iloc[:, 0]
        cleanCol = firstCol.str.replace(r'-?\n', '', regex=True).str.replace(r'\n', '', regex=True)
        cleanCol = cleanCol[cleanCol.apply(lambda x: re.match(r'^ПК|[а-я]', x) is not None)]


        # Инициализация списка для хранения строк
        mergedTable = []
        previousRow = None
        
        # Цикл для роверки строк на необходимость конкатенации с предыдущей строкой
        for row in cleanCol:
            if previousRow is None:
                mergedTable.append(row)
            else:
                # Проверка на перенос слова
                if previousRow.endswith('-'):
                    # Удаление дефиса перед конкатенацией
                    mergedTable[-1] = mergedTable[-1][:-1] + row
                else:
                    # Проверка на то, что строка НЕ начинается с "ПК"
                    if not row.startswith("ПК"):
                        # Конкатенация с предыдущей строкой
                        mergedTable[-1] += " " + row
                    else:
                        mergedTable.append(row)
            
            # Переход на следующую строку
            previousRow = row
        
        # Конвертация списка соединенных строк в датафрейм
        merged_df = pd.DataFrame(mergedTable,  columns=['Код и наименование профессиональной компетенции'])
        
        # Экспорт в csv
        filename = "05_PK.csv"
        merged_df.to_csv(filename, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
        
        print(f"Сохранено в {filename}")
    else:
        print("На указанных страницах таблиц не обнаружено.")
except FileNotFoundError:
    print("Файл не найден.")
except Exception as e:
    print(f"Ошибка: {e}")
