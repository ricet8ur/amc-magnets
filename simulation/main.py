import dearpygui.dearpygui as dpg
import math
import time

dpg.create_context()
dpg.create_viewport(width=1000, height=800)
dpg.setup_dearpygui()


color1=[50,150,255]
color2=[0,250,0]


f = open("data.csv")
param =f.readline().replace('\n','').split()
dt = float(param[0])
g = [[float(y) for y in x.replace('\n','').split(';')] for x in f.readlines()[:-1]]
f.close()

dpg.show_viewport()
t=0
view_mult=3500

old_pos = []

r = 10
# 2*g[0][0]==l; real_r/(2*g[0][0])==r/l = =>  real_r = r/(l/2)*view_mult
if len(param)>1:
    r = float(param[1])*view_mult


with dpg.window(label="main", width=1000, height=800):

    with dpg.drawlist(width=1000, height=800) as drawlist:

        with dpg.draw_node(tag="c1"):
            dpg.draw_circle([0, 0], r, color=color1, fill=color1) 

        with dpg.draw_node(tag="c2"):
            dpg.draw_circle([0, 0], r, color=color2, fill=color2) 



# starting pos
cm=[150, 150] # center of mass
def listadd(a,b):
    return [a[x]+b[x] for x in range(2)]
def listdiff(a,b):
    return [a[x]-b[x] for x in range(2)]
def listmul(a,b):
    return [a*b[x] for x in range(2)]




while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    # trajectory
    new_pos = (listadd(cm,listmul(view_mult,listadd(g[0],g[t]))),
            listadd(cm,listmul(view_mult,listdiff(g[0],g[t]))))
    dpg.draw_circle(new_pos[0], 1, color=color1, fill=color1, parent=drawlist) 
    dpg.draw_circle(new_pos[1], 1, color=color2, fill=color2, parent=drawlist) 
    if old_pos:
        dpg.draw_line(old_pos[0],new_pos[0],color=color1,parent=drawlist)
        dpg.draw_line(old_pos[1],new_pos[1],color=color2,parent=drawlist)
    old_pos = new_pos

    # moving circles
    dpg.apply_transform("c1",
        dpg.create_translation_matrix(listadd(cm,listmul(view_mult,listadd(g[0],g[t])))))
    dpg.apply_transform("c2",
        dpg.create_translation_matrix(listadd(cm,listmul(view_mult,listdiff(g[0],g[t])))))
    t+=1
    while t>= len(g):
        print('stop')
    time.sleep(dt*20)
dpg.destroy_context()
# при численных симуляциях бывает такое, что на близких расстояниях между мат точками происходит неточное вычисление.