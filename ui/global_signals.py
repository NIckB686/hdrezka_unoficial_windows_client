from PySide6.QtCore import QObject, Signal


class GlobalSignals(QObject):
    card_clicked = Signal(str)

signals = GlobalSignals()
