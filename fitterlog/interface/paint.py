import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from ..sql_proxy import Figure as Core_Figure

class Painter:
	def __init__(self , name , expe):
		self.name = name
		self.expe = expe
		self.fig = Core_Figure(name = name , experiment = expe.core)

	def __enter__(self):
		plt.figure()
		plt.title(self.name)
		return self

	def __exit__(self , *pargs , **kwargs):
		self.fig.html = self.save_html()
		pass

	def save_html(self):
		'''将当前的plt内容保存成html img对象
		'''
		buf = BytesIO()
		plt.savefig(buf)  
		plot_data = buf.getvalue()

		img_src = base64.b64encode(plot_data)

		img_src = img_src.decode()
		img_src = "data:image/png;base64," + img_src
		ele = "<img src=\"%s\">" % img_src

		return ele
