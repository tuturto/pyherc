"""{-
Copyright (c) 2009 Pauli Henrikki Rikula

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
-}"""

class NotImplemented(Exception):
    pass



class HeapSet(list):
    """
    This class tries to implement the 'index'-fnc of the list class
    more efficiently. Using this, you can chance the value of item in a
    heap in an efficient manner.
    Only those functionalities used in pyheapq.py file  are implemented.
    If you have one item in this tructure more than once, this class
    does not work properly anymore..
    """
    def __init__(self, iterator = None):
        self.pos_dict = {}
        self.pop_begin = 0
        if iterator != None:
            for i in iterator:
                self.append(i)

    def append(self, item):
        if item in self.pos_dict:
            raise ValueError("item %s appended twice."%str(item))
        self.pos_dict[item] = self.pop_begin + len(self)
        list.append(self, item)

    def __setitem__(self,pos, item):
        oldvalue = self.__getitem__(pos)
        if self.pos_dict[oldvalue] == pos:
            del self.pos_dict[oldvalue]

        list.__setitem__(self,pos, item)
        self.pos_dict[item] = self.pop_begin + pos


    def pop(self, pos = None):
        if pos == None:
            item = list.pop(self)
            pos = len(self)
        elif pos == 0:
            item = list.pop(self,0)
            self.pop_begin += 1
        else:
            raise ValueError('pop is implemented just for begin and end')

        del self.pos_dict[item]

        return item

    def index(self,item):
        return self.pos_dict[item] - self.pop_begin

    def __str__(self):
        return list.__str__(self) + str(self.pos_dict) + "pops %d"%self.pop_begin
