import random

from simulation import TicketCounterSimulation


def main():
    counter = TicketCounterSimulation(numAgents=2, numMinutes=100, betweenTime=2, serviceTime=3)
    random.seed(4500)
    counter.run()
    counter.printResults()


main()
