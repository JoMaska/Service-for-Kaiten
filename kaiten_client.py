import logging

from request import make_request

async def get_kaiten_config():
    try:
        return await make_request(url='https://test.born-in-july.ru/api/settings', method="GET", data=None, headers=None)
    except Exception:
        logging.error(f"Ошибка при получении конфигурации Kaiten: {Exception}")
        return {"Error": str(Exception)}, 500

async def add_file_to_bug_ticket(kaiten_url, files, bug_ticket_id):
    try:
        return await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/files',
                           method='PUT',
                           data={'card_id': bug_ticket_id},
                           headers=files)
    except Exception:
        logging.error(f"Ошибка при приклеплении файла к баге Kaiten: {Exception}")
        return {"Error": str(Exception)}, 400

async def create_bug_ticket(kaiten_url, api_token, board_id, title, description):
    try:
        return await make_request(url=f'{kaiten_url}/api/latest/cards',
                           method='POST',
                           data={'title': title, 'description': description, 'board_id': board_id},
                           headers={"Authorization": f'Bearer {api_token}'})
    except Exception:
        logging.error(f"Ошибка при создании баги Kaiten: {Exception}")
        return {"Error": str(Exception)}, 400

async def create_task_ticket(kaiten_url, bug_ticket_id):
    try:
        return await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/children')
    except Exception:
        logging.error(f"Ошибка при создании дочерней задачи Kaiten: {Exception}")
        return {"Error": str(Exception)}, 400
