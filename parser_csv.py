import pandas as pd
import re

def csv_to_sql_inserts(csv_file, table_name, output_file, include_index=True):
    """
    Преобразует CSV-файл в чистый SQL INSERT без комментариев
    
    Args:
        csv_file (str): Путь к CSV-файлу
        table_name (str): Имя таблицы для вставки данных
        output_file (str): Путь для сохранения SQL-файла
        include_index (bool): Включать ли индексы в SQL запрос
    """
    try:
        # Загрузка CSV
        df = pd.read_csv(csv_file)
        
        # Проверка на наличие 'Unnamed' столбцов
        unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
        
        if not include_index:
            df = df.drop(columns=unnamed_cols)
        
        # Очистка имен столбцов
        clean_columns = {}
        for col in df.columns:
            clean_col = re.sub(r'[^a-zA-Z0-9_]', '_', col).lower()
            clean_col = re.sub(r'_+', '_', clean_col)
            clean_col = clean_col.strip('_')
            if 'unnamed' in clean_col and not include_index:
                continue
            if not clean_col:
                clean_col = "column_" + str(len(clean_columns))
            clean_columns[col] = clean_col
            
        # Переименование колонок
        df = df.rename(columns=clean_columns)
        
        # Получение списка столбцов
        columns = list(df.columns)
        
        # Создание INSERT-запроса
        sql_content = [f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES"]
        
        # Добавление данных
        rows = []
        for _, row in df.iterrows():
            values = []
            for col in columns:
                value = row[col]
                
                # Обработка разных типов данных
                if pd.isna(value):
                    values.append("NULL")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    value_str = str(value)
                    
                    # Удаление символа рупии и запятых из чисел
                    if '₹' in value_str or ',' in value_str and any(c.isdigit() for c in value_str):
                        value_str = value_str.replace('₹', '').replace(',', '')
                        try:
                            if '.' in value_str:
                                float_value = float(value_str)
                                values.append(str(float_value))
                                continue
                            else:
                                int_value = int(value_str)
                                values.append(str(int_value))
                                continue
                        except ValueError:
                            pass
                    
                    # Экранирование кавычек в строках
                    value_str = value_str.replace("'", "''")
                    values.append(f"'{value_str}'")
            
            rows.append(f"    ({', '.join(values)})")
        
        # Объединение в один INSERT-запрос
        sql_content.append(',\n'.join(rows) + ";")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_content))
        
        print(f"SQL-файл успешно создан: {output_file}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    csv_file = "Sub_Genre_df.csv" 
    table_name = "sub_genres"
    output_file = "V3.1.0__insert_subgenre.sql"
    include_index = True
    
    csv_to_sql_inserts(csv_file, table_name, output_file, include_index)