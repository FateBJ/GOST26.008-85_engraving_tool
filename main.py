##VARIABLE SECTION##
output=str('') #Output file text
mode=0 #mode. 0 - engraving, 1 - drawing
h=20 #font high in mm
origin=0 #position of the origin. 0 - bottom-center, 1 - bottom-left, 2 - bottom-right, 3 - center, 4 - center-left, 5 - center-right, 6 - upper-center, 7 - upper-left 8 - upper-right
talign=0 #type of aligning. 0 - center, 1 - left, 2 - right.
zdepth=-0.1 #z-depth. It uses negative numbers
shigh=1 #safe high Z mm
cspeed=100 #cutting/drawing moves speed
fspeed=3000 #free movement speed
spindel=25000 #spindel rotation speed RPM
xpos=0
ypos=0
zpos=10
text=''
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
    text=str (input("Enter the text\n"))

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
    if mode==0: print("Spindle speed: "+str(cspeed)+" RPM\n"+"Text: "+text+"\n")
    again=input("Is that correct? Y/N\n")
    if again=="Y" or again=="y": return (mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
    else: mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text=input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
    return (mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)

#mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text=input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)

##VALIDATION##

#placeholder#

#DEBUG
def cut(): #Cutting stroke
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output += "G01 X"+str(xpos)+" Y"+str(ypos)+" Z" + str(zpos)+" F"+str(cspeed)+'\n'
    return()
def move(): #Free movement stroke
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output += "G00 X" + str(xpos) + " Y" + str(ypos) + " Z" + str(zpos) + " F" + str(fspeed)+'\n'
    return()
def arccw(i,j,r): #Cutting CW arc
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output+="G02 X"+str (xpos)+" Y"+str(ypos)+" I"+str(i)+" J"+str (j)+" R"+str(r)+" F"+str(cspeed)+"\n"
    return()
def arcccw(i,j,r):  # Cutting CCW arc
    global output,xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth
    output+="G03 X"+str (xpos)+" Y"+str(ypos)+" I"+str(i)+" J"+str (j)+" R"+str(r)+" F"+str(cspeed)+"\n"
    return ()
def cutin():
    global xpos,ypos,zdepth,output,cspeed
    output += "G01 X"+str(xpos)+" Y"+str(ypos)+" Z" + str(zdepth)+" F"+str(cspeed)+'\n'
def cutout():
    global xpos, ypos, shigh, output, fspeed
    output += "G01 X" + str(xpos) + " Y" + str(ypos) + " Z" + str(shigh) + " F" + str(fspeed) + '\n'
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
    zpos=shigh
    move()
    #11 moving to the end position
    xpos=startxpos+16*K
    ypos=startypos
    move()
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
    xpos+=2.75*K+9.1*K
    ypos+=10.3*K+13.5*K
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
    xpos+=9.6*K-3.5*K
    cut()
    #6 cutting 4th element
    r = 3.5 * K
    ypos+=r*2
    i=0
    j=ypos-r
    arcccw(i,j,r)
    #7 cutting 5th element
    xpos-=9.6*K-3.5*K
    cut()
    #8 cutting out
    cutout()
    #8 moving to the end position
    xpos=startxpos+14.4*K
    ypos=startypos
    move()
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
    move()
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
    xpos = startxpos + 14.4 * K
    ypos = startypos
    move()
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
    move()
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
    move()
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
def cyrJ():
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
    move()
    return()




#output+='G90 G94 G91.1 G40 G49 G17\nG21\nG28 G91 Z0.\nG90\nT3 M6\nS'
#output+=str(spindel)
#output+=' M3\nG17 G90 G94\nG54\n'

cyrJ()

print (output)
