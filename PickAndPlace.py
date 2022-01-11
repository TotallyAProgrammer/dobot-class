from DobotAbbs import DBA
import time

bot = DBA(250, 0, 50)

bot.dobotConnect()

bot.moveHome()

bot.pickToggle(-56)
bot.toggleSuction()
bot.pickToggle(-56)

for x in range(4):
    bot.moveArmXY(125, -225)
    bot.pickToggle(-56)
    bot.toggleSuction()
    bot.pickToggle(-56)
    bot.moveHome()
else:
    bot.pickToggle(-56)
    bot.toggleSuction()
    bot.pickToggle(-56)