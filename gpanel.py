from gpanel import *

makeGPanel(0, 30, 0, 30)
for i in range(31):
    line(i, 0, 30, i)
keep()
