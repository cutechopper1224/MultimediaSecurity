import json
class TreeNodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TreeNode):
            d = {}
            d['ID'] = obj.ID
            d['PL'] = obj.PL
            d['PR'] = obj.PR
            d['FID'] = obj.FID
            d['D'] = list(obj.D)
            return d
        return json.JSONEncoder.default(self, obj)

class TreeNode():
    def __init__(self, ID, FID):
        self.ID = ID
        self.FID = FID
        self.PL = None
        self.PR = None
        self.D = []
