import matplotlib.pyplot as plt
import numpy as np


class HiddenMarkovModel(object):#隠れマルコフモデルのクラス

    def __init__(self, n_states_hidden, n_states_observe): #初期化の関数
        self.n_states_hidden = n_states_hidden #潜在変数の状態数
        self.n_states_observe = n_states_observe #観測変数の状態数
        #初期潜在変数の分布パラメータpiの初期化
        self.initial = np.ones(n_states_hidden) / n_states_hidden
        #遷移確率行列Aの初期化
        self.transition = np.ones((n_states_hidden, n_states_hidden)) / (2 * n_states_hidden)
        self.transition += np.eye(n_states_hidden) * 0.5
        #観測変数の分布のパラメータmuの初期化
        self.observation = np.random.rand(n_states_observe, n_states_hidden)
        self.observation /= np.sum(self.observation, axis=0, keepdims=True)

    #pi, A, muの最尤推定
    def fit(self, sequence, iter_max=100):
        #EMステップを繰り返す
        for i in xrange(iter_max):
            params = np.hstack((self.transition.ravel(), self.observation.ravel()))
            #Eステップ
            p_hidden, p_transition = self.expectation(sequence)
            #Mステップ
            self.maximization(sequence, p_hidden, p_transition)

            #収束しているかどうか確認
            if np.allclose(params, np.hstack((self.transition.ravel(), self.observation.ravel()))):
                break

    #Eステップ
    def expectation(self, sequence):
        N = len(sequence)
        forward = np.zeros(shape=(N, self.n_states_hidden))
        #alpha(z_1)=p(x_1,z_1)を計算
        forward[0] = self.initial * self.observation[sequence[0]]
        backward = np.zeros_like(forward)
        #beta(z_N)=p(x_N|z_N)を計算
        backward[-1] = self.observation[sequence[-1]]

        #フォーワード
        for i in xrange(1, len(sequence)):
            forward[i] = self.transition.dot(forward[i - 1]) * self.observation[sequence[i]]

        #バックワード
        for j in xrange(N - 2, -1, -1):
            backward[j] = (self.observation[sequence[j + 1]] * backward[j + 1]).dot(self.transition)
        #潜在変数z_nの事後確率分布gamma(z_n)を計算
        p_hidden = forward * backward
        p_hidden /= np.sum(p_hidden, axis=-1, keepdims=True)

        #連続した潜在変数の同時事後確率分布xi(z_{n-1},z_n)を計算
        p_transition = self.transition * (self.observation[sequence[1:]] * backward[1:])[:, :, None] * forward[:-1, None, :]
        p_transition /= np.sum(p_transition, axis=(1, 2), keepdims=True)

        return p_hidden, p_transition

    #Mステップ
    def maximization(self, sequence, p_hidden, p_transition):
        #初期潜在変数の分布パラメータの更新
        self.initial = p_hidden[0] / np.sum(p_hidden[0])
        #遷移確率行列の更新
        self.transition = np.sum(p_transition, axis=0) / np.sum(p_transition, axis=(0, 2))
        self.transition /= np.sum(self.transition, axis=0, keepdims=True)
        #観測モデルのパラメータ更新
        x = p_hidden[:, None, :] * (np.eye(self.n_states_observe)[sequence])[:, :, None]
        self.observation = np.sum(x, axis=0) / np.sum(p_hidden, axis=0)


def create_toy_data(sample_size=100):

    def throw_coin(bias):
        if bias == 1:
            return np.random.choice(range(2), p=[0.01, 0.99])
        else:
            return np.random.choice(range(2), p=[0.03, 0.97])

    bias = np.random.uniform() > 0.5
    coin = []
    cheats = []
    for i in xrange(sample_size):
        coin.append(throw_coin(bias))
        cheats.append(bias)
        bias = bias + np.random.choice(range(2), p=[0.99, 0.01])
        bias = bias % 2
    coin = np.asarray(coin)

    return coin, cheats


def main():
    coin, cheats = create_toy_data(200)

    hmm = HiddenMarkovModel(2, 2)
    hmm.fit(coin, 100)
    p_hidden, p_transition = hmm.expectation(coin)

    plt.plot(cheats)
    plt.plot(p_hidden[:, 1])
    for i in xrange(0, len(coin), 2):
        plt.annotate(str(coin[i]), (i - .75, coin[i] / 2. + 0.2))
    plt.ylim(-0.1, 1.1)
    plt.show()
    print(p_transition)
    print(p_hidden)

if __name__ == '__main__':
    main()
