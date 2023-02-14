# Goal

## High level inputs and outputs

- Input:
    1. a list of rules
    2. a problem stated with the language of the rules
    3. Optional: the quest to prove
- Output:
    1. the fixed point, i.e., all the facts that can be deducted with the provided problem and rules
    2. if the quest is given, return whether the quest can be proved


## Algorithm

Data-driven Forward chaining

1. Maintain NEW_FACTS_LIST and DATABASE, and initialize both of them to be the list of hypotheses
2. Pop the first fact/predicate `d` from NEW_FACTS_LIST
    1. Fetch rules based on the type of the fact/predicate
    2. Apply rules, obtain new fact `d'`
    3. Insert `d'` into the DATABASE
    4. IF `d'` is not in the NEWFACTSLIST, attach it to the list
3. Continue step 2 until the NEWFACTSLIST is empty


Structure of DATABASE

1. coll
2. eqangle
3. para


## Implementation

Class: Predicate
    '''Predicate is simple fact, such as coll(A,B,C) or para(A,B,C,D)
    where A,B,C,D are concrete points.

    Predicate will mostly be used when parsing the input hypotheses.
    '''
    def from_line(cls, line: str)

    @property
    def type(self)



Class: Fact
    '''Fact is how fact is stored in the database. For example,
    collinear points is stored as a list of points on the same line;
    para lines is stored as a pair of line pointers l1 and l2...


    '''
    def add(self, predicate: Predicate)


Class: Database
    def add(self, predicate: Predicate)


Class Prover
    def fixedpoint()