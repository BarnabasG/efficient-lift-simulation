import random
import os
import time
import copy
import matplotlib.pyplot as plt


MAXIMUM = []            # Testing - stores the maximum results from all the itterations of the system
MINIMUM = []            # Testing - stores the minimum results from all the itterations of the system
MAX_PERSON = []         # Testing - stores the result of the maximum individual person from all the
                        #           itterations of the system (to see if anyone has to wait very long)

def button_calls(total_people: int, max_floor: int) -> tuple:
    '''
    This function is called to generate the start and destination floors of the people who use the
    lift in the simulation as well as the time gap between each person if this setting is activated.

    Arguments:
    total_people - set to select the total number of people in the system
    max_floor - set to select the total number of floors in the system
    '''
    call_order = []     # Creates new list to store the start and end positions of each person
    time_gap = []

    for i in range(total_people):
        call_order.append([i, random.randint(0, max_floor), random.randint(0, max_floor)])
        while call_order[-1][-1] == call_order[-1][-2]:
            call_order[-1][-1] = (random.randint(0, max_floor))

        # time_gap.append([i, random.randint(0,30)])      # Random time delay between people - UNCOMMENT TO ENABLE
        time_gap.append([i, 0])       # Original code (everyone already waiting) - COMMENT TO DISABLE

    return call_order, time_gap

def display_lift(max_floor: int, wait_list: list, pos: int, in_lift: list):
    '''
    This function is ues to draw and display the current state of the lift after each lift movement.

    Arguments:
    max_floor - set to select the total number of floors in the system
    wait_list - the list of people currently waiting for the lift including the start and end positions
    pos - the current position (floor number) of the lift
    in_lift - the list of people currently inside the lift including the start and end positions
    '''
    if DRAW == True:        # global boolean variable to determine whether the program should be in draw mode or test mode
        time.sleep(0.01)                    # time delay to reduce screen flicker
        clear = lambda: os.system('cls')   # lambda function to call the system function to clear the screen
        clear()
        in_lift[:] = [x for x in in_lift if x != [-1, -1, -1]]  # list comprehension to remove people who have
                                                                # left the lift
        for i in range(max_floor, -1, -1):
            if pos == i:
                lift = "|" + str(len(in_lift)) + "|"
            else:
                lift = "    "
            floor_count = ""
            for j in range(len(wait_list)):
                if i == wait_list[j][1]:
                    floor_count = floor_count + "O"
            print(str(i) + " " + lift + "  " + floor_count)
            print("  -----------")
        print()


def check_in_lift(in_lift, pos):
    '''
    This function will simply chech all the people in the lift and mark anyone who should be getting off the
    lift so they can be removed. They are not removed straight away to avoid errors from comparing changing lists
    in a loop.

    Arguments:
    in_lift - the list of people currently inside the lift including the start and end positions
    pos - the current position (floor number) of the lift
    '''
    for i in range(len(in_lift)):
        if in_lift[i][2] == pos:
            in_lift[i] = [-1, -1, -1]

