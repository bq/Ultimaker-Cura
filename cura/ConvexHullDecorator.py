from UM.Scene.SceneNodeDecorator import SceneNodeDecorator
from UM.Application import Application

class ConvexHullDecorator(SceneNodeDecorator):
    def __init__(self):
        super().__init__()
        self._convex_hull = None
        
        # In case of printing all at once this is the same as the convex hull. For one at the time this is the area without the head.
        self._convex_hull_boundary = None 
        
        # In case of printing all at once this is the same as the convex hull. For one at the time this is area with full head
        self._convex_hull_head = None
        
        self._convex_hull_node = None
        self._convex_hull_job = None

        self._profile = None
        Application.getInstance().getMachineManager().activeProfileChanged.connect(self._onActiveProfileChanged)
        self._onActiveProfileChanged()
    
    def getConvexHull(self):
        return self._convex_hull
    
    def getConvexHullHead(self):
        if not self._convex_hull_head:
            return self.getConvexHull()
        return self._convex_hull_head
    
    def getConvexHullBoundary(self):
        if not self._convex_hull_boundary:
            return self.getConvexHull()
        return self._convex_hull_boundary
    
    def setConvexHullBoundary(self, hull):
        self._convex_hull_boundary = hull
        
    def setConvexHullHead(self, hull):
        self._convex_hull_head = hull
    
    def setConvexHull(self, hull):
        self._convex_hull = hull
    
    def getConvexHullJob(self):
        return self._convex_hull_job
    
    def setConvexHullJob(self, job):
        self._convex_hull_job = job
    
    def getConvexHullNode(self):
        return self._convex_hull_node
    
    def setConvexHullNode(self, node):
        self._convex_hull_node = node
            
    def _onActiveProfileChanged(self):
        if self._profile:
            self._profile.settingValueChanged.disconnect(self._onSettingValueChanged)

        self._profile = Application.getInstance().getMachineManager().getActiveProfile()

        if self._profile:
            self._profile.settingValueChanged.connect(self._onSettingValueChanged)

    def _onSettingValueChanged(self, setting):
        if setting == "print_sequence":
            if self._convex_hull_job:
                self._convex_hull_job.cancel()
            self.setConvexHull(None)
            if self._convex_hull_node:
                self._convex_hull_node.setParent(None)
                self._convex_hull_node = None
