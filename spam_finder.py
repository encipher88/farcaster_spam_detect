import json
import requests
import datetime

def read_fids_from_file(filename):
    """Читает FID из файла."""
    with open(filename, 'r') as file:
        # Удаляем пробелы и переносы строк, фильтруем пустые строки
        fids = [line.strip() for line in file.readlines() if line.strip()]
    return set(fids)  # Используем set для быстрого поиска

def download_spam_data(url):
    """Загружает данные о спаме из URL."""
    response = requests.get(url)
    if response.status_code == 200:
        # Разделяем текст на строки и парсим каждую как JSON
        return [json.loads(line) for line in response.text.splitlines() if line.strip()]
    else:
        raise Exception(f"Не удалось загрузить данные. Код ответа: {response.status_code}")

def find_matching_records(spam_data, target_fids):
    """Находит записи, соответствующие FID."""
    matching_records = []
    
    for record in spam_data:
        # Проверяем, что запись содержит FID и он находится в нашем списке
        if ("type" in record and 
            "fid" in record["type"] and 
            str(record["type"]["fid"]) in target_fids):
            matching_records.append(record)
    
    return matching_records

def get_label_description(label_value):
    """Преобразует числовое значение метки в текстовое описание."""
    if label_value == 0:
        return "Level 0: Worst Label"
    elif label_value == 1:
        return "Level 1: Limbo Label"
    elif label_value == 2:
        return "Level 2: Best Label"
    else:
        return f"Unknown Level: {label_value}"

def convert_timestamp(unix_timestamp):
    """Конвертирует UNIX timestamp в человекочитаемый формат даты и времени UTC."""
    dt = datetime.datetime.utcfromtimestamp(unix_timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def save_results(matching_records, output_filename):
    """Сохраняет результаты в файл CSV."""
    import csv
    
    # Используем utf-8-sig для правильного отображения кириллицы в Excel
    with open(output_filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        
        # Записываем заголовки с добавлением человекочитаемого времени
        writer.writerow(['FID', 'Label Value', 'Label Description', 'Status', 'Timestamp', 'Date Time (UTC)'])
        
        # Записываем данные
        for record in matching_records:
            fid = record['type']['fid']
            label_value = record['label_value']
            label_description = get_label_description(label_value)
            
            # Status переименован на OK/SPAM
            status = "OK" if label_value == 2 else "SPAM"
            timestamp = record['timestamp']
            
            # Конвертируем timestamp в человекочитаемый формат
            date_time_utc = convert_timestamp(timestamp)
            
            writer.writerow([fid, label_value, label_description, status, timestamp, date_time_utc])

def main():
    # Определение файлов и URL
    fid_filename = 'fid.txt'
    spam_url = 'https://raw.githubusercontent.com/warpcast/labels/refs/heads/main/spam.jsonl'
    output_filename = 'spam_results.csv'  # Изменено на CSV файл
    
    # Выполнение основных шагов
    print(f"Чтение FID из {fid_filename}...")
    target_fids = read_fids_from_file(fid_filename)
    print(f"Найдено {len(target_fids)} FID для поиска.")
    
    print(f"Загрузка данных о спаме...")
    spam_data = download_spam_data(spam_url)
    print(f"Загружено {len(spam_data)} записей о спаме.")
    
    print("Поиск совпадающих записей...")
    matching_records = find_matching_records(spam_data, target_fids)
    print(f"Найдено {len(matching_records)} совпадающих записей.")
    
    print(f"Сохранение результатов в {output_filename}...")
    save_results(matching_records, output_filename)
    
    # Вывод краткой статистики и примера конвертированного timestamp
    print("\nПример конвертации времени:")
    if len(matching_records) > 0:
        sample_timestamp = matching_records[0]['timestamp']
        sample_date_time = convert_timestamp(sample_timestamp)
        print(f"Unix timestamp {sample_timestamp} = {sample_date_time}")
    
    label_counts = {'Level 0 (Worst)': 0, 'Level 1 (Limbo)': 0, 'Level 2 (Best)': 0}
    for record in matching_records:
        label_value = record['label_value']
        if label_value == 0:
            label_counts['Level 0 (Worst)'] += 1
        elif label_value == 1:
            label_counts['Level 1 (Limbo)'] += 1
        elif label_value == 2:
            label_counts['Level 2 (Best)'] += 1
    
    print("\nСтатистика по меткам:")
    for label, count in label_counts.items():
        status = "OK" if "Best" in label else "SPAM"
        print(f"{label}: {count} записей - {status}")
    
    print("\nГотово! Результаты сохранены в", output_filename)

if __name__ == "__main__":
    main()