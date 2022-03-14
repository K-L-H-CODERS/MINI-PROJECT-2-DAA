# Mini-Project-2-DAA

# Flow Shop Scheduling
There are n machines and m jobs. Each job contains exactly n operations. The i-th operation of the job must be executed on the i-th machine. No machine can perform more than one operation simultaneously. For each operation of each job, execution time is specified. Operations within one job must be performed in the specified order. The first operation gets executed on the first machine, then (as the first operation is finished) the second operation on the second machine, and so until the n-th operation. Jobs can be executed in any order, however. Problem definition implies that this job order is exactly the same for each machine. The problem is to determine the optimal such arrangement, i.e. the one with the shortest possible total job execution makespan.

# Existing Solutions for Flow Shop Scheduling

<li>Branch and Bound.</li>
<li>Dynamic programming.</li>
<li>Heuristic algorithm.</li>
<li>Meta-heuristics.</li>



# Our Algorithm  [Johnson's Algorithm]

Algorithm JOHNSON_FLOWSHOP(T, Q)
// T is array of time of jobs, each column indicating time on machine Mi
// Q is queue of jobs
Q = Φ
for j = 1 to n do
  t = minimum machine time scanning in booth columns
  if t occurs in column 1 then
    Add Jobj to the first empty slot of Q
  else
    Add Jobj to last empty slot of Q
  end
  Remove processed job from consideration
end
return Q
![image](https://user-images.githubusercontent.com/87629978/158102552-57110bce-717a-4e9f-8ab9-688eb7e44b3b.png)


