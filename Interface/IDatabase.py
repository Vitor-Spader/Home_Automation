class IDatabase:
    def __init__(self):
        return
    def insert(self, data:any) -> bool:
        return False
    def update(self, data:any, id:str) -> bool:
        return False
    def delete(self, id:str) -> bool:
        return False
    def search(self, _query:str) -> list():
        return list()