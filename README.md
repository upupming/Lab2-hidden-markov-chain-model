# 实验二 - 隐马尔科夫模型

李一鸣

2018 年 10 月 12 日

## 马尔科夫链的生成

假设晴天和雨天的初始概率分别为 $p$ 和 $1 - p$。如果前一天是晴天，则第二天晴天和雨天的概率仍然是 $p$ 和 $1 - p$。如果前一天是雨天，则第二天晴天和雨天的概率分别为 $q$ 和 $1 - q$。

将上述天气变化问题抽象成马尔科夫链，记天气序列为以 $\mathrm{\pi} = (\pi_1, \pi_2) = (p, 1 - p)$ 为初始状态概率的随机过程 $\{X_n, n \ge 0\}$，其状态空间为 $S = \{1, 2\}$（$1$ 表示晴天，$2$ 表示雨天）。其状态转移矩阵为 $P$，则有：

$$
\begin{aligned}
    P &= \begin{pmatrix}
        p_{11} & p_{12} \\
        p_{21} & p_{22} 
    \end{pmatrix} \\ \\
    &= \begin{pmatrix}
        p & 1 - p \\
        q & 1 - q
    \end{pmatrix}
\end{aligned}
\tag{1}
$$

为了随机生成前 $N$ 天的天气序列 $W$，我们可以根据前一天的天气情况再乘以相应的转移概率得到后一天的天气情况。例如：第一天生成晴天的概率为 $p$，如果第一天生成的天气为 $1$（晴天），那么第二天生成晴天的概率为 $p$；如果第二天生成的天气为 $2$（雨天），那么第二天生成晴天的概率为 $q$……

**实验结果**

取 $p = 0.6, q = 0.3, N = 20$，执行 `make 1` 进行实验，得到的结果如下：

<object data="./results/1_weather-20.txt" height="80px" width="1000px"></object>

## 马尔科夫链的生成

某人每天根据天气按以下概率决定当天的活动：

```py
emission_probability = {
    'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
    'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5}
}
```

用 1 表示散步，2 表示购物，3表示清理，根据前面生成的 $W$，我们根据 $W[i]$ 的值，可以得到这个人的活动 $activity[i]$ 为：

$$
p(activity[i] = j)
\begin{aligned}
    &=  \begin{cases}
            \begin{cases}
                0.6, & j = 1 \\
                0.3, & j = 2 \\
                0.1, & j = 3
            \end{cases} , & W[i] = 1\\ \\
            \begin{cases}
                0.1, & j = 1 \\
                0.4, & j = 2 \\
                0.5, & j = 3
            \end{cases} , & W[i] = 2
        \end{cases}
\end{aligned}

\tag{2}
$$

**实验结果**

执行 `make 2` 进行实验，得到的结果如下：

<object data="./results/2_activity-20.txt" height="100px" width="1000px"></object>

## 隐马尔科夫模型

隐马尔科夫模型的三个问题：

+ 概率计算

    计算特定观测序列的概率 -  forward/backward 算法

+ 预测问题

    给定模型和观测序列，求给定观测序列条件下，最可能出现的对应的状态序列 - viterbi 解码算法，基于动态规划算法

+ 学习问题

    给定观测序列，估计模型的参数，使得在该模型下观测序列的条件概率最大 - baum-welch 算法


假设在 $N$ 天内，此人发布的活动状态分别是 $\mathrm{A} = (A_1, A_2, ..., A_N)$，推测这 $N$ 天的天气 $\mathrm{T} = (T_1, T_2, ..., T_N)$。

求解最可能的隐状态序列是 HMM 的三个典型问题之一，通常用维特比（viterbi）算法解决。维特比算法就是求解 HMM 上的最短路径（-log(prob)，也即是最大概率）的算法。

<!-- 
记该人的活动为以 $\mathrm{\pi} = (\pi_1, \pi_2, \pi_3) = (0.6p + 0.1(1 - p), 0.3p + 0.4(1 - p), 0.1p + 0.5(1 - p)) = (0.5p + 0.1, -0.1p + 0.4, -0.4p + 0.5)$ 为初始状态概率的马尔科夫链 $\{X_n, n\ge 0\}$，状态空间为 $S = \{1, 2, 3\}$。 -->

### 举例以理解 viterbi 算法的思想

现在假设此人第一天去散步、第二天清理了、第三天购物了（$\mathrm{A} =(1, 3, 2)$），我们按以下方式估计天气情况：

