if __name__ == "__main__":
    from worktime import WorkTime
    import sys
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    app = QApplication(sys.argv)
    w = WorkTime()
    sys.exit(app.exec_())
