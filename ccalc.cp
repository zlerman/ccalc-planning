:- include 'settings.cp'.

:- sorts
    team;
    robot;
    number.

:- objects
   team1, team2, team3, team4   :: team;
   workerRobot                  :: robot;
   0..100                       :: number.

:- constants
   allowBorrowing                    :: inertialFluent;
   has(team, robot),
   lendEarliest(team),
   workRemaining(team)               :: inertialFluent(0..l);
   lend(team, team, robot, number),
   tick(team),
   performWork(team, robot)          :: exogenousAction.

:- variables
   N, M, L   :: number;
   R         :: robot;
   T, T2     :: team.

performWork(T, R) causes workRemaining(T)=N-M if has(T, R)=M & workRemaining(T)=N.
lend(T, T2, R, N) causes has(T2, R)=M+N & has(T, R)=L-N if has(T2, R)=M & has(T, R)=L.
tick(T) causes lendEarliest(T)=N-1 if lendEarliest(T)=N.

nonexecutable lend(T, T2, R, N) & performWork(T, R).
nonexecutable lend(T, T2, R, N) if -allowBorrowing.
nonexecutable lend(T, T, R, N).  % Do not allow teams to lend to themselves.
nonexecutable lend(T, T2, R, N) if lendEarliest(T) > 0.  % Cannot lend until we've reached the lendEarliest time step
nonexecutable lend(T, T2, R, N) if N=0.  % Cannot lend 0 robots
nonexecutable performWork(T, R) if workRemaining(T)=0.  % Cannot perform work if no work remains.

% Question 1: Can you solve your task in k steps?
:- query
   label   :: questionOne;
   maxstep :: l;
   0: has(team1, workerRobot)=teamOneBots   &
      has(team2, workerRobot)=teamTwoBots   &
      has(team3, workerRobot)=teamThreeBots &      
      has(team4, workerRobot)=teamFourBots &
      -allowBorrowing &
      workRemaining(currentTeam)=8;
   maxstep: workRemaining(currentTeam)=0.

% Question 2: Can you solve your task in k steps, if you lend m robots?
:- query 
   label   :: questionTwo;
   maxstep :: l;
   0: has(team1, workerRobot)=teamOneBots &
      has(team2, workerRobot)=teamTwoBots &      
      has(team3, workerRobot)=teamThreeBots &
      has(team4, workerRobot)=teamFourBots &
      allowBorrowing=true &
      workRemaining(team2)=0 &
      workRemaining(currentTeam)=8;
   maxstep: workRemaining(currentTeam)=0 & has(currentTeam, workerRobot)=currentTeamBots-m.

% Question 3: Can you solve your task in k steps, if you borrow m robots?
:- query 
   label   :: questionThree;
   maxstep :: l;
   0: has(team1, workerRobot)=teamOneBots &
      has(team2, workerRobot)=teamTwoBots &
      has(team3, workerRobot)=teamThreeBots &
      has(team4, workerRobot)=teamFourBots &
      lendEarliest(team1)=team1LendEarliestValue &
      lendEarliest(team3)=team3LendEarliestValue &
      workRemaining(currentTeam)=8;
   maxstep: workRemaining(currentTeam)=0 & has(currentTeam, workerRobot)=currentTeamBots+m.