def check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count,
               total_times, wait_list, itr, mode, up, bypass=False):
    '''
    This function is used by both the mechanical and efficient lift models to check the lift after each movement.
    The function will call time_step to increment the wait time for each person waiting, call check_in_lift,
    and check the wait_list list to move people who are waiting on the current floor into the lift.
    If the mechanical system is moved, the only restriction on this is if the lift capcity is full, but in the
    efficient model there are other modifications that may affect this.

    Arguments:
    max_floor - set to select the total number of floors in the system
    lift_capacity - set to select the maximum number of people in the lift at once
    call_order - list to store the start and end positions of each person
    time_gap - the time delay between each person arriving. 0 if not enabled in 'button_calls' function
    in_lift - the list of people currently inside the lift including the start and end positions
    pos - the current position (floor number) of the lift
    step_count - the number of steps of the lift each person has been waiting for
    total_times - stores the step_counts of people who have got on the lift to track how long each person waited
    wait_list - the list of people currently waiting for the lift including the start and end positions
    itr - passed into time_step function to determine whether this call should increment people's step_counts
    mode - if mode is 1 then the function is called from the effiecient model, else is from the mechanical
    up - the direction the lift is heading
    bypass - default false. passed as true if a rare situation occurs from the efficient model to increase efficiency
    '''
    time_step(call_order, time_gap, step_count, wait_list, itr)

    check_in_lift(in_lift, pos)

    in_lift[:] = [x for x in in_lift if x != [-1, -1, -1]]

    j = 0
    removes = []

    while j < len(wait_list):
        count = 0
        if wait_list[j][1] == pos and len(in_lift) < lift_capacity and not wait_list[j] in in_lift:
            up_now = wait_list[j][1] < wait_list[j][2]
            if mode == 1 and up != up_now and len(wait_list) > lift_capacity - 1 and not bypass:
                j += 1
                continue
            total_times.append(step_count[j])
            in_lift.append(wait_list[j])
            step_count[j] = -1
            wait_list[j] = -1
            removes.append(j)
        j += 1
    for index in removes:               # items to be removedin the wait_list are tagged (set to -1) when found
                                        # and removed at the end of checking everything to avoid errors from 
                                        # comparing changing lists in a loop
        del wait_list[index - count]
        del step_count[index - count]
        count += 1
    removes.clear()
    display_lift(max_floor, wait_list, pos, in_lift)
    return


def lift_pos_base(average_times, total_people, lift_capacity, max_floor, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list):
    '''
    This is the function that runs the functionality of the mechanical lift system. It will only change diretion after
    reaching the top or bottom floor and has no efficiency modifications.

    Arguments:
    average_times - passed into average_time to store the average times of previous test runs of the system
    total_people - set to select the total number of people in the system
    lift_capacity - set to select the maximum number of people in the lift at once
    max_floor - set to select the total number of floors in the system
    call_order - list to store the start and end positions of each person
    time_gap - the time delay between each person arriving. 0 if not enabled in 'button_calls' function
    in_lift - the list of people currently inside the lift including the start and end positions
    pos - the current position (floor number) of the lift
    step_count - the number of steps of the lift each person has been waiting for
    total_times - stores the step_counts of people who have got on the lift to track how long each person waited
    wait_list - the list of people currently waiting for the lift including the start and end positions
    '''
    check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, False, 0, True)

    while len(total_times) != total_people:
        while pos != max_floor:         # Ascending
            pos += 1
            check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, True, 0, True)
            in_lift[:] = [x for x in in_lift if x != [-1, -1, -1]]
        while pos != 0:                 # Descending
            pos -= 1
            check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, True, 0, False)
            in_lift[:] = [x for x in in_lift if x != [-1, -1, -1]]

        display_lift(max_floor, wait_list, pos, in_lift)        #Display the current state of the lift

    average_time(average_times, total_times)