**第 1 步：**

$$
p(第一天是晴天 | 第一天散步) = \frac{p(第一天晴天, 第一天散步)}{p(第一天散步)}

\tag{3}
$$

用数学公式可以表达为：

$$
\begin{aligned}
    p(W_1 = 1 | A_1 = 1) 
    &= \frac{p(W_1 = 1, A_1 = 1)}{p(A_1 = 1)} \\
    &= \frac{p(W_1 = 1)p(A_1 = 1 | W_1 = 1)}{p(A_1 = 1)} \\
    &\xlongequal{p = 0.6} \frac{0.6 \times 0.6}{p(A_1 = 1)} \\
    &= \frac{0.36}{p(A_1 = 1)}
\end{aligned}

\tag{4}
$$

$$
\begin{aligned}
    p(W_1 = 2 | A_1 = 1)
    &= \frac{p(W_1 = 2)p(A_1 = 1 | W_1 = 2)}{p(A_1 = 1)} \\
    &= \frac{0.4 \times 0.1}{p(A_1 = 1)} \\
    &= \frac{0.04}{p(A_1 = 1)} 
\end{aligned}

\tag{5}
$$

我们知道 $p(A_1 = 1) = 0.4$，验算 $p(W_1 = 1 | A_1 = 1) + p(W_1 = 2 | A_1 = 1) = 1$ 符合全概率公式。

因为 $p(W_1 = 1 | A_1 = 1)$ 更大，也就是说在朋友第一天去散步时，第一天天气是晴天的概率更大，因此我们得到推测值 $T_1 = 1$。

**第 2 步：**

利用动态规划的思想，在已知 $T_1 = 1$（第一天晴天）和此人第二天清理（$A_2 = 3$）的情况下，我们再来看看第二天天气的概率情况：

$$
\begin{aligned}
    p(W_2 = 1 | W_1 = 1, A_2 = 3)
    &= \frac{p(W_2 = 1, W_1 = 1, A_2 = 3)}{p(W_1 = 1, A_2 = 3)} \\
    &= \frac{p(W_1 = 1)p(W_2 = 1 | W_1 = 1)p(A_2 = 3| W_1 = 1, W_2 = 1 )}{p(W_1 = 1, A_2 = 3)} \\
    &= \frac{0.6 \times P_{11} \times 0.1}{p(W_1 = 1, A_2 = 3)} \\
    &= \frac{0.6 \times 0.6 \times 0.1}{p(W_1 = 1, A_2 = 3)} \\
    &= \frac{0.036}{p(W_1 = 1, A_2 = 3)}
\end{aligned}

\tag{6}
$$

$$
\begin{aligned}
    p(W_2 = 2 | W_1 = 1, A_2 = 3) 
    &= \frac{p(W_1 = 1)p(W_2 = 2 | W_1 = 1)p(A_2 = 3| W_1 = 1, W_2 = 2 )}{p(W_1 = 1, A_2 = 3)} \\
    &= \frac{0.6 \times 0.4 \times 0.5}{p(W_1 = 1, A_2 = 3)} \\
    &= \frac{0.12}{p(W_1 = 1, A_2 = 3)}
\end{aligned}

\tag{7}
$$

同样我们知道 $p(W_1 = 1, A_2 = 3) = 0.6 \times (0.6 \times 0.1 + 0.4 \times 0.5) = 0.156$，验算 $p(W_2 = 1 | W_1 = 1, A_2 = 3) + p(W_2 = 2 | W_1 = 1, A_2 = 3) = 1$ 符合全概率公式。

因为 $p(W_2 = 2 | W_1 = 1, A_2 = 3)$ 更大，也就是说在第一天天晴和朋友第二天清理的情况下，第二天是雨天的概率更大，因此我们得到推测值 $T_2 = 2$。

**第 3 步：**

在已知 $T_1 = 1, T_2 = 2$ 和 $A_3 = 2$ 的情况下，我们再来计算第三天的天气概率情况：

$$
\begin{aligned}
    p(W_3 = 1 | W_1 = 1, W_2 = 2, A_3 = 2)
    &= \frac{p(W_1 = 1, W_2 = 2, W_3 = 1, A_3 = 2)}{p(W_1 = 1, W_2 = 2, A_3 = 2)} \\
    &= \frac{p(W_1 = 1)p(W_2 = 2 | W_1 = 1)p(W_3 = 1 | W_2 = 2)p(A_3 = 2| W_3 = 1 )}{p(W_1 = 1, W_2 = 2, A_3 = 2)} \\
    &= \frac{0.6 \times 0.4 \times 0.3 \times 0.3}{p(W_1 = 1, W_2 = 2, A_3 = 2)} \\
    &= \frac{0.0216}{p(W_1 = 1, W_2 = 2, A_3 = 2)} 
