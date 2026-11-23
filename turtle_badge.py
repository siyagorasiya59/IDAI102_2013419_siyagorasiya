"""Run `python turtle_badge.py` to draw a MedTimer reward badge."""
import turtle

screen=turtle.Screen()
screen.title("MedTimer Turtle Reward")
screen.bgcolor("#eef7f3")
screen.setup(700,560)
p=turtle.Turtle()
p.speed(0)
p.pensize(4)

def circle(x,y,r,fill,edge="#286b55"):
    p.penup(); p.goto(x,y-r); p.setheading(0); p.pendown()
    p.color(edge,fill); p.begin_fill(); p.circle(r); p.end_fill()

circle(0,10,190,"#d9f3e7","#4d8d78")
circle(0,10,165,"white","#4d8d78")
circle(0,-5,78,"#68b88e")
for x,y in [(-38,18),(0,38),(38,18),(-38,-25),(0,-45),(38,-25)]:
    p.penup(); p.goto(x,y); p.pendown(); p.circle(17)
circle(0,105,38,"#9bdc9b")
for x,y in [(-13,112),(13,112)]: circle(x,y,4,"#183b32","#183b32")
p.penup(); p.goto(-10,91); p.setheading(-60); p.pendown(); p.color("#286b55"); p.circle(12,120)
for x,y in [(-82,48),(82,48),(-82,-52),(82,-52)]: circle(x,y,19,"#9bdc9b")
p.penup(); p.goto(0,225); p.color("#25445b"); p.write("MEDTIMER STAR!",align="center",font=("Arial",22,"bold"))
p.goto(0,-230); p.write("Small steps. Great consistency.",align="center",font=("Arial",14,"normal"))
p.hideturtle()
screen.mainloop()
