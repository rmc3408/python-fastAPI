
def find(keyTarget, valueTarget, listObj):
    for index, obj in enumerate(listObj):
        if obj.get(keyTarget) == valueTarget:
            return [index, obj]
    return [ -1, {}]    

