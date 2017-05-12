import random
import time

starting_time = time.time()


def findMRTandMST(cutoff = 1, total_jobs = 10000000, num_servers = 2, arrival_rate = .9, service_size_mean = 1, res_servers = 1):

    expov = random.expovariate
    #in busy serv array, first is job number, second is when that job will be finished, third is initial size, 4th arriv time
    busy_server_array = [(-1,-1,-1,-1) for x in range(num_servers)]
    waiting_queue_high = []
    waiting_queue_low = []
    jobs_arrived = 0
    curr_time = 0
    myservs = range(num_servers)
    backserv = reversed(myservs)
    myunres = myservs[res_servers:]
    tresponsetime = 0
    tslowdown = 0
    finished_jobs = 0
    waiting_info = {}
    arrivused = 1




    while finished_jobs < total_jobs:
        if arrivused:
            next_arrival_time = curr_time + expov(arrival_rate)
            arrivused = 0
        next_event_time = next_arrival_time
        to_depart = -1
        for server_num in myservs:
            if busy_server_array[server_num][1] > 0 and busy_server_array[server_num][1] < next_event_time:
                next_event_time = busy_server_array[server_num][1]
                to_depart = server_num
        #so no departures before the next arrival - need to try to assign arrival to server, add to full job array
        if next_event_time == next_arrival_time:
            assigned = 0
            curr_time = next_arrival_time
            new_job_size = expov(service_size_mean)

            # while new_job_size < .0001:
            #     new_job_size = random.expovariate(service_size_mean)
            which_queue = 0
            if new_job_size > cutoff:
                which_queue = 1

            #decision here about if 1+ servers free, small arriv, assign to normal or res. Going with norm here
            if which_queue == 0:
                for server_num in backserv:
                    if busy_server_array[server_num][1] == -1: # check if this is faster without ind, comp to tuple
                        busy_server_array[server_num] = (jobs_arrived, curr_time+new_job_size, new_job_size, curr_time)
                        assigned = 1
                        break
            elif which_queue == 1:
                for server_num in myunres:
                    if busy_server_array[server_num][1] == -1:  # check if this is faster without ind, comp to tuple
                        busy_server_array[server_num] = (
                        jobs_arrived, curr_time + new_job_size, new_job_size, curr_time)
                        assigned = 1
                        break
            if assigned == 0:
                if which_queue == 0:
                    waiting_queue_high.append(jobs_arrived)
                    waiting_info[jobs_arrived] =  (new_job_size, curr_time)
                else:
                    waiting_queue_low.append(jobs_arrived)
                    waiting_info[jobs_arrived] = (new_job_size, curr_time)
            jobs_arrived += 1
            arrivused = 1
        else:

            curr_time = next_event_time
            assert to_depart != -1
            myresp = curr_time - busy_server_array[to_depart][3]
            tresponsetime += myresp
            myslow = max(myresp / float(busy_server_array[to_depart][2]), 1.0)
            tslowdown += myslow

            finished_jobs += 1
            busy_server_array[to_depart] = (-1, -1, -1, -1)
            if len(waiting_queue_high):

                high_pri_job = waiting_queue_high[0]
                initsize = waiting_info[high_pri_job][0]
                comp_time = curr_time + initsize
                busy_server_array[to_depart] = (high_pri_job, comp_time, initsize, waiting_info[high_pri_job][1])
                waiting_queue_high.remove(high_pri_job)
                waiting_info.pop(high_pri_job)
            elif len(waiting_queue_low) and to_depart >= res_servers:
                next_job = waiting_queue_low[0]
                initsize = waiting_info[next_job][0]
                comp_time = curr_time + initsize
                busy_server_array[to_depart] = (next_job, comp_time, initsize, waiting_info[next_job][1])
                waiting_queue_low.remove(next_job)
                waiting_info.pop(next_job)

    # jobs that finished will have a nonzero val in their finished times array, and that val larger than their arriv time

    mean_response_time = tresponsetime / float(finished_jobs)
    mean_slowdown = tslowdown / float(finished_jobs)

    print num_servers, cutoff, mean_response_time, mean_slowdown


findMRTandMST()

print time.time() - starting_time, "seconds"
