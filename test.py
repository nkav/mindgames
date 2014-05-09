import game
from time import sleep

def doit():
  game.writetk("hi")
  game.writetk("hello")
  for x in xrange(100):
    sleep(3)
    game.writetk(str(x))
