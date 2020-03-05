import numpy as np

def read_tabular( name ) :
    with open(name) as f:
        content = f.readlines()
    content = [x.split() for x in [x.strip().replace(',', '.') for x in content] if not x[0] == '#' ]
    return content

def float_list( l ):
    ret = []
    for x in l:
        try:
            ret.append(float(x))
        except ValueError:
            continue
    return ret

class Tabular:
    def __init__(self, tab, raw=True):
        if raw :
            self.columns = tab[0][::2]
            self.units = tab[0][1::2]
            data = tab[1:]
        else :
            self.columns = tab[0]
            self.units = tab[1]
            data = tab[2:]
        self.data = np.array([ float_list(x) for x in data ])

    def __str__(self):
        string = "Tabular( {},\n{},\n".format(self.columns, self.units)
        for d in self.data[:-1]:
            string += "{},\n".format(d)
        return string + "{} )".format(self.data[-1])

    def __repr__(self):
        return str(self)

def configure_tabular( tab, config_name ):
    configs = read_tabular( config_name )
    data = [ list(d[0]) + list(d[1]) for d in list(zip(configs, tab.data)) ]
    x_dat = [ float_list(t[1:]) for t in data if t[0] == 'x']
    y_dat = [ float_list(t[1:]) for t in data if t[0] == 'y']
    columns = [ 'n1', 'n2', 'theta' ] + tab.columns
    units = [ '[1]', '[1]', '[°]' ] + tab.units
    return (
            Tabular( [columns, units] + x_dat, False),
            Tabular( [columns, units] + y_dat, False)
            )

def read_configure_tabular( tab_name, config_name ):
    tab = Tabular( read_tabular( tab_name ) )
    return configure_tabular( tab, config_name )


class Graph:
    def __init__(self, name, x_unit, y_unit, x_data, y_data):
        self.name = name
        self.units = (x_unit, y_unit)
        self.data = np.array([x_data , y_data]).T
    def __str__(self):
        return "Graph(\"{}\", {}, {})".format(self.name, self.units, self.data)
    def __repr__(self):
        return str(self)

def read_graph_data( name ):
    content = read_tabular( name )
    names = content[0]
    axis = content[1]
    units = content[2]
    data = content[3:]
    data = [[ row[i] for row in data] for i in range(len(data[0]))]
    data = list(map( float_list, data ))
    ret = []
    for i in range(len(names)):
        ret.append(
                Graph( names[i], units[2*i], units[2*i+1], data[2*i], data[2*i+1] )
                )
    return ret

def configure_graph( graphs, config_name ):
    configs = read_tabular( config_name )
    ret = []
    for config in configs:
            graph = next(( x for x in graphs if x.name == config[0] ))
            data1 = np.array( [ x for x in graph.data if x[0] < float(config[1]) ] ).T
            data2 = np.array( [ x for x in graph.data if x[0] > float(config[2]) ] ).T
            graph1 = Graph( "{}.part".format(graph.name), graph.units[0], graph.units[1],
                    data1[0], data1[1]
                    )
            graph2 = Graph( "{}.part".format(graph.name), graph.units[0], graph.units[1],
                    data2[0], data2[1]
                    )
            ret.append((graph, graph1, graph2))
    return ret

def read_configure_graph( graph_name, config_name ):
    graphs = read_graph_data( graph_name )
    return configure_graph( graphs, config_name )
