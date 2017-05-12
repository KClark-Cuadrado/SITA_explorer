# SITA_explorer

This is a simulation, as coded, of an M/M/k queueing system with several queues, priority classes over the jobs by size (SITA cutoffs), non-preemption across jobs and transferable, multiple servers as resources. Any of these parameters can be changed easily in the main file, SITAoptreserve, when running, by, for example, simply changing the random exponential to whichever distribution you desire for a G/G/k. 

If you wish to test the effect of reserving servers for high priority jobs, in the form of not allowing low priority jobs to take new servers on arrival when load is above a certain threshold, use SITAoptreserve.

Both files can be run as is and by default use 10 million jobs as a minimum: for most distributions, numbers below this lead to unreliable results due to high variance. Mean slowdown and mean response time for the parameter choice are outputted automatically, but more statistics can be collected simply.

Contact: clark-cuadrado@wustl.edu
