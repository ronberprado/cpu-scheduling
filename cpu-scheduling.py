import operator
import sys
from collections import deque

x, y, z = sys.stdin.readline().split()
x = int(x) # 0 = fcfs, 1 = sjf, 2 = srtf, 3 = rr
y = int(y) # Number of processes
z = int(z) # Time slice value

if x == 0:
    input_dict = dict.fromkeys((range(1, y+1)))
    for key, value in input_dict.items():
        a, b, c = sys.stdin.readline().split()
        a = int(a) # PID
        b = int(b) # ARRIVAL TIME
        c = int(c) # BURST TIME
        input_dict[key] = [b, c, 0, 0, 0, 0]

    # input_dict = dict(sorted(input_dict.items(), key=operator.itemgetter(1, 0)))
    input_dict = dict(sorted(input_dict.items(), key=lambda item: item[1][0]))
    sum_waiting_time, prev_key = 0, 0

    for key, value in input_dict.items():
        if prev_key == 0:
            value[2] = value[0]
        else:
            value[2] = max(value[0], input_dict[prev_key][3])
        value[3] = value[2] + value[1]
        value[4] = value[3] - value[0]
        value[5] = value[4] - value[1]

        prev_key = key
        sum_waiting_time += value[5]

    input_dict = dict(sorted(input_dict.items(), key=lambda item: item[0]))

    for key, value in input_dict.items():
        sys.stdout.write(str(key))
        sys.stdout.write(" start time: ")
        sys.stdout.write(str(value[2]))
        sys.stdout.write(" end time: ")
        sys.stdout.write(str(value[3]))
        sys.stdout.write(" | Waiting time: ")
        sys.stdout.write(str(value[5]) + "\n")

    average = (sum_waiting_time / y)
    sys.stdout.write(f"Average waiting time: {average:.1f}")

elif x == 1:
    input_dict = dict.fromkeys((range(1, y+1)))
    for key, value in input_dict.items():
        a, b, c = sys.stdin.readline().split()
        a = int(a)
        b = int(b)
        c = int(c)
        input_dict[key] = [b, c, 0, 0, 0, 0]

    input_dict = dict(sorted(input_dict.items(), key=lambda item: item[1][1]))
    current_time, sum_waiting_time = 0, 0
    print_dict = {}
    inside_flag = False

    while len(input_dict) != 0:
        for key, value in input_dict.items():
            if value[0] <= current_time:
                value[2] = current_time
                value[3] = value[2] + value[1]
                value[4] = value[3] - value[0]
                value[5] = value[4] - value[1]
                inside_flag = True

                sum_waiting_time += value[5]
                current_time = value[3]
                print_dict[key] = value
                del input_dict[key]
                break
        if inside_flag:
            inside_flag = False
        else:
            current_time += 1

    print_dict = dict(sorted(print_dict.items(), key=lambda item: item[0]))

    for key, value in print_dict.items():
        sys.stdout.write(str(key))
        sys.stdout.write(" start time: ")
        sys.stdout.write(str(value[2]))
        sys.stdout.write(" end time: ")
        sys.stdout.write(str(value[3]))
        sys.stdout.write(" | Waiting time: ")
        sys.stdout.write(str(value[5]) + "\n")

    average = (sum_waiting_time / y)
    sys.stdout.write(f"Average waiting time: {average:.1f}")

