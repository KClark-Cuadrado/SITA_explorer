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
        if next_event_time == next_arrival_time:
            assigned = 0
            curr_time = next_arrival_time
            new_job_size = expov(service_size_mean)

            # while new_job_size < .0001:
            #     new_job_size = random.expovariate(service_size_mean)
            which_queue = 0
            if new_job_size > cutoff:
                which_queue = 1


            for server_num in myservs:
                if busy_server_array[server_num][1] == -1:
                    busy_server_array[server_num] = (jobs_arrived, curr_time+new_job_size, new_job_size, curr_time)
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
            #so that we have a departure before this new arrival, possibly several
            curr_time = next_event_time
            assert to_depart != -1
            myresp = curr_time - busy_server_array[to_depart][3]
            tresponsetime += myresp
            myslow = myresp / float(busy_server_array[to_depart][2])
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


for mynumservs in [y for y in range(100,1000, 100)]:
    for mycutoff in [0 + .01 * x for x in range(10)]:
        findMRTandMST(num_servers= mynumservs, cutoff=mycutoff, arrival_rate=.9*mynumservs)

print time.time() - starting_time, "seconds"
