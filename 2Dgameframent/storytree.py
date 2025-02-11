
class StoryNode:
    def __init__(self):
        self.story=None
        self.childNode=[]

if __name__=="__main__":
    Node0=StoryNode()
    Node0.story="first meet"
    Node1=StoryNode()
    Node1.story="merry"
    Node2=StoryNode()
    Node2.story="depart"
    Node0.childNode=[Node1,Node2]
