---
layout: default
title: "16. Game Theory"
parent: Lecture Notes
nav_order: 16
---

# Game Theory
{: .no_toc }

- TOC
{:toc}

## What is game theory?

Game theory is a branch of economics and mathematics that studies strategic interactions.
It has many applications in business, politics, warfare, sports and entertainment, and 
even computer networking.

The formal mathematical foundations of game theory were largely developed in the aftermath
of World War 2. The prospect of nuclear war made the study of strategic interactions 
vital for global security.

## General setup

Every game consists of three components:

- The players: $$i = 1, \ldots, N$$

- For each player $$i$$, a set of strategies: $$\mathbb{S}_i$$

- For each player $$i$$, a mapping from the strategies chosen by *all* players to player $$i$$'s payoff or utility: $$ u_i(s_1, \ldots, s_N) $$

## Normal form

Two player games can be represented using a diagram known as the game's **normal form**. This is a table where you put the possible strategies of player 1 
on the rows and you put the possible strategies of player 2 on the columns.

In each cell of the table, you write the payoffs that each player gets from that combination of strategies, in the following form:

$$
\text{Utility of player 1, Utility of player 2}
$$

Normal forms of a 2-player game will therefore always look like this:

{: .blue-callout-title }
> Example
>
> The Prisoner's Dilemma is a game that goes like this. There are two suspects of a crime, for which the maximum sentence is 10 years.
> The police put the suspects into separate rooms and try to get them to snitch on each other.
> Each suspect can either snitch or not snitch. 
> 
> - If neither suspect snitches, the police only have enough evidence to convict each suspect for 4 years (6 years avoided.)
> - If both suspects snitch, they are both found guilty but the police let them have 2 years off for snitching (2 years avoided.)
> - If one suspect snitches but the other doesn't, the one who snitches is found innocent (10 years avoided) while the one who didn't snitch gets the maximum sentence (0 years avoided).
>
> Draw the normal form of the game, where the payoffs are measured in years of jail avoided.
>
> *Answer.*
>
> <table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Suspect 2</td></tr><tr><td></td><td></td><td align="center">Snitch</td><td align="center">No Snitch</td></tr><tr><td rowspan=2>Suspect 1</td><td>Snitch</td><td align="center">2, 2</td><td align="center">10, 0</td></tr><tr><td>No Snitch</td><td align="center">0, 10</td><td align="center">6, 6</td></tr></table>


## Optimization problem

Players seek to maximize their utility by choosing their own strategy $$s_i$$, taking the strategies of each other player, 
$$s_1, \ldots, s_{i-1}, s_{i+1}, \ldots, s_N$$, as given.

As a useful notation, we define $$s_{-i}$$ as the strategies chosen by all players *other than* $$i$$:

$$
s_{-i} = s_1, s_2, \ldots, s_{i-1}, s_{i+1}, \ldots, s_N
$$

With this notation, we can write player $$i$$'s payoff from choosing $$s_i$$ when the other players are playing $$s_{-i}$$ as $$u_i(s_i, s_{-i})$$. 

Player $$i$$'s optimization problem is therefore:

$$
\max_{s_i \in \mathbb{S}_i} ~ u_i (s_i, s_{-i}) ~ \text{taking} ~ s_{-i} ~ \text{as given}
$$

## Best response function

In game theory, a person's optimal choice depends on the choices that other players are making. 
The optimal choice is therefore *dependent* on $$s_{-i}$$. 

We call player $$i$$'s best choice when other players are playing $$s_{-i}$$ as **player $$i$$'s best response to $$s_{-i}$$**.

Formally, the best response function $$b_i(s_{-i})$$, is defined as:

$$
b_i(s_{-i}) = \arg \max_{s_i \in \mathbb{S}_i} ~ u_i (s_i, s_{-i})
$$

In other words, the best response is simply the solution to the optimization problem above. The best response is a function because it depends on what the other players are playing.

{: .green-callout-title }
> Example
>
> Consider the normal form of the Prisoner's Dilemma:
>
> <table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Suspect 2</td></tr><tr><td></td><td></td><td align="center">Snitch</td><td align="center">No Snitch</td></tr><tr><td rowspan=2>Suspect 1</td><td>Snitch</td><td align="center">2, 2</td><td align="center">10, 0</td></tr><tr><td>No Snitch</td><td align="center">0, 10</td><td align="center">6, 6</td></tr></table>
>
> 1. What is Suspect 1's best response to Suspect 2 snitching?
> 2. What is Suspect 1's best response to Suspect 2 not snitching?
> 3. What is Suspect 2's best response to Suspect 1 snitching?
> 4. What is Suspect 2's best response to Suspect 1 not snitching?
>
> *Answer.*
>
> 1. Snitch
> 2. Snitch
> 3. Snitch
> 4. Snitch
>
> It's often useful to "circle" the best response for each player in each situation. That would result in the table below:
>
> <table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Suspect 2</td></tr><tr><td></td><td></td><td align="center">Snitch</td><td align="center">No Snitch</td></tr><tr><td rowspan=2>Suspect 1</td><td>Snitch</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">2</span>, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">2</span></td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">10</span>, 0</td></tr><tr><td>No Snitch</td><td align="center">0, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">10</span></td><td align="center">6, 6</td></tr></table>

