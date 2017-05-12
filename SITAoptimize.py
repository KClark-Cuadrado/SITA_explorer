import random
import time

starting_time = time.time()


def findMRTandMST(cutoff = 1, total_jobs = 10000000, num_servers = 1, arrival_rate = .9, service_size_mean = 1):

    expov = random.expovariate
    busy_server_array = [(-1,-1,-1,-1) for x in range(num_servers)]

    waiting_queue_high = []
    waiting_queue_low = []
    jobs_arrived = 0
    curr_time = 0
    myservs = range(num_servers)

    #total response time and total slowdown
    tresponsetime = 0
    tslowdown = 0
    finished_jobs = 0
    waiting_info = {}
    arrivused = 1



    """ We wait until we have exactly total_jobs finished to terminate, even if jobs are remaining in the system
        This causes some inaccuracy for small numbers of jobs, as the size of jobs that have finished will be slightly
        smaller than that of all jobs that have arrived """


    while finished_jobs < total_jobs:

        #arrivused tests whether the last arrival has been added to the queue
        if arrivused:
            next_arrival_time = curr_time + expov(arrival_rate)
            arrivused = 0

        #we check to see if the next event is an arrival or a departure
        next_event_time = next_arrival_time

        #to_depart holds the index of the server with the next departure
        to_depart = -1
        for server_num in myservs:
            if busy_server_array[server_num][1] > 0 and busy_server_array[server_num][1] < next_event_time:
                next_event_time = busy_server_array[server_num][1]
                to_depart = server_num
        if next_event_time == next_arrival_time:
            assigned = 0
            curr_time = next_arrival_time
            new_job_size = expov(service_size_mean)


            # uncomment the next two lines to allow truncation of job sizes

            # while new_job_size < .0001:
            #     new_job_size = random.expovariate(service_size_mean)


            #queue 0 is for high priority jobs, queue 1 is for jobs above the cutoff (low priority)
            which_queue = 0
            if new_job_size > cutoff:
                which_queue = 1


            for server_num in myservs:
                #check if the server at server num is free (equal to -1 if free)
                if busy_server_array[server_num][1] == -1:

                    #the server at server_num is assigned the job, the tuple is (job_number, finish_time, size and arrival time)
                    busy_server_array[server_num] = (jobs_arrived, curr_time+new_job_size, new_job_size, curr_time)
                    assigned = 1
                    break

            #this happens if the job couldn't be assigned as no servers were free
            if assigned == 0:
                #separate queues into high and priority
                if which_queue == 0:
                    waiting_queue_high.append(jobs_arrived)

                    #waiting info holds information on the job in the queue for statistics
                    waiting_info[jobs_arrived] =  (new_job_size, curr_time)
                else:
                    waiting_queue_low.append(jobs_arrived)
                    waiting_info[jobs_arrived] = (new_job_size, curr_time)
            jobs_arrived += 1
            arrivused = 1

        #this else statement is triggered if the next event will be a departure
        else:

            curr_time = next_event_time

            #sanity check that a real server holds the departure
            assert to_depart != -1

            #this measures statistics at departure time: we add the response time and slowdown for the job to the
            #total response time and slowdown so far
            myresp = curr_time - busy_server_array[to_depart][3]
            tresponsetime += myresp
            myslow = myresp / float(busy_server_array[to_depart][2])
            tslowdown += myslow

            finished_jobs += 1

            #sets the server at to_depart to be free
            busy_server_array[to_depart] = (-1, -1, -1, -1)

            #check if there is a job waiting, if so, assign it. First check our high priority waiting queue, then low
            if len(waiting_queue_high):
                high_pri_job = waiting_queue_high[0]
                initsize = waiting_info[high_pri_job][0]
                comp_time = curr_time + initsize
                busy_server_array[to_depart] = (high_pri_job, comp_time, initsize, waiting_info[high_pri_job][1])
                waiting_queue_high.remove(high_pri_job)
                waiting_info.pop(high_pri_job)
            elif len(waiting_queue_low):
                next_job = waiting_queue_low[0]
                initsize = waiting_info[next_job][0]
                comp_time = curr_time + initsize
                busy_server_array[to_depart] = (next_job, comp_time, initsize, waiting_info[next_job][1])
                waiting_queue_low.remove(next_job)
                waiting_info.pop(next_job)

    mean_response_time = tresponsetime / float(finished_jobs)
    mean_slowdown = tslowdown / float(finished_jobs)

    print num_servers, cutoff, mean_response_time, mean_slowdown


findMRTandMST()

print time.time() - starting_time, "seconds"