def lift_pos_good(average_times, max_floor, total_people, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list):
    '''
    This function runs the functionality of my efficient lift system. It is similar to the mechanical system, but includes edits to
    the earlieset point the lift can change direction.

    Arguments:
    average_times - passed into average_time to store the average times of previous test runs of the system
    max_floor - set to select the total number of floors in the system
    total_people - set to select the total number of people in the system
    lift_capacity - set to select the maximum number of people in the lift at once
    call_order - list to store the start and end positions of each person
    time_gap - the time delay between each person arriving. 0 if not enabled in 'button_calls' function
    in_lift - the list of people currently inside the lift including the start and end positions
    pos - the current position (floor number) of the lift
    step_count - the number of steps of the lift each person has been waiting for
    total_times - stores the step_counts of people who have got on the lift to track how long each person waited
    wait_list - the list of people currently waiting for the lift including the start and end positions
    '''
    check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, False, 1, True)
    i = 0

    while len(total_times) != total_people:

        copy_list = copy.deepcopy(wait_list)        # copy used to create an identical but seperate list

        end = False
        while not end:                              # ascending
            pos += 1
            end = True
            for call in wait_list:
                if call[1] > pos:
                    end = False
            for call in in_lift:
                if call[2] > pos:
                    end = False
            if end:
                check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, True, 1, False)
            else:
                check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, True, 1, True)
            in_lift[:] = [x for x in in_lift if x != [-1, -1, -1]]
        if copy_list == wait_list:                  # if no-one has moved, the lift has reached a rare point where everyone is stuck on specific
                                                    # floors and so the check function is called with a bypass in place to improve efficiency
            check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, False, 1, True, True)

        copy_list = copy.deepcopy(wait_list)
        end = False
        while not end:                              # decending
            pos -= 1
            end = True
            for call in wait_list:
                if call[1] < pos:
                    end = False
            for call in in_lift:
                if call[2] < pos:
                    end = False
            if end:
                check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, True, 1, True)
            else:
                check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, True, 1, False)
            in_lift[:] = [x for x in in_lift if x != [-1, -1, -1]]
        if copy_list == wait_list:
            check_lift(max_floor, lift_capacity, call_order, time_gap, in_lift, pos, step_count, total_times, wait_list, False, 1, True, True)
        display_lift(max_floor, wait_list, pos, in_lift)

    average_time(average_times, total_times)


def time_step(call_order, time_gap, step_count, wait_list, itr):
    '''
    This function increments the step_count (wait time) of people waiting as well as decrementing the
    time gap between each person (live arrival mode) by 1 each lift movement

    Arguments:
    call_order - list to store the start and end positions of each person
    time_gap - the time delay between each person arriving. 0 if not enabled in 'button_calls' function
    step_count - the number of steps of the lift each person has been waiting for
    wait_list - the list of people currently waiting for the lift including the start and end positions
    itr - used to determine whether this call should increment people's step_counts or not
    '''
    count = 0
    for index, item in enumerate(time_gap):
        if itr:
            time_gap[index][1] -= 1
        if time_gap[index][1] <= 0 and not call_order[index] in wait_list:
            wait_list.append(call_order[index])
            step_count.append(0)
            time_gap[index] = -1
    time_gap[:] = [x for x in time_gap if x != -1]      # list comprehension to remove time gaps which have reached 0 and been marked
    if itr:
        for i in range(len(wait_list)):
            step_count[i] += 1


def average_time(average_times, total_times, setting=0):
    '''
    The function has a list inputted and calculates the average of the list, before adding it to
    average_times if it is a test result list or just returning it if it isn't

    Arguments:
    average_times - used to store the average times of previous test runs of the system
    total_times - stores the step_counts of people who have got on the lift to track how long each person waited
    set - default 0. If passed in as 2, will just return the average of the input list and not add it to average_times
    '''
    global MAXIMUM
    global MINIMUM
    global MAX_PERSON

    avr = round(sum(total_times) / len(total_times), 2)
    if setting == 2:
        return avr
    if len(average_times) == 0 or not average_times == avr:
        if max(total_times) > MAX_PERSON[-1]:
            MAX_PERSON[-1] = max(total_times)
        average_times.append(avr)
        if avr > MAXIMUM[-1]:
            MAXIMUM[-1] = avr
        if avr < MINIMUM[-1]:
            MINIMUM[-1] = avr
    return average_times

def appender():
    '''
    Used to append new default values to the lists of maximum and minumum results when the settings or system are changed
    '''
    global MINIMUM, MAXIMUM

    MINIMUM.append(10000)
    MAXIMUM.append(0)
    MAX_PERSON.append(0)

