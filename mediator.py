import re
import subprocess

# Config of problem
config = {
    "m": '2',  # number of robots to lend.
    "team1LendEarliestValue": '5', 
    "team3LendEarliestValue": '5'
}

# Meta-data on each team.
teams = [
    {"name": "team1", "numBots": "2", "questionOne": False, "questionTwo": False, "questionThree": False, "index": "1"},
    {"name": "team3", "numBots": "2", "questionOne": False, "questionTwo": False, "questionThree": False, "index": "3"},
    {"name": "team2", "numBots": "0", "questionOne": False, "questionTwo": False, "questionThree": False, "index": "2"},
    {"name": "team4", "numBots": "0", "questionOne": False, "questionTwo": False, "questionThree": False, "index": "4"}
]

# Write the problem settings to the macro file.
def write_settings(l, team):
    settings = ["l -> " + str(l), 
                        "teamOneBots -> 2",                        
                        "teamTwoBots -> 0",
                        "teamThreeBots -> 2", 
                        "teamFourBots -> 0",
                        "team1LendEarliestValue -> " + config['team1LendEarliestValue'],
                        "team3LendEarliestValue -> " + config['team3LendEarliestValue'],
                        "m -> " + config['m'],
                        "currentTeamBots -> " + team['numBots'],
                        "currentTeam -> " + team['name']]

    # Create settings file and ask each team question 1.
    with open('./settings.cp', 'w') as f:
        f.write(":- macros\n")
        for j in range(len(settings)):
            f.write("\t" + settings[j])
            f.write(";\n") if j != len(settings) - 1 else f.write(".")


# Parse the response of question two to get the earliest lending time.
def get_lend_earliest(answer):
    lines = answer.split("\n")
    lend_earliest = -1 
    current_step = -1
    for line in lines:
        timestep = re.findall(r'\d:', line)
        if len(timestep) == 1:
            current_step += 1
        if "lend(" in line:
            # At this point parse which team lent to which team.
            lend_earliest = current_step
    return lend_earliest


# Constant delay.
def delay():
    return 2


# Query each team the three questions in order to determine lenders/borrowers in the minimum time.
def phase_one():
    l = 1  # The optimal time step. Start at one and increment if not solvable in that time.
    solved = False 

    # Holds the pairs of (team index, lend earliest step) and (team index, borrow latest pairs)
    lenders = []
    borrowers = []
    while not solved:       
        for team in teams:
            write_settings(l, team)
            answers = []
            for question in ["questionOne", "questionTwo", "questionThree"]:
                answer = subprocess.check_output(['cplus2asp', 'ccalc.cp', 'query=' + question])
                answers.append(answer)
                
                if "UNSATISFIABLE" not in answer:
                    team[question] = True

                    # If this is question two, get the earliest time they can lend from the response + delay
                    if question == "questionTwo":
                        earliest = get_lend_earliest(answer) + delay()
                        team['lendEarliest'] = earliest
                        config['lendEarliestValue'] = str(earliest)
                        lenders.append((team['index'], str(earliest)))

            if not team['questionOne'] and not team['questionTwo'] and not team['questionThree']:
                team['role'] = "Unsatisfied"
            elif team['questionOne'] and not team['questionTwo'] and not team['questionThree']:
                team['role'] = "Neither"
            elif team['questionOne'] and team['questionTwo']:
                team['role'] = "Lender"
            else: 
                team['role'] = "Borrower"
                borrowers.append(team['index'])

            team['answers'] = answers

        # Check that every team was satisfied
        solved = True
        for team in teams:
            if team['role'] == "Unsatisfied":
                solved = False
                l += 1  # Try to see if satisfiable with longer plan.

    # Print out each teams roles
    print("Phase 1 - Determining Lenders and Borrowers:")
    print("Plan of length: " + str(l) + " exists")
    for team in teams:
        print("Team: " + team['name'] + " Role: " + team['role'])

    return l, lenders, borrowers


def phase_two(l, lenders, borrowers):
    # Goal of algorithm, the ml collaboration. Describes m robot transfers in l steps.
    print("Phase 2 - Outputting ml-collboration:")
    print("Robot Transfers (m): " + config['m'])
    print("Optimal Timesteps (l): " + str(l))
    print("Transfers: ")

    index = 0
    for borrower in borrowers:
        # Find an appropriate lender.
        lender_index, time_step = lenders[index]
        print("f(" + lender_index + ", " + borrower + ") = (" + config['m'] + ", " + time_step + ")")
        index += 1


if __name__ == "__main__":
    optimal_time, lenders, borrowers = phase_one()
    print("---------------------------------\n")
    phase_two(optimal_time, lenders, borrowers)
