from PySide6.QtCore import QObject, Signal


def create_signal(signal_type):
    class CustomSignal(QObject):
        signal = Signal(signal_type)

    return CustomSignal()
