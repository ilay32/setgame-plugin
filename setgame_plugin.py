from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from openexp.log import log
from openexp.mouse import mouse
import os,re,sys
sys.path.insert(0,os.path.dirname(__file__)+'/setgame')
from playset import play

class setgame_plugin(item):
    description = u'An example game  plug-in'
    ordpat = re.compile(".*_(\d{1,2})$")
    def reset(self):
        self.var.duration = 1000*60*2
        self.var.sets_found = 0


    def prepare(self):
        item.prepare(self)
        self.c = canvas(self.experiment)
        ordm = setgame_plugin.ordpat.match(self.name)
        self.ord = 0 if ordm is None else int(ordm.group(1))
        
    #def run(self):
    #    self.set_item_onset(self.playsets()) 

    def run(self):
        mmouse = mouse(self.experiment)
        mmouse.show_cursor()
        self.c.show()
        fullscreen = False if self.experiment.var.fullscreen == "no" else True
        gameresults = play(self.experiment.window,self.var.duration,fullscreen)
        self.var.sets_found = gameresults['found']
        self.experiment.var.score = self.var.sets_found

class qtsetgame_plugin(setgame_plugin, qtautoplugin):
    def __init__(self, name, experiment, script=None):
        setgame_plugin.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def init_edit_widget(self):
        qtautoplugin.init_edit_widget(self)

