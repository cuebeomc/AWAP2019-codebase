# AWAP 2019 Design Document
Last updated 10/12/18

## Game overview

Our game this year is, in short, a TOC simulator. In order to accurately simulate the "feel" of TOC, the TOC simulator should be able to represent some of the key characteristics of a career fair. In particular, we want to emulate:
1. The hectic environment
  * This is perhaps the most important - we need to be able to emulate an environment where it's difficult for an individual to navigate through the floor of the fair and only being able to see maybe 5 feet around you.
2. The lack of time
  * Whenever someone goes to the TOC, they have to pick a small subset out of all the companies to go to, and sometimes, their goals change. Why? First, companies don't come all days (which will probably not be emulated), but also, lines get too long, and so students are unable to attend everything they wanted to go to. Thus, we want to simulate the need to plan and re-plan based on changing conditions inside the fair.
3. The actual point of a career fair
  * Career fairs are a way for students to, well, get careers. We want this to be our measure of success in the game; the more companies' interests align with the students, and vice versa, the student will do "better" at the career fair. (Obviously, there are many other factors, some of which we will include and some we will ignore.)

Thus, when designing our game, we should always keep these three points in mind - if our game diverges from these three core principles, we should take a step back to reevaluate.

## Software overview

We are aiming to write robust, object-oriented Python code that makes it easy for the central game to handle a large amount of state changes (100+ bots moving every time interval), yet have fast lookup to send partial information to the player. More will be described below on the proposed solution for the game. We also need to write robust server code to handle submissions, and possibly, be able to handle multiple REST calls from multiple teams concurrently. However, work on infrastructure will start around 4 weeks from now, when we (hopefully) start wrapping up our work on the game.

## Context

As most of you (should) know, this game will be the core infrastructure behind our competition in the spring, Algorithms with a Purpose. The event this year will take place on 2/2 in Rashid. (Specific times are TBD, will make as long/short as necessary.) Thus, this code, both for the game and for the server, **must** be robust. The server code is definitely more important in terms of robustness - it should have very little downtime, and it should be able to handle around 75-100 concurrent requests (As the competition nears the end, many teams will start trying to submit). Likewise, the game should also be robust - it should be able to handle malformed or buggy competitor code (although we would like to filter those out beforehand), and be able to support the high amount of state changes that each game will experience.

## Current progress

None. Check back later.

## Mechanics



## Proposed implementation

In order to implement the mechanics above, the code should have the following structure:

1. The board
  * The board should keep track of a m x n set of tiles, and it should implement a "step" function. For each step, the board should update each of the m x n tiles, each of which should have their own step function for the board to use.
  * Initialization should use a config file that we generate/create and initialize the m x n set of tiles by placing random companies into select zones. Afterwards, it should initialize the bots - note that we do not want them all entering the career fair (in other words, we don't want them near the entrance) once the game starts for the player. The board should already be hectic once the player starts the game.
