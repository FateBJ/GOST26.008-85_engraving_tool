##VARIABLE SECTION##
import pyperclip
output=str('') #Output file text
mode=0 #mode. 0 - engraving, 1 - drawing
h=16 #font high in mm
origin=1 #position of the origin. 0 - bottom-center, 1 - bottom-left, 2 - bottom-right, 3 - center, 4 - center-left, 5 - center-right, 6 - upper-center, 7 - upper-left 8 - upper-right
talign=1 #type of aligning. 0 - center, 1 - left, 2 - right.
zdepth=-0.1 #z-depth. It uses negative numbers
shigh=1 #safe high Z mm
cspeed=100 #cutting/drawing moves speed
fspeed=3000 #free movement speed
spindel=25000 #spindel rotation speed RPM
xpos=0.0
ypos=0.0
zpos=10.0
textBoxWidth=0.0
K = h / 16
widthdict={
    'А':16*K,   'Б':14.4*K, 'В':14.4*K,     'Й':15.2*K, 'К':14.4*K, 'Л':16*K,
    'Г':12.8*K, 'Д':17.6*K, 'Е':13.6*K,     'М':17.6*K, 'Н':15.2*K, 'О':16*K,
    'Ж':19.2*K, 'З':13.6*K, 'И':15.2*K,     'П':15.2*K, 'Р':14.4*K, 'С':14.4*K,

    'Т':14.4*K, 'У':14.4*K, 'Ф':17.6*K,     'Ы':20*K,   'Ь':14.4*K, 'Э':14.4*K,
    'Х':15.2*K, 'Ц':16*K,   "Ч":13.6*K,     'Ю':20.8*K, 'Я':14.4*K,
    'Ш':20*K,   'Щ':20.8*K, 'Ъ':16*K,

    ' ':15.2*K
}
##FETHING THE PARAMETERS##
def input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text):

    mode=int (input("Choose the mode.\n\n0-engraving\n1-drawing\n\n"))
    if mode!=1: mode=0
    h=float (input("Enter the high of the font.\n\n"))
    origin=int (input("Choose the anchor pont of the text box\n0 - bottom-center\n1 - bottom-left\n2 - bottom-right\n3 - center\n4 - middle-left\n5 - middle-right\n6 - upper-center\n7 - upper-left\n8 - upper-right\n"))
    talign=int (input("Aligning:\n0-center\n1-left\n2-right\n"))
    zdepth=float (input("Enter the z-depth\n-"))
    zdepth=0-zdepth
    shigh=float (input("Enter the safe high\n"))
    cspeed=int (input("Enter the speed of cutting/drawing\n"))
    fspeed=int (input("Enter the speed of free movements\n"))
    if mode==0: spindel=int (input("Enter the spindle rotation speed\n"))
    inptext=str (input("Enter the text. For next line use symbol \\n \n"))

