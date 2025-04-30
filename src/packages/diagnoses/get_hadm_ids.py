import os


def get_hadm_ids_from_responses(experiment: str) -> list[str]:
    directory = f'./assets/responses/{experiment}'
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith('.json')
    ]
