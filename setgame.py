from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from openexp.log import log
from openexp.mouse import mouse
from playsets import play 
import os,re

class setgame(item):
    description = u'An example game  plug-in'
    ordpat = re.compile(".*_(\d{1,2})$")
    def reset(self):
        self.var.duration = 1000*60*2
        self.experiment.var.sets_found = 0

    def prepare(self):
        item.prepare(self)
        self.c = canvas(self.experiment)
        ordm = setgame.ordpat.match(self.name)
        self.ord = 0 if ordm is None else int(ordm.group(1))

    def run(self):
        self.set_item_onset(self.playsets()) 

    def playsets(self):
        mmouse = mouse(self.experiment)
        mmouse.show_cursor()
        self.c.show()
        gameresults = play(self.experiment.window,self.var.duration)
                v = gameresults['found']
        #self.experiment.var[pref+'__wrong_attempts'] = gameresults['wrong']

class qtsetgame(setgame, qtautoplugin):
    def __init__(self, name, experiment, script=None):
        setgame.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def init_edit_widget(self):
        qtautoplugin.init_edit_widget(self)

