import os
import json
import random

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
directory = "discourse"

def handle_td_request(handler, query_params):
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    random_json_file = random.choice(json_files)
    category_from_filename = os.path.splitext(random_json_file)[0]  # 提取不含扩展名的文件名作为分类参数
    handler.send_response(200)
    
    with open(os.path.join(directory, random_json_file), 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
        selected_data = random.choice(data)

        final_data = {
            'status': '200',
            'msg': '成功',
            'category': category_from_filename,
            'content': selected_data.get('content'),
            'from': selected_data.get('from'),
            'creator': selected_data.get('creator'),
            'date': selected_data.get('date')
        }

    return json.dumps(final_data, ensure_ascii=False).encode()