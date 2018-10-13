# AWAP 2019 Design Document
Last updated 10/13/18, v1.0

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

## Game mechanics

The player will get to control one main bot and 3 friend bots. The four bots will be referred to as a team. Each team has their own list of preferences; they'll have x big companies they like, y medium-size companies they like, and z small companies they like. The team will get more points for prioritizing these companies. The team is there for the main bot, and so there will be a penalty if a friend bot converses with the recruiter on behalf of the team.

The player will be placed into a map similar to that of Wiegand Gym or Rangos, and we will simulate the hectic feel of the TOC by using a lot of bots. These should not be explicitly random in their movements, but they should have long-cycling deterministic algorithms that make it difficult for the player to predict their movement. Also, bots should also have preferences and agendas - they might have a strategy of going to every short line for the swag (swag, unfortunately, will not be implemented), or they might just go to every big company because they think they have a chance.

The map itself will consist of zones where companies will be placed - however, each zone will be allocated to a certain size of a company. The motivation behind the zoning strategy is to introduce some level of RNG and unpredictability to the game, but reduce the unfairness of such RNG. For example, if one team prefers Apple and Facebook, while another team prefers Facebook and Google, yet Apple and Facebook are in one corner and Google is in the other corner, the second team is at a severe disadvantage, especially considering that movement is meant to be a pain in this game. Thus, we zone areas and have them contain all big companies, for example, to reduce some level of unfairness to the game.

We will be using a tile system for this game. Although we thought about the idea of using hitboxes/collision system for movement, we decided that would be too difficult for our development timeline. Thus, we opted for a tile system, where the map is separated into discrete areas.

Movement will be heavily dependent on the crowd. If there are no people on the tile where a bot is trying to go, it will take a very short time to get there. However, if there are a lot of people, it should take more time. Because we are working with a tile system, we need a way to simulate the difficulty of getting from one location to the next. To achieve this goal, we add movement penalties to get from one tile to the next based on the number of people in the next tile. The more people, the slower it takes, and the slower the movement progresses.

## Proposed implementation

In order to implement the mechanics above, the code should have the following structure:

1. The board
    * The board should keep track of a m x n set of tiles in a graph, and it should implement a "step" function. For each step, the board should update each of the m x n tiles, each of which should have their own step function for the board to use.
    * Initialization should use a config file that we generate/create and initialize the m x n set of tiles that are either empty, are a line for a booth, or contain booths. Config files should indicate where a booth can go and should create zones for different sizes of companies. For each company, it should also create line zones for each recruiter in the company. Afterwards, it should initialize the bots - note that we do not want them all entering the career fair (in other words, we don't want them near the entrance) once the game starts for the player. The board should already be hectic once the player starts the game.
    * Since the board will be a graph, we have the option of adding weights onto the edges of the graph to indicate the amount of time it will take for a bot to get from one tile to the other, or we can calculate every time a bot starts to move into a tile. However, the second option is computationally inefficient once we have multiple bots in a tile, and so we should also have a function to update the weights every step to make sure movement penalties get updated with the number of people on a tile.
2. The tiles
    * Each tile should either be part of a booth (in which case it should have no one on it), have a line for a booth, or be empty. For the first two cases, it should also have the name of the booth that it is a line for/part of. If it is a line, it should have a boolean whether or not the tile is the end of the current line. If it's empty, it should not keep track of any company data.
    * A tile should keep track of the bots on the tile (and their movement progress to another tile, if moving) and the number of bots standing in line and their position (if the tile is in a line zone). The tile should have a step function that uses the bots' step function, or if the bots decide to do nothing, automatically progresses their movement or updates their position in the line.
3. The bots
    * The bot class should contain a step function as well, and their objects should be kept in the tile. Implementation of these is up to the Bot/AI team.
4. The player(s)
    * The players will be modeled as bots - however, they will have more information about which team they're on (since this is a competition between two teams), as well as which bot is the main bot. However, **code for the player will not be stored in the bot class**. They will be modeled as bots in the graph, but they will have no code behind them - instead, we will have competitors write code in a separate class that will pass their decisions to the step function. The step function will then pass down the information to the placeholder bots, where the information will update the placeholder bot's line status, movement progress, etc. We will provide boilerplate code that allows them to play the game locally (pass decisions to the boards' step function) or play the game on our servers (send REST calls with information to play the game on our server). The code that we will provide will be more fleshed out in this document later down the line.
