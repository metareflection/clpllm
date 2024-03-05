-*- mode: org -*-

* LLM is the solver for partially ground constraints (basically skolem constants in the constraints themselves).

* What remains is the role for: 
- search
- backtracking
- logic variables

* Reifier
Michael's suggestion was employ the LLM in (also in) the reifier; have
it /generate/ values for the variables in the output (for instance in
a story), like it's solving a Mad Lib.

* filler-inner
A complementary idea is to have the LLM generate the story /skeleton/,
and then iteratively ask the LLM to fill in passages and scenes as it
goes. 

Step 1. Get completed story skeleton
Step 2. Create passages consistent w/this part and full story context.
[CLP doesn't show up much in this part, it'd be in the first].

* Story skeleton.

Why would you want CLP or search for something like this. Actual
stories don't have that fractal shape to them. 

**Episodic stories 

Episodic stories go sequence by sequence (Harman cycle)

These don't have an arbitrarily deep 2nd direction, though.

*** Hero's journey cycle
The Ordinary World: the hero is seen in their everyday life
The Call to Adventure: the initiating incident of the story
Refusal of the Call: the hero experiences some hesitation to answer the call
Meeting with the Mentor: the hero gains the supplies, knowledge, and confidence needed to commence the adventure
Crossing the First Threshold: the hero commits wholeheartedly to the adventure
Tests, Allies, and Enemies: the hero explores the special world, faces trial, and makes friends and enemies
Approach to the Innermost Cave: the hero nears the center of the story and the special world
The Ordeal: the hero faces the greatest challenge yet and experiences death and rebirth
Reward: the hero experiences the consequences of surviving death
The Road Back: the hero returns to the ordinary world or continues to an ultimate destination
The Resurrection: the hero experiences a final moment of death and rebirth so they are pure when they reenter the ordinary world
Return with the Elixir: the hero returns with something to improve the ordinary world

*** Harman Episodic Circle
A character is in a zone of comfort or familiarity.
They desire something.
They enter an unfamiliar situation.
They adapt to that situation.
They get that which they wanted.
They pay a heavy price for it.
They return to their familiar situation.
They have changed as a result of the journey.

*** Episodic stories with story-in-story components

Maybe each would need an order of magnitude more "interest/excitement**
threshhold in order to allow to go that direction :/

I'm not sure I see the benefit of going that direction. 

*** Meta: Narratology isn't our area of expertise, feels out on a limb here.

* I was thinking what about natural language versions of legal, ethical, etc

** Useful if it's better for LLM to just straight constraint solve on nat.lang.text as is rather than 2-step (encode as facts, then LP over**.

Encoding fancy logics and constraints *is* a difficult problem, and can require whole-system re-encoding. 

*** Scheduling?

You get the schedules as text messages, it's your job now to make sure
that every shift has 2 people, that it's consistent with each person's
shift.

*** Not clear though that Prolog-style LP is the best approach?
- Funlog
- Datalog
- Arntzenius-log
- ASP

** I don't like the *is-interesting*** check as we came up with it

I suspect something w/a maximization function and usual AI backjumping
kinda stuff will be more effective, if that's the technique.

Large enough the LLM cannot by itself keep track, and you'd need to
break up the problem. 

* LP *is* generate-and-test

At it's heart LP is a search based generation system, the conceit is
that you can improve the behavior and augment the search with known
data.

** Imptly, benefits from partial knowledge to specialize.
When you have some thing that you're aware of, maybe the equivalent of
desired skolem constants for variables, or better some partial
structure, and you want to help fill in the rest of it.

** A tad bit of promise:

https://en.wikipedia.org/wiki/The_Thirty-Six_Dramatic_Situations

These tell you what elements you *need* to have already for the
situation to manifest, and then a rough description of what happens.

** Difficulty

- One scene can resolve multiple narrative arcs, e.g Gift of Magi
- Some may be left unresolved at the end, e.g. Lady or Tiger
- Not clear there's a general tool to extract from movie, episodic tv, folk tale, short story, novel + genres

** Semi-structured?

MUD style directions and places
choose-your-own-adventure

*** (Are these now strictly dominated by full open-ended storytelling improv D&D style?)
D&D is manual LLM improv w/dice for randomness.





* Route

Route sucks right now.

No wonder, b/c obv the wrong way to do it. The description of the
problem does lots to


John takes 2*n steps. A circuit must be (u+l) + (d + r), in some
sequence

u=d
r=l

u+d+r+l = number of steps, in some order.

John takes n+m steps up/left, and if it's to be a circuit, he must
also take n steps down and m steps right. So we could represent that
information compactly somehow.

