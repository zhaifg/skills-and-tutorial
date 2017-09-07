#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-01 11:27:18
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import os
import turtle
myTurtle = turtle.Turtle()
myWin = turtle.Screen()


def drawSpiral(myTurtle, lineLen):
    if lineLen > 0:
        myTurtle.forward(lineLen)
        myTurtle.right(90)
        drawSpiral(myTurtle, lineLen - 5)


# drawSpiral(myTurtle, 200)
# myWin.exitonclick()


def tree(branchLen, t):
    if branchLen > 5:
        t.forward(branchLen)
        t.right(20)
        tree(branchLen - 15, t)
        t.left(40)
        tree(branchLen - 10, t)
        t.right(20)
        t.backward(branchLen)


def main():
    t = turtle.Turtle()
    myWin = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    t.color("green")
    tree(100, t)
    myWin.exitonclick()


main()
