import json

import wx

import questions as q


# Some global constants
# I know this violates the wx style guide but I'm still revising this
ID_EASY = wx.NewId()
ID_MEDIUM = wx.NewId()
ID_HARD = wx.NewId()
ID_PLUS = wx.NewId()
ID_MINUS = wx.NewId()
ID_TIMES = wx.NewId()
ID_DIVIDE = wx.NewId()


class MainMenu(wx.MenuBar):
    """This class defines the main menues of the app."""
    
    def __init__(self, parent):
        """Creates the main menues"""
        super(MainMenu, self).__init__()
        self.parentframe = parent
        self.InitMenus()
        
    def InitMenus(self):
        """Initializes the main menues"""
        file_menu = wx.Menu()
        file_item_reset = file_menu.Append(id=wx.ID_ANY, text='Rese&t',
                                           help='Reset score')
        file_item_exit = wx.MenuItem(parentMenu=file_menu,  id=wx.ID_EXIT,
                                     text='&Quit')
        file_menu.AppendItem(item=file_item_exit)
        
        # Option menu
        self.options_menu = wx.Menu()
        
        # Difficulty radio items
        self.options_menu.Append(id=ID_EASY, text='&Easy',
                                 kind=wx.ITEM_RADIO)
        self.options_menu.Append(id=ID_MEDIUM, text='&Medium',
                                 kind=wx.ITEM_RADIO)
        self.options_menu.Append(id=ID_HARD, text='&Hard', kind=wx.ITEM_RADIO)
        
        # check easy option by default
        self.options_menu.Check(id=ID_EASY, check=True)
        
        self.options_menu.AppendSeparator()
        
        # Operations check items
        self.options_menu.Append(id=ID_PLUS, text='Addition',
                                 help='Include addition questions',
                                 kind=wx.ITEM_CHECK)  
        self.options_menu.Append(id=ID_MINUS, text='Subtraction',
                                 help='Include subtraction questions',
                                 kind=wx.ITEM_CHECK)
        self.options_menu.Append(id=ID_TIMES, text='Multiplication',
                                 help='Include multiplication questions',
                                 kind=wx.ITEM_CHECK)
        self.options_menu.Append(id=ID_DIVIDE, text='Division',
                                 help='Include division questions',
                                 kind=wx.ITEM_CHECK)
        
        # Check plus and minus options by default
        self.options_menu.Check(id=ID_PLUS, check=True)
        self.options_menu.Check(id=ID_MINUS, check=True)
        
        # help menus
        help_menu = wx.Menu()
        help_about = help_menu.Append(id=wx.ID_ANY,
                                      text='&About ArithmoPhile...')  
        
        # Bind all the menu items
        self.Bind(wx.EVT_MENU, self.SetDifficulty, id=ID_EASY)
        self.Bind(wx.EVT_MENU, self.SetDifficulty, id=ID_MEDIUM)
        self.Bind(wx.EVT_MENU, self.SetDifficulty, id=ID_HARD)
        self.Bind(wx.EVT_MENU, self.SetQuestionTypes, id=ID_PLUS)
        self.Bind(wx.EVT_MENU, self.SetQuestionTypes, id=ID_MINUS)
        self.Bind(wx.EVT_MENU, self.SetQuestionTypes, id=ID_TIMES)
        self.Bind(wx.EVT_MENU, self.SetQuestionTypes, id=ID_DIVIDE)
        self.Bind(wx.EVT_MENU, self.OnReset, file_item_reset)
        self.Bind(wx.EVT_MENU, self.parentframe.OnCloseWindow, file_item_exit)
        self.Bind(wx.EVT_MENU, self.OnAbout, help_about)
        
        self.Append(file_menu, '&File')
        self.Append(self.options_menu, '&Options')
        self.Append(help_menu, '&Help')
    
    def OnReset(self, e):
        """Resets the scoreboard to zero"""
        self.parentframe.InitScore()
    
    def SetDifficulty(self, e):
        """Sets the difficulty then generates new question"""
        easy = self.options_menu.FindItemById(ID_EASY).IsChecked()
        medium = self.options_menu.FindItemById(ID_MEDIUM).IsChecked()
        hard = self.options_menu.FindItemById(ID_HARD).IsChecked()
        
        level = (easy * q.EASY)|(medium * q.MEDIUM)|(hard * q.HARD)
        self.parentframe.difficulty = level
        self.parentframe.GenerateProblem()
    
    def SetQuestionTypes(self, e):
        """Sets operations to include then generates new question"""
        plus   = self.options_menu.FindItemById(ID_PLUS).IsChecked()
        minus  = self.options_menu.FindItemById(ID_MINUS).IsChecked()
        times  = self.options_menu.FindItemById(ID_TIMES).IsChecked()
        divide = self.options_menu.FindItemById(ID_DIVIDE).IsChecked()
        
        # bitwise operation to set user choice
        ops = (plus * q.PLUS)|(minus * q.MINUS)|\
              (times * q.TIMES)|(divide * q.DIVIDE)
        
        if not ops:
            wx.MessageBox('You must select at least one arithmetic operation.', 'Error')
            self.options_menu.Check(ID_PLUS, True)
            self.options_menu.Check(ID_MINUS, True)
            ops = q.PLUS|q.MINUS
        
        self.parentframe.operations = ops
        self.parentframe.GenerateProblem()
    
    def OnAbout(self, e):
        """Brings out the About dialog box"""
        with open('about.dat', 'r') as f:
            data = json.load(f)
            info = wx.AboutDialogInfo()
            info.SetName(data['name'])
            info.SetVersion(data['version'])
            info.SetDescription(data['description'])
            info.SetCopyright(data['copyright'])
            info.SetWebSite(data['website'])
            info.SetLicence(data['license'])
            info.AddDeveloper(data['developer'])
            wx.AboutBox(info)


