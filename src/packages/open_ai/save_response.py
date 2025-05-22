from os import makedirs


def save_response(response: str, hadm_id: str, prefix):
    dir_path = f'./assets/responses/{prefix}'
    makedirs(dir_path, exist_ok=True)
    with open(f'./assets/responses/{prefix}/{hadm_id}.json', 'w') as f:
        f.write(response)