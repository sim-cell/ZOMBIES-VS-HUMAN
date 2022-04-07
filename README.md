BABANAZAROVA Dilyara 28709428
CELIK Simay 28713301
KUDRYAVTSEVA Kristina 21137133

# ZOMBIES vs HUMANS

## IMPORTANT 

When adding agents, pls do not create a new variable and instead just add them to the list. Creating a variable causes display problems

## WHAT HAPPENS IN THE SIMULATION (BY FAR)
  If humans see a zombie close to them they run away, if a zombie sees a human in front of them (depends on their random  direction) they run towards them. PROBABILITY TO MOVE for humans is lower so that zombies can catch up. When a zombie and a human are on the same coords : explained in combat function in DONE list. If two opposite sexes of humans REPRODUCE a baby is born (might add the aging factors) and human couples tend to move together.

  ## PROBLEM SOLVING
  - readding the cure
  - basic agents - food gun display problem
  - night and day
  - slow down the iteration 
  - change probabilities -> zombies can't win right now
  - fps drop


## TO DO:
  - couples becoming groups (K) --------------
  - adding day and night (S) !!!!!
  - adding images for zombies and humans (S) !!!!!   - visual changements concerning agents and objects (S)
  - changing the transitioning process from human to zombie (-)
    - a transitioning period
    - immunity 
  - working on a player (-)



## DONE:

  - attributs of agents (zombies and humans)<br>
    - age decomp hunger etc...<br>
  - combat function
    - if human has a gun and PROBSHOOT (shoot function) then zombie dies and gets removed
    - else if zombie bites human, human gets deleted from humans list and a zombie in the same coordinates gets added to the zombies list
    - else human gets older, energy -- etc.
  - move functions
    - move -> random movement
    - move2 -> movement to given coords
    - move 3
      - humans: if there is a zombie in north, south, east or west moves to opposite direction
      - zombies: if there is a human in front of them they go towards the human
  - stepAgents function
    - scroll through humans and zombies lists and remove them if necessary (death from hunger, combat etc.)
  - render
    - for level in range... <br>
      goes through agents lists and implements them on the program
  
  - food drops
  - gun drops
  - reproduction (DONE)
  - gun and food probabilities
  - objects vs humans
  - randomising the environment

## lighting 
https://www.youtube.com/watch?v=oicpNiye6c0
https://www.youtube.com/watch?v=NGFk44fY0O4