##ENSURING##

    print ("Mode: ")
    if mode==0: print("engraving\n")
    if mode==1: print("drawing\n")
    print("Text high: "+str(h)+"mm\n"+"Origin pont: ")
    if origin==0: print("bottom-center\n")
    if origin==1: print("bottom-left\n")
    if origin==2: print("bottom-right\n")
    if origin==3: print("center\n")
    if origin==4: print("middle-left\n")
    if origin==5: print("middle-right\n")
    if origin==6: print("upper-center\n")
    if origin==7: print("upper-left\n")
    if origin==8: print("upper-right\n")
    print("Text aligning: ")
    if talign==0: print("centered\n")
    if talign==1: print("to left\n")
    if talign==2: print("to right\n")
    print("Z-depth: "+str(zdepth)+"mm \nSafe high: "+str(shigh)+"mm \nCutting speed: "+str(cspeed)+"mm/min\nFree movement speed: "+str(fspeed)+"mm/min\n")
    if mode==0: print("Spindle speed: "+str(cspeed)+" RPM\n"+"letter: "+text+"\n")
    again=input("Is that correct? Y/N\n")
    if again=="Y" or again=="y": return (mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
    else: mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text=input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
    return (mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
##TEXT PREPARATION##
inptext='ООО\nОО\nООО\nОО ОООО ОО\nО' #DEBUG
text=inptext.split('\n')
lines = len(text)
thigh=13.9*K*len(text)+6.95*K*(len(text)-1)
##VALIDATION##

##THE SECTION OF FORMING G-CODE LINES##
def cut(): #Cutting stroke
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output += "G01 X"+str('{:.3f}'.format(xpos))+" Y"+str('{:.3f}'.format(ypos))+" Z" + str(zdepth)+" F"+str(cspeed)+'\n'
    return()
def move(): #Free movement stroke
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output += "G00 X" + str('{:.3f}'.format(xpos)) + " Y" + str('{:.3f}'.format(ypos)) + " Z" + str(zpos) + " F" + str(fspeed)+'\n'
    return()
def arccw(i,j,r): #Cutting CW arc
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output+="G02 X"+str ('{:.3f}'.format(xpos))+" Y"+str('{:.3f}'.format(ypos))+" Z" + str(zdepth)+" I"+str('{:.3f}'.format(i))+" J"+str ('{:.3f}'.format(j))+" R"+str('{:.3f}'.format(r))+" F"+str(cspeed)+"\n"
    return()
def arcccw(i,j,r):  # Cutting CCW arc
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output+="G03 X"+str ('{:.3f}'.format(xpos))+" Y"+str('{:.3f}'.format(ypos))+" Z" + str(zdepth)+" I"+str('{:.3f}'.format(i))+" J"+str ('{:.3f}'.format(j))+" R"+str('{:.3f}'.format(r))+" F"+str(cspeed)+"\n"
    return ()
def cutin():
    global xpos,ypos,zdepth,output,cspeed
    output += "G01 X"+str('{:.3f}'.format(xpos))+" Y"+str('{:.3f}'.format(ypos))+" Z" + str(zdepth)+" F"+str(cspeed)+'\n'
def cutout():
    global xpos, ypos, shigh, output, fspeed
    output += "G00 X" + str('{:.3f}'.format(xpos)) + " Y" + str('{:.3f}'.format(ypos)) + " Z" + str(shigh) + " F" + str(fspeed) + '\n'
########################################################################################################################
#           2
#          ###
#         #   #
#   1    #     #  3
#       #       #
#      #    4    #
#     #############
#    #             #
#   #               #
########################################################################################################################
def latA():
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    K=h/16
    zpos=shigh
    startxpos=xpos
    startypos=ypos

    #1 start point
    xpos+=((8*K)-((11.8*K)/2))
    ypos+=(10*K)
    move()
    #2 cutting in
    zpos=zdepth
    cut()
    #3 1st element
    xpos+=(((11.8*K)/2)-((0.5*K)/2))
    ypos+=13.9*K
    cut()
    #4 2nd element
    xpos+=(0.5*K)
    cut()
    #5 3rd element
    xpos += (((11.8 * K) / 2) - (0.25 * K))
    ypos -= (13.9 * K)
    cut()
    #6 cutting out
    zpos=shigh
    move()
    #7 moving to position for the 4th element
    xpos-=(11.8 * K - (0.5*K+2*((13.9 * K - 3.7 * K) * ((11.8 * K - 0.5 * K) / 2) / (13.9 * K))))/2
    ypos+=(3.7*K)
    move()
    #8 cutting in
    zpos=zdepth
    cut()
    #9 4th element
    xpos-=0.5*K+2*((13.9 * K - 3.7 * K) * ((11.8 * K - 0.5 * K) / 2) / (13.9 * K))
    cut()
    #10 cutting out
    cutout()
    #11 moving to the end position
    xpos=startxpos+16*K
    ypos=startypos
    return ()
########################################################################################################################
#          1
#   ###############
#   #
#   #      5
# 2 ###############
#   #               #
#   #          +     #  4
#   #               #
#   ###############
#           3
########################################################################################################################
def cyrB():
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    K=h/16
    zpos=shigh
    startxpos=xpos
    startypos=ypos

    #1 going to the start point
    xpos+=(2.75+9.1)*K
    ypos+=(10.2+13.5)*K
    move()
    #2 cutting in
    cutin()
    #3 cutting 1st element
    xpos-=9.1*K
    cut()
    #4 cutting 2nd element
    ypos-=13.5*K
    cut()
    #5 cutting 3rd element
    xpos+=(9.6-3.5)*K
    cut()
    #6 cutting 4th element
    r = 3.5 * K
    ypos+=r*2
    i=0
    j=ypos+r
    arcccw(i,j,r)
    #7 cutting 5th element
    xpos-=(9.6-3.5)*K
    cut()
    #8 cutting out
    cutout()
    #8 moving to the end position
    xpos=startxpos+14.4*K
    ypos=startypos
    return ()
########################################################################################################################
#       4
#   #########
#   #        #  3
#   #   6    #
# 5 #########
#   #        #
#   #         # 2
#   #        #
#   #########
#       1
########################################################################################################################
def latB():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10.2*K
    move()
    # cutting in
    cutin()
    # 1st element
    xpos+=9.6*K-3.5*K
    cut()
    # 2nd element
    r=3.5*K
    ypos += r * 2
    i = 0
    j = ypos - r
    arcccw(i,j,r)
    # 3rd element
    r=3.25*K
    ypos += r * 2
    i = 0
    j = ypos - r
    arcccw(i, j, r)
    # 4th element
    xpos-=9.4*K-3.25*K
    cut()
    # 5th element
    ypos-=13.5*K
    cut()
    # cutting out
    cutout()
    # going to the 6th element
    ypos+=7*K
    move()
    # cutting in
    cutin()
    # 6th element
    xpos+=9.6*K-3.5*K
    cut()
    # cutting out
    cutout()
    # 8 moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#         2
#   ############
#   #
#   #
# 1 #
#   #
#   #
#   #
#   #
#
########################################################################################################################
def cyrG():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.7*K
    cut()
    #4 2nd element
    xpos+=8*K
    cut()
    #5 cutting out
    cutout()
    #6 8 moving to the end position
    xpos = startxpos + 12.8 * K
    ypos = startypos
    return()
########################################################################################################################
#            5
#          #####
#         #     #
#        #       #
#     4 #         # 6
#      #           #
#     #      2      #
#   ###################
# 1 #                 # 3
#
########################################################################################################################
def cyrD():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos
    x1=startxpos+8.8*K-(13.6*K)/2
    y1=startypos+10.2*K-4.2*K

    #1 going to the start point
    xpos=x1
    ypos=y1
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=4.2*K
    cut()
    #4 2nd
    xpos+=13.6*K
    cut()
    #5 3rd
    ypos-=4.2*K
    cut()
    #6 cutting out
    cutout()
    #7 moving to 4th
    xpos-=(13.6-11.2)*K/2+11.2*K
    ypos+=4.2*K
    move()
    #8 cutting in
    cutin()
    #9 4th
    xpos+=11.2/2*K-0.5/2*K
    ypos+=13.7*K
    cut()
    #10 5th
    xpos+=0.5*K
    cut()
    #11 6th
    xpos+=11.2/2*K-0.5/2*K
    ypos-=13.7*K
    cut()
    #5 cutting out
    cutout()
    #6 8 moving to the end position
    xpos = startxpos + 17.6 * K
    ypos = startypos
    return()
########################################################################################################################
#       3
#   #############
#   #
#   #
#  2#   4
#   #########
#   #
#   #
#   #############
#         1
########################################################################################################################
def latE():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K+8.8*K
    ypos+=10.2*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    xpos-=8.8*K
    cut()
    #4 2nd element
    ypos+=13.5*K
    cut()
    #5 3rd element
    xpos+=8.8*K
    cut()
    #6 cutting out
    cutout()
    #7 going to 4th
    xpos-=8.8*K
    ypos-=13.5*K-6.8*K
    move()
    #8 cutting in
    cutin()
    #9 4th
    xpos+=8*K
    cut()
    #10 cutting out
    cutout()
    #11 moving to the end position
    xpos = startxpos + 13.6 * K
    ypos = startypos
    return()
########################################################################################################################
#          3
#    #     #     #
#  2  #    #    #  5
#      #   #   #
#       #  #  #
#  1   #   #   #  4
#     #    #    #
#    #     #     #
#
########################################################################################################################
def cyrZH():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=9.6*K-15*K/2
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    xpos+=4.5*K
    ypos+=7.2*K
    cut()
    #4 2nd element
    xpos-=4.5*K
    ypos+=6.7*K
    cut()
    #5 cutting out
    cutout()
    #6 going to 3rd
    xpos+=4.5*K+3*K
    move()
    #7 cutting in
    cutin()
    #8 3rd element
    ypos-=13.9*K
    cut()
    #9 cutting out
    cutout()
    #10 going to 4th
    xpos += 4.5 * K + 3 * K
    move()
    #11 cutting in
    cutin()
    #12 4th
    xpos -= 4.5 * K
    ypos += 7.2 * K
    cut()
    #13 5th
    xpos+=4.5*K
    ypos+=6.7*K
    cut()
    # cutting out
    cutout()
    # 8 moving to the end position
    xpos = startxpos + 19.2 * K
    ypos = startypos
    return()
########################################################################################################################
#     4
#       #########
#     ##         #  3
#                #
#         5  ####
#                #
#                #  2
#    ## 1        #
#      #########
#
########################################################################################################################
def cyrZ():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.1*K
    ypos+=13.3931369*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    r = 5.235 * K
    xpos = startxpos + 10.1385998*K
    ypos = startypos + 11.0453026*K
    i = startxpos + (70-21)*K/2
    j = startxpos - (13.3931369-11.0453026)*K/2
    arcccw(i, j, r)
    #4 2nd element
    r=3.4*K
    xpos= startxpos+8.1*K
    ypos=startypos+17.1663522*K
    i=(8.1-10.1385998)*K
    j=(11.0453026-13.7663522)*K
    arcccw(i, j, r)
    #5 3rd element
    r=3.3*K
    xpos=startxpos+9.3157895*K
    ypos=startypos+23.534227*K
    i=(9.3157895-8.1)*K/2
    j=(23.534227-17.1663522)*K/2
    arcccw(i, j, r)
    #6 4th element
    r=5.2*K
    xpos=startxpos+2.7*K
    ypos=startypos+20.9248595*K
    i=(7.4-9.3157895)*K/2
    j=(20.9248595-23.534227)*K/2
    arcccw(i, j, r)
    #7 cutting out
    cutout()
    #8 moving to 5th element
    xpos=startxpos+8.1*K
    ypos=startypos+17.1663522*K
    move()
    #9 cutting in
    cutin()
    #10 5th element
    xpos-=1.9*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 13.6 * K
    ypos = startypos
    return()
########################################################################################################################
#                   4
#   #              # #
#   #            #   #
#   #          #     #
# 1 #      3 #       # 5
#   #      #         #
#   #    #           #
#   #   #            #
#   # #              #
#    2
########################################################################################################################
def cyrI():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=23.9*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos-=13.9*K
    cut()
    #4 2nd element
    xpos+=0.5*K
    cut()
    #5 3rd element
    xpos+=8.7*K
    ypos+=13.9*K
    cut()
    #6 4th element
    xpos+=0.5*K
    cut()
    #7 5th element
    ypos-=13.9*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 15.2 * K
    ypos = startypos
    return()
########################################################################################################################
#          ####     4
#   #        6     # #
#   #            #   #
#   #          #     #
# 1 #      3 #       # 5
#   #      #         #
#   #    #           #
#   #   #            #
#   # #              #
#    2
########################################################################################################################
def cyrJ():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=23.9*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos-=13.9*K
    cut()
    #4 2nd element
    xpos+=0.5*K
    cut()
    #5 3rd element
    xpos+=8.7*K
    ypos+=13.9*K
    cut()
    #6 4th element
    xpos+=0.5*K
    cut()
    #7 5th element
    ypos-=13.9*K
    cut()
    #8 cutting out
    cutout()
    #9 moving to 6th
    xpos-=2.6*K
    ypos+=17.9*K
    move()
    #10 6th element
    xpos-=4.5*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 15.2 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   #        #
#   #     #  2
#   #  #
#   #   #
# 1 #    #
#   #     #   3
#   #      #
#   #        #
#
########################################################################################################################
def latK():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.9*K
    cut()
    #4 cutout
    cutout()
    #5 go to 2nd
    xpos+=9.5*K
    move()
    #6 cut in
    cutin()
    #7 2nd
    xpos-=6.5*K
    ypos-=6.7*K
    cut()
    #8 3rd
    xpos+=6.5*K
    ypos-=7.2*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#           2
#          ####
#         #    #
#        #      #
#    1  #        #  3
#      #          #
#     #            #
#    #              #
#   #                #
#
########################################################################################################################
def cyrL():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.1*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    xpos+=5.65*K
    ypos+=13.9*K
    cut()
    #4
    xpos+=0.5*K
    cut()
    #5
    xpos+=5.65*K
    ypos-=13.9*K
    cut()
    #6 cutting out
    cutout()
    #7 moving to the end position
    xpos = startxpos + 16 * K
    ypos = startypos
    return()
########################################################################################################################
#    2              6
#   ###           ###
#   #   # 3   5 #   #
#   #     #   #     #
#   #      ###      #  7
#  1#       4       #
#   #               #
#   #               #
#   #               #
#
########################################################################################################################
def latM():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.9*K
    cut()
    #4 2nd element
    xpos+=0.5*K
    cut()
    #5 3rd element
    xpos+=5.3*K
    ypos-=7.6*K
    cut()
    #6 4th
    xpos+=0.5*K
    cut()
    #7 5th
    xpos+=5.3*K
    ypos+=7.6*K
    cut()
    #8 6th
    xpos+=0.5*K
    cut()
    #9 7th
    ypos-=13.9*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 17.6 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   #           #
#   #           #
#   #      2    #
#   #############
# 1 #           #  3
#   #           #
#   #           #
#   #           #
#
########################################################################################################################
def latH():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.9*K
    cut()
    #4 cutting out
    cutout()
    #5 go to 2nd
    ypos-=6.7*K
    move()
    #6 cutting in
    cutin()
    #7 2nd
    xpos+=9.7*K
    cut()
    #8 cutting out
    cutout()
    #9 goto 3rd
    ypos+=6.7*K
    move()
    #10 cutting in
    cutin()
    #11 3rd
    ypos-=13.9*K
    cut()
    #12 cutting out
    cutout()
    #13 moving to the end position
    xpos = startxpos + 15.2 * K
    ypos = startypos
    return()
########################################################################################################################
#       2
#      ######
#   #           #
#   #           #
#  1#           # 3
#   #           #
#   #           #
#   #           #
#      ######
#       4
########################################################################################################################
def latO():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=4.113104*K
    ypos+=11.8548387*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    r=8.1*K
    ypos=startypos+22.0451613*K
    i=(10.4098755+4.113104)*K/2
    j=(22.0451613-11.8548387)*K/2
    arccw(i, j, r)
    #4 2nd element
    r=5*K
    xpos=startxpos+11.886896*K
    i=3.886896*K
    j=(18.9-22.0451613)*K
    arccw(i, j, r)
    #5 3rd
    r=8.1*K
    ypos=startypos+11.8548387*K
    i=(10.4098755-11.886896)*K
    j=(16.95-22.0451613)*K
    arccw(i, j, r)
    #6 4th
    r=5*K
    xpos=startxpos+4.113104*K
    i=(8-11.886896)*K
    j=(15-11.8548387)*K
    arccw(i, j, r)
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 16 * K
    ypos = startypos
    return()
########################################################################################################################
#         2
#   #############
#   #           #
#   #           #
# 1 #           #  3
#   #           #
#   #           #
#   #           #
#   #           #
#
########################################################################################################################
def cyrP():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.7*K
    cut()
    #4 2nd
    xpos+=9.7*K
    cut()
    #5 3rd
    ypos-=13.7*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 15.2 * K
    ypos = startypos
    return()
########################################################################################################################
#       2
#   ###########
#   #           #
#   #           #  3
# 1 #           #
#   ###########
#   #   4
#   #
#   #
#
########################################################################################################################
def latP():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.7*K
    cut()
    #4 2nd
    xpos+=5.8*K
    cut()
    #5 3rd
    r=3.8*K
    ypos-=7.6*K
    i=0
    j=-3.8*K
    arccw(i, j, r)
    #6 4th
    xpos-=5.8*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#       3
#      ######
#   #          #
#   #
#  2#
#   #
#   #
#   #          #
#      ######
#       1
########################################################################################################################
def latC():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=12.25*K
    ypos+=12.3660866*K
    move()
    #2 cutting in
    cutin()
    #3 4th
    r = 5 * K
    xpos = startxpos + 4.113104 * K
    ypos = startypos +11.8548387*K
    i = (8 - 12.25) * K
    j = (15 - 12.3660866) * K
    arccw(i, j, r)
    #4 1st element
    r=8.1*K
    ypos=startypos+22.0451613*K
    i=(10.4098755+4.113104)*K/2
    j=(22.0451613-11.8548387)*K/2
    arccw(i, j, r)
    #5 2nd element
    r=5*K
    xpos=startxpos+12.25*K
    ypos=startypos+21.5339134*K
    i=3.886896*K
    j=(18.9-22.0451613)*K
    arccw(i, j, r)
    #6 cutting out
    cutout()
    #7 moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#       2
#   ##########
#       #
#       #
#       #
#       #  1
#       #
#       #
#       #
#
########################################################################################################################
def latT():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=7.2*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.7*K
    cut()
    #4 cutting out
    cutout()
    #5 goto 2
    xpos-=5.15*K
    move()
    #6 cutting in
    cutin()
    #7 2nd
    xpos+=10.3*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   #           #
#    #         #
#     #       #
#    2  #    #  1
#        #  #
#          #
#         #
#        #
#
########################################################################################################################
def cyrU():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=(12.3-62.55/8.8)*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    xpos+=(62.55/8.5)*K
    ypos+=13.9*K
    cut()
    cutout()
    xpos=startxpos+2.1*K
    move()
    cutin()
    xpos+=5.7*K
    ypos-=8.8*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#
#       5   #
#     #############
#   #       #       #
#   # 4    1#       #   2
#   #       #    3  #
#     #############
#           #
#           #
#
########################################################################################################################
def cyrF():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=8.8*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.9*K
    cut()
    #
    cutout()
    #
    ypos-=1.5*K
    xpos+=2.35*K
    move()
    #
    cutin()
    # 2nd
    r=4.4*K
    ypos-=8.8*K
    i=0
    j=-4.4*K
    arccw(i,j,r)
    # 3rd
    xpos-=4.7*K
    cut()
    # 4th
    r=4.4*K
    ypos+=8.8*K
    i=0
    j=4.4*K
    arccw(i, j, r)
    # 5th
    xpos+=4.7*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 17.6 * K
    ypos = startypos
    return()
########################################################################################################################
#
#    #     #
#     #   #
#  2   # #
#       #
#      # #
#   1 #   #
#    #     #
#   #       #
#
########################################################################################################################
def latX():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.1*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    xpos+=10.8*K
    ypos+=13.9*K
    cut()
    #cutout
    cutout()
    #
    xpos-=10.6*K
    move()
    #
    cutin()
    #
    xpos+=10.8*K
    ypos-=13.9*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 15.2 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   #           #
#   #           #
# 3 #           # 4
#   #           #
#   #           #
#   #        2  #
#   ################
#                  # 1
#
########################################################################################################################
def cyrC():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=13.75*K
    ypos+=5.9*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=4.3*K
    cut()
    #
    xpos-=11*K
    cut()
    #
    ypos+=13.7*K
    cut()
    #
    cutout()
    #
    xpos+=9.5*K
    move()
    #
    cutin()
    #
    ypos-=13.7*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 16 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   # 3         #
#   #           #
#    #     2  # #
#       #####   #
#               #  1
#               #
#               #
#               #
#
########################################################################################################################
def cyrCH():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=10.85*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.9*K
    cut()
    #
    cutout()
    #
    ypos=startypos+17.542223*K
    move()
    #
    cutin()
    #
    r=4.8*K
    xpos-=8.5*K
    ypos=startypos+20.6*K
    i=-3.7*K
    j=8.1*K-(startypos+17.542223*K)
    arccw(i, j, r)
    #
    ypos+=3.3*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 13.6 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   #       #       #
#   #       #       #
#   #       #       #
# 1 #       #   4   #  3
#   #       #       #
#   #       #       #
#   #       #       #
#   #################
#           2
########################################################################################################################
def cyrSH():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=23.9*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos-=13.7*K
    cut()
    #
    xpos+=14.5*K
    cut()
    #
    ypos+=13.7*K
    cut()
    #
    cutout()
    #
    xpos-=7.25*K
    move()
    #
    cutin()
    #
    ypos-=13.7*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 20 * K
    ypos = startypos
    return()
########################################################################################################################
#
#   #       #       #
#   #       #       #
#   #       #       #
# 1 #       #   4   #  3
#   #       #       #
#   #       #       #
#   #       #       #
#   ###################
#           2         #
########################################################################################################################
def cyrSCH():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=23.9*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos-=13.7*K
    cut()
    #
    xpos+=14.5*K
    cut()
    #
    ypos+=13.7*K
    cut()
    #
    cutout()
    #
    xpos-=7.25*K
    move()
    #
    cutin()
    #
    ypos-=13.7*K
    cut()
    #
    cutout()
    #
    xpos+=7.25*K
    move()
    #
    cutin()
    #
    xpos+=1.5*K
    cut()
    #
    ypos-=4.3*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 20.8 * K
    ypos = startypos
    return()
########################################################################################################################
#   1
#  ##
#   #
#   #  5
#   #######
# 2 #       #
#   #       # 4
#   #       #
#   #######
#       3
########################################################################################################################
def cyrHS():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    # 1 going to the start point
    xpos += 2 * K
    ypos += 23.7 * K
    move()
    # 2 cutting in
    cutin()
    # 3 1st element
    xpos+=2.4*K
    cut()
    #
    ypos-=13.5*K
    cut()
    #
    xpos+=6.1*K
    cut()
    #
    r=3.5*K
    ypos+=7*K
    i=0
    j=3.5
    arcccw(i, j, r)
    #
    xpos-=6.1*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 16 *K
    ypos = startypos
    return ()
########################################################################################################################
#
#   #               #
#   #               #
#   #  4            #
#   #######         #  5
# 1 #       #       #
#   #       # 3     #
#   #       #       #
#   #######         #
#       2
########################################################################################################################
def cyrY():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    # 1 going to the start point
    xpos += 2.75 * K
    ypos += 23.9 * K
    move()
    # 2 cutting in
    cutin()
    # 3 1st element
    ypos-=13.7*K
    cut()
    #
    xpos+=6.1*K
    cut()
    #
    r=3.5*K
    ypos+=7*K
    i=0
    j=3.5
    arcccw(i, j, r)
    #
    xpos-=6.1*K
    cut()
    #
    cutout()
    #
    xpos+=14.5*K
    ypos+=6.7*K
    move()
    #
    cutin()
    ypos-=13.9*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 20 *K
    ypos = startypos
    return ()
########################################################################################################################
#
#   #
#   #
#   #  4
#   #######
# 1 #       #
#   #       # 3
#   #       #
#   #######
#       2
########################################################################################################################
def cyrSS():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    # 1 going to the start point
    xpos += 2.75 * K
    ypos += 23.9 * K
    move()
    # 2 cutting in
    cutin()
    # 3 1st element
    ypos-=13.7*K
    cut()
    #
    xpos+=6.1*K
    cut()
    #
    r=3.5*K
    ypos+=7*K
    i=0
    j=3.5
    arcccw(i, j, r)
    #
    xpos-=6.1*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return ()
########################################################################################################################
#       3
#     #########
#   #           #
#            4   #
#        #########
#                #  2
#                #
#   #           #
#     #########
#       1
########################################################################################################################
def cyrJE():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.15*K
    ypos+=12.366*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    r=5*K
    xpos=startxpos+10.19*K
    ypos=startypos+11.739*K
    i=6.4*K-10.19*K
    j=15*K-11.739*K
    arcccw(i, j, r)
    #
    r=8.1*K
    ypos=startypos+22.304*K
    j=17.022*K-22.304*K
    i=4.05*K-10.19*K
    arcccw(i, j, r)
    #
    r=5*K
    xpos=startxpos+2.15*K
    ypos=startypos+21.677*K
    i=6.4*K-2.15*K
    j=19.044*K-21.677*K
    arcccw(i,j,r)
    #
    cutout()
    #
    xpos=startxpos+4.15*K
    ypos=startypos+17.022*K
    move()
    #
    cutin()
    #
    xpos=startxpos+12.15*K
    ypos=startypos+17.022*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#           4
#   #    3  ##
#   #    #      #
#   # 2 #        #
#   #####        #  5
#   #   #        #
# 1 #   #        #
#   #  7 #      #
#   #       ##
#           6
########################################################################################################################
def cyrJU():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.75*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    ypos+=13.9*K
    cut()
    #
    cutout()
    #
    ypos-=6.95*K
    move()
    #
    cutin()
    #
    xpos=startxpos+7.25*K
    cut()
    #
    r=8.1*K
    xpos=startxpos+8.954*K
    ypos=startypos+21.920*K
    i=15.35*K-7.25*K
    j=(21.920-16.95)*K
    arccw(i, j, r)
    #
    r=5.124*K
    xpos=startxpos+17.046*K
    i=(13-17.046)*K
    j=(18.776-21.920)*K
    arccw(i, j, r)
    #
    r=8.1*K
    ypos=startypos+11.98*K
    i=(17.046-15.35)*K
    j=(11.980-16.95)*K
    arccw(i, j, r)
    #
    r=5.124*K
    xpos=startxpos+8.954*K
    i=(13-17.046)*K
    j=(15.124-11.980)*K
    arccw(i, j, r)
    #
    r=8.1*K
    xpos=startxpos+7.25*K
    ypos=startypos+16.95*K
    i=(15.35-7.25)*K
    j=0
    arccw(i, j, r)
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 20.8 * K
    ypos = startypos
    return()
########################################################################################################################
#           4
#    ############
#  3#           #
#   #     2     #
#    ############  5
#      #        #
#   1 #         #
#    #          #
#   #           #
#
########################################################################################################################
def cyrJA():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    startxpos = xpos
    startypos = ypos

    #1 going to the start point
    xpos+=2.05*K
    ypos+=10*K
    move()
    #2 cutting in
    cutin()
    #3 1st element
    xpos+=5*K
    ypos+=6.7*K
    cut()
    #
    cutout()
    #
    xpos+=4.6*K
    move()
    #
    cutin()
    #
    xpos-=6.1*K
    cut()
    #
    r=3.5*K
    ypos+=7*K
    i=0
    j=-3.5*K
    arccw(i,j,r)
    #
    xpos+=6.1*K
    cut()
    #
    ypos-=13.7*K
    cut()
    # cutting out
    cutout()
    # moving to the end position
    xpos = startxpos + 14.4 * K
    ypos = startypos
    return()
########################################################################################################################
#
#
#
#
#
#
#
#       #                           #
#       #############################
#
########################################################################################################################
def space():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth
    K = h / 16
    zpos = shigh
    xpos+= 15.2 * K
    move()
    return()
########################################################################################################################
#
#                       #
#                       #
#                       #
#                       #
#           #           #
#         #             #
#       #################
#         #
#           #
########################################################################################################################
def nextline():
    global output, xpos, ypos, zpos, shigh, h, fspeed, cspeed, zdepth, thigh,K
    output+='G00 Z'+str(shigh)+'\n'
    ypos-=20.85*K
    return()
##FORMING TEXT##
def textparser(i):
    global text,output
    for letter in text[i]:
        if 'А' in letter:
            latA()
        if 'Б' in letter:
            cyrB()
        if 'В' in letter:
            latB()
        if 'Г' in letter:
            cyrG()
        if 'Д' in letter:
            cyrD()
        if 'Е' in letter:
            latE()
        if 'Ж' in letter:
            cyrZH()
        if 'З' in letter:
            cyrZ()
        if 'И' in letter:
            cyrI()
        if 'Й' in letter:
            cyrJ()
        if 'К' in letter:
            latK()
        if 'Л' in letter:
            cyrL()
        if 'М' in letter:
            latM()
        if 'Н' in letter:
            latH()
        if 'О' in letter:
            latO()
        if 'П' in letter:
            cyrP()
        if 'Р' in letter:
            latP()
        if 'С' in letter:
            latC()
        if 'Т' in letter:
            latT()
        if 'У' in letter:
            cyrU()
        if 'Ф' in letter:
            cyrF()
        if 'Х' in letter:
            latX()
        if 'Ц' in letter:
            cyrC()
        if 'Ч' in letter:
            cyrCH()
        if 'Ш' in letter:
            cyrSH()
        if 'Щ' in letter:
            cyrSCH()
        if 'Ъ' in letter:
            cyrHS()
        if 'Ы' in letter:
            cyrY()
        if 'Ь' in letter:
            cyrSS()
        if 'Э' in letter:
            cyrJE()
        if 'Ю' in letter:
            cyrJU()
        if 'Я' in letter:
            cyrJA()
        if ' ' in letter:
            space()
    return()
##DETERMINING THE ORIGIN POINT##
origin=3
def originationx():
    global text, xpos, ypos,h, origin, thigh, textBoxWidth, K, widthdict,talign
    i=0
    line=str()
    while i<len(text):
        textBoxWidth = 0.0
        for letter in text[i]:
            textBoxWidth+=widthdict.get(letter)
        i+=1
        line+=str(textBoxWidth)+','
    line=line[:-1]
    mostlong = list(map(float, line.split(',')))
    mostlong.sort()
    mostlong.reverse()
    textBoxWidth=float (mostlong[0])
    cx=0-textBoxWidth/2
    lx=0-2.6*K
    rx=0-textBoxWidth+2.6*K
    if origin==0:
        xpos=cx
    if origin==1:
        xpos=lx
    if origin==2:
        xpos=rx
    if origin==3:
        xpos=cx
    if origin==4:
        xpos=lx
    if origin==5:
        xpos=rx
    if origin==6:
        xpos=cx
    if origin==7:
        xpos=lx
    if origin==8:
        xpos=rx
    return(textBoxWidth)
def originationy():
    global thigh,K,ypos,xpos
    cy=thigh/2-24*K
    by=thigh-24*K
    ty=0-thigh/2+25*K
    if origin==0:
        ypos=by
    if origin==1:
        ypos=by
    if origin==2:
        ypos=by
    if origin==3:
        ypos=cy
    if origin==4:
        ypos=cy
    if origin==5:
        ypos=cy
    if origin==6:
        ypos=ty
    if origin==7:
        ypos=ty
    if origin==8:
        ypos=ty
    return()

#talign=2

def aligning(i,textBoxWidth):
    global talign,xpos,ypos
    currlen=0.0
    for letter in text[i]:
        currlen+=widthdict.get(letter)
    if talign==0:
        xpos-=currlen/2+textBoxWidth*1.5
    if talign==1:
        xpos-=2.6*K
    if talign==2:
        xpos-=(textBoxWidth*2-currlen+2.6*K)
    return()

output+='G90 G94 G91.1 G40 G49 G17\nG21\nG28 G91 Z0.\nG90\nT3 M6\nS'
output+=str(spindel)
output+=' M3\nG17 G90 G94\nG54\n'

move()
textBoxWidth=originationx()
originationy()

i=0
while i<len(text):
    xpos=0
    originationx()
    #aligning(i,textBoxWidth)
    textparser(i)
    output+='(line)\n' #debug
    i+=1
    nextline()



output+='G00 X0 Y0 Z10 F'+str(fspeed)+'\n'
pyperclip.copy(output)