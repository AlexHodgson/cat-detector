'''
UI For the cat picture detector
'''

import wx
import wx.xrc

import cat_detector as cat

# Global Variables
recursive_search: bool = False  # If subfolders are searched for cat pics
folder_to_search: str # Folder to inspect for cats
files_with_cats = list[str] # Images containing cats

class frameMain ( wx.Frame ):

	def __init__( self):
		wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Cat Detector", pos = wx.DefaultPosition, size = wx.Size( 750,535 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		# Show cat pics here
		self.m_bitmap2 = wx.StaticBitmap( self.panelMain, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_bitmap2, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( bSizer12, 1, wx.EXPAND, 0 )


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
		self.settingsMenu_recursive.Check( recursive_search )

		self.m_menubar1.Append( self.menuSettings, u"Settings" )

		self.menuHelp = wx.Menu()
		self.m_menubar1.Append( self.menuHelp, u"Help" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )
		self.Show()

		# Connect Events
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged )
		self.buttonDetect.Bind( wx.EVT_BUTTON, self.buttonDetectOnButtonClick )
		self.m_listBox1.Bind( wx.EVT_LISTBOX, self.m_listBox1OnListBox )
		self.Bind( wx.EVT_MENU, self.settingsMenu_recursiveOnMenuSelection, id = self.settingsMenu_recursive.GetId() )

	def __del__( self ):
		pass


	# Event Handlers
	def m_dirPicker1OnDirChanged( self, event ):
		event.Skip()

	def buttonDetectOnButtonClick( self, event ):
		event.Skip()

	def m_listBox1OnListBox( self, event ):
		event.Skip()

	def settingsMenu_recursiveOnMenuSelection( self, event ):
		event.Skip()


def detect_cats():




if __name__ == "__main__":
    app = wx.App(False)
    frame = frameMain()
    app.MainLoop()