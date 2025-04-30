def load_codes() -> list[str]:
    with open('./assets/icd_codes.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]
