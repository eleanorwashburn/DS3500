import pandas as pd
import numpy as np

class TA_Assignment:
    def __init__(self, tas_df, sections_df, solution):
        """Initializes the TA_Assignment object with TAs, sections, and the solution."""
        self.tas = self.load_tas(tas_df)
        self.sections = self.load_sections(sections_df)
        self.solution = solution
        self.assign_times_to_tas()

    def load_tas(self, tas_df):
        """Converts the TA dataframe to a dictionary."""
        tas = {}
        for _, row in tas_df.iterrows():
            ta_id = row['ta_id']
            max_assigned = row['max_assigned']
            availability = [row[str(i)].strip() for i in range(17)]  # Assuming 17 columns for availability
            tas[ta_id] = {
                'max_assigned': max_assigned,
                'availability': availability,
                'assigned_times': []
            }
        return tas

    def load_sections(self, sections_df):
        """Converts the sections dataframe to a dictionary."""
        sections = {}
        for _, row in sections_df.iterrows():
            section_id = row['section']
            min_ta = row['min_ta']
            max_ta = row['max_ta']
            daytime = row['daytime'].strip()
            sections[section_id] = {'min_ta': min_ta, 'max_ta': max_ta, 'daytime': daytime}
        return sections

    def load_solution_matrix(self, solution_data):
        """Converts the solution matrix (dict) to a solution assignment."""
        return solution_data  # Already provided as a dictionary, so no changes needed

    def assign_times_to_tas(self):
        """Assigns section times to TAs based on the solution."""
        for section_id, assigned_tas in self.solution.items():
            section_daytime = self.sections[section_id]['daytime']
            for ta_id in assigned_tas:
                if ta_id in self.tas:
                    self.tas[ta_id]['assigned_times'].append((section_id, section_daytime))

    def overallocation(self):
        """Calculates the overallocation penalty for TAs."""
        ta_assigned_labs = np.zeros(len(self.tas), dtype=int)
        for section_id, assigned_tas in self.solution.items():
            ta_assigned_labs[list(assigned_tas)] += 1

        max_assigned = np.array([ta['max_assigned'] for ta in self.tas.values()])
        over_count = np.sum(np.maximum(0, ta_assigned_labs - max_assigned))
        return over_count

    def conflicts(self):
        """Calculates the number of conflicts based on TA availability and section timings."""
        conflict_count = 0
        conflicted_tas = set()

        for section_id, assigned_tas in self.solution.items():
            section_daytime = self.sections[section_id]['daytime']

            for ta in assigned_tas:
                if ta not in conflicted_tas:
                    for assigned_section_id, assigned_time in self.tas[ta]['assigned_times']:
                        if assigned_section_id != section_id and assigned_time == section_daytime:
                            conflicted_tas.add(ta)
                            conflict_count += 1
                            break

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


# Load the data from your CSVs
tas_df = pd.read_csv("tas.csv")
sections_df = pd.read_csv("sections.csv")

# Provided Solution Data: section_id -> list of TA ids assigned to that section
solution_data = {
    0: [30, 30, 8],
    1: [9, 37, 18],
    2: [18, 31, 7],
    3: [39, 21],
    4: [5, 22, 15],
    5: [27],
    6: [12, 16],
    7: [],
    8: [0, 33],
    9: [39, 28],
    10: [24, 32, 19],
    11: [28, 14, 10],
    12: [33, 25],
    13: [33, 6],
    14: [3, 11],
    15: [23, 24],
    16: [20, 41, 23],
}

# Create an instance of the TA_Assignment class
ta_assignment = TA_Assignment(tas_df, sections_df, solution_data)

# Calculate and print the scores
print("Overallocation Score:", ta_assignment.overallocation())
print("Conflicts Score:", ta_assignment.conflicts())
print("Undersupport Score:", ta_assignment.undersupport())
print("Unwilling Score:", ta_assignment.unwilling())
print("Unpreferred Score:", ta_assignment.unpreferred())
