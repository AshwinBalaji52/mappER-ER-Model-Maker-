from tkinter import *
from graphviz import *
import os

os.environ["PATH"] += os.pathsep + 'C:/Graphviz2.38/bin/'


def Exit_Program():
    root.destroy()


def draw_function(listEN,listREL,listCAR,listAT):

    def relation(x, r):
        for key, value in r.items():
            if value == 'identify':
                type = 'Mdiamond'
            else:
                type = 'diamond'
            x.node(key, shape=type)

    def entity(x, l, c, rel):

        for key, value in l.items():
            count = 0  # number of classifications
            if 'W' in c[key]:
                sh = 'box3d'
            else:
                sh = 'rect'
            x.node(key, shape=sh)
            for i in range(0, len(value)):

                if c[key][i] == 'N':  # cardinality is many
                    point = 'none'
                else:
                    point = 'diamond'
                if 'W' in c[key] and rel[
                    value[i]] == 'identify':  # if entity is weak , hence cardinality is always one-many
                    point = 'none'
                    x.edge(value[i], key, len='1.50', dir='both', arrowhead='none', arrowtail=point)
                if value[i] in list(l):
                    if count == 0:
                        new = key + 'cls'
                        x.node(new, label='IS-A', shape='invtriangle')
                        x.attr('node', shape='rect')
                        x.edge(key, new, dir='none', penwidth='3')
                        x.edge(value[i], new, dir='none')
                        count = 1
                    else:
                        x.edge(value[i], new, dir='none')
                else:
                    x.edge(key, value[i], dir='both', arrowhead='none', arrowtail=point)

    def attribute(x, e, a):
        temp = list(e)

        for i in range(0, len(a)):
            for j in range(0, len(a[i])):
                if len(a[i][j]) != 0:
                    id = 0
                    for atr, ctr in a[i][j].items():
                        sty = 'solid'  # style
                        shp = 'circle'  # shape
                        # Keys
                        if ctr[0] == 'P':
                            col = 'red'
                            wid = '2'
                        elif ctr[0] == 'F':
                            col = 'blue'
                            wid = '2'
                        else:
                            col = 'black'
                            wid = '1'
                        # AttributeType
                        if ctr[1] == 'D':
                            sty = 'dashed'
                        elif ctr[1] == 'M':
                            shp = 'doublecircle'
                        foo = str(temp[i]) + str(id)  # temp id variable
                        # print(foo)
                        x.node(foo, label=str(atr), color=col, penwidth=wid, shape=shp, style=sty, fontsize='10')
                        x.edge(temp[i], foo, dir='none')
                        id += 1
    check = 0  # check Cardinality and Entity list: number of relation must match cardinalities given
    for keyE in listEN.keys():

        if len(listEN[keyE]) != len(listCAR[keyE]):
            print("Relations-Cardinality Mismatch for - ", keyE)
            check = 1

    if check == 0:
        page = Digraph(name='Model', engine='neato')
        relation(page, listREL)
        entity(page, listEN, listCAR, listREL)
        attribute(page, listEN, listAT)
        page.edge_attr.update(len='1.3')
        page.format = 'png'
        page.render('test-output/School.gv', view=True)


def parser():

    n = int(entry_ent_count.get())
    strings = entry_ent_attr.get("1.0","end-1c")
    strings = strings.splitlines()
    string0 = entry_ent_card_rel.get("1.0","end-1c")
    string0 = string0.replace('\n', '')

    Atr = []
    for string in strings:

        replacements = ('/', '[', '(', ')', ',', ']')  # fix
        for r in replacements:
            string = string.replace(r, ' ')
        L = string.split()
        L1 = []
        L2 = []
        L3 = []
        L4 = []
        L1.append(L[0])
        L2.append(L[1])
        for v in range(2, len(L), 2):
            L3.append(L[v])
        print(L3)
        for i in range(3, len(L), 2):
            L4.append(L[i])
        d = {}
        L5 = []
        for y in range(len(L3)):
            d[L3[y]] = L4[y].split('-')
        L5.append(d)
        Atr.append(L5)

    replacements = (';')  # fix
    for r in replacements:
        string0 = string0.replace(r, ' ')
    string0 = string0.split()
    EntRel = {}
    EntCar = {}
    RelRel = {}
    for en in string0:
        replacement1 = ('(', ')', '[', ',', ']')
        for r in replacement1:
            en = en.replace(r, ' ')
        en = en.split()
        key_temp = en[0]
        val_rel_temp = []
        val_car_temp = []
        for i in range(1, len(en), 2):
            val_car_temp.append(en[i + 1])
            val_rel_temp.append(en[i])
            check = 0
            for kk in RelRel.keys():
                if kk == en[i] and RelRel[kk] == 'identify':
                    check = 1
            if check == 1:
                continue
            if en[i + 1] == 'W':
                RelRel[en[i]] = 'identify'
            else:
                RelRel[en[i]] = 'none'

        EntCar[key_temp] = val_car_temp
        EntRel[key_temp] = val_rel_temp
    print(EntRel)
    print(EntCar)
    print(RelRel)
    print(Atr)
    listEN = EntRel
    listREL = RelRel
    listCAR = EntCar
    listAT = Atr

    draw_function(listEN,listREL,listCAR,listAT)

