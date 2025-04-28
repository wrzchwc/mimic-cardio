class CaseSizeError(Exception):
    def __init__(self, hadm_id: str):
        self.message = f'CSE: {hadm_id}'