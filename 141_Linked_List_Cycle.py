class ListNode(object):
    def __init__(self,x):
        self.val=x
        self.next=None

class Solution(object):
    def hasCycle(self,head):
        ListRemine=[]
        while head:
            if head.val in ListRemine:
                return True
            else:
                ListRemine.append(head.val)
                head=head.next
        return False
