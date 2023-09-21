#najítí všech tras(path,start,end) ->trasy
#začít na startu a jít po barevnejch pixelech. každé rozdvojení vytváří novou cestu
#   pohyb enemáků(trasy) ->pohyb vektor

#může věž střílet(věž,enemak) ->bool
#vyslat fake projektil a zjistit jestli tam není zeď

#jakým směrem střílet(věž,enemak) ->vektor
#   jak dlouho to poletí na současnou polohu
#   posunout enemaka o ten čas vrátit jeho směr od věže
from pygame import Rect
from queue import Queue
from pygame.sprite import RenderUpdates
class AI:
    """Class for moving enemies and firing towers"""
    def __init__(self,level:dict,enemies:RenderUpdates) -> None:
        self.level=level
        self.enemies = enemies
        self.enemypaths ={}
        self.available_paths = {}


        #this is silly needs to be done better
        for i in range(len(enemies)):
            self.enemypaths[i]=["",0]

    #path finding methods
    def najdi_sousedy(self,vertex:Rect,visited:list[Rect]=[])->list[Rect]:
        """Returns not visited neighbours for a vertex"""
        path=self.level["path"]
        sousedi=[]
        for node in path:
            if node in visited:continue
            distance = (abs(node.x-vertex.x),abs(node.y-vertex.y))
            if distance == (0,16) or distance == (16,0):
                sousedi.append(node)
        return sousedi

    def find_paths(self,start:Rect)->None:
        """Finds all the paths in the level"""
        vertex=start[0]
        q = Queue()
        q.put((vertex,1))
        self.available_paths[1]=[]
        while not q.empty():
            node,cesta=q.get()
            self.available_paths[cesta].append(node)
            sousedi = self.najdi_sousedy(node,self.available_paths[cesta])

            if node == self.level["end"][0] or not len(sousedi):
                continue

            
            q.put((sousedi.pop(),cesta))
            for soused in sousedi:
                pathid = len(list(self.available_paths))+1
                self.available_paths[pathid] = self.available_paths[cesta].copy()
                q.put((soused,pathid))

    def get_next_step(self,enemy):
        """Returns next step in the apropriet path for the enemy"""
        pathid = self.enemypaths[enemy][0]
        self.enemypaths[enemy][1] +=1
        positionindex =self.enemypaths[enemy][1]
        try:
            return self.available_paths[pathid][positionindex]
        except:
            pass
    
    def filter_paths(self):
        pruchozi_cesty = {}
        for path in self.available_paths:
            if self.available_paths[path]==self.level["end"][0]:
                pruchozi_cesty[path]=self.available_paths[path]
        self.available_paths = pruchozi_cesty