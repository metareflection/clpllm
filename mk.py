import llm


def var(n):
    return str(n)


def callFresh(f):
    def inner(s_c):
        c = s_c[1]
        new_var = var(c)
        new_state = (s_c[0], c + 1)
        return f(new_var)(new_state)
    return inner


def conj(goal1, goal2):
    def goal3(state):
        return [s2 for s in goal1(state) for s2 in goal2(s)]
    return goal3


def disj(goal1, goal2):
    def goal3(state):
        return goal1(state) + goal2(state)
    return goal3


def sentence(x):
    def goal(s_c):
        new_state = s_c[0] + " " + x
        if llm.constraint(new_state):
            return [(new_state, s_c[1])]
        else:
            return []
    return goal


def run(goal):
    return goal(("", 0))


if __name__ == '__main__':
    print(run(sentence("I love bananas.")))
    # [' I love bananas.']
    print(run(conj(
        sentence("I love bananas."),
        sentence("I don't love bananas."))))
    # []
    print(run(disj(
        sentence("I love bananas."),
        sentence("I don't love bananas."))))
    # [' I love bananas.', " I don't love bananas."]
    print(run(disj(
        conj(
            sentence("I love bananas."),
            sentence("I love apples.")),
        sentence("I don't like fruits."))))
    # [' I love bananas. I love apples.', " I don't like fruits."]
    print(run(conj(
        disj(
            sentence("I love bananas."),
            sentence("I love apples.")),
        sentence("I don't like fruits."))))
    # []
    print(run(callFresh
              (lambda x: conj(disj(
                                  sentence("I love bananas."),
                                  sentence("I love apples.")),
                              sentence("I don't like fruits.")))))
    # []
    print(run(callFresh
              (lambda x: conj(disj(
                                  sentence(("".join(["I love ", "x#", x, " ."]))),
                                  sentence("I love apples.")),
                              sentence("".join(["I don't like ", "x#", x, " ."]))))))
    # [(" I love apples. I don't like x#0 .", 1)]
