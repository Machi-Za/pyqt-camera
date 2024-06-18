import sys
import Main
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)       
    main = Main.Main()
    main.show()
    sys.exit(app.exec_())
    