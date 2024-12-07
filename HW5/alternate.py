import csv
import numpy as np
from evo import Evo
from profiler import Profiler
import sys
sys.stdout = open("output.txt", "w")

class DataLoader:
    def __init__(self, tas_filename, sections_filename, solution_filename):
        """Initializes the DataLoader by loading TAs, sections, and solution matrix."""
        # Load data
        self.tas = self.load_tas(tas_filename)
        self.sections = self.load_sections(sections_filename)
        self.solution = self.load_solution_matrix(solution_filename)
        # Assign times to TAs based on the solution
        self.assign_times_to_tas()

    def load_tas(self, filename):
        """Loads the TA data from the provided CSV file."""
        # Dictionary to store TAs information
        tas = {}
        # Read in the csv file
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # TA identifier
                ta_id = int(row['ta_id'])
                # Max number of sections a TA can be assigned
                max_assigned = int(row['max_assigned'])
                # Availability is a list of 17 entries representing the availability per section
                availability = [row[str(i)].strip() for i in range(17)]
                # Creating TA dictionary
                tas[ta_id] = {
                    'max_assigned': max_assigned,
                    'availability': availability,
                    'assigned_times': []
                }
        return tas

    def load_sections(self, filename):
        """Loads the section data from the provided CSV file."""
        # Dictionary to store section information
        sections = {}
        # Read in the csv file
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Section identifier
                section_id = int(row['section'])
                # Minimum number of TAs required for the section
                min_ta = int(row['min_ta'])
                # Maximum number of TAs required for the section
                max_ta = int(row['max_ta'])
                # Day and time when the section occurs
                daytime = row['daytime'].strip()
                # Creating the sections dictionary
                sections[section_id] = {'min_ta': min_ta, 'max_ta': max_ta, 'daytime': daytime}
        return sections

    def load_solution_matrix(self, filename):
        """Loads the solution matrix from the provided CSV file."""
        # Dictionary to store solution information
        solution = {}
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row_num, row in enumerate(reader):
                # For each row, check which TAs are assigned to which sections
                for section_id, ta_assigned in enumerate(row):
                    # '1' indicates the TA is assigned to the section
                    if ta_assigned == '1':
                        if section_id not in solution:
                            # Initialize section if not already in dictionary
                            solution[section_id] = []
                            # Add TA ID to the section's list
                        solution[section_id].append(row_num)
        return solution

    def assign_times_to_tas(self):
        """Assigns section times to TAs based on the solution."""
        for section_id, assigned_tas in self.solution.items():
            # Get the time for the section
            section_daytime = self.sections[section_id]['daytime']
            for ta_id in assigned_tas:
                if ta_id in self.tas:
                    # If 'assigned_times' doesn't exist yet for this TA, initialize it
                    if 'assigned_times' not in self.tas[ta_id]:
                        self.tas[ta_id]['assigned_times'] = []
                    # Add the section ID and section time to the TA's assigned times list
                    self.tas[ta_id]['assigned_times'].append((section_id, section_daytime))

class Calculator:
    def __init__(self, solution, tas, sections):
        """Initializes the Calculator class with the given data."""
        self.solution = solution
        self.tas = tas
        self.sections = sections

    def overallocation(self):
        """Calculates the overallocation penalty for TAs."""
        # Count assigned labs using numpy
        ta_assigned_labs = np.zeros(len(self.tas), dtype=int)
        for section_id, assigned_tas in self.solution.items():
            ta_assigned_labs[list(assigned_tas)] += 1

        max_assigned = np.array([ta['max_assigned'] for ta in self.tas.values()])
        over_count = np.sum(np.maximum(0, ta_assigned_labs - max_assigned))
        return over_count

    def conflicts(self):
        """Calculates the number of conflicts based on TA availability and section timings."""
        conflict_count = 0
        # Set to track TAs that have conflicts already
        conflicted_tas = set()

        # Check for time conflicts for each section
        for section_id, assigned_tas in self.solution.items():
            section_daytime = self.sections[section_id]['daytime']

            # Check each TA assigned to this section
            for ta in assigned_tas:
                # If the TA has not been conflicted already
                if ta not in conflicted_tas:
                    # Check for time conflicts with other sections
                    for assigned_section_id, assigned_time in self.tas[ta]['assigned_times']:
                        if assigned_section_id != section_id and assigned_time == section_daytime:
                            # If a conflict is found, add to the conflicted set and count
                            conflicted_tas.add(ta)
                            conflict_count += 1
                            break  # Stop after the first conflict is found for this TA

        return conflict_count

    def undersupport(self):
        """Calculates the undersupport penalty."""
        required_tas = np.array([self.sections[section_id]['min_ta'] for section_id in self.sections])
        assigned_counts = np.array([len(self.solution.get(section_id, [])) for section_id in self.sections])
        missing_tas = np.maximum(0, required_tas - assigned_counts)
        return np.sum(missing_tas)

    def unwilling(self):
        """Calculates the penalty for assigning TAs to sections they are unwilling to support."""
        unwilling_mask = np.array([self.tas[ta]['availability'][section_id] == 'U' for
                                   section_id in self.sections for ta in self.solution.get(section_id, [])])
        return np.sum(unwilling_mask)

    def unpreferred(self):
        """Calculates the penalty for assigning TAs to sections they are willing to support, but not their preferred sections."""
        unpreferred_mask = np.array([self.tas[ta]['availability'][section_id] == 'W' and
                                     self.tas[ta]['availability'][section_id] != 'P' for section_id in
                                     self.sections for ta in self.solution.get(section_id, [])])
        return np.sum(unpreferred_mask)


