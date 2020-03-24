from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from gym import spaces
import numpy as np

from .manual_control import manual_control

from .board import Board


class env(AECEnv):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self):
        super(env, self).__init__()
        self.board = Board()

        self.num_agents = 2
        self.agents = list(range(self.num_agents))

        self.agent_order = list(self.agents)

        self.action_spaces = {i: spaces.Discrete(9) for i in range(2)}
        self.observation_spaces = {i: spaces.Box(low=0, high=2, shape=(3, 3), dtype=np.int8) for i in range(2)}

        self.rewards = {i: 0 for i in range(self.num_agents)}
        self.dones = {i: False for i in range(self.num_agents)}
        self.infos = {i: {'legal_moves': list(range(0, 9))} for i in range(self.num_agents)}

        self.agent_selection = 0

    # Key
    # ----
    # blank space = 0
    # agent 0 = 1
    # agent 1 = 2
    # An observation is list of lists, where each list represents a row
    #
    # [[0,0,2]
    #  [1,2,1]
    #  [2,1,0]]
    def observe(self, agent):
        # return observation of an agent
        s = np.array(self.board.squares)
        return s.reshape(3, 3).T

    # action in this case is a value from 0 to 8 indicating position to move on tictactoe board
    def step(self, action, observe=True):
        # check if input action is a valid move (0 == empty spot)
        if(self.board.squares[action] == 0):
            # play turn
            self.board.play_turn(self.agent_selection, action)

            # update infos
            # list of valid actions (indexes in board)
            self.infos[self.agent_selection]['legal_moves'] = [i for i in range(len(self.board.squares)) if self.board.squares[i] == 0]

            if self.board.check_game_over():
                winner = self.board.check_for_winner()

                if winner == -1:
                    # tie
                    pass
                elif winner == 1:
                    # agent 0 won
                    self.rewards[0] += 100
                    self.rewards[1] -= 100
                else:
                    # agent 1 won
                    self.rewards[1] += 100
                    self.rewards[0] -= 100

                # once either play wins or there is a draw, game over, both players are done
                self.dones = {i: True for i in range(self.num_agents)}

        else:
            # invalid move, some sort of negative reward
            self.rewards[self.agent_selection] += -10

        # Switch selection to next agents
        self.agent_selection = 1 if (self.agent_selection == 0) else 0

        if observe:
            return self.observe(self.agent_selection)
        else:
            return

    def reset(self, observe=True):
        # reset environment
        self.board = Board()

        self.rewards = {i: 0 for i in range(self.num_agents)}
        self.dones = {i: False for i in range(self.num_agents)}
        self.infos = {i: {'legal_moves': list(range(0, 9))} for i in range(self.num_agents)}

        # selects the first agent
        self.agent_selection = 0
        if observe:
            return self.observe(self.agent_selection)
        else:
            return

    def render(self, mode='human'):
        if mode == 'ansi':
            def getSymbol(input):
                if input == 0:
                    return '-'
                elif input == 1:
                    return 'X'
                else:
                    return 'O'

            board = list(map(getSymbol, self.board.squares))

            print(" " * 5 + "|" + " " * 5 + "|" + " " * 5)
            print(f"  {board[0]}  " + "|" + f"  {board[3]}  " + "|" + f"  {board[6]}  ")
            print("_" * 5 + "|" + "_" * 5 + "|" + "_" * 5)

            print(" " * 5 + "|" + " " * 5 + "|" + " " * 5)
            print(f"  {board[1]}  " + "|" + f"  {board[4]}  " + "|" + f"  {board[7]}  ")
            print("_" * 5 + "|" + "_" * 5 + "|" + "_" * 5)

            print(" " * 5 + "|" + " " * 5 + "|" + " " * 5)
            print(f"  {board[2]}  " + "|" + f"  {board[5]}  " + "|" + f"  {board[8]}  ")
            print(" " * 5 + "|" + " " * 5 + "|" + " " * 5)

    def close(self):
        pass

# import pettingzoo as pz
# env = pz.classic.tictactoe.env()

# import pettingzoo as pz
# env = pz.classic.tictactoe.manual_control()
