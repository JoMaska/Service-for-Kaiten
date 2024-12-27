import uvicorn
import logging
from fastapi import FastAPI, File, Form, UploadFile
from typing import List

from kaiten_client import get_kaiten_config, create_bug_ticket, create_task_ticket, add_file_to_bug_ticket

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/api/tickets")
async def create_tickets(
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    config = await get_kaiten_config()
    result = list()
    
    for item in config['kaiten_urls']:
        kaiten_url = item['url']
        board_id = item['board_id']
        api_token = item['token']
        primary_key = item['primary']

        bug_ticket = await create_bug_ticket(kaiten_url, api_token, board_id, title, description)
        await add_file_to_bug_ticket(kaiten_url, files, bug_ticket['id'])
        await create_task_ticket(kaiten_url, bug_ticket['id'])

        if primary_key:
            result.append({"ticket_url": f'{kaiten_url}/ticket/{bug_ticket["id"]}'})

    return result[0]

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8080)