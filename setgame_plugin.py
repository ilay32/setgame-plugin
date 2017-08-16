from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from openexp.log import log
from openexp.mouse import mouse
import os,re,sys,pprint
sys.path.insert(0,os.path.dirname(__file__)+'/setgame')
from playset import RunGame

class setgame_plugin(item):
    description = u'An example game  plug-in'
    #ordpat = re.compile(".*_(\d{1,2})$")
    def reset(self):
        self.var.duration = 1000*60*2
        self.var.mode = "play"
        self.var.lang = "he" #one may add a language option in the gui and...
        self.var.show_timer = "yes"

    def prepare(self):
        self.experiment.var.personal_record = 0
        item.prepare(self)
        self.c = canvas(self.experiment)
        #ordm = setgame_plugin.ordpat.match(self.name)
        #self.ord = 0 if ordm is None else int(ordm.group(1))
        self.fullscreen = False if self.experiment.var.fullscreen == "no" else True
        

    def run(self):
        mmouse = mouse(self.experiment)
        mmouse.show_cursor()
        self.c.show()
        runner = RunGame(mode=self.var.mode, \
            frame  = self.experiment.window, \
            duration = self.var.duration, \
            language = self.lang, \
            fullscreen = self.fullscreen, \
            show_timer = self.var.show_timer
        )

        gameresults = runner.run()()
        if gameresults != "keyboard interrupt":
            pr = runner.feedback_screen(gameresults,self.experiment.var.personal_record)
            self.experiment.var.set('personal_record',pr)
            self.set_vars(gameresults)

    def set_vars(self,data):
        for k,v in data.iteritems():
            self.experiment.var.set(k,v)
            if k == 'score' and v > self.experiment.var.personal_record:
                self.experiment.var.personal_record = v

            
class qtsetgame_plugin(setgame_plugin, qtautoplugin):
    def __init__(self, name, experiment, script=None):
        setgame_plugin.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def init_edit_widget(self):
        qtautoplugin.init_edit_widget(self)

