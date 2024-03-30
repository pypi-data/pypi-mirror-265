import czastc.turtle as turtle
turtle = turtle.Turtle()
turtle.speed(0)
color_list = czastc.turtle.generate_color_gradient(100, [[255, 255, 0], [255, 0, 0], [255, 0, 255]])
for i, color in enumerate(color_list):
    if i % 2 == 0:
        turtle.right(90)
        turtle.color(color)
        turtle.forward(100)
        turtle.left(90)
        turtle.forward(1)
    else:
        turtle.left(90)
        turtle.color(color)
        turtle.forward(100)
        turtle.right(90)
        turtle.forward(1)
czastc.turtle.polygon(turtle, 5, 100, [[255, 0, 0], [255, 0, 255]])
turtle.screen.mainloop()