# GUI Starts here
root = Tk()
root.title("mappER --->>  Entity Relationship Model")
top = Frame(root)
bottom = Frame(root)

top.pack(side=TOP)
bottom.pack(side=BOTTOM)

# BASIC_ELEMENTS_OF_THIS_PROGRAM
str_count = IntVar()

# SCREEN_SIZE_DEFINITION

root.geometry("800x600+0+0") # ( width x height + x +y )


Screen_bg = Frame(root, relief='flat', bg="moccasin")
Screen_bg.place(height=720, width=1370, x=0, y=0)  # ( " order should be like this " )

#  [ no pack() required because we need this code to be implemented till end ]

# =TITLE_CONFIGURATION=========

Title_label = Label(root, text='mappER', font=("Arial Rounded MT Bold", 40, "normal"),
                    relief='flat', fg='midnight blue', bg='moccasin').pack(side=TOP)

# =TITLE_CONFIGURATION_END=========
label1 = Label(root,
               text='Enter the total number of Entities:',
               width=100, height=2, font=('ariel round MT bold', 12, 'bold'),
               bg='moccasin', relief='flat', fg='midnight blue')

entry_ent_count = Entry(root, textvariable=str_count, font=('times new roman', 12, 'normal'), bg='antique white',
                       fg='black',
                       justify='left', relief='sunken')

label2 = Label(root,
               text='Enter in the given format\n\n  Entity/Type[Attribute1(KeyConstraint1-AttributeConstraint2)...]...',
               width=100, height=4, font=('ariel round MT bold', 12, 'bold'),
               bg='moccasin', relief='flat', fg='midnight blue')

entry_ent_attr = Text(root, font=('times new roman', 12, 'normal'), width=100, height=6,
                      bg='antique white',fg='black', relief='sunken')

label3 = Label(root,
                text='Enter Realtionships and/or Classifications \n\n Entity1[Relation1(Cardinal1)];Entity2[];'
                     'Entity1[Relation2(Cardinal2),Relation3(Cardinal3)]',width=150, height=4,
                font=('ariel round MT bold', 12, 'bold'),bg='moccasin', relief='flat', fg='midnight blue')

entry_ent_card_rel= Text(root, font=('times new roman', 12, 'normal'), width=100, height=6,
                      bg='antique white',fg='black', relief='sunken')



cancel_button = Button(root, text="Abort", font=("Times new roman", 15, "bold"),
                       height=1, width=30, bd=4, fg='red2', bg="burlywood", relief='raised', command=Exit_Program)

generateERD_button = Button(root, text="Generate ER-Diagram", font=("Times new roman", 15, "bold"),
                            height=1, width=30, bd=4, fg='maroon4', bg="burlywood", relief='raised',
                            command=parser)

generateERD_button.pack(in_=bottom, side=LEFT, pady=25)
cancel_button.pack(in_=bottom, side=LEFT, padx=25)

# ==============================
label1.pack(side=TOP)
entry_ent_count.pack(side=TOP)
label2.pack(side=TOP)
entry_ent_attr.pack(side=TOP)
label3.pack(side=TOP)
entry_ent_card_rel.pack(side=TOP)


# ROOT_LOOP
root.mainloop()
# you just can't use them both grid and pack on widgets that share the same parent.

# EXIT_FUNCTION
