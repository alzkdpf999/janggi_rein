import random
# from collections import defaultdict
from tqdm import tqdm
import environment
import time
import json

q_value_dic = {}
TOTAL = 10000
FILENAME = "model.dat"
class Agent():
    def __init__(self,learing_rate,epsilon):
        self.learing_rate = learing_rate
        self.epsilon = epsilon

    def egreedy(self,obs,possibleMove,episode,cho):
        e = random.random()
        if e < self.epsilon / (episode + 1):
            action = random.choice(possibleMove)
        else:
            action = self.greedy_act(obs,possibleMove,cho)
        return action
    
    def greedy_act(self,obs,possibleMove,cho):
        possible_val = []
        for i in possibleMove:
            obs_t = obs.copy()
            nobs = self.next_obs(obs_t,i[:4]) # 다음 상태 가져오기
            nval = self.check_value(nobs,i[-1]) 
            possible_val.append(nval)
            # print(nobs,"이건가\n")

        if cho: # 초나라는 보상이 큰 것을 고르게
            best = max(possible_val)
            val_idx = [i for i, j in enumerate(possible_val) if j == best]
        else: # 한나라는 보상이 작은 것을 고르게
            best = min(possible_val)
            val_idx = [i for i, j in enumerate(possible_val) if j == best]

        idx = random.choice(val_idx)
        action = possibleMove[idx] 
        
        val_cur = self.check_value(obs) # 현재 보상 가져오기
        val_new = self.check_value(self.next_obs(obs.copy(),action[:4]),action[-1]) # 현재에서 액션 취하고 가장 큰 보상 가져오기
        obs = tuple([tuple(e) for e in nobs])
        q_value_dic[obs] = val_cur * (1 - self.learing_rate) + self.learing_rate * (val_new - val_cur) # 현재 보상 수정해주기
        return action
    
    # 액션 후 다음 상태 반환
    def next_obs(self,obs,position):
        piece = obs[position[2],position[3]]
        obs[position[2],position[3]] = "--"
        obs[position[0],position[1]] = piece
        return obs
    
    # 액션 후 보상 반환해주기
    def check_value(self,nobs,reward=0):
        nobs = tuple([tuple(e) for e in nobs])
        if nobs not in q_value_dic:
            val = reward
            q_value_dic[nobs] = val
        return q_value_dic[nobs]
    



def learn(filenmae):
    env = environment.JanggiEnv(1,1)
    agent = Agent(0.2,0.1) # env.cho == True면 초나라 False면 한나라여서 에이전트 한개로만 해도 될 것 같음  cho에 따라 움직일 수 있는 기물 달라지게 설정함
    for i in tqdm(range(TOTAL)):
        obs = env.reset().copy()
        done = False
        while not done:
            possibleMove = env.move() # 현재 위치에서 가능한 움직임 가져오기
            action = agent.egreedy(obs,possibleMove,i,env.cho)
            nobs, reward, done, info = env.step(action)    
            obs = nobs.copy()
    save_model(filenmae,TOTAL,agent.epsilon,agent.learing_rate)

def save_model(filename,episode,epsilon,learing_rate):
    with open(filename,"wt") as f:
        info = dict(total_episode = episode, epsilon = epsilon, learing_rate= learing_rate)
        f.write("{}\n".format(json.dumps(info)))
        
        for obs, value in q_value_dic.items():
            f.write('{}\t{:0.3f}\n'.format(obs, value))

def load_model(file):
    with open(file,"rb") as f:
        info = json.loads(f.readline().decode("ascii"))
        for line in f:
            elms = line.decode("ascii").split('\t')
            obs = eval(elms[0])
            val = eval(elms[1])
            q_value_dic[obs] = val
    return info

def play(load_file):
    load_model(load_file)
    env = environment.JanggiEnv(1,1)
    agent = Agent(0,0)
    done = False
    obs = env.reset()
    while not done:
        env.render()
        possibleMove = env.move()
        action = agent.egreedy(obs,possibleMove,0,env.cho)
        time.sleep(1)
        nobs, reward, done, info = env.step(action)
        obs = nobs

learn(FILENAME)

