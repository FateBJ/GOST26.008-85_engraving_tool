##VARIABLE SECTION##

mode=0 #mode. 0 - engraving, 1 - drawing
h=5 #font high in mm
origin=0 #position of the origin. 0 - bottom-center, 1 - bottom-left, 2 - bottom-right, 3 - center, 4 - center-left, 5 - center-right, 6 - upper-center, 7 - upper-left 8 - upper-right
talign=0 #type of aligning. 0 - center, 1 - left, 2 - right.
zdepth=-0.35 #z-depth. It uses negative numbers
shigh=1 #safe high Z mm
cspeed=100 #cutting/drawing moves speed
fspeed=3000 #free movement speed
spindel=25000 #spindel rotation speed RPM

##FETHING THE DATA##

mode=input("Choose the mode.\n\n"
      "0-engraving\n"
      "1-drawing\n\n")
print("\n")
h=input("Enter the high of the font.\n\n")
print("\n")
origin=input("Choose the anchor pont of the text box\n"
             "0 - bottom-center\n"
             "1 - bottom-left\n"
             "2 - bottom-right\n"
             "3 - center\n"
             "4 - center-left\n"
             "5 - center-right\n"
             "6 - upper-center\n"
             "7 - upper-left\n"
             "8 - upper-right\n")
print("\n")
