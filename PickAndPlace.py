from DobotAbbs import DBA
import time

bot = DBA(250, 0, 50)

bot.dobotConnect()


bot.moveHome()

bot.pickToggle(-56)
bot.toggleSuction()
bot.pickToggle(-56)

for x in range(3):
    newLoc = 25 * x
    bot.moveArmXY(125, -225)
    bot.moveArmXY(newLoc, -225)
    bot.pickToggle(-56)
    bot.toggleSuction()
    bot.pickToggle(-56)
    bot.moveArmXY(125, -225)
    bot.moveHome()
    time.sleep(0.5)
    bot.moveArmXY(125, -225)
    bot.moveArmXY(newLoc, -225)
    bot.pickToggle(-56)
    bot.toggleSuction()
    bot.pickToggle(-56)
else:
    bot.pickToggle(-56)
    bot.toggleSuction()
    bot.pickToggle(-56)
