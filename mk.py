import llm

def conj(goal1, goal2):
    def goal3(state):
        return [s2 for s in goal1(state) for s2 in goal2(s) ]
    return goal3

def disj(goal1, goal2):
    def goal3(state):
        return goal1(state) + goal2(state)
    return goal3

def sentence(x):
    def goal(state):
        new_state = state + " " + x
        if llm.constraint(new_state):
            return [new_state]
        else:
            return []
    return goal

def run(goal):
    return goal("")

if __name__ == '__main__':
    print(run(sentence("I love bananas.")))
    print(run(conj(
        sentence("I love bananas."),
        sentence("I don't love bananas."))))
    print(run(disj(
        sentence("I love bananas."),
        sentence("I don't love bananas."))))
    print(run(disj(
        conj(
            sentence("I love bananas."),
            sentence("I love apples.")),
        sentence("I don't like fruits."))))
    print(run(conj(
        disj(
            sentence("I love bananas."),
            sentence("I love apples.")),
        sentence("I don't like fruits."))))
