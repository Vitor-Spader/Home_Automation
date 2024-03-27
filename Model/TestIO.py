from Interface import IBoard

class TestIO(Model.IBoard):
    def __init__(self, _mode='BCM', _list_input=[], list_output=[], _list_relationship=[]):
        self.list_input = _list_input
        self.list_output = _list_output
        self.list_relationship = _list_relationship

    def set_on(self, _id:list) -> None:
        print(f'On {_id}')
    def set_off(self, _id:list) -> None:
        print(f'Off {_id}')
    def get_state(self, _id:list) -> bool:
        return True
    def get_mode(self, _id:list) -> str:
        return 'Input' if _id in self.list_input else 'Output'
    def switch(self, _id:list) -> None:
        pass
    def set_input(self, _id:int) -> bool:
        try:
            self.list_input.append(
                                    self.list_output.pop(
                                                            self.list_output.index(_id)
                                                        )
                                  )
        except:
            return False
        return True

    def set_output(self, _id:int) -> None:
        try:
            self.list_output.append(
                                    self.list_input.pop(
                                                            self.list_input.index(_id)
                                                        )
                                  )
        except:
            return False
        return True

    def list_input(self) -> list:
        return self.list_input

    def list_output(self) -> list:
        return self.list_output

    def close(self):
        pass