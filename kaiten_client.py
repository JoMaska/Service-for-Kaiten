from request import make_request

async def get_kaiten_config(url='http://127.0.0.1:8081/api/settings'):
    try:
        return await make_request(url=url)
    except Exception:
        return {"Error": str(Exception)}, 500

async def add_file_to_bug_ticket(kaiten_url, files, bug_ticket_id):
    try:
        await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/files',
                           method='PUT',
                           data={'card_id': bug_ticket_id},
                           headers=files)
    except Exception:
        return {"Error": str(Exception)}, 400

async def create_bug_ticket(kaiten_url, api_token, board_id, title, description):
    try:
        await make_request(url=f'{kaiten_url}/api/latest/cards',
                           method='POST',
                           data={'title': title, 'description': description, 'board_id': board_id},
                           headers=f'Authorization: Bearer {api_token}')
    except Exception:
        return {"Error": str(Exception)}, 400

async def create_task_ticket(kaiten_url, api_token, board_id, title, description, bug_ticket_id):
    try:
        await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/children',
                           method='POST',
                           data={'title': title, 'description': description, 'board_id': board_id},
                           headers=f'Authorization: Bearer {api_token}')
    except Exception:
        return {"Error": str(Exception)}, 400
