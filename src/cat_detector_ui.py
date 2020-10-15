'''
UI For the cat picture detector
Base window built with Wx Form Builder
'''
import os
import threading

import wx
import wx.xrc

import detector_backend as cat

class frameMain ( wx.Frame ):

	def __init__( self):

		self.recursive_search: bool = False  # If subfolders are searched for cat pics
		self.folder_to_search: str # Folder to inspect for cats
		self.files_to_scan = list # Files to scan for cats
		self.files_with_cats = list # Images containing cats

		wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Cat Detector", pos = wx.DefaultPosition, size = wx.Size( 750,535 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.SetIcon(wx.Icon("media/icon_cat.png"))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

		bSizerMainFrame = wx.BoxSizer( wx.VERTICAL )

		self.panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerMainPanel = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		# Directory selector
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.panelMain, wx.ID_ANY, u"Selected Folder" ), wx.VERTICAL )
		self.m_dirPicker1 = wx.DirPickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		sbSizer1.Add( self.m_dirPicker1, 0, wx.ALL|wx.EXPAND, 10 )


		bSizer11.Add( sbSizer1, 1, wx.EXPAND, 0 )

		# Button to run search
		self.buttonDetect = wx.Button( self.panelMain, wx.ID_ANY, u"Detect Cats", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.buttonDetect, 0, wx.EXPAND, 10 )
		bSizerMainPanel.Add( bSizer11, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		# List of cat pictures
		m_listBox1Choices = []
		self.m_listBox1 = wx.ListBox( self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), m_listBox1Choices, 0 )
		bSizer9.Add( self.m_listBox1, 1, wx.ALL, 10 )


		bSizer8.Add( bSizer9, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		# Show cat pics here
		self.bSizerBitmap = wx.BoxSizer( wx.HORIZONTAL )
		self.bitmap1 = wx.StaticBitmap( self.panelMain, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bSizerBitmap.Add( self.bitmap1, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( self.bSizerBitmap, 1, wx.EXPAND, 0 )


		bSizer8.Add( bSizer10, 1, wx.EXPAND, 5 )


		bSizerMainPanel.Add( bSizer8, 1, wx.EXPAND, 5 )


		self.panelMain.SetSizer( bSizerMainPanel )
		self.panelMain.Layout()
		bSizerMainPanel.Fit( self.panelMain )
		bSizerMainFrame.Add( self.panelMain, 1, wx.EXPAND |wx.ALL, 0 )


		bSizerFrameMain.Add( bSizerMainFrame, 1, wx.ALL|wx.EXPAND, 0 )

		# Status and menu bars
		self.SetSizer( bSizerFrameMain )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.menuDetect = wx.Menu()
		self.m_menubar1.Append( self.menuDetect, u"Detect Cats" )

		self.menuSettings = wx.Menu()
		self.settingsMenu_recursive = wx.MenuItem( self.menuSettings, wx.ID_ANY, u"Search Subfolders", wx.EmptyString, wx.ITEM_CHECK )
		self.menuSettings.Append( self.settingsMenu_recursive )
		self.settingsMenu_recursive.Check( self.recursive_search )

		self.m_menubar1.Append( self.menuSettings, u"Settings" )

		self.menuHelp = wx.Menu()
		self.m_menubar1.Append( self.menuHelp, u"Help" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )
		self.Show()

		# Connect Events
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged )
		self.buttonDetect.Bind( wx.EVT_BUTTON, self.buttonDetectOnButtonClick)
		self.m_listBox1.Bind( wx.EVT_LISTBOX, self.m_listBox1OnListBox )
		self.Bind( wx.EVT_MENU, self.settingsMenu_recursiveOnMenuSelection, id = self.settingsMenu_recursive.GetId() )

	def __del__( self ):
		pass


	# Event Handlers

	# New directory chosen
	def m_dirPicker1OnDirChanged( self, event):
		self.folder_to_search = event.GetPath()

	# Click the detect cat button
	def buttonDetectOnButtonClick( self, event):

		# Make list of candiate files
		if (self.recursive_search):
			absFiles = self.getListOfFiles(self.folder_to_search)

			# Change to relative paths
			relFiles = list()
			for f in absFiles:
				relFiles.append(os.path.relpath(f, start = self.folder_to_search))

			self.files_to_scan = relFiles
		else:
			self.files_to_scan = os.listdir(self.folder_to_search)
			



		# Send to NN
		if (self.folder_to_search):
			self.files_with_cats = self.detect_cats()

			# Put cat pic names in list box
			self.m_listBox1.Clear()
			for f in self.files_with_cats:
				self.m_listBox1.Append(f)

		else:
			raise TypeError("The Base Directory Cannot Be None")
	
	# On selection of image name in list box, show a preview
	def m_listBox1OnListBox( self, event):
		try:
			file_name = event.GetString()
			img_file = os.path.join(self.folder_to_search,file_name)
			# load the image
			Img = wx.Image(img_file, wx.BITMAP_TYPE_ANY)
		except Exception as e:
			print(str(e))

		#scale the image, preserving the aspect ratio
		W = Img.GetWidth()
		H = Img.GetHeight()

		# Fit image to sizer with a border of 10
		boxSize = self.bSizerBitmap.GetSize()
		boxW = boxSize.GetWidth() - 10
		boxH = boxSize.GetHeight() - 10
		if W > H:
			NewW = boxW
			NewH = boxH * H / W
		else:
			NewH = boxH
			NewW = boxW * W / H
		Img = Img.Scale(NewW,NewH)
 
		# convert it to a wx.Bitmap, and put it on the wx.StaticBitmap
		self.bitmap1.SetBitmap(wx.Bitmap(Img)) # wx.BitmapFromImage

	# Toggle recursive file search
	def settingsMenu_recursiveOnMenuSelection( self, event ):
		
		if self.settingsMenu_recursive.IsChecked():
			self.recursive_search = True
		else:
			self.recursive_search = False

	# Call cat detection
	def detect_cats(self):
		return cat.find_cats(self.folder_to_search, self.files_to_scan) # Leave threshold at default for now

	def getListOfFiles(self, dirName):
		'''
		Recursively create a list of file and sub directories names in the given directory
		'''
		listOfFile = os.listdir(dirName)
		allFiles = list()
		# Iterate over all the entries
		for entry in listOfFile:
			# Create full path
			fullPath = os.path.join(dirName, entry)
			# If entry is a directory then get the list of files in this directory 
			if os.path.isdir(fullPath):
				allFiles = allFiles + self.getListOfFiles(fullPath)
			else:
				allFiles.append(fullPath)

		return allFiles

if __name__ == "__main__":
    app = wx.App(False)
    frame = frameMain()
    app.MainLoop()