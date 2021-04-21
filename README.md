# efficient-lift-simulation
Data structures and algorithms module coursework

The basic premise of my lift control system is based on the functionality of the mechanical lift (base
case), with efficiency modifications to minimise the wait time a person experiences between calling
the lift and when they actually enter it. I chose to optimise this aspect since studies show that
sometimes it’s better to make a person wait longer overall if it means they wait less time to actually
get inside the lift, since waiting for the lift to arrive is usually much more tedious than waiting in
the lift for it to reach your floor. It also feel like you’re making progress when inside the lift, but
not when waiting for it on the outside.
The first implementation I made was editing the requirements to turn around. While the mechanical
lift system has the restriction of only changing direction after reaching either the top or bottom floor,
I included a check to find, if ascending, the highest floor number which didn’t require someone to
be picked up or dropped off at. After reaching this floor, the lift can start descending straight away
since it has no need to go any higher. The same addition is included for the descending lift as well.
Already, just this change gave an improvement of around 2-3% over the mechanical system when
running 1000 iterations of each system with 100 floors and 1000 people waiting and comparing the
average wait time of each person for each system.
In addition to this, my system also places a restriction on who it picks up in order to better manage
lift capacity problems. This restriction means that a person waiting is only picked up by the lift
if the direction they want to go (which is chosen by them pressing up or down when calling the
lift) is the same as the direction the lift is currently heading. Therefore, if a person wants to go
from floor 8 to 6 but the lift is heading up, they would have to wait in the lift while it reached its
highest required floor (or the top in the mechanical lift), before going all the way back down, past
the floor they started on, and finally to their destination. Since their starting floor is passed again
anyway, the person may as well be picked up on the way down and leave an extra space in the lift
for someone else.
This addition, when tested alongside the mechanical system, gives an efficiency increase of 40-50%
meaning the people modeled in this system wait significantly less time for the lift on average. The
results of thousands of test runs and clear logical superiority mean my modified lift model is undeiniably superior to the mechanical model provided
