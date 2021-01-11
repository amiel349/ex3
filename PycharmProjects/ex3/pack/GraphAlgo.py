import json
import queue
import time

from pack.DiGraph import DiGraph
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import random




class GraphAlgo:

    def __init__(self, d_graph = None):
        if d_graph is None:
            self.g =DiGraph()
        else:
            self.g = d_graph

    def get_graph(self):
        return self.g

    def load_from_json(self, file_name: str):
        if self is None:
            return False
        new_graph = DiGraph()
        try:
          with open(file_name, 'r') as fp:
               jsn = json.load(fp)
          for item in jsn['Nodes']:
             new_graph.add_node(item.get('id'))
             if item.get('pos') is not None:
                pos = item.get('pos')
                x, y,z = pos.split(',')
                x=float(x)
                y = float(y)
                z= float(z)
                new_graph.get_node(item.get('id')).pos=(x,y,z)
          for edge in jsn['Edges']:
             src = edge['src']
             dest = edge['dest']
             w = edge['w']
             new_graph.add_edge(src, dest, w)
          self.g = new_graph
        except:
             print('cant open file')
             return False
        return True

    def save_to_json(self, filename):
        if self is None or self.g is None:
            return False
        x = []
        y = []
        try:
         for key, value in self.g.get_all_v().items():
             if value.pos is None :
                 x.append({"id": value.id})
             else:
                 s,t,u = value.pos
                 str_pos=str(s)+", "+str(t)+", "+"0.0"
                 x.append({"id": value.id, "pos": str_pos})
         for key, value in self.g.get_all_v().items():
             for sec_key, sec_val in self.g.all_out_edges_of_node(value.id).items():
                 y.append({"src": value.id, "dest": sec_val[0].id, "w": sec_val[1]})
         w = {}
         w["Nodes"] = x
         w["Edges"] = y
         with open(filename, 'w') as json_file:
             json.dump(w, json_file)
        except:
          print('Eror saving file')
          return False
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self is None or  self.g is None:
            return (float('inf'), [])
        if self.g.get_node(id1) is None or self.g.get_node(id2) is None:
            return (float('inf'), [])
        if id1 == id2:
            return (0, [id1])
        for key, node in self.g.get_all_v().items():
            node.w = -1
            node.tag = 0
        q = queue.PriorityQueue()
        dict_node = {}
        node = self.g.get_node(id1)
        node.w = 0
        q.put(node)
        while not q.empty():
            node = q.get()
            node.tag = 1
            ni_list = self.g.all_out_edges_of_node(node.id)
            for key, ni_node in ni_list.items():
                if self.g.get_node(ni_node[0].id).tag == 0:
                    sum = node.w+self.g.get_edge(node.id, ni_node[0].id)
                    if sum < self.g.get_node(ni_node[0].id).w or self.g.get_node(ni_node[0].id).w == -1:
                        self.g.get_node(ni_node[0].id).w=sum
                        dict_node[ni_node[0].id]=node.id
                        q.put( ni_node[0])
        arr_list = []
        if self.g.get_node(id2).w == -1:
            return (float('inf'), [])
        else:
            prev_node = id2
            arr_list.append(prev_node)
            prev_node = dict_node.get(prev_node)
            while prev_node != id1:
                arr_list.append(prev_node)
                prev_node = dict_node.get(prev_node)
            arr_list.append(id1)
            arr_list.reverse()
        tuple_list = (self.g.get_node(id2).w, arr_list)
        return tuple_list



    def connected_component(self, id1: int):
        if self.g is None or self.g.get_node(id1) is None:
            return []
        graph = GraphAlgo()
        self.DFS(self.g.get_node(id1))
        graph.g = self.reverse_graph(self.g)
        graph.DFS(graph.g.get_node(id1))
        list = []
        for node in graph.g.get_all_v().values():
            if node.tag == 1 and self.g.get_node(node.id).tag == 1:
                list.append(node.id)
        return list

    def reverse_graph(self, graph):
        graph2 = DiGraph()
        for node in graph.get_all_v().keys():
            graph2.add_node(node)
        for ver in graph.get_all_v().values():
            for edge in graph.all_out_edges_of_node(ver.id).values():
                graph2.add_edge(edge[0].id, ver.id, 0)
        return graph2

    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v):
        for node in self.g.get_all_v().values():
            node.tag = 0
        q = queue.LifoQueue(maxsize=0)
        v.tag = 1
        q.put_nowait(v)
        while not q.empty():
            v = q.get()
            for neighbour in self.g.all_out_edges_of_node(v.id).values():
                if neighbour[0].tag == 0:
                    neighbour[0].tag = 1
                    q.put(neighbour[0])

    def connected_components(self):
        list = []
        for ver in self.g.get_all_v().values():
            ver.w=-1
        for vertex in self.g.get_all_v().values():
            if vertex.w==1:
                continue;
            list2 = self.connected_component(vertex.id)
            for i in list2:
                self.g.get_node(i).w=1
            list.append(list2)
        return list

    def plot_graph(self):
      x = []
      y = []
      n = []
      max_x = -1000
      min_x = 1000
      max_y = -1000
      min_y = 1000

      for node in self.g.get_all_v().values():
          n.append(node.id)
          if node.pos is None:
              node.pos = (int(random.randrange(0, 100, 3)),int(random.randrange(0, 100, 8)),0)
          x.append(node.pos[0])
          y.append(node.pos[1])
          if node.pos[0] >max_x:
              max_x = node.pos[0]
          if node.pos[1] >max_y:
              max_y = node.pos[1]
          if node.pos[0] < min_x:
              min_x = node.pos[0]
          if node.pos[1] < min_y:
              min_y = node.pos[1]
      fig, ax = plt.subplots(facecolor=(0.5,0.8,0.8))
      ax.scatter(x, y,100,'red')
      for ver in self.g.get_all_v().values():#type Node
          for neighbour in self.g.all_out_edges_of_node(ver.id).values():
                    from_xy=(ver.pos[0],ver.pos[1])
                    to_xy=(neighbour[0].pos[0],neighbour[0].pos[1])
                    con = ConnectionPatch(from_xy, to_xy, "data", "data",
                                          arrowstyle="-|>", shrinkA=5, shrinkB=5,
                                          mutation_scale=18, fc="orange")
                    ax.add_artist(con)
                    #plt.annotate('', to_xy, from_xy ,arrowprops=dict(headwidth=5, width=0.5, shrink=0.07),)
      for i, txt in enumerate(n):
          ax.annotate(txt, (x[i], y[i]+0.0002))
      ax.text(0.5, 0.5, 'created by aviem and amiel', transform=ax.transAxes,
              fontsize=30, color='gray', alpha=0.5,
              ha='center', va='center', rotation='30')
      plt.axis([min_x-0.001,max_x+0.001,min_y-0.001,max_y+0.001])
      #plt.axis([0, 100, 0, 100])
      plt.xlabel('X axis')
      plt.ylabel('Y axis')
      ax.set_facecolor('#eafff5')
      ax.set_title('Directed Weighted Graph')
      plt.show()

    def __str__(self):
        print (self.g)
        return ""

if __name__ == '__main__':
    graph = GraphAlgo()
    for n in range(5):
        graph.g.add_node(n)
    graph.get_graph().add_edge(0, 2, 3.5)
    graph.get_graph().add_edge(1, 2, 3.5)
    graph.get_graph().add_edge(1, 3, 5)
    graph.get_graph().add_edge(1, 6, 6)
    graph.get_graph().add_edge(2, 0, 4)
    graph.get_graph().add_edge(2, 4, 4)
    graph.get_graph().add_edge(2, 5, 7)
    graph.get_graph().add_edge(3, 4, 1)
    graph.get_graph().add_edge(4, 1, 3)
    graph.get_graph().add_edge(6, 7, 2.3)
    graph.get_graph().add_edge(7, 6, 2.3)
    graph.get_graph().add_edge(6, 2, 2.3)
    graph.load_from_json('../data/A3')
    graph.plot_graph()
    # start = time.time()
    # #print(graph.connected_components())
    # end= time.time()
    # #print("time is ",end-start)



