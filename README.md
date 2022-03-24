BABANAZAROVA Dilyara 28709428
CELIK Simay 28713301
KUDRYAVTSEVA Kristina 21137133

# ZOMBIES vs HUMANS

## WHAT HAPPENS IN THE SIMULATION (BY FAR)
  If humans see a zombie close to them they run away, if a zombie sees a human in front of them (depends on their random  direction) they run towards them. PROBABILITY TO MOVE for humans is lower so that zombies can catch up. When a zombie and a human are on the same coords : explained in combat function in DONE list. If two opposite sexes of humans REPRODUCE a baby is born (might add the aging factors) and human couples tend to move together.

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


## TO DO:
  - reproduction (DONE)
  - couples becoming groups (K)
  - adding day and night (S)
  - visual changements concerning agents and objects (S)
  - adding environmental changes
    - random mountains (S)
    - environmental changes (D)
  - environment x agents x objects 
    - climbing a mountain etc (S-D)
  - changing the transitioning process from human to zombie (-)
    - a transitioning period
    - immunity
  - working on a player (-)





