import llm


def var(n):
    return str(n)


def stream_append(stream1, stream2):
    if stream1 == []:
        return stream2
    else:
        head = stream1[0]
        tail = stream1[1:]
        # If the tail is a lambda, wrap it in a list
        if tail == [] and callable(head):
            return [lambda: stream_append(head(), stream2)]
        else:
            # Regular concatenation
            return [head] + stream_append(tail, stream2)


def stream_append_map(stream, g):
    if stream == []:
        return []
    else:
        head = stream[0]
        tail = stream[1:]
        if tail == [] and callable(head):
            return [lambda: stream_append_map(head(), g)]
        else:
            # Regular concatenation
            return stream_append(g(head), stream_append_map(tail, g))


def callFresh(f):
    def inner(s_c):
        c = s_c[1]
        new_var = var(c)
        new_state = (s_c[0], c + 1)
        return f(new_var)(new_state)
    return inner


def conj(goal1, goal2):
    def goal3(state):
        return stream_append_map(goal1(state), goal2)
    return goal3


def disj(goal1, goal2):
    def goal3(state):
        return stream_append(goal1(state), goal2(state))
    return goal3


def sentence(x):
    def goal(s_c):
        new_state = s_c[0] + " " + x
        if llm.constraint(new_state):
            return [(new_state, s_c[1])]
        else:
            return []
    return goal


def take(n, stream):
    if n <= 0 or stream == []:
        return []
    else:
        head = stream[0]
        tail = stream[1:]
        # If the tail is a lambda, wrap it in a list
        if tail == [] and callable(head):
            return take(n, head())
        else:
            return [head] + take(n - 1, tail)


def run(n, goal):
    return take(n, goal(("", 0)))


def test(x):
    def goal(s_c):
        return [lambda: sentence("My favorite food are pomegranates")(s_c)]
    return goal


def ancestor(x, y):
    def goal(s_c):
        return [lambda: disj(sentence("".join([x, " is the parent of ", y, "."])),
                             callFresh(lambda z:
                                       conj(
                                           sentence(
                                               "".join(
                                                   [x, " is the parent of ", z, "."])),
                                           ancestor(z, y))))(s_c)]
    return goal


if __name__ == '__main__':
    print(run(1, sentence("I love bananas.")))
    # [' I love bananas.']
    print(run(1, conj(
        sentence("I love bananas."),
        sentence("I don't love bananas."))))
    # []
    print(run(2, disj(
        sentence("I love bananas."),
        sentence("I don't love bananas."))))
    # [' I love bananas.', " I don't love bananas."]
    print(run(2, disj(
        conj(
            sentence("I love bananas."),
            sentence("I love apples.")),
        sentence("I don't like fruits."))))
    # [' I love bananas. I love apples.', " I don't like fruits."]
    print(run(2, conj(
        disj(
            sentence("I love bananas."),
            sentence("I love apples.")),
        sentence("I don't like fruits."))))
    # []
    print(run(2, callFresh
              (lambda x: conj(disj(
                                  sentence("I love bananas."),
                                  sentence("I love apples.")),
                              sentence("I don't like fruits.")))))
    # []
    print(run(2, callFresh
              (lambda x: conj(disj(
                                  sentence(("".join(["I love ", "x#", x, " ."]))),
                                  sentence("I love apples.")),
                              sentence("".join(["I don't like ", "x#", x, " ."]))))))
    # [(" I love apples. I don't like x#0 .", 1)]
    print(run(2, callFresh
              (lambda x: conj(disj(
                                  sentence(
                                      ("".join(["I love ", "x#", x, " ."]))),
                                  sentence("I love apples.")),
                              callFresh
                              (lambda x:
                               sentence(
                                   "".join(["I don't like ", "x#", x, " ."]
                                           )))))))
    # [(" I love x#0 . I don't like x#1 .", 2), (" I love apples. I don't like x#1 .", 2)]
    print(run(3, test("John")))
    # [(' My favorite food are pomegranates', 0)]
    print(run(3, callFresh(lambda x: callFresh(lambda y: ancestor("John", "Kathy")))))
    # [(' John is the parent of Kathy.', 2), (' John is the parent of 2. 2 is the parent of Kathy.', 3), (' John is the parent of 2. 2 is the parent of 3. 3 is the parent of Kathy.', 4)]
