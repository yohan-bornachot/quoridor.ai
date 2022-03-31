from torch import batch_norm, nn, cuda, no_grad, tensor, argmax, unsqueeze, vstack, max, zeros, sum, mul
from torch.optim import Adam
import random as rd
import copy

from .ai import AI

class DQN(AI):
    def __init__(self, play_as, time_to_play, board_size, nb_walls, check_licit, eps, eps_decay, min_eps, gamma, network, lr) -> None:
        super().__init__(play_as, time_to_play)

        self.eps = eps 
        self.eps_decay = eps_decay
        self.min_eps = min_eps
        self.gamma = gamma
        
        self.board_size = board_size-1
        self.nb_actions = 12 + 2*(self.board_size**2)
        self.check_licit = check_licit

        self.net = network
        self.lr = lr
        self.optimizer = Adam(self.net.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

        self.nb_walls = nb_walls

        self.use_cuda = cuda.is_available()
        if self.use_cuda:
            device="cuda"
        else :
            device = "cpu"
        self.device = device

        self.net.to(device)
        self.target_net = copy.deepcopy(self.net)
        

        self.state_list = ["u", "d", "l", "r", "uu", "dd", "ll", "rr", "ur", "ul", "dr", "dl"]
        self.state_list = self.state_list + ["h{}.{}".format(i%self.board_size,i//self.board_size) for i in range(self.board_size**2)]
        self.state_list = self.state_list + ["v{}.{}".format(i%self.board_size,i//self.board_size) for i in range(self.board_size**2)]


    def policy(self, state):
        if rd.random() < self.eps :
            return tensor(rd.randint(0, self.nb_actions - 1))
        else :
            c_1 = unsqueeze(tensor(state.board.walls_h),0)
            c_2 = unsqueeze(tensor(state.board.walls_v),0)
            c = unsqueeze(vstack((c_1,c_2)),0).to(self.device).float()

            n = state.board.board_size + 1

            nb_walls = [state.players[self.play_as].get_nb_wall()]
            pos = [state.players[self.play_as].i, state.players[self.play_as].j]
            goals = [state.players[self.play_as].goal_i]
            for i,player in enumerate(state.players):
                if i!=self.play_as:
                    nb_walls.append(player.get_nb_wall())
                    pos.append(player.i)
                    pos.append(player.j)
                    goals.append(player.goal_i)
            nb_walls = unsqueeze(tensor(nb_walls)/self.nb_walls,0).to(self.device).float()
            pos = unsqueeze(tensor(pos)/n,0).to(self.device).float()
            goals = unsqueeze(tensor(goals)/n,0).to(self.device).float()

            return argmax(self.net.forward(c, pos, goals, nb_walls))

    def decrease_eps(self):
        tmp = self.eps*self.eps_decay
        if tmp > self.min_eps :
            self.eps = tmp

    def legal_move(self, game_state, idx):
        state_name = self.state_list[idx]
        x = game_state.possible_moves.get(state_name)
        return x

    def select_next_step(self, game_state, next_steps):
        idx = self.policy(game_state)

        legal = self.legal_move(game_state, idx)

        if self.check_licit and legal == None:
            print("mauvaise action")
            return next_steps[rd.randint(0, len(next_steps)-1)]
        
        return next_steps[legal]

    def update_target(self):
        self.target_net = copy.deepcopy(self.net)
    
    def train_on_batch(self, states, rewards, next_states, actions):
        c, pos, goals, nb_walls = next_states
        c = c.to(self.device).float()
        pos = pos.to(self.device).float()
        goals = goals.to(self.device).float()
        nb_walls = nb_walls.to(self.device).float()
        with no_grad() :
            target = self.target_net(c, pos, goals, nb_walls)
            target = max(target, 1)[0]
            target = rewards.to(self.device) + tensor(self.gamma).to(self.device)*target

        batch_size = len(rewards)
        mask = zeros((batch_size,self.nb_actions))
        for i, action in enumerate(actions):
            mask[i,action] = 1
        mask = mask.to(self.device).float()

        c, pos, goals, nb_walls = states
        c = c.to(self.device).float()
        pos = pos.to(self.device).float()
        goals = goals.to(self.device).float()
        nb_walls = nb_walls.to(self.device).float()
        pred = self.net(c, pos, goals, nb_walls)
        pred = sum(mul(pred, mask), 1)

        loss = self.loss_fn(pred, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()