class Vertex:
    """ A Vertex in a graph. """


    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
        element - the data or label to be associated with the vertex
        """
        self._element = element


    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)


    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()


    def element(self):
        """ Return the data for the vertex. """
        return self._element


class Edge:
    """
    An edge in a graph.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class Graph:
    """ Represent a simple graph.

    Variable oneway allows for directed graphs

    Implements the Adjacency Map style. Also maintains a top level
    dictionary of vertices.
    """

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edge appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """
        Add and return a vertex with element, if not already in graph.
        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    # Added variable oneway to handle directed graphs
    def add_edge(self, v, w, element, oneway = False):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        if oneway is True or v == w:
            self._structure[v][w] = e
        elif oneway is False:
            self._structure[v][w] = e
            self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)


def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        oneway = bool(file.readline().split()[1]) #read the one-way data
        edge = graph.add_edge(sv, tv, length, oneway)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


class Element:
    """ A key, value and index. """
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key

    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None


class APQ:
    def __init__(self):
        self._queue = []

    def min_leaf(self, i):
        """
        gets the lowest leaf for bubbling
        """
        if 2 * i + 2 > len(self._queue) - 1:
            return 2 * i + 1
        elif self._queue[2 * i + 1] < self._queue[2 * i + 2]:
            return 2 * i + 1
        else:
            return 2 * i + 2

    def bubble_down(self, index):
        '''
        Function for bubbling down through the list also checks if bubbling is needed
        '''
        while 2 * index + 1 < len(self._queue):
            # check that we still need to bubble down
            if self._queue[index] < self._queue[self.min_leaf(index)]:
                break
            min_leaf = self.min_leaf(index)
            self._queue[index]._index = min_leaf
            self._queue[min_leaf]._index = index
            self._queue[index], self._queue[min_leaf] = self._queue[min_leaf], self._queue[index]
            index = min_leaf

    def bubble_up(self, index):
        '''
        bubbles up through the queue also checks if its needed
        '''
        if index > 0:
            while self._queue[index] < self._queue[(index - 1) // 2]:
                parent = (index - 1) // 2
                self._queue[index]._index = parent
                self._queue[parent]._index = index
                self._queue[index], self._queue[parent] = self._queue[parent], self._queue[index]
                index = parent

    def add(self, key, item):
        # add key to end of list
        i = len(self._queue)
        element = Element(key, item, i)
        self._queue.append(element)
        # if it's not the first item bubble it up changing indices as you go
        self.bubble_up(i)
        return element

    def min(self):
        return self._queue[0]

    def remove_min(self):
        self._queue[0]._index = len(self._queue) - 1
        self._queue[len(self._queue)-1]._index = 0
        self._queue[0], self._queue[-1] = self._queue[-1], self._queue[0]
        # pop removed entry
        removed = self._queue.pop(-1)
        # bubble down
        self.bubble_down(0)
        return removed

    def update_key(self, element, newkey):
        if element._key > newkey:
            element._key = newkey
            self.bubble_up(element._index)
        elif element._key < newkey:
            element._key = newkey
            self.bubble_down(element._index)

    def get_key(self, element):
        return element._key


    def remove(self, element):
        self._queue[element._index]._index = len(self._queue) - 1
        self._queue[len(self._queue) - 1]._index = element._index
        self._queue[element._index], self._queue[-1] = self._queue[-1], self._queue[element._index]
        # pop removed entry
        removed = self._queue.pop(-1)
        # run both bubble functions as they have inbuilt check to see if they're needed before continuing
        self.bubble_down(element._index)
        self.bubble_up(element._index)
        return removed


def dijkstra(graph, vertex):
    open = APQ()
    locs = {}
    closed = {}
    preds = {vertex: None}
    open.add(0, vertex)
    locs[vertex] = 0
    while len(open._queue) > 0:
        min = open.remove_min()
        vert = min._value
        loc = locs.pop(vert)
        pred = preds.pop(vert)
        closed[vert] = (min._key, pred)
        v = graph.get_vertex_by_label(vert)
        if graph.get_edges(v) is not None:
            for edge in graph.get_edges(v):
                opposite = edge.opposite(v)
                if opposite._element not in closed:
                    newcost = min._key + edge._element
                    if opposite._element not in locs:
                        preds[opposite._element] = vert
                        added = open.add(newcost, opposite._element)
                        locs[opposite._element] = added
                    elif locs[opposite._element]._key > newcost:
                        preds[opposite._element] = vert
                        open.update_key(locs[opposite._element], newcost)
    print(closed)
    for unit in closed.items():
        print('Destination vertex:' + str(unit[0]) + '  Path length:' + str(unit[1][0]) + '   Previous vertex:'
              + str(unit[1][1]))
    return closed


def graphmapreader(filename):
    """ Read and return the route map in filename. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        coords = file.readline().split()
        coord1 = float(coords[1])
        coord2 = float(coords[2])
        vertex = graph.add_vertex(nodeid, coord1, coord2)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        file.readline()# read length
        time = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, time)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


class RouteMap(Graph):
    '''
    Used by the map reader function to generate the route map
    '''
    def __init__(self):
        Graph.__init__(self)
        self._vertexcoords = {}
        self._findvertex = {}

    def add_vertex(self, element, coord1=None, coord2=None):
        v = Vertex(element)
        self._findvertex[element] = v
        self._vertexcoords[v] = (coord1, coord2)
        self._structure[v] = dict()
        return v

    def __str__(self):
        if super().num_vertices() < 100 and super().num_vertices() < 100:
            return super().__str__()
        else:
            return 'To many entries wil not be represented by string'

    def get_vertex_by_label(self, element):
        return self._findvertex[element]

    def sp(self, v, w):
        closed = dijkstra(self, v)
        print('Type,Latitude,Longitude,element,cost')
        while w != v:
            label = self.get_vertex_by_label(w)
            latitude = self._vertexcoords[label][0]
            longitude = self._vertexcoords[label][1]
            element = w
            cost = closed[w][0]
            print('W,' + str(latitude) + ',' + str(longitude) + ',' + str(element) + ',' + str(cost))
            w = closed[w][1]
