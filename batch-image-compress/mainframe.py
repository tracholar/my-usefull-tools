# coding:utf-8
import wx
import os
from camera_compress import batch_compress_image

class MainFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(600,350), \
				style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
		
		self.panel = wx.Panel(self)
		self.button = wx.Button(self.panel, label="start",pos=(10,200))
		
		wx.Button(self.panel, label="source", pos=(10,10))
		self.src = wx.TextCtrl(self.panel, size=(400,30), pos=(150, 10))
		
		wx.Button(self.panel, label="target", pos=(10,50))
		self.target = wx.TextCtrl(self.panel,  size=(400,30), pos=(150, 50))
		
		
		
		
		self.statusbar = self.CreateStatusBar()
		
		self.panel.Bind(wx.EVT_BUTTON, self.OnButtonClick)
		
		wx.StaticText(self.panel, label="Create by tracholar, all right reserved.", pos=(10, 250))

		
		self.Show(True)
	def OnButtonClick(self, event):
		label = event.GetEventObject().GetLabel()
		if label == 'source':
			d = self.select_src()
			self.src.SetValue(d)
		if label == 'target':
			d = self.select_src()
			self.target.SetValue(d)
			
		if label == 'start':
			src = self.src.GetValue()
			target = self.target.GetValue()
			if src == '' or not os.path.exists(src):
				self.statusbar.SetStatusText('Error: source directory not found!')
				return
				
			self.statusbar.SetStatusText('start ...')
			batch_compress_image(src, target,
								callback = lambda msg: self.statusbar.SetStatusText(msg))
			self.statusbar.SetStatusText('done ...')
			
	def select_src(self):
		dialog = wx.DirDialog(self, "Choose a directory")
		dialog.ShowModal()
		d = dialog.GetPath()
		dialog.Destroy()
		return d
		
app = wx.App(False)
frame = MainFrame(None,  "Camera Image Compress")
app.MainLoop()
