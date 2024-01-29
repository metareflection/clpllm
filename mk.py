import llm


def var(vname, n):
    return vname + "#" + str(n)


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


def callFresh(vname, f):
    def inner(s_c):
        c = s_c[1]
        new_var = var(vname, c)
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
                             callFresh("z", lambda z:
                                       conj(
                                           sentence(
                                               "".join(
                                                   [x, " is the parent of ", z, "."])),
                                           ancestor(z, y))))(s_c)]
    return goal


def appendo(x, y, z):
    def goal(s_c):
        return [lambda: disj(conj(sentence("".join([x, " is an empty list"])),
                                  sentence("".join([y, " is the same as ", z, "."]))),
                             callFresh("a",
                                       lambda a: callFresh("d",
                                                           lambda d: conj(sentence("".join([x, " is a pair consisting of ", a, " and ", d,  " ."])),
                                                                          callFresh("res", lambda res: conj(sentence("".join([z, " is a pair consisting of ", a, " and ", res,  " ."])),
                                                                                                                      appendo(d, y, res)))))))(s_c)]
    return goal


# Does not seem to work super duper well right now.
def route():
    def goal(s_c):
        return [lambda:
                disj(sentence("You stop here"),
                     conj(disj(sentence("You next go one block to the right, but do not stop yet."),
                               disj(sentence("You next go one block to the left, but do not stop yet."),
                                    disj(sentence("You next go one block up, but do not stop yet."),
                                         sentence("You next go one block down, but do not stop yet.")))),
                          route()))(s_c)]
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
              ("x", lambda x: conj(disj(
                                  sentence("I love bananas."),
                                  sentence("I love apples.")),
                              sentence("I don't like fruits.")))))
    # []
    print(run(2, callFresh
              ("x", lambda x: conj(disj(
                                  sentence(("".join(["I love ", x, " ."]))),
                                  sentence("I love apples.")),
                              sentence("".join(["I don't like ", x, " ."]))))))
    # [(" I love apples. I don't like x#0 .", 1)]
    print(run(2, callFresh
              ("x", lambda x: conj(disj(
                                  sentence(
                                      ("".join(["I love ", x, " ."]))),
                                  sentence("I love apples.")),
                              callFresh
                              ("x", lambda x:
                               sentence(
                                   "".join(["I don't like ", x, " ."]
                                           )))))))
    # [(" I love x#0 . I don't like x#1 .", 2), (" I love apples. I don't like x#1 .", 2)]
    print(run(3, test("John")))
    # [(' My favorite food are pomegranates', 0)]
    print(run(3, callFresh("x", lambda x: callFresh("y", lambda y: ancestor("John", "Kathy")))))
    # [(' John is the parent of Kathy.', 2),
    #  (' John is the parent of z#2. z#2 is the parent of Kathy.', 3),
    #  (' John is the parent of z#2. z#2 is the parent of z#3. z#3 is the parent of Kathy.', 4)]
    print(run(3, callFresh("x", lambda x: callFresh("y", lambda y: ancestor(x, "Kathy")))))
    # [(' x#0 is the parent of Kathy.', 2),
    #  (' x#0 is the parent of z#2. z#2 is the parent of Kathy.', 3),
    #  (' x#0 is the parent of z#2. z#2 is the parent of z#3. z#3 is the parent of Kathy.', 4)]
    print(run(10, callFresh("x", lambda x: callFresh("y", lambda y: appendo(x, y, "cons(p, cons(q, cons(r, nil)))")))))
    # [(' x#0 is an empty list y#1 is the same as cons(p, cons(q, cons(r, nil))).', 2),
    #  (' x#0 is a pair consisting of a#2 and d#3 . cons(p, cons(q, cons(r, nil))) is a pair consisting of a#2 and res#4 . d#3 is an empty list y#1 is the same as res#4.', 5),
    #  (' x#0 is a pair consisting of a#2 and d#3 . cons(p, cons(q, cons(r, nil))) is a pair consisting of a#2 and res#4 . d#3 is a pair consisting of a#5 and d#6 . res#4 is a pair consisting of a#5 and res#7 . d#6 is an empty list y#1 is the same as res#7.', 8),
    #  (' x#0 is a pair consisting of a#2 and d#3 . cons(p, cons(q, cons(r, nil))) is a pair consisting of a#2 and res#4 . d#3 is a pair consisting of a#5 and d#6 . res#4 is a pair consisting of a#5 and res#7 . d#6 is a pair consisting of a#8 and d#9 . res#7 is a pair consisting of a#8 and res#10 . d#9 is an empty list y#1 is the same as res#10.', 11)]
    print(run(1,conj(sentence("John always fulfils his obligations."),
                     conj(sentence("John must attend all meetings he knows of."),
                          conj(sentence("There are no meetings for the next three days."),
                               sentence("John just began a mandatory three day leave where he will be unavailable for meetings."))))))
    # [(' John always fulfils his obligations. John must attend all meetings he knows of. There are no meetings for the next three days. John just began a mandatory three day leave where he will be unavailable for meetings.', 0)]
    print(run(1,conj(sentence("John always fulfils his obligations."),
                     conj(sentence("John must attend all meetings he knows of."),
                          conj(sentence("John just began a mandatory three day leave where he will be unavailable for meetings."),
                               conj(sentence("John learned yesterday about an upcoming meeting's time and place."),
                                    sentence("The meeting is scheduled for tomorrow.")))))))
    # []
    print(run(6,conj(sentence("You are in a city with a grid layout. You must end your walk at the same place you start. You start your walk."), route())))
    # Bad behavior. Doesn't work on this one. Maybe better prompting w/constraints?