class TextPanel(wx.Panel):
    """This panel holds the string of the question to be posted."""
    
    def __init__(self, parent):
        """Creates the text panel"""
        super(TextPanel, self).__init__(parent)
        self.InitUI()
    
    def InitUI(self):
        """Initializes panel properties such as fonts and layout"""
        font = wx.Font(pointSize=32,
                       family=wx.FONTFAMILY_MODERN,
                       style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_BOLD)
        
        self.text = wx.StaticText(self, label='Loading...',
            style=wx.ALIGN_CENTRE_HORIZONTAL)
        
        self.text.SetFont(font)
        self.vbox = wx.StaticBoxSizer(
            box=wx.StaticBox(self, label='&Problem'),
            orient=wx.VERTICAL
        )
        
        vbox_flag = wx.ALL|wx.EXPAND|\
                    wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL    
        
        self.vbox.Add(
            item=self.text,
            proportion=1,
            flag=vbox_flag,
            border=5
        )
        
        self.SetSizer(self.vbox)
        self.Show()
    
    def PostProblem(self, problem):
        """Displays the question onto the panel"""
        x, y, a, s = problem
        self.text.SetLabel('%d %s %d' % (x, s, y))
        
        self.vbox.Layout()
        self.Update()


class ScoreBoard(wx.Panel):
    """This defines the display and behavior of the scoreboard."""
    
    def __init__(self, parent):
        """Creates the scoreboard object"""
        super(ScoreBoard, self).__init__(parent)
        self.InitUI()
        self.Show()
    
    def InitUI(self):
        """Initializes the scoreboard display and layout"""
        self.correct = wx.StaticText(parent=self, label='0', 
                                     style=wx.ALIGN_LEFT)
        self.wrong = wx.StaticText(self, label='0', style=wx.ALIGN_LEFT)
        
        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_SWISS,
                       style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        
        self.correct.SetFont(font)
        self.wrong.SetFont(font)
        
        c_icon = wx.StaticBitmap(
            parent=self,
            bitmap=wx.Bitmap('Images\\correct.png')
        )
        w_icon = wx.StaticBitmap(
            parent=self,
            bitmap=wx.Bitmap('Images\\wrong.png')
        )
        
        pnl = wx.Panel(self)    # blank
        
        self.sizer = wx.GridBagSizer(5, 5)
        self.sizer.Add(pnl, pos=(0, 0), span=(1, 6), flag=wx.EXPAND)
        self.sizer.Add(c_icon, pos=(0, 6), flag=wx.EXPAND)
        self.sizer.Add(self.correct, pos=(0, 7),
                       flag=wx.RIGHT|wx.EXPAND, border=10)
        self.sizer.Add(w_icon, pos=(0, 8), flag=wx.EXPAND)
        self.sizer.Add(self.wrong, pos=(0, 9),
                       flag=wx.RIGHT|wx.EXPAND, border=10)
        
        self.sizer.AddGrowableCol(0)
        self.SetSizerAndFit(self.sizer)
    
    def UpdateScore(self, c, w):
        """Updates the current score of the user"""
        self.correct.SetLabel('%d' % c)
        self.wrong.SetLabel('%d' % w)
        self.sizer.Layout()
        self.Update()


