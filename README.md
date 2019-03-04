# HarvestMemory

A programming game written by Austin Henley for his software engineering courses at the University of Tennessee. Currently it is a graphical Python app that requires all the players' programs to be local in order to execute, and currently supports up to 30 players.

The object of the game is to harvest more _fruit_ than any other player. Each player writes a program in an assembly-like language. Each program has access to shared memory where they can _plant_ and _harvest_ the fruit.

![Harvest Memory's GUI.](https://github.com/AZHenley/HarvestMemory/blob/master/screenshot.png "Havest Memory's GUI. The left shows player scores. The right shows the memory. Red is fruit.")


## Fruit

Fruits are represented in the memory by -100. _Harvesting_ a fruit will yield +5 to your current fruit score. Attempting to harvest a location that does not contain fruit will result in the CPU scheduler penalizing your program.

You may also _plant_ fruit. This will set the memory value to -1 and will automatically decrement 1 each CPU cycle. Once the value reaches -100, it becomes a harvestable fruit.

Fruit in memory can be destroyed by setting the value to any positive value.

All players start with 3 fruit.

The game begins with fruit randomly placed in the memory in groups. The groups are calculated based on an exponential decay function (e.g., 0.75^x where x is the initial memory location plus/minus an offset). This means that multiple fruit will likely be within 1-5 memory locations of each other, though they may be as far apart as 15.


## CPU Scheduler

The CPU uses a round-robin scheduling algorithm with a fairness constraint. At the start of the game, it shuffles all players randomly. It will proceed to execute 1 instruction per player. If the instruction takes more than 1 cycle (as most of them do), then that player's program will not execute again until all other players' programs have been provided at least the same number of cycles.

For example: if Player A takes 1 cycle on their turn and Player B takes 10 cycles on their turn, then Player B will be skipped until Player A has taken at least 9 more cycles (the delta between the cycles consumed on their respective turns).


## CPU Architecture

Registers, immediates, and memory values are unsigned 32-bit values. Memory addresses are 12-bit. You can **not** set a memory value to a negative value. Registers and immediates will wrap as expected. Memory values will wrap to a positive value. Memory addresses do not wrap.

The registers are:
* r0  - general purpose
* r1  - general purpose
* r2  - general purpose
* r3  - general purpose
* rs  - number of fruit you have (read-only)
* rw  - current winning score (read-only)
* rf  - error flag (read-only)... 0 for nothing, 1 for underflow register, 2 for overflow register, 3 for underflow memory, 4 for overflow memory, 5 for out of bounds memory, 6 for poking negative value to memory, 7 for undefined label, 8 for invalid plant, 9 for invalid harvest, 10 for misc invalid operand
* rt  - number of cycles elapsed since start of game (read-only) 


## Instruction set

The language allows 1 instruction or 1 label per line. A label takes the form: `main:`

Operands for instructions: 

* _a_ is a register/immediate that is used as an address
* _r_ is a register that is used as a destination
* _v_ is a register/immediate that is used as a value
* _l_ is a label
* _$_ is a prefix for _v_ used to fetch the value at that address

The instructions:

* harvest a
  * Harvests fruit at _a_.
  * Takes 5 cycles if there is fruit, 20 if not.
* plant a
  * Plants 1 of your fruits at _a_.
  * Takes 4 cycles.
* peek r, a
  * Copies value at _a_ to _r_.
  * Takes 4 cyles.
* poke a, v
  * Sets _a_ to _v_.
  Takes 3 cycles.
* goto l
  * Jumps to _l_.
  * Takes 1 cycle.
* ifequal v, v, l
  * If _v_<sub>1</sub> equals _v_<sub>2</sub> then jump to _l_.
  * Takes 2 cycles.
* ifless v, v, l
  * If _v_<sub>1</sub> is less than _v_<sub>2</sub> then jump to _l_.
  * Takes 2 cycles.
* ifmore v, v, l
  * If _v_<sub>1</sub> is greater than _v_<sub>2</sub> then jump to _l_.
  * Takes 2 cycles.
* add r, v, v
  * Sets _r_ to _v_<sub>1</sub> plus _v_<sub>2</sub>.
  * Takes 3 cycles.
* sub r, v, v
  * Sets _r_ to _v_<sub>1</sub> minus _v_<sub>2</sub>.
  * Takes 3 cycles.
* mult r, v, v
  * Sets _r_ to _v_<sub>1</sub> times _v_<sub>2</sub>.
  * Takes 5 cycles.
* div r, v, v
  * Sets _r_ to _v_<sub>1</sub> divided by _v_<sub>2</sub>.
  * Takes 8 cycles.
* mod r, v, v
  * Sets _r_ to the remainder of _v_<sub>1</sub> divided by _v_<sub>2</sub>.
  * Takes 7 cycles.
* random r, v, v
  * Sets _r_ to a random value between _v_<sub>1</sub> and _v_<sub>2</sub>, inclusive.
  * Takes 6 cycles.


## Example program

This program will check random locations for fruit. If it finds one, it harvests it.

    main:
        random r0, 0, 4095
        ifequal $r0, -100, found 
    found:
        harvest $r0
        goto main
