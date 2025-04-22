from json import loads


def load_cases():
    cases = []
    with open('./assets/cases.jsonl', 'r') as file:
        for case in file:
            case = loads(case)
            cases.append(case)
    return cases