##VARIABLE SECTION##

mode=int #mode. 0 - engraving, 1 - drawing
h=float #font high in mm
origin=int #position of the origin. 0  - bottom-center, 1 - bottom-left, 2 - bottom-right, 3 - center, 4 - center-left, # 5 - center-right, 6 - upper-center, 7 - upper-left 8 - upper-right
talign=int #type of aligning. 0 - center, 1 - left, 2 - right.
zdepth=float #z-depth. It uses negative numbers
shigh=float #safe high Z
cspeed=int #cutting/drawing moves speed
fspeed=int #free movement speed
spindel=int #spindel rotation speed RPM

##FETHING THE DATA##

mode=input("Choose the mode.\n\n"
      "0-engraving\n"
      "1-drawing\n\n")
print("\n")
h=input("Enter the high of the font.\n\n")
print("\n")