elif x == 2:
  # a - pid
  # b - AT
  # c - BT
  # 3 to 6 - TAT, ET, WT
  # 7
  # d = Remaining BT
  input_queue = deque()
  ready_queue = []
  arrival_time_list = []
  
  for i in range(y):
      a, b, c = sys.stdin.readline().split()
      a = int(a)
      b = int(b)
      c = int(c)
      d = c
      input_queue.append([a, b, c, 0, 0, 0, 0, d, [], False, [], [], []])
      arrival_time_list.append(b)
  
  arrival_time_list = deque(sorted(arrival_time_list))
  if arrival_time_list[0] == 0:
      arrival_time_list.popleft()
  
  current_time = 0
  finish_counter = 0
  sum_waiting_time = 0
  prev_pid = 0
  start_time = "start time:"
  end_time = "end time:"
  end_bar = "|"
  record_flag = False
  print_queue = []
  
  while finish_counter != y:
      if len(input_queue) != 0:
          if input_queue[0][1] <= current_time:
              ready_queue.append(input_queue.popleft())
              ready_queue = sorted(ready_queue, key=lambda item: item[7])

      if len(ready_queue) > 0:
          if prev_pid != ready_queue[0][0] and prev_pid != 0:
              ready_queue[0][8].append(start_time)
              ready_queue[0][8].append(current_time)
          elif prev_pid == 0:
              ready_queue[0][8].append(start_time)
              ready_queue[0][8].append(current_time)

          # computation to get time to be added in current time ========start
          if len(arrival_time_list) != 0:
              burst_time_used = arrival_time_list[0] - current_time
              if ready_queue[0][7] < burst_time_used or burst_time_used < 0:
                  burst_time_used = ready_queue[0][7]
              else:
                  arrival_time_list.popleft()
          else:
              burst_time_used = ready_queue[0][7]

          # computation to get time to be added in current time ==========end
  
          current_time += burst_time_used
          ready_queue[0][7] -= burst_time_used

          # if prev pid == current pid, delete appended end time because it will be duplicated
          if prev_pid == ready_queue[0][0]:
              ready_queue[0][8].pop()
              ready_queue[0][8].pop()
              ready_queue[0][8].pop()

          # append end time
          ready_queue[0][8].append(end_time)
          ready_queue[0][8].append(current_time)
          ready_queue[0][8].append(end_bar)
  
          prev_pid = ready_queue[0][0]
  
          if ready_queue[0][7] == 0:
              ready_queue[0][4] = current_time
              ready_queue[0][5] = ready_queue[0][4] - ready_queue[0][1]
              ready_queue[0][6] = ready_queue[0][5] - ready_queue[0][2]
  
              ready_queue[0][10] = " ".join(map(str, ready_queue[0][8]))
              ready_queue[0][11].append(ready_queue[0][0])
              ready_queue[0][11].append(ready_queue[0][10])
              ready_queue[0][11].append("Waiting time:")
              ready_queue[0][11].append(ready_queue[0][6])
              ready_queue[0][11].append("\n")
              ready_queue[0][12] = " ".join(map(str, ready_queue[0][11]))
  
              finish_counter += 1
              sum_waiting_time += ready_queue[0][6]
              print_queue.append(ready_queue.popleft())
      else:
          current_time += arrival_time_list[0]
          arrival_time_list.popleft()
  
  print_queue = sorted(print_queue, key=lambda item: item[0])
  
  for i in range(len(print_queue)):
      sys.stdout.write(str(print_queue[i][12]))
  
  average = (sum_waiting_time / y)
  sys.stdout.write(f"Average waiting time: {average:.1f}")

elif x == 3:
    input_queue = []
    for i in range(y):
        a, b, c = sys.stdin.readline().split()
        a = int(a)
        b = int(b)
        c = int(c)
        input_queue.append([a, b, c, 0, 0, 0, 0, c, [], False, []])

    current_time = 0
    finish_counter = 0
    ready_queue = deque()
    print_queue = []
    delete_flag = False
    sum_waiting_time = 0
    start_time = "start time:"
    end_time = "end time:"
    end_bar = "|"
    removed_heap = []  # reset to 0

    while finish_counter != y:
        removed_heap = []  # reset to 0

        # check for process and transfer to ready queue
        for i in range(len(input_queue)):
            if input_queue[i][1] <= current_time and input_queue[i][9] is False:
                ready_queue.append(input_queue[i])
                input_queue[i][9] = True
                # del input_queue[i]
                # break

        if len(ready_queue) > 0:
            # compute first process in ready_queue[0]
            if ready_queue[0][7] - z > 0:
                ready_queue[0][8].append(start_time)
                ready_queue[0][8].append(current_time)

                ready_queue[0][7] -= z
                current_time += z

                ready_queue[0][8].append(end_time)
                ready_queue[0][8].append(current_time)
                ready_queue[0][8].append(end_bar)

                # removed_heap = ready_queue[0]  # store to be pushed again into queue

                removed_heap = ready_queue.popleft()

                # pop from ready queue
                # ready_queue.popleft()
            else:
                ready_queue[0][8].append(start_time)
                ready_queue[0][8].append(current_time)

                current_time += ready_queue[0][7]
                ready_queue[0][7] = 0

                ready_queue[0][8].append(end_time)
                ready_queue[0][8].append(current_time)
                ready_queue[0][8].append(end_bar)

                # store start time array in list
                ready_queue[0][10] = " ".join(map(str, ready_queue[0][8]))

                # compute
                ready_queue[0][4] = current_time
                ready_queue[0][5] = ready_queue[0][4] - ready_queue[0][1]
                ready_queue[0][6] = ready_queue[0][5] - ready_queue[0][2]

                sum_waiting_time += ready_queue[0][6]
                finish_counter += 1

                # transfer to another queue
                print_queue.append(ready_queue[0])

                # pop from ready queue
                ready_queue.popleft()
        else:
            current_time += 1

        # add if some process go into queue while subtracting time quantum
        for i in range(len(input_queue)):
            if input_queue[i][1] <= current_time and input_queue[i][9] is False:
                ready_queue.append(input_queue[i])
                input_queue[i][9] = True
                # del input_queue[i]
                # break

        # also push what was pop earlier in ready queue
        if len(removed_heap) > 0 and removed_heap[7] > 0:
            ready_queue.append(removed_heap)

    print_queue = sorted(print_queue, key=lambda item: item[0])

    for i in range(len(print_queue)):
        sys.stdout.write(str(print_queue[i][0]) + " ")
        sys.stdout.write(str(print_queue[i][10]))
        sys.stdout.write(" Waiting time: ")
        sys.stdout.write(str(print_queue[i][6]) + "\n")

    average = (sum_waiting_time / y)
    sys.stdout.write(f"Average waiting time: {average:.1f}")
