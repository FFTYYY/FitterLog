from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
import pdb
import os , sys
from YChat.objects import Member
from YChat.ui.gui_actions import message_box
from YChat.utils.rand_val import rand_port

class Liaison(QObject):

	def __init__(self , parent = None):
		super().__init__(parent = parent)
		self.memb = None
		self._logedin = False

	@pyqtSlot(str,str,str,int)
	def login(self,name,my_ip,room_ip,room_port):
		port = rand_port()
		self.memb = Member(my_ip = my_ip , name = name , listenport = port).prepare()
		self.memb.connect_room(room_ip = room_ip , room_port = room_port)

		self._logedin = True

	@pyqtSlot(result = bool)
	def logedin(self):
		return self._logedin

	@pyqtSlot(str)
	def say(self,words):
		if not self._logedin:
			return
		self.memb.say(words)

	@pyqtSlot(result = str)
	def messages(self):
		if not self._logedin:
			return
		return "\n".join(message_box)

	@pyqtSlot(result = str)
	def members(self):
		if not self._logedin:
			return ""
		return "\n".join(self.memb.room_members)


	@pyqtSlot()
	def logout(self):
		self.memb.logout()
		self._logedin = False


def main():
	import urllib
	import urllib.request
	import pickle
	resp = urllib.request.urlopen("http://127.0.0.1:8000/test").read()
	print(pickle.loads(resp))
	quit()
	
	path = os.path.abspath(os.path.join(os.path.dirname(__file__) , './main.qml'))
	path = path.replace("\\" , "/")
	path = "file:///" + path

	app = QGuiApplication([])
	view = QQuickView()
	view.setTitle("行云")

	lia = Liaison()
	cont = view.rootContext()
	cont.setContextProperty("lia", lia)

	view.setSource(QUrl(path))
	
	view.show()
	app.exec_()

if __name__ == "__main__":
	main()