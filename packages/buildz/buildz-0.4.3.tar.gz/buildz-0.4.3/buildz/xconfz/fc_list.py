#coding=utf-8
from buildz.xconfz.base import *

from buildz.xconfz.fmt_base import *

class ListDeal(BaseDeal):
    def init(self, reg):
        self.k_l = reg(self.l)
        self.k_r = reg(self.r)
    def __init__(self, left, right):
        self.l = left
        self.r = right
    def prev(self, buff, queue):
        #c = buff.curr()
        if self.check_curr(buff,self.l):
            if buff.remain_size()>0:
                raise FormatExp("error string before list:", buff.pos_curr(), buff.full())
            queue.append(Item(self.k_l, buff.pos_curr()))
            buff.deal2curr(len(self.l))
            return True
        elif self.check_curr(buff, self.r):
            if buff.remain_size()>0:
                r = buff.remain().strip()
                if len(r)>0:
                    queue.append(Item(r, buff.pos_remain()))
            queue.append(Item(self.k_r, buff.pos_curr()))
            buff.deal2curr(len(self.r))
            return True
        return False
    def deal(self, queue, stack):
        if len(queue)==0:
            return False
        it = queue[0]
        rst = False
        if self.k_r.equal(it.val):
            tmp = []
            find_l = False
            while len(stack)>0:
                it_1 =  stack.pop(-1)
                if self.k_l.equal(it_1.val):
                    find_l = True
                    break
                tmp.append(it_1.val)
            if not find_l:
                print("queue:", queue)
                print("stack:", stack)
                print("list:", tmp)
                raise FormatExp("can't  find list left side for right side",it.pos)
            tmp.reverse()
            stack.append(Item(tmp, it_1.pos))
            rst = True
        elif self.k_l.equal(it.val):
            stack.append(it)
            rst = True
        if rst:
            queue.pop(0)
        return rst

pass


class ListFormat(BaseFormat):
    def __init__(self, left, right):
        self.l = left
        self.r = right 
    def deal(self, data, fc):
        if type(data) not in [list, tuple]:
            raise FormatExp("not list found:"+type(data), [-1,-1])
        node = FormatNode().init()
        node.add(SymbolFormatNode().init().val(self.l))
        #_node = FormatNode().init()
        #node.add(_node)
        nds = []
        for dt in data:
            nds.append(SpcFormatNode(0,1))
            nds.append(fc(dt))
            nds.append(SptFormatNode())
        for nd in nds[:-1]:
            node.add(nd)
        node.add(SpcFormatNode(0, 0))
        node.add(SymbolFormatNode().init().val(self.r))
        return node


pass