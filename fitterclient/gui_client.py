from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
import pdb
import os , sys
from YTools.network.server.client import Requester

class Liaison(QObject):

	def __init__(self , parent = None):
		super().__init__(parent = parent)
		self.req = None
		self.num_nouns = -1

	@pyqtSlot(str , str , result = bool)
	def connect(self , ip , port):
		self.req = Requester(ip = ip , port = port)
		return True

	@pyqtSlot(result = int)
	def noun_cnt(self):
		self.num_nouns = int( self.req.request("noun_cnt") )
		return self.num_nouns

def main():
	
	path = os.path.abspath(os.path.join(os.path.dirname(__file__) , './enter.qml'))
	path = path.replace("\\" , "/")
	path = "file:///" + path

	app = QGuiApplication([])
	view = QQuickView()
	view.setTitle("行云")

	liaison = Liaison()
	cont = view.rootContext()
	cont.setContextProperty("L", liaison)

	view.setSource(QUrl(path))
	
	view.show()
	app.exec_()

if __name__ == "__main__":
	main()