def run():
    '''
    This function controls my program functionality, calling the correct function in the correct order to run the system
    as well as displaying on screen the results of program testing.
    '''
    global DRAW

    mod = ""
    while mod not in("1", "2"):
        print("Pick your mode - (1)Test varity of floors and capacities/ (2)Single custom settings test")
        mod = input()
    print()
    if mod == "1":
        total_people = 100                  # set before running the program to choose the total number of people in the system
        max_floor = 5                       # set before running the program to choose the total number of floors in the system
                                            # 5 in the starting value for the default test, it will raise in the simulation
        types = 20                          # the number of times the settings change - leave at 20 here
        loops = 25                          # the number of loops per settings change - increase to raise result reliability
        DRAW = False
    else:
        print("The mechanical lift with display first, then the improved model")
        print("Enter the number of floors you want to simulate")
        max_floor = int(input())
        print("Enter the number of people you want to simulate")
        total_people = int(input())
        types = 1                           # the number of times the settings change - only one test is run here
        loops = 1                           # increase this number to make the program run multiple times on each setting
                                            # (if this is greater than 1 it is recommended to deactivate the system display code)
        DRAW = True


    lift_capacity = 8                       # set before running the program to choose the maximum capacity of the lift
    average_times = []

    floors = []
    capacities = []
    final_times = []
    for i in range(4):
        final_times.append([])
    percents = []
    percents.append([])
    percents.append([])
    max_floor -= 1

    for i in range(types):

        avr_time = []
        average_times.clear()
        appender()

        for j in range(loops):                                      # calling the mechanical lift system
            button_data = button_calls(total_people, max_floor)
            call_order = button_data[0]
            time_gap = button_data[1]
            lift_pos_base(average_times, total_people, lift_capacity, max_floor, call_order, time_gap, [], 0, [], [], [])
        avr_time.append(str(average_time(0, average_times, 2)))

        appender()

        average_times.clear()
        for j in range(loops):                                      # calling the efficient lift system
            button_data = button_calls(total_people, max_floor)
            call_order = button_data[0]
            time_gap = button_data[1]
            lift_pos_good(average_times, max_floor, total_people, lift_capacity, call_order, time_gap, [], 0, [], [], [])
        avr_time.append(str(average_time(0, average_times, 2)))
        percent = round(((float(avr_time[0])/float(avr_time[-1]))*100)-100, 3)

        print("Floors: " + str(max_floor + 1) + " People: " + str(total_people) + " Capacity: " + str(lift_capacity))
        print("Times Run: " + str(loops))
        print()
        print("Base model:")
        print("Average Time: " + avr_time[0])
        print("Maximum: " + str(MAXIMUM[-2]) + "  Minimum: " + str(MINIMUM[-2]))
        print("Maximum individual: " + str(MAX_PERSON[-2]))

        print()

        print("Efficient model:")
        print("Average Time: " + avr_time[1])
        print("Percentage change: " + str(percent) + "%")
        print("Maximum: " + str(MAXIMUM[-1]) + "  Minimum: " + str(MINIMUM[-1]))
        print("Maximum individual: " + str(MAX_PERSON[-1]))

        if mod == "1":
            if i < 10:                                      # edits the setting in the mode which tests a variety in depth
                floors.append(max_floor + 1)
                max_floor += 5
                percents[0].append(percent)
                final_times[0].append(float(avr_time[0]))
                final_times[1].append(float(avr_time[1]))
                if i == 9:
                    max_floor = 19
                    lift_capacity = 15
            else:
                capacities.append(lift_capacity)
                lift_capacity -= 1
                percents[1].append(percent)
                final_times[2].append(float(avr_time[0]))
                final_times[3].append(float(avr_time[1]))
        print()

    if mod == "1":
        plot(final_times, floors, total_people, max_floor, percents, capacities)


