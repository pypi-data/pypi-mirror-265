import numpy as np


class BeliefPropagation:

    def __init__(self, n, b, q):
        self.n = n
        self.b = b
        self.q = q
        self.beliefs = np.array((n * q))
        self.alpha1 = 3
        self.alpha2 = 10
        self.beta = 1/self.n

    def decode_bp(self, angles, M, j):
        q_roots = 2 * np.pi / self.q * np.arange(self.q + 1)
        k = np.zeros(self.n, dtype=int)
        for i in range(self.n):
            k[i] = (np.abs(q_roots - angles[i])).argmin() % self.q
        gap = (j - M.T @ k) % self.q
        while np.any(gap != 0):
            # print(k)
            degrees = np.sum(M, axis=0)
            messages = gap / degrees
            for i in range(self.n):
                message_i = 0
                for r in range(self.b):
                    if M[i, r] != 0:
                        message_i += messages[r]
                to_switch = (k[i] - int(np.sign(message_i))) % self.q
                message_str = abs(message_i)
                old_angle = (q_roots[k[i]] - angles[i]) % (2 * np.pi)
                old_angle = min(old_angle, 2 * np.pi - old_angle)
                new_angle = (q_roots[to_switch] - angles[i]) % (2 * np.pi)
                new_angle = min(new_angle, 2 * np.pi - new_angle)
                prob_switch = self.beta/(1 + np.exp(self.alpha1 * (new_angle - old_angle) - self.alpha2 * message_str))
                z = np.random.choice(2, p=[1-prob_switch, prob_switch])
                k[i] = to_switch if z == 1 else k[i]
            gap = (j - M.T @ k) % self.q
        return k


if __name__ == "__main__":
    b = 5
    n = 30
    q = 4
    M = np.random.randint(2, size=(n, b))
    bp = BeliefPropagation(n, b, q)
    k = np.random.randint(q, size=n)
    j = (M.T @ k) % q
    print(f"k = {k}")
    print(f"j = {j}")
    angles = np.zeros(n)
    q_roots = 2 * np.pi / q * np.arange(q + 1)
    for i in range(n):
        angles[i] = (q_roots[k[i]] + 0.3 * np.random.normal()) % (2 * np.pi)

    k_init = np.zeros(n, dtype=int)
    for i in range(n):
        k_init[i] = (np.abs(q_roots - angles[i])).argmin() % q
    print(f"k_init = {k_init}")
    print(f"k_init error = {sum(k_init != k)}")

    k_decoded = bp.decode_bp(angles, M, j)
    print(f"k_decoded = {k_decoded}")
    print(f"k_decoded error = {sum(k_decoded != k)}")
    print(f"j_decoded = {(M.T @ k_decoded) % q}")
