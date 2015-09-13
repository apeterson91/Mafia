"""
Support code for Mafia simulation:
Contains 2 classes:
    1. Town
    2. Resident
"""
import numpy as np
from collections import Counter


class Town:
    """
    Main class for Mafia simulation
    Determines number of residents in town
    conducts voting cycle, maintains voting log, etc.
    """

    def __init__(self,n):
        self.r_ = [Resident(True,_) if _<=int(np.floor(.2*n)) else Resident(False,_) for _ in range(1,n+1)]
        self.voting_log_ = {_:[] for _ in range(1,n+1)}
        self.num_cycle_ = 0

    def lynch(self):
        """
        conducts voting cycle for townspeople
        """
        vote_results = False
        while not vote_results:
            vote_index = self.get_votes()
            vote_results = self.is_voting_majority(vote_index)
            if vote_results:
                for resident in self.r_:
                    if resident.get_ID() == vote_results:
                        resident.kill()

    def assassination(self):
        """
        conducts 'voting cycle' for mafia
        """
        victim = np.random.choice([resident for resident in self.r_ if resident.is_alive() and not resident.is_mafia()])
        victim.kill()

    def get_votes(self):
        """
        conducts randomized voting
        for individuals in town
        for lynching
        returns index of list to consult in
        voting log
        """
        for resident in self.r_:
            vote = resident.vote(self.r_)
            self.voting_log_[vote[0]].append(vote[1])
        return len(self.voting_log_.values()[0])-1

    def is_voting_majority(self,index):
        """
        Determines if there is a voting majority
        to sentence one individual to death
        """
        votes = [vote_log[index] for vote_log in self.voting_log_.values()]
        votes = [vote for vote in votes if vote!=np.nan]
        vote_count = Counter(votes)
        if max(vote_count.values()) > np.floor(.5*len([_ for _ in self.r_ if _.is_alive()])):
            for key,value in vote_count.items():
                if value == max(vote_count.values()):
                    return key
        else:
            return False

    def get_votinglog(self):
        """
        retrieves the town's voting log
        """
        return self.voting_log_

    def num_alive_mafia(self):
        return sum([1 for _ in self.r_ if _.is_alive() and _.is_mafia()])

    def num_alive_res(self):
        return sum([1 for _ in self.r_ if _.is_alive() and not _.is_mafia()])

    def initiate_game(self):
        """
        starts the game
        and continues until
        mafia equal or greater than
        townspeople
        """
        while self.num_alive_mafia()<self.num_alive_res():
            self.assassination()
            self.lynch()
            self.num_cycle_+=1

    def __str__(self):
        outstr = ''
        for resident in self.r_:
            outstr += resident.__str__()
            outstr += "\n"
        return outstr

class Resident:
    """
    main object class
    performs voting according to
    mafia status
    """

    def __init__(self,is_mafia,ID):
        self.is_mafia_ = is_mafia
        self.alive_ = True
        self.ID_ = ID

    def vote(self,residents):
        """
        casts vote according to is_mafia bool
        """
        if self.alive_:
            if self.is_mafia():
                vote = np.random.choice([resident.get_ID() for resident in residents if resident.is_alive() and not resident.is_mafia() and resident.get_ID()!=self.ID_])
            else:
                vote = np.random.choice([resident.get_ID() for resident in residents if resident.is_alive() and resident.get_ID()!=self.ID_ ])
        else:
            vote = np.nan 
        return (self.get_ID(),vote)

    def is_mafia(self):
        return self.is_mafia_

    def is_alive(self):
        return self.alive_

    def get_ID(self):
        return self.ID_

    def kill(self):
        self.alive_ = False

    def __str__(self):
        status = "Alive" if self.is_alive() else "Dead"
        return '( ' +str(self.ID_)+ ' , ' + str(self.is_mafia_) + ', ' + status + ' ) '
