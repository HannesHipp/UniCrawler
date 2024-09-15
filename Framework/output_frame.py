from framework.frame import Frame
from framework.function import Function


class OutputFrame(Frame):

    def __init__(
            self, 
            path, 
            function: Function, 
            datapoints=[],
            next_frame_button_names=[], 
            start_button_name=None, 
            cancel_button_name=None):
        super().__init__(path, datapoints, next_frame_button_names)
        self.function = function
        self.function.setAutoDelete(False)

        if cancel_button_name:
           getattr(self, cancel_button_name).pressed.connect(self.function.cancel_execution)

        if start_button_name:
           self.auto_start = False
           getattr(self, start_button_name).pressed.connect(self.function.start_execution)
        else:
           self.auto_start = True

        if not next_frame_button_names:
           self.function.signals.ended.connect(self.finalize)
            
    def show(self):
        if self.auto_start:
            self.function.start_execution()
        super().show()

    def finalize(self):
        function_error = self.function.error
        if function_error:
            self.show_errors(function_error)
        super().finalize()

    def get_sender_name(self, sender):
        try:
            sender_name = super().get_sender_name(sender)
        except:
            sender_name = None
        return sender_name
