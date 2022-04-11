# Import libraries
import collections
import ortools.sat.python.cp_model
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# This class represent a task
class Task:
    # Create a new task
    def __init__(self, start: object, interval: object, end: object):
        # Set values for instance variables
        self.start = start
        self.interval = interval
        self.end = end


# This class represent an assignment
class Assignment:
    # Create a new assignment
    def __init__(self, job_id: int, task_id: int, start: int, duration: int):
        # Set values for instance variables
        self.job_id = job_id
        self.task_id = task_id
        self.start = start
        self.duration = duration

    # Sort
    def __lt__(self, other):
        return self.start + self.duration < other.start + other.duration

    # Print
    def __repr__(self):
        return ('(Job: {0}, Task: {1}, Start: {2}, End: {3})'.format(self.job_id, self.task_id, self.start,
                                                                     self.start + self.duration))


# The main entry point for this module
def main():
    # Input data: Task = (machine_id, duration)
    jobs = [[(0, 3), (1, 2), (2, 2)],  # Job0
            [(0, 2), (2, 1), (1, 4)],  # Job1
            [(1, 4), (2, 3)]  # Job2
            ]
    # Variables
    machine_count = 3
    tasks = {}
    intervals = collections.defaultdict(list)
    assignments = collections.defaultdict(list)
    # Compute horizon dynamically (sum of all durations)
    horizon = sum(task[1] for job in jobs for task in job)
    # Create a model
    model = ortools.sat.python.cp_model.CpModel()
    # Loop jobs
    for job_id, job in enumerate(jobs):
        # Loop tasks in a job
        for task_id, task in enumerate(job):
            # Variables
            machine_id = task[0]
            duration = task[1]
            suffix = '_{0}_{1}'.format(job_id, task_id)
            # Create model variables
            start = model.NewIntVar(0, horizon, 'start' + suffix)
            end = model.NewIntVar(0, horizon, 'end' + suffix)
            interval = model.NewIntervalVar(start, duration, end, 'interval' + suffix)
            # Add a task
            tasks[job_id, task_id] = Task(start, interval, end)
            # Add an interval for the machine
            intervals[machine_id].append(interval)
    # Add no-overlap constraints
    # A machine can only work with 1 task at a time
    for machine in range(machine_count):
        model.AddNoOverlap(intervals[machine])
    # Add precedence constraints
    # Tasks in a job must be performed in the specified order
    for job_id, job in enumerate(jobs):
        # Loop tasks in a job
        for task_id in range(len(job) - 1):
            # Add a precedence constraint
            model.Add(tasks[job_id, task_id + 1].start >= tasks[job_id, task_id].end)
    # Create an objective function
    objective = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(objective, [tasks[job_id, len(job) - 1].end for job_id, job in enumerate(jobs)])
    model.Minimize(objective)
    # Create a solver
    solver = ortools.sat.python.cp_model.CpSolver()
    # Set a time limit of 30 seconds.
    solver.parameters.max_time_in_seconds = 30.0
    # Solve the problem
    status = solver.Solve(model)
    # Print output if the solution is optimal
    if (status == ortools.sat.python.cp_model.OPTIMAL):
        # Loop jobs
        for job_id, job in enumerate(jobs):
            # Loop tasks in a job
            for task_id, task in enumerate(job):
                # Add an assignment
                machine_id = task[0]
                start = solver.Value(tasks[job_id, task_id].start)
                assignments[machine_id].append(Assignment(job_id, task_id, start, task[1]))
        # Create bars and sort assignments
        bars = []
        for machine in range(machine_count):
            assignments[machine].sort()
            bar_tasks = []
            for ass in assignments[machine]:
                bar_tasks.append((ass.start, ass.duration))
            bars.append(bar_tasks)

        # Print the solution
        print('--- Final solution ---\n')
        print('Optimal Schedule Length: {0}\n'.format(solver.ObjectiveValue()))
        print('Schedules:')
        for machine in range(machine_count):
            print(machine, ':', *assignments[machine])
        print()
        # Plot gantt chart
        fig, gnt = plt.subplots(figsize=(12, 8))
        fig.suptitle('Gantt Chart', fontsize=16)
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Machines')
        gnt.set_yticks([12, 22, 32])
        gnt.set_yticklabels(['0', '1', '2'])
        gnt.grid(True)
        # Loop bars
        for i in range(len(bars)):
            gnt.broken_barh(bars[i], (10 + i * 10, 4), facecolors=('tab:orange', 'tab:green', 'tab:red'))
            j = 0
            for x1, x2 in bars[i]:
                gnt.text(x=x1 + x2 / 2, y=12 + i * 10, s=j, ha='center', va='center', color='white')
                j += 1
        # Create a legend
        labels = []
        labels.append(mpatches.Patch(color='tab:orange', label='Task 0'))
        labels.append(mpatches.Patch(color='tab:green', label='Task 1'))
        labels.append(mpatches.Patch(color='tab:red', label='Task 2'))
        plt.legend(handles=labels, loc=4)
        # Show or save the plot
        # plt.show()
        plt.savefig('plots\\schedule-gantt.png')


# Tell python to run main method
if __name__ == '__main__': main()