\end{aligned}

\tag{8}
$$

$$
\begin{aligned}
    p(W_3 = 2 | W_1 = 1, W_2 = 2, A_3 = 2)
    &= \frac{p(W_1 = 1, W_2 = 2, W_3 = 2, A_3 = 2)}{p(W_1 = 1, W_2 = 2, A_3 = 2)} \\
    &= \frac{p(W_1 = 1)p(W_2 = 2 | W_1 = 1)p(W_3 = 2 | W_2 = 2)p(A_3 = 2| W_3 = 2 )}{p(W_1 = 1, W_2 = 2, A_3 = 2)} \\
    &= \frac{0.6 \times 0.4 \times 0.7 \times 0.4}{p(W_1 = 1, W_2 = 2, A_3 = 2)} \\
    &= \frac{0.0672}{p(W_1 = 1, W_2 = 2, A_3 = 2)} 
\end{aligned}

\tag{9}
$$

我们知道 $p(W_1 = 1, W_2 = 2, A_3 = 2) = 0.6 \times 0.4 \times (0.3 \times 0.3 + 0.7 \times 0.4) = 0.0888$，验算 $p(W_3 = 1 | W_1 = 1, W_2 = 2 , A_3 = 2) + (W_3 = 2 | W_1 = 1, W_2 = 2 , A_3 = 2) = 1$ 符合全概率公式。

因为 $p(W_2 = 2 | W_1 = 1, A_2 = 3)$ 更大，也就是说在第一天天晴和朋友第二天清理的情况下，第二天是雨天的概率更大，因此我们得到推测值 $T_2 = 2$。


**... 第 i 步 ...**($i \in [4, N]$)


### viterbi 算法的实现

我们在实际计算时，可以不用计算 $(4) (5) (6) (7)$ 中的分母，因为做比较时分母都是相同的。记分子为 $p_1 = p(W_1 = T_1, ..., W_n = 1, A_n)$。

算法的伪代码如下：

$\begin{aligned}
\\&
for\ n \in [1, N]: \\&
\quad p_1 = p(W_1 = T_1 | S)p(W_2 = T_2 | W_1 = T_1) ... p(W_n = 1 | W_{n - 1} = T_{n - 1})p(A_n | W_n = 1) \\&
\quad p_2 = p(W_1 = T_1 | S)p(W_2 = T_2 | W_1 = T_1) ... p(W_n = 2 | W_{n - 1} = T_{n - 1})p(A_n | W_n = 2) \\&
\quad if\ p_1 \ge p_2: \\&
\quad \qquad T_n = 1 \\&
\quad else: \\&
\quad \qquad T_n =2
\end{aligned}$

### 实验结果

#### 前面的例子

前面的例子计算结果如下：

<object data="./results/3_example.txt" width="1000px" height="100px"></object>

与前文的手算结果完全吻合。

#### 问题 1

假设他连续三天发布的活动状态分别是$\text{(1 2 3)}$，请计算这三天天气序列为$\text{(1 2 2)}$的概率。

计算结果如下：

<object data="./results/3_problem1.txt" width="1000px" height="100px"></object>

也就是说天气序列 $\mathrm{W} = (1, 2, 2)$ 的概率为 $0.0672$，比其他天气序列的概率都大，因此预测天气序列就是 $\mathrm{T} = (1, 2, 2)$。

#### 问题 2

假设他连续二十天发布的状态是$\text{(2 1 3 2 3 2 2 3 3 1 2 1 1 1 2 3 3 3 3 2)}$ ，请推测这 20 天的天气。

计算结果如下：

<object data="./results/3_problem2.txt" width="1000px" height="400px"></object>

#### 问题 3

按照前面生成的活动序列，来推测天气序列，并验证是否与问题一中生成的天气序列相同。

生成的天气序列：

<object data="./results/1_weather-20.txt" height="50px" width="1000px"></object>

生成的活动序列：

<object data="./results/2_activity-20.txt" height="50px" width="1000px"></object>

推测的天气序列：

<object data="./results/3_most-likely-weather-20.txt" width="1000px" height="400px"></object>