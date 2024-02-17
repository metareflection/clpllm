
# Michael's idea, or ideas on Michael's idea

Michael's suggestion was for a "reifier" to, at the end, create a fleshed-out story about the adumbrated pieces and facts (skeleton) that we produce from the search. The search should hopefully be able to, from what we've accumulated so far, add consistent pieces (like an "and then what happened" to the story, based upon what's come before).

Also, and this I had imagined as a different kind of constraint from the "continue the story" mode, but to generate particular details for a character, location that we ask for, based upon the information we know about it.

For a noun, pull all the information we know about that noun, and then ask for a something related to that noun. Job, house, outfit, transportation. Time

This isn't quite the CLP thing that I'd had in mind from before. But I think what we might be getting to is something where you could keep around the basic skeleton of the story, which takes up less context, and then you add onto it the kinda "literary fluff" detail things, and you can keep that outside of the main context, so you can do more interesting intricate story generation from "just the facts" POV.


# Route

Route sucks right now.

No wonder, b/c obv the wrong way to do it. The description of the problem does lots to


John takes 2*n steps. A circuit must be (u+l) + (d + r), in some sequence
u=d
r=l
u+d+r+l = number of steps, in some order.

John takes n+m steps up/left, and if it's to be a circuit, he must also take n steps down and m steps right. So we could represent that information compactly somehow.


 search being a different kind of mode than the


# Story shape

1. Setup
2. Tension
3. First resolution (calls to the same relation that does a twist)
4. Second tension
5. Final resolution

# story within a story : substory

sibling branches are different kinds of plot devices
child nodes next narrative arc

interesting check. 

;; https://en.wikipedia.org/wiki/The_Seven_Basic_Plots
;; Definition: An event forces the main character to change their ways and often become a better individual.
(defrel (rebirth text)
  (fresh (setup event)
    (== setup (gen "" "setup"))
    (== event (gen setup "tragic event"))
    (fresh (story-so-far)
      (appendo setup event story-so-far)
      (fresh (res)
        (== res (gen story-so-far "resolution"))
        (appendo story-so-far res text)))))

(defrel (story text)
  (conde
   [(overcoming-the-monster text)]
   [(rebirth text)]))

## DSL nicer

Make it so that you could "gen+append to existing"
Doing the recursion for subplots `(conde (change-ways) (become-better-individual))`
turn to a microKanrenesque pythonesque
more plots stories and different structures
IsInteresting checks to kill branches (other ways to prune?)
Role of the reifier (story shape that's consistent)->dialog, fully fleshed out scenes, etc.
Ping Evan Donahug?
Can GPT write a better story w/our help or by itself.
(And by what metric?? Have it assess itself vs our?)
