from langchain_community.llms import Ollama

ollama = Ollama(model='constraint_solver')

constraints = ["""John always fulfils his obligations.
             John must attend all meetings he knows of.
             John just began a mandatory three day leave where he will be unavailable for meetings.
             John learned yesterday about an upcoming meeting's time and place.
             The meeting is scheduled for tomorrow.""",

             """I like apples.
             I like bananas
             I like to travel"""]

QandAs = {}

def constraint_solver(list_of_constraints):
    for constraint in list_of_constraints:
        QandAs[constraint] = ollama.invoke(constraint)

constraint_solver(constraints)

print(QandAs)
