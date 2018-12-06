import time

import Controller




if __name__ == '__main__':
    year = 2018
    month = 0
    day = 1

    list = []

    for i in range(12):
        day = 1
        month += 1
        for j in range(7):
            list.append('{0}.{1}.{2}'.format(day, month, year))
            day += 2



    controller = Controller.Controller()
    # controller.first()
    # controller.second()
    controller.third()

    # controller.testInsertClient()