# Implementation of the main simulation class.
import random

from my_array import Array
from llistqueue import Queue
from simpeople import TicketAgent, Passenger

import logging

logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.INFO,
                    filemode="w")


class TicketCounterSimulation:
    # Create a simulation object.
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        # Parameters supplied by the user.
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes
        # Simulation components.
        self._passengerQ = Queue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)
        # Computed during the simulation.
        self._totalWaitTime = 0
        self._numPassengers = 0

    # Run the simulation using the parameters supplied earlier.
    def run(self):
        for curTime in range(self._numMinutes + 1):
            # print(curTime)
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def _handleArrival(self, cur_time):
        """Add new passengers to queue"""
        if 0 <= random.random() <= self._arriveProb:
            self._numPassengers += 1
            self._passengerQ.enqueue(Passenger(self._numPassengers, cur_time))
            logging.info(f"TIME {cur_time}: Passenger {self._numPassengers} arrived in queue")

    def _handleBeginService(self, cur_time):
        """Begin service for passengrs in queue with free agents """
        for i in range(len(self._theAgents)):
            if self._passengerQ.isEmpty():
                return
            if self._theAgents[i].isFree():
                passenger = self._passengerQ.dequeue()
                self._theAgents[i].startService(passenger, cur_time + self._serviceTime)
                self._totalWaitTime += cur_time - passenger.timeArrived()
                logging.info(f"TIME {cur_time}: Agent {i + 1} started serving Passenger {passenger.idNum()}. "
                             f"Waiting time: {cur_time - passenger.timeArrived()}")
                # logging.info(f"")

    def _handleEndService(self, cur_time):
        """End service for passengrs"""
        for i in range(len(self._theAgents)):
            if self._theAgents[i].isFinished(cur_time):
                passenger = self._theAgents[i].stopService()
                logging.info(f"TIME {cur_time}: Agent {i + 1} finished serving Passenger {passenger.idNum()}")

    # Print the simulation results.
    def printResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWait = float(self._totalWaitTime) / numServed
        print("")
        print("Number of passengers served = ", numServed)
        print("Number of passengers remaining in line = %d" %
              len(self._passengerQ))
        print("The average wait time was %4.2f minutes." % avgWait)
