from pygraphviz import *
import sys
import math
import os 

G=AGraph()
G.graph_attr['overlap']='scale'
G.graph_attr['outputorder']='edgesfirst'
G.node_attr['shape']='circle'
G.node_attr['style']='filled'
G.node_attr['fixedsize']='true'

with open(sys.argv[1],'r') as f:
    counter = 1 
    size = int(f.readline())
    #Find unique edges and put them into a list to create complete graph
    elist = []
    for i in range(1,size+1):
        for j in range (2,size+1):
            if i != j and (j, i) not in elist:
                elist.append((i,j))
    #Create node and edges 
    for i in range(size):
        color = f.readline().rstrip("\n")
        G.add_node(i+1, color = color, style = 'invis') 
    G.add_edges_from(elist)
    progeny = None
    progenitor = None
    for line in f:
        line = line.split()
        num = len((line)) 
        for i in range(num):
            if i == 0:
                progeny = int(line[i])
            elif i == 1: 
                progenitor = int(line[i])
                G.add_node(progeny)
                G.get_node(progeny).attr['style']="invis"
                G.get_node(progeny).attr['color']=G.get_node(progenitor).attr['color']
            else: 
                if 'c' in line[i]:
                    copy_edge = int(line[i].replace('c', ''))
                    G.add_edge(progeny, copy_edge)
                elif 'm' in line[i]:
                    remove_edge = int(line[i].replace('m', ''))
                    G.remove_edge(progenitor, remove_edge)
                    G.add_edge(progeny, remove_edge)
    G.layout(prog="neato")
    G.remove_edges_from(G.edges())
    coordinates = []
    total_num_node = G.number_of_nodes()
    for i in range(1, total_num_node+1):
        coordinates.append(G.get_node(i).attr['pos'])
        #print(f'{i} : {G.get_node(i).attr["pos"]}')
    #Part 2
    f.seek(0)
    elist.clear()
    size = int(f.readline())
    for i in range(total_num_node+1, total_num_node+size+1):
        for j in range (total_num_node+2, total_num_node+size+1):
            if i != j and (j, i) not in elist:
                elist.append((i,j))
    progeny = total_num_node
    for i in range(1, size+1):
        color = f.readline().rstrip("\n")
        progeny += 1
        G.add_node(progeny, label = i)
        G.get_node(progeny).attr['color']=G.get_node(i).attr['color']
        G.get_node(progeny).attr['pos']=G.get_node(i).attr['pos']
    progeny += 1
    G.add_edges_from(elist)
    draw_counter = 0
    G.draw('gifdir/%03dfile.gif' % (counter), prog='neato', args='-n2')
    draw_counter += 1
    for line in f:
        line = line.split()
        num = len((line)) 
        child_node = None
        for i in range(num):
            if i == 0:
                child_node = int(line[i])
            elif i == 1: 
                progenitor = int(line[i])
                G.add_node(progeny, label = child_node)
                G.get_node(progeny).attr['color']=G.get_node(progenitor).attr['color']
                G.get_node(progeny).attr['pos']=G.get_node(progenitor).attr['pos']
            else: 
                if 'c' in line[i]:
                    copy_edge = int(line[i].replace('c', ''))
                    G.add_edge(progeny, copy_edge+total_num_node)
                elif 'm' in line[i]:
                    remove_edge = int(line[i].replace('m', ''))
                    G.remove_edge(progenitor+total_num_node, remove_edge+total_num_node)
                    G.add_edge(progeny, remove_edge+total_num_node)
        xyc = coordinates[progenitor-1].split(',')
        x_parent = float(xyc[0])
        y_parent = float(xyc[1])
        xyc = coordinates[child_node-1].split(',')
        x_child = float(xyc[0])
        y_child = float(xyc[1])
        delta_x = x_child - x_parent
        delta_y = y_child - y_parent

        if sys.argv[2] == 'linear':
            for i in range(1, 11):
                #print(f'{i} : ({x_parent}, {y_parent})')
                G.get_node(progeny).attr['pos']= str(x_parent) + "," + str(y_parent)
                G.draw('gifdir/%03dfile.gif'% (counter), prog='neato', args='-n2')
                #draw_counter += 1
                #print(f"{progeny} is drown")
                counter += 1 
                x_parent = x_parent + (delta_x/10)
                y_parent = y_parent + (delta_y/10)
                #print(f'{i} : ({x_parent}, {y_parent})')
        elif sys.argv[2] == 'logarithmic':
            for i in range(1, 11):
                #G.get_node(progeny).attr['pos'] = str(x_parent+delta_x*(1-math.log10(11-i))) + "," + str(y_parent+delta_y*(1-math.log10(11-i)))
                G.get_node(progeny).attr['pos'] = str(x_parent+delta_x*(1-math.log10(11-i))) + "," + str(y_parent+delta_y*(1-math.log10(11-i)))
                G.draw('gifdir/%03dfile.gif'% (counter), prog='neato', args='-n2')
                draw_counter += 1
                counter += 1
        progeny += 1

    print(f"draw_counter is {draw_counter}")
    os.system("gifsicle --colors 255 --delay=10 --optimize=3 %s/* > %s" % ('gifdir', sys.argv[3]))
    print('\n') 
    print(f"draw_counter is {draw_counter}")
