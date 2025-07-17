from gui.datapoint import Datapoint


class GuiModule:

    def __init__(self, datapoint: Datapoint, changed_signal=None) -> None:
        self.datapoint = datapoint
        self.error = None
        if changed_signal:
            changed_signal.connect(self.publish)
        self.datapoint.value_changed.connect(self.update)

    def publish(self):
        value = self.get_value()
        error = self.datapoint.submit_value(value)
        self.error = error
    
    def update(self):
        self.set_value(self.datapoint.value)

    def get_value(self):
        return None
    
    def set_value(self, value):
        raise Exception(
            f"set_value() method not implemented for {self.__class__.__name__}"
        )

