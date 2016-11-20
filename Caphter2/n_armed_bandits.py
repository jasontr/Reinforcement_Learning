import random
import matplotlib.pyplot as plt
%pylab inline --no-import-all
#initialize
time = 3000
task = 2000
q = []
n_method = 4
for i in range(10):
    q.append(random.gauss(0, 1))
#a_elements = range(10)
#A = []#elements of A is the action chosen #A[t]
K = [0.0]*10 # K(a) counter of action a
R = [0.0]*10 # R(a) sum of the reward of a
Q = [0.0]*10 
qm = max(q)
Rt = [[[0.0 for i in range(time)] for j in range(task)] for k in range(n_method)] 
e = 0.1
         
def random_pick(Probility_Variable, Probility):
    x = random.uniform(0, 1)
    cumu_prob = 0.0
    for item, prob in zip(Probility_Variable, Probility):
        cumu_prob += prob
        if x < cumu_prob :break
    return item

def Qt(K_a, R_a, q_a):
    K_a += 1
    R_a += random.gauss(q_a, 1)
    Q_a = R_a/K_a
    return K_a, R_a, Q_a

def greedy(t, task, method):
    for ti in range(t):
        if ti < 1:
            act = random_pick(range(10), [0.1]*10)
            K[act], R[act], Q[act] = Qt(K[act], R[act], q[act])
        else:
            act = Q.index(max(Q))#list index & max min
            K[act], R[act], Q[act] = Qt(K[act], R[act], q[act])
        Rt[method][task][ti] = sum(R)/(ti+1)


def egreedy(t, e, task, method):
    for ti in range(t):
        if ti < 1 or random_pick([True, False],[e, 1-e]):
            act = random_pick(range(10), [0.1]*10)
            K[act], R[act], Q[act] = Qt(K[act], R[act], q[act])
        else:
            act = Q.index(max(Q))#list index & max min
            K[act], R[act], Q[act] = Qt(K[act], R[act], q[act])
        Rt[method][task][ti] = sum(R)/(ti+1)


for k in range(task):    
    greedy(time, k, 0)
    K = [0.0]*10
    R = [0.0]*10
    Q = [0.0]*10
    egreedy(time, 0.1, k, 1)
    K = [0.0]*10
    R = [0.0]*10
    Q = [0.0]*10
    egreedy(time, 0.01, k, 2)
    K = [0.0]*10
    R = [0.0]*10
    Q = [0.0]*10
    if k % 500 == 0:
        if e > 0.01:
            e -= 0.01
    egreedy(time, e, k, 3)
    K = [0.0]*10
    R = [0.0]*10
    Q = [0.0]*10

for method_ in range(n_method):
    for ti in range(time):
        for task_ in range(1,task):
            Rt[method_][0][ti] += Rt[method_][task_][ti]
        Rt[method_][0][ti] = Rt[method_][0][ti]/task

plt.plot(range(time), [qm]*time)
plt.plot(range(time), Rt[0][0][:], label = "greedy")
plt.plot(range(time), Rt[1][0][:], label = "egreedy 0.1")
plt.plot(range(time), Rt[2][0][:], label = "egreedy 0.01")
plt.plot(range(time), Rt[3][0][:], label = "egreedy e")

plt.legend(loc="lower right")