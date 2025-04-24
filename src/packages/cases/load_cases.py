from json import loads


def load_cases(file_name: str):
    cases = []
    with open(f'./assets/{file_name}', 'r') as file:
        for case in file:
            case = loads(case)
            cases.append(case)
    return cases