@Profiler.profile
def swapper(solutions):
    """Agent #1: Randomly swap two TAs between sections."""
    solution = solutions[0]
    section_ids = list(solution.keys())
    sec1, sec2 = np.random.choice(section_ids, 2, replace=False)

    if solution[sec1] and solution[sec2]:
        ta1, ta2 = np.random.choice(solution[sec1]), np.random.choice(solution[sec2])
        solution[sec1].remove(ta1)
        solution[sec1].append(ta2)
        solution[sec2].remove(ta2)
        solution[sec2].append(ta1)

    return solution


@Profiler.profile
def add_random_ta(solutions):
    """Agent #2: Randomly add a TA to a section."""
    solution = solutions[0]
    section_ids = list(solution.keys())
    sec = np.random.choice(section_ids)
    ta_ids = list(tas.keys())
    new_ta = np.random.choice(ta_ids)
    if new_ta not in solution[sec]:
        solution[sec].append(new_ta)
    return solution


@Profiler.profile
def remove_random_ta(solutions):
    """Agent #3: Randomly remove a TA from a section."""
    solution = solutions[0]
    section_ids = list(solution.keys())
    sec = np.random.choice(section_ids)
    if solution[sec]:
        remove_ta = np.random.choice(solution[sec])
        solution[sec].remove(remove_ta)
    return solution


@Profiler.profile
def shift_ta(solutions):
    """Agent #4: Shift a TA from one section to another."""
    solution = solutions[0]
    section_ids = list(solution.keys())
    sec_from, sec_to = np.random.choice(section_ids, 2, replace=False)

    if solution[sec_from]:
        ta_to_move = np.random.choice(solution[sec_from])
        solution[sec_from].remove(ta_to_move)
        solution[sec_to].append(ta_to_move)

    return solution


def export_summary_table_csv(final_population, group_name="teamdata", filename="summary_table.csv"):
    """
    Exports the final population of Pareto-optimal solutions to a CSV file.
    """
    objective_rows = [
        [group_name] + [value for _, value in objectives]
        for objectives, _ in final_population
    ]

    headers = ["groupname", "overallocation", "conflicts", "undersupport", "unwilling", "unpreferred"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(objective_rows)

    print(f"CSV file '{filename}' has been created with {len(objective_rows)} solutions.")


def main():
    global tas, sections

    # Create the environment
    E = Evo()

    # Add the objective functions
    E.add_fitness_criteria("overallocation", Profiler.profile(lambda sol: Calculator(sol, tas, sections).overallocation()))
    E.add_fitness_criteria("conflicts", Profiler.profile(lambda sol: Calculator(sol, tas, sections).conflicts()))
    E.add_fitness_criteria("undersupport", Profiler.profile(lambda sol: Calculator(sol, tas, sections).undersupport()))
    E.add_fitness_criteria("unwilling", Profiler.profile(lambda sol: Calculator(sol, tas, sections).unwilling()))
    E.add_fitness_criteria("unpreferred", Profiler.profile(lambda sol: Calculator(sol, tas, sections).unpreferred()))

    # Register our agents with Evo
    E.add_agent("swapper", swapper, k=1)
    E.add_agent("add_random_ta", add_random_ta, k=1)
    E.add_agent("remove_random_ta", remove_random_ta, k=1)
    E.add_agent("shift_ta", shift_ta, k=1)

    # Load data and create an initial solution
    data_loader = DataLoader("tas.csv", "sections.csv", "test1.csv")
    tas = data_loader.tas
    sections = data_loader.sections

    # Create an empty initial solution
    initial_solution = {section: [] for section in sections}
    E.add_solution(initial_solution)

    # Run the evolutionary algorithm
    print("Initial Population:")
    print(E)
    E.evolve(n=5000000, dom=100, status=100000, time_limit=290)
    print("Final Population:")
    print(E)

    # Generate and print the profiling report and export it as a .txt file
    Profiler.report(filename="profiler_report.txt")

    # Prepare final population data for export
    final_population = [(evaluation, solution) for evaluation, solution in E.pop.items()]

    # Export the CSV file
    export_summary_table_csv(final_population, group_name="teamewlt")

# Run the main function
if __name__ == "__main__":
    main()