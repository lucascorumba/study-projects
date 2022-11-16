from itertools import combinations
import re



class Candidate():
    def __init__(self, name: str):
        self.name = name
        # point to another Candidate instance - means the current instance is the matchup winner
        self.points_to = list()
        self.is_source = True

    # insert edge if current instance wins matchup
    def lock_edge(self, node: 'Candidate'):
        self.points_to.append(node)
        node.is_source = False 

    def __repr__(self) -> str:
        return f"Candidate {self.name}"


# type alias for a pair of candidates
Pair = tuple[Candidate, Candidate]
# type alias for a resolved matchup - (winner_candidate, loser_candidate, margin)
Settled = tuple[Candidate, Candidate, int]


def initialize_ballot() -> list[Candidate]:
    """
    Prompt user for candidate names and enforce minimum number of candidates.
    Returns a list of Candidate instances.
    """
    # prompt message
    print("Commencing ballot... \nPlease, insert at least two candidates names (separated by space)")
    while(True):
        candidate_names = input().split()
        # enforce minimum number of candidates
        if len(candidate_names) < 2:
            print("There should be at least two candidates for the ballot")
        # initialize Candidate objects and return a list of them
        else:
            return [Candidate(candidate) for candidate in candidate_names]


def get_vote(candidates: list[Candidate], names: list[str]) -> list[str]:
    """
    Promp user for votes.
    When prompted, the user should type the candidate's name correctly, otherwise
    a warning will be displayed asking for another try for that specific rank.
    """
    # informative message
    print("---> Now it's time to register your vote! \nPlease, rank the candidates by preference\n\
You may select your most preferred candidate first, and the least preferred last \nYour choices are:")
    for candidate in candidates:
        print(candidate.name)
    # initialize current voter rank, initialize loop counter, calculate lenght of candidates list
    rank, step, len_candidates = list(), 1, len(candidates)    
    # prompt message
    while(len(rank) < len_candidates):
        selection = input(f"Rank {step}: ")
        if selection not in names:
            print("Candidate not found")
        elif selection in rank:
            print("Candidate already selected")
        else:
            rank.append(selection)
            step += 1
    return rank


def make_pairs(li: list[Candidate]) -> list[tuple[Pair]]:
    """
    Takes a list of Candidate instances and combines them in all possible ways, returning a list containing
    each combination in tuples. [(candidade_A, candidate_Xi), ..., (candidade_A, candidate_Xn)]
    """
    return list(combinations(li, 2))


def get_preferences(candidates: list[Candidate]) -> list[list[str]]:
    """
    Keeps a loop to register voters preferences among the candidates. The loop can be terminated
    after a voter selects all of it's preferences. Each vote 'session' produces a list 
    (returned from get_vote()). list[0] is the most preferred, list[n] is the least preferred.
    """
    # create list with only the candidate's names
    candidate_names = [i.name for i in candidates]
    # get voters preferences 
    keep_voting, votes = True, list()
    while(keep_voting):
        vote = get_vote(candidates, candidate_names)
        votes.append(vote)
        # anything starting with "n" or "N" will terminate the loop
        response = re.search('^[Nn].*', input("Is there another voter? [y/n] "))
        if response:
            keep_voting = False
    return votes


def tally(pair: Pair, votes: list[list[str]]) -> Settled:
    """
    Checks who is the winner of the matchup and by what margin.
    The return format is (winner_candidate, loser_candidate, margin).
    In a tie, the matchup is discarded and 'None' is returned.
    """
    # initialize vote count for both candidates
    votes_a, votes_b = 0, 0
    # checks who is the most preferred
    for vote in votes:
        # variables storing the index of each candidate in a voter's choice list
        # 'pair[0]' represents 'candidate_a' -- 'pair[1]', 'candidate_b'
        index_a = vote.index(pair[0].name)
        index_b = vote.index(pair[1].name)
        if index_a < index_b:
            votes_a += 1
        elif index_a > index_b:
            votes_b += 1
    if votes_a > votes_b:
        return pair[0], pair[1], votes_a - votes_b
    elif votes_b > votes_a:
        return pair[1], pair[0], votes_b - votes_a
    # if votes_a == votes_b : return None
    return None, None, None


def sort(matchups: list[Settled]) -> None:
    """
    Sorts tuples in decreasing order according to the 'margin' parameter.
    """
    matchups.sort(key=lambda x : x[2], reverse=True)
    return 


def check_cycle(current: Candidate, visited: list[Candidate]) -> bool:
    """
    Depth First Search algorithm. Returns 'True' if a cycle is found in the graph.
    """
    # check if current node was already visited
    if current in visited:
        return True
    visited.append(current)
    try:
        # check every node the current node is pointing to
        for edge in current.points_to:
            return check_cycle(edge, visited)
    # current node still does not point to any other node (points_to = None)
    except AttributeError:
        return False

    
def no_source(candidates: list[Pair]) -> bool:
    """
    Returns 'True' if there is no source node. Otherwise, returns 'False'.
    """
    if True in [i[0].is_source for i in candidates]:
        return False
    return True


def lock(edge: Settled) -> Pair:
    """
    Connects graph nodes.
    """
    edge[0].lock_edge(edge[1])
    # return (winner, loser) tuple
    return edge[0], edge[1]


def resolve_matchups(pairs: list[tuple[Pair]], votes: list[list[str]]) -> list[Settled]:
    """
    Resolves all matchups individually, returning a list of 'Settled' tuples.
    """
    matchups = list()
    for pair in pairs:
        winner, loser, margin = tally(pair, votes)
        # exclude ties
        if winner:
            matchups.append((winner, loser, margin))
    return matchups


def resolve_ballot(matchups: list[Settled]) -> list[Pair]:
    """
    Locks edges in the graph, avoiding cycles.
    """
    # variable to store the graph - list to store visited nodes (for check_cycle())
    result, visited = list(), list()
    # lock edges in the graph, avoiding cycles
    for matchup in matchups:
        result.append(lock(matchup))
        # if cycle was created, and no source node -> remove last edge inserted
        if check_cycle(result[-1][0], visited) and no_source(result):
            result.pop()
            result[-1][0].is_source = True
        else:
            continue
    return result


def get_result(graph: list[Pair]) -> str:
    """
    Returns the ballot winner.
    """
    for candidate in graph:
        if candidate[0].is_source:
            return f"{candidate[0].name} is the winner of the ballot!"
    return "Well, that was unexpected... Seems like we have a tie (or a bug)"


def tideman() -> str:
    """
    Runs the ranked-pairs voting method.
    First, gets all the candidate names from 'initialize_ballot()', then proceed to resolve 
    the ballot following the method:
        tally - for each pair of candidates, determine who is the preferred and by what margin.
        sort - sort the pair of candidates in decreasing order of strength of victory.
        lock - starting with the strongest pair, 'lock-in' each pair to the graph, avoiding
            the creation of cycles.
    """
    # get candidate's names to initialize the ballot
    candidates = initialize_ballot()
    
    # loop to get voters preferences
    votes = get_preferences(candidates)

    # make combination of candidates by pairs
    pairs = make_pairs(candidates)

    # resolve all matchups individually
    matchups = resolve_matchups(pairs, votes)    

    # sort candidates by 'strength of victory'
    sort(matchups)

    # lock edges in the graph, avoiding cycles
    ballot = resolve_ballot(matchups)
    
    # get the ballot winner
    final = get_result(ballot)
    print(final)
    return final



if __name__ == "__main__":
    tideman()