## Nash Equilibrium

A collection of strategies, one for each player, $$s^\ast = (s_1^\ast, \ldots, s_N^\ast)$$, is called a **Nash Equilibrium** if they are **mutual best responses**.
That is, if:

$$s_i^\ast = b_i(s_{-i}^\ast) ~ \forall ~ i = 1, \ldots, N$$

A Nash equilibrium characterizes a situation with *strategic stability*. 

- In a non-Nash equilibrium, one or more players have an incentive to change their strategy. We therefore aren't likely to observe non-Nash equilibria in games with experienced players.

- In a Nash equilibrium, no individual player has an incentive to change their strategy. We therefore *are* likely to observe Nash equilibria as the outcome in games with experienced players.

{: .purple-callout-title }
> Economic Insight
>
> We can use Nash equilibria to make predictions about the outcomes of games, because non-Nash equilibria are unlikely to occur in games that are played many times or played by experienced players.

{: .yellow-callout-title }
> Example
>
> What is(are) the Nash equilibria of the Prisoner's Dilemma?
>
> *Answer.*
>
> The normal form with circled best responses looks like this:
>
> <table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Suspect 2</td></tr><tr><td></td><td></td><td align="center">Snitch</td><td align="center">No Snitch</td></tr><tr><td rowspan=2>Suspect 1</td><td>Snitch</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">2</span>, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">2</span></td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">10</span>, 0</td></tr><tr><td>No Snitch</td><td align="center">0, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">10</span></td><td align="center">6, 6</td></tr></table>
>
> In a normal form with circled best responses, Nash equilibria will be the table cells with both choices circled. There is therefore one Nash equilibrium in the Prisoner's Dilemma, and that's the outcome where both suspects snitch.

## Prisoner's Dilemma

The Prisoner's Dilemma has an interesting result. In the Nash equilibrium, both suspects snitch and only manage to avoid 2 years in prison. However, they would have been better off if neither nad snitched. Then they'd each avoid 6 years in prison.

Why isn't it a Nash equilibrium for both suspects to not snitch? Because if the other suspect has chosen not to snitch, you can avoid prison entirely by snitching. The outcome of (No Snitch, No Snitch) is therefore not Nash.

The Prisoner's Dilemma illustrates strategic situations in which both players would be better off if they could somehow commit to cooperating with each other, but they can't actually commit to doing so.  Cooperation is rendered impossible because of the incentives: if everyone else is choosing to cooperate, you still have an incentive to defect.

Real life examples of Prisoner's Dilemmas include:

- Nuclear arms race
- Clickbait in advertising
- Political attack ads
- Tragedy of the Commons
- Price wars 