class Sounds(object):
    """This class defines the properties of sounds used in the app."""

    def __init__(self, parent):
        """Creates an instance of the Sounds class"""
        self.clips = {}
        self.InitSoundClips()
    
    def InitSoundClips(self):
        """Initializes the sound files and properties"""
        self.clips['correct'] = wx.Sound('Sounds\\ding.wav')
        self.clips['wrong'] = wx.Sound('Sounds\\buzz.wav')
        
        for k, v in self.clips.iteritems():
            if not v.IsOk():
                wx.MessageBox('Invalid sound file', 'Error')


class MainFrame(wx.Frame):
    """This is the main window and controls the overall app."""

    def __init__(self, parent, title):
        """Creates an instance of the main class window"""
        super(
            MainFrame,
            self).__init__(parent,
            title=title,
            style=wx.SYSTEM_MENU|wx.CAPTION|wx.MINIMIZE_BOX|wx.CLOSE_BOX
        )
        self.InitUI()
        self.Centre()
        self.Show()
        self.InitScore()
        self.InitOptions()
        self.GenerateProblem()
        self.sound = Sounds(self)
    
    def InitScore(self):
        """Sets the initial state of the scoreboard"""
        self.score = {'tries':0, 'correct':0, 'wrong':0, 'skips':0}
        self.scoreboard.UpdateScore(
            self.score['correct'],
            self.score['wrong']
        )
    
    def InitOptions(self):
        """Sets the initial state of the app options"""
        self.difficulty = q.EASY
        self.operations = q.PLUS|q.MINUS
    
    def InitUI(self):
        """Sets the display and layout properties of the main window"""
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 5)
        
        menu_bar = MainMenu(self)
        
        self.scoreboard = ScoreBoard(panel)
        sizer.Add(self.scoreboard, pos=(0, 0), span=(1, 5),
                  flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        self.txt_panel = TextPanel(panel)
        sizer.Add(self.txt_panel, pos=(1, 0), span=(4, 5),
                  flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        text = wx.StaticText(panel, label='&Answer:')
        sizer.Add(text, pos=(6, 0),
                  flag=wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL,
                  border=10)
        
        self.tc = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER|wx.TE_RIGHT)
        sizer.Add(self.tc, pos=(6, 1), span=(1, 2),
                  flag=wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL,
                  border=10)
        
        go_btn = wx.Button(panel, label='Sub&mit')
        sizer.Add(go_btn, pos=(6, 3),
                  flag=wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL,
                  border=10)
        
        read_btn = wx.Button(panel, label='&Read')
        sizer.Add(read_btn, pos=(6, 4),
                  flag=wx.BOTTOM|wx.RIGHT, border=10)
        
        self.tc.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        go_btn.Bind(wx.EVT_BUTTON, self.OnTextEnter)
        read_btn.Bind(wx.EVT_BUTTON, self.OnRead)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        self.SetMenuBar(menu_bar)
        
        panel.SetSizer(sizer)
        
        panel.Fit()
        self.Fit()
        self.tc.SetFocus()
    
    def GenerateProblem(self):
        """Gets the question object"""
        ops = q.Question(self.difficulty, self.operations).GetQuestion()
        self.txt_panel.PostProblem(ops)
        self.x, self.y, self.a, self.s = ops
        self.Update()
        self.score['tries'] += 1
    
    def OnTextEnter(self, event):
        """Processes the user's answer"""
        input = self.tc.GetValue().strip()
        
        if len(input) == 0:
            self.score['skips'] += 1
        else:
            try:
                ans = int(input)
            except Exception, e:
                wx.MessageBox('Error:%s' % e, 'Error', 
                      wx.OK | wx.ICON_INFORMATION)
            else:
                if ans == self.a:
                    self.sound.clips['correct'].Play()
                    self.score['correct'] += 1
                else:
                    self.sound.clips['wrong'].Play()
                    self.score['wrong'] += 1
                
                self.scoreboard.UpdateScore(
                    self.score['correct'],
                    self.score['wrong']
                )
            finally:
                self.tc.SetFocus()
                self.tc.Clear()
                self.GenerateProblem()
    
    def OnRead(self, event):
        """Sets focus on question so screenreaders can read"""
        self.txt_panel.text.SetFocus()
    
    def OnCloseWindow(self, e):
        """Prompts user on exit"""
        dial = wx.MessageDialog(None, 'Are you sure you want to quit?', 'Question',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            
        ret = dial.ShowModal()
        
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()


if __name__ == '__main__':
    app = wx.App()
    mnf = MainFrame(None, title='ArithmoPhile')
    app.MainLoop()
