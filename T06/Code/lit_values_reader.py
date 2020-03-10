import numpy as np

def read_header( name ) :
    with open(name) as f:
        content = f.readlines()
        columns = content[7:12] + content[13:20]
        columns = [ [ y.strip() for y in x.split('=') ]
            for x in columns]
        length = [ [int(y.strip()) for y in columns[i][1].split('-')]
            for i in range(len(columns)) ]
        name = [ y[0] for y in columns]
        content = content[23:]
    return content, length, name
def read_tabular ( name ):
    content, length, name = read_header(name)
    columns = []
    for l, n in zip(length, name):
        vals = []
        for i in range(len(content)):
            
            temp = (content[i][l[0]-1:l[1]]).strip()
            if (temp == ''):
                temp = None
            vals.append(temp)
        columns.append( (n, vals) )
    print(columns[6])

            
    
    
    
name = "Data/Lit_values"
data = read_tabular(name)
        