{: .purple-callout-title }
> Note
>
> In our simple Prisoner's Dilemma, the suspects cannot cooperate because there's no threat of punishment for the suspect who snitches. (They play the game once, and that's it.) If, however, the suspects could interact again in the future, then the possibility for punishment arises. If we extended the game theoretic analysis to account for potential future actions, we would find that cooperation can potentially be sustained via the threat of future punishment.

## Stag Hunt

There are two hunters who independently must decide whether to hunt for a stag or for a rabbit. 

- If both hunters choose to hunt the stag, they capture the stag and each get 4 utility.
- If both hunters go for the rabbit, they each get a rabbit and get 1 utility.
- If one hunter goes for the stag and one for the rabbit, the hunter who went for the stag fails and gets 0 utility. The hunter who went for the rabbit still gets a rabbit and gets 1 utility.

The normal form of the game is:

<table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Hunter 2</td></tr><tr><td></td><td></td><td align="center">Stag</td><td align="center">Rabbit</td></tr><tr><td rowspan=2>Hunter 1</td><td>Stag</td><td align="center">4, 4</td><td align="center">0, 1</td></tr><tr><td>Rabbit</td><td align="center">1, 0</td><td align="center">1, 1</td></tr></table>

If we circle best responses we get:

<table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Hunter 2</td></tr><tr><td></td><td></td><td align="center">Stag</td><td align="center">Rabbit</td></tr><tr><td rowspan=2>Hunter 1</td><td>Stag</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">4</span>, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">4</span></td><td align="center">0, 1</td></tr><tr><td>Rabbit</td><td align="center">1, 0</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span>, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span></td></tr></table>

There are therefore two Nash equilibria: (Stag, Stag) and (Rabbit, Rabbit).

The Stag Hunt, also sometimes called a **coordination game**, illustrates strategic situations in which cooperation is a Nash equilibrium, but so is non-cooperation.

It differs from the Prisoner's Dilemma in that if everyone is cooperating in the Stag Hunt, then everyone else wants to cooperate. But if someone defects in the Stag Hunt, then everyone else will also want to defect.

It therefore illustrates situations where the players can get "stuck" in a bad equilibrium, i.e. a vicious cycle of non-cooperation. The only way to move from the "bad" equilibrium to the "good" equilibrium is to move together as a group, which requires coordination.

Real life examples of coordination games include:

- Electric vehicle and charging station adoption
- Group projects

Because Stag Hunt-like situations require coordination (i.e. leadership), we sometimes observe government take the lead in moving society towards the better equilibrium. This is one of the arguments for electric vehicle subsidies.

## Chicken

There are two teenagers who drive their cars straight at each other. At the last minute, the teens can choose to swerve or keep going.

- If both teens swerve, nothing happens and they get 0 utility.
- If both teens keep going, they crash and get -10 utility.
- If one teen keeps going while the other one swerves, the one who kept going wins prestige worth 5 utility. The one who swerved is called a chicken and gets -5 utility.

The normal form of the game is:

<table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Teen 2</td></tr><tr><td></td><td></td><td align="center">Go</td><td align="center">Swerve</td></tr><tr><td rowspan=2>Teen 1</td><td>Go</td><td align="center">-10, -10</td><td align="center">5, -5</td></tr><tr><td>Swerve</td><td align="center">-5, 5</td><td align="center">0, 0</td></tr></table>

And with circled best responses:

<table border=1px align="center"><tr><td></td><td></td><td colspan=2 align="center">Teen 2</td></tr><tr><td></td><td></td><td align="center">Go</td><td align="center">Swerve</td></tr><tr><td rowspan=2>Teen 1</td><td>Go</td><td align="center">-10, -10</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">5</span>, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">-5</span></td></tr><tr><td>Swerve</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">-5</span>, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">5</span></td><td align="center">0, 0</td></tr></table>

There are two Nash equilibria: (Go, Swerve) and (Swerve, Go).

Like the Stag Hunt, there are two Nash equilibria. Unlike the Stag Hunt, there isn't a "good" or a "bad" equilibrium. Rather, each player prefers a different Nash equilibrium.

Chicken illustrates strategic situations where neither side wants to compromise, but if no one compromises then something even worse is going to happen. Examples of chicken in real life include:

- Feuding sports stars
- Congressional brinksmanship
- Apologizing after a fight

Games of chicken can be exciting and explosive because each side has an incentive to wait until the last minute to compromise, if at all. And if neither side compromises, disastrous results could occur, leading to a tense situation. For this reason, you'll often see games of Chicken in the plots of movies and TV shows.

## Rock Paper Scissors

We all know the game of Rock Paper Scissors. Let the utility of a win be 1, the utility of a loss be -1, and the utility of a tie be 0.

The normal form of the game is:

<table border=1px align="center"><tr><td></td><td></td><td colspan=3 align="center">Player 2</td></tr><tr><td></td><td></td><td align="center">Rock</td><td align="center">Paper</td><td align="center">Scissors</td></tr><tr><td rowspan=3>Player 1</td><td>Rock</td><td align="center">0, 0</td><td align="center">-1, 1</td><td align="center">1, -1</td></tr><tr><td>Paper</td><td align="center">1, -1</td><td align="center">0, 0</td><td align="center">-1, 1</td></tr><tr><td>Scissors</td><td align="center">-1, 1</td><td align="center">1, -1</td><td align="center">0, 0</td></tr></table>

With circled best responses:

<table border=1px align="center"><tr><td></td><td></td><td colspan=3 align="center">Player 2</td></tr><tr><td></td><td></td><td align="center">Rock</td><td align="center">Paper</td><td align="center">Scissors</td></tr><tr><td rowspan=3>Player 1</td><td>Rock</td><td align="center">0, 0</td><td align="center">-1, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span></td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span>, -1</td></tr><tr><td>Paper</td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span>, -1</td><td align="center">0, 0</td><td align="center">-1, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span></td></tr><tr><td>Scissors</td><td align="center">-1, <span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span></td><td align="center"><span style="border-width:2px; border-style:solid; border-color:#FF0000;">1</span>, -1</td><td align="center">0, 0</td></tr></table>

Rock Paper Scissors has **no** Nash equilibria. In other words, there is no stable outcome. Whatever the outcome of the game, one of the players has an incentive to make a different choice.

You often see Rock Paper Scissors-like mechanics in games made for entertainment. This is because the lack of strategic stability is a feature, not a bug, when it comes to entertainment. The lack of stability makes the games unpredictable, and a psychological element becomes important as both sides need to try and guess what the other side is going to do.

Examples of Rock Paper Scissors in real life include:

- Penalty kicks in soccer
- Run vs. pass offense in football
- Counterpicking in video games