def plot(final_times, floors, total_people, max_floor, percents, capacities):
    '''
    This function uses matplotlib.pyplot to plot graphs of the results of various tests of the system to better
    understand thier correlation.

    Arguments:
    final_times - a list storing the final time result averages of each lift setting
    floors - a list of all the total floor numbers tested
    total_people - set to select the total number of people in the system
    max_floor - set to select the total number of floors in the system
    percents - a list of all the percentage changes from the mechanical lift to the effiecient lift
    capacities - a list of all the lift capacities tested
    '''
    avr_percents = average_time(0, percents[0], 2)
    percents_hold = []
    for i in range(len(percents[0])):
        percents_hold.append(avr_percents)

    axes = plt.gca()                # plot mechanical vs efficient lift systems with varying maximum floor
    axes.set_ylim(0, max(max(final_times[0]), max(final_times[1])) + 5)
    plt.plot(floors, final_times[0], label='Base Model')
    plt.plot(floors, final_times[1], 'tab:green', label='Efficient Model')
    plt.xlabel('Total Floors')
    plt.ylabel('Average time per person')
    plt.title('Plot of time per person vs total floor number for the \n base model and my efficient model \n with varying maximum floor')
    plt.text(floors[-1]//1.8, final_times[1][-1]//3, "Floors: "+str(floors[0])+"-"+str(floors[-1]), fontsize='10')
    plt.text(floors[-1]//1.8, final_times[1][-1]//3-10, "People: "+str(total_people), fontsize='10')
    plt.text(floors[-1]//1.8, final_times[1][-1]//3-20, "Lift Capacity: 8", fontsize='10')

    plt.legend()
    plt.show()

    axes = plt.gca()                # plot percentage efficiency increase of my model with varying maximum floor
    axes.set_ylim(0, max(percents[0]) + 5)
    plt.plot(floors, percents[0], 'tab:green')
    plt.plot(floors, percents_hold, 'tab:green', linestyle='--', alpha=0.7)
    plt.text(floors[-1]//3, avr_percents//2, 'Average time reduction '+str(avr_percents)+'%')
    plt.title('Plot of how much more efficient my model is than the base \n with varying maximum floor')
    plt.xlabel('Total Floors')
    plt.ylabel('Average percentage more efficient')

    plt.show()


    avr_percents = average_time(0, percents[1], 2)
    percents_hold = []
    for i in range(len(percents[1])):
        percents_hold.append(avr_percents)

    axes = plt.gca()            # plot mechanical vs efficient lift systems with varying maximum lift capacity
    axes.set_ylim(0, max(max(final_times[2]), max(final_times[3])) + 5)
    plt.plot(capacities, final_times[2], label='Base Model')
    plt.plot(capacities, final_times[3], 'tab:green', label='Efficient Model')
    plt.xlabel('Lift Capacity')
    plt.ylabel('Average time per person')
    plt.title('Plot of time per person vs lift capacity for the \n base model and my efficient model \n with varying lift capacity')
    plt.text(capacities[0]//1.8, final_times[3][-1]//3, "Floors: " + str(max_floor), fontsize='10')
    plt.text(capacities[0]//1.8, final_times[3][-1]//3-5, "People: "+str(total_people), fontsize='10')
    plt.text(capacities[0]//1.8, final_times[3][-1]//3-10, "Lift Capacity: "+str(capacities[-1])+"-"+str(capacities[0]), fontsize='10')

    plt.legend()
    plt.show()

    axes = plt.gca()            # plot percentage efficiency increase of my model with varying lift capacity
    axes.set_ylim(0, max(percents[1]) + 5)
    plt.plot(capacities, percents[1], 'tab:green')
    plt.plot(capacities, percents_hold, 'tab:green', linestyle='--', alpha=0.7)
    plt.text(capacities[0]//1.8, avr_percents//2, 'Average time reduction '+str(avr_percents)+'%')
    plt.title('Plot of how much more efficient my model is than the base \n with varying lift capacity')
    plt.xlabel('Lift Capacity')
    plt.ylabel('Average percentage more efficient')

    plt.show()

if __name__ == "__main__":
    run()
