# Data-Driven Dynamic Systems: Dynamic Mode Decomposition and Koopman Operator

This is a very interesting topic I learned recently, which use a data-driven method to analyze the dynamic systems. All thanks to my advisor Dr. Liu who recommended a paper which really draws my attention and interest:

> Avila, A. M., and I. Mezić. "Data-driven analysis and forecasting of highway traffic dynamics." Nature Communications 11.1 (2020): 1-16.

This paper utilized Koopman mode decomposition to analyze the highway dynamics in a fully data-driven fashion, which in some sense can be interpretable.

This article will introduce the techniques used by the paper including dynamic mode decomposition (DMD) and Koopman analysis. I strongly recommend the following websites and YouTube channels and I really appreciate Professor Steve Brunton and his collaborators who have explained their works clearly, easy to understand through all kinds of techniques including their amazing YouTube channels.

YouTube channels of Steve Brunton: `https://www.youtube.com/channel/UCm5mt-A4w61lknZ9lCsZtBw`

YouTube channels of Nathan Kutz: `https://www.youtube.com/channel/UCoUOaSVYkTV6W4uLvxvgiFA`

Website for DMD book: `http://dmdbook.com/`

Website for the online course (inferring structures of complex systems): `https://faculty.washington.edu/kutz/am563/page1/page15/am563.html`

These are amazing materials, very easy to understand for engineering students.

## Dynamic Systems

Almost all real-world systems evolving with time can be regarded as a dynamic system. Let $x$ be the representation of the system state, which can be a vector with very high dimensions; the dynamic systems can be abstracted as:

$$\frac{dx}{dt}=f(x, u, t, \beta)$$

where $u$ can be the controlled variable, $\beta$ is the parameters. The function $f(\cdot)$ is named as *dynamics*. The traditional method to analyze the dynamic system is to establish the model to represent the dynamics. For example, Newton's second law is one of the modeling methods. However, using the traditional way, the dynamic systems can be very hard to analyze due to the following challenges:

* Unknow dynamics
* Nonlinear
* High-dimensionality
* Noise or even missing data
* Chaos, transient
* Uncertainty

Therefore, sometimes a data-driven method might be preferable to the traditional method by establishing models, solving, and analyzing the models. dynamic mode decomposition (DMD) is such a method that does not require any prior domain knowledge but only the data to analyze the dynamic systems using a linear approximation.

Before we go to the details of the DMD and Koopman analysis which could be regarded as an extension, here we recap the analysis for a linear system.

The discrete linear system can be written as:

$$x_{t+1}= Ax_t$$

With an initial state $x_0$, the $x_t$ can be simply solved as:

$$x_{t}=A^t x_0$$

Apply the eigenvalue decomposition to the matrix $A$: $A=W\Lambda W^*$, where $WW^*=I$ and $\Sigma$ is a diagonal matrix. The the $x_t$ becomes:

$$x_t=W\Lambda^tW^* x_0$$

where the matrix $W$ remains unchanged and only the diagonal matrix changes exponentially over time. The magnitude of the eigenvalue tells us how the corresponding *mode* delay or grow over time while the angle of the eigenvalue indicates the frequency of the mode. An eigenvalue with a magnitude larger than $1$ will lead the system to be unstable. This is only the stability analysis of linear systems. The goodness of a linear system is obvious: **we know almost everything about linear systems**, especially, how to control the systems including optimal control (LQR), etc.

Later in DMD, we will show that what DMD does is essentially to approximate the dynamic system using a linear system and decompose the state to a series of modes associated with a spatial-temporal pattern and eigenvalue indicating the evolving of the pattern.

## Dynamic Mode Decomposition

As we stated before, DMD is to use a linear approximation (with respect to least square error) for a dynamic system and then decompose the state to a series of *modes* associated with a particular spatial-temporal pattern under a fixed frequency and delay or growth rate.

Let $X$ be the observation of the system from $1:t-1$ and $X'$ be the observation of the system from $2:t$.

$$X=[x_1, x_2,...,x_{t-1}]\quad\quad X'=[x_2, x_3,...,x_t]$$

Then the transition $A$ can be inferred as:

$$X'=AX \rightarrow A=X'X^\dagger$$

where $X^\dagger$ is the pseudo-inverse of the matrix. With matrix $A$ and we can find the eigenvalue and eigenvectors of the matrix and then transform the state $x$ to the coordinates of the eigenvectors. This is called *exact DMD*.

However, if the dynamic system has a very high dimension, then matrix $A$ will be a very large matrix, which is a $n$ by $n$ matrix where $n$ equals the dimension of the systems. To deal with this issue, the following algorithm finds the eigenvalue and eigenvectors directly without performing the eigendecomposition for the entire matrix $A$. The intuition is that the eigenvalues and eigenvectors have much less dimension than the original matrix.

Here is the algorithm:

1. Find the singular value decomposition of matrix $X$: $X=U\Sigma V^*, X'=AU\Sigma V^*$;
2. Project the matrix $A$ to the $U$ matrix (SVD of $X$) and get $\tilde{A}$: $\tilde{A}=U^*AU=U^*X'V\Sigma^{-1}$;
3. Apply eigendecomposition to the $\tilde{A}$: $\tilde{A}W=W\Lambda$;
4. Project back to original space to get the base of the *mode*: $\Phi=X'V\Sigma^{-1}W$.

**Comments for the algorithm**:

> * The first step is to conduct an SVD for the matrix $X$. Almost all the high dimensional matrix has some certain low-rank properties (Eckart-Young theorem).
> * Project the matrix $A$ to linear space expanded by $U$ is the key step of the algorithms, which essentially projects the dynamics (transition matrix) to the bases of $U$, which are composed of the dominant singular vectors (aka, principal components). In other words, $\tilde{A}$ is about how the dominant singular vectors evolve with time.
> * The reduction of the calculation is also due to the second step, where the dimension of $\tilde{A}$ is determined by the time horizon instead of the dimension of the systems. We can further reduce the calculation by using the truncated SVD, which is usually what we will do.

Then the $X_t$ can be decomposed as:

$$\hat{X}_t = \Phi \Lambda^t b_0=\sum_i \phi_i\cdot b_0 \cdot \lambda_i^t$$

where $b_0$ is determined by the initial state.

Then if we look at the decomposition results, DMD can somehow be regarded as a combination of singular value decomposition or principal component analysis (they are very closely related) and the Fourier analysis. The results include different modes associated with space-temporal pattern (mode: $\phi_i$), frequency and decay/growth rate (determined by the eigenvalues $\lambda_i$). Therefore, DMD is a very powerful technique to analyze periodic or quasi-periodic systems.

## Examples of DMD

Here is an example of the dynamic mode decomposition and comparison with PCA (SVD). Here is a python package for the PyDMD: `https://github.com/mathLab/PyDMD` associated with a document of brief introduction: `https://dsweb.siam.org/Software/pydmd-python-dynamic-mode-decomposition`.

This example is a problem that is tailored for DMD; it will show you how DMD can find the hidden structure of a linear dynamic system.

As shown in this figure:

![Input signal modes](https://imgkr.cn-bj.ufileos.com/1579ed19-6cfb-480d-a3c4-1a1f8ecde63e.png)

We have two mixed linear signals $f=f_1+f_2$:

$$f_1(x,t) =\text{sech}(x+3)\exp(i2.3t)$$
$$f_2(x,t) =2\text{sech}(x)\tanh(x)\exp(i2.8t)$$

They have different profiles given by the first figure and dynamics with different frequencies given by the second figure. The last two figures are 3D plots of how the two modes evolve with time. The following figure is the mixed signal spatial-temporal plot:

![Mixed signal](https://imgkr.cn-bj.ufileos.com/76cb6071-dc10-49cc-9fbf-72f76652604c.png)

Use this mixed signal as the input, we will try to find the hidden structure of the dynamic system. Since the dynamics of both signals are circle functions (sine, cosine), this can be regarded as the state generated by a linear system. This is the exact problem that DMD can deal with. Here are the results of the DMD, including the profiles of the two modes and the corresponding dynamics. We can see DMD can split the different modes clearly and recognize their frequencies.

![DMD results](https://imgkr.cn-bj.ufileos.com/2d056ddf-b97c-47cb-ad09-8c0169493044.png)

Here we compare DMD with the SVD or PCA analysis. The following figures are the results for the singular value decomposition of the mixed signals. Firstly, when we look at the third figure, SVD can successfully identify the rank of the systems. However, it failed to separate the two modes as shown in the first two figures.

![Singular value decomposition for the mixed signal](https://imgkr.cn-bj.ufileos.com/b5b33558-0b10-4a60-a5b4-ecc996304874.png)

One of the interpretations to DMD, which I really like, is that **DMD is like a baby of the principal component analysis and the Fourier analysis**.

## Koopman Theory

We have seen that DMD can find the hidden structure of a linear system. This section we will try to answer what if the dynamic system is not a linear system.

Date back to 1931, Koopman has introduced the **Koopman operator**, which is an infinite linear operator that *lift* the state of the dynamic systems to an **observable space** where the dynamic become linear. This field does not draw the attention of researchers for decades until 2005, Igor Mezić brought the Koopman back to mainstream focus, in which the Koopman operator was introduced to analyze the fluid dynamics.

Here is a brief introduction for the Koopman operator. For a general dynamic system:

$$\frac{dx}{dt}=f(x)$$

or discrete version:

$$x_{t+1}=F_t(x_k)$$

The $F_t(\cdot)$ is a mapping for the system state to move forward a time slot, which could be a nonlinear system. What the Koopman operator does is to transform the state to an observable space $g$:

$$\mathcal{K}_t g = g \circ F_t$$

For discrete time:

$$g(x_{t+1})=\mathcal{K}_t g(x_k)$$

where $g(x)$ is called an **observable** of the state representation. What we want is that when we map the $x$ to the $g(x)$, we will get a linear dynamic system in the observable space, which in Koopman theory, has infinite dimensions.

What we want is to find a finite approximation to the Koopman operator. We want to find finite numbers of observable and get a finite Koopman invariant space.

It could be very easy to find the Koopman operator sometimes. For example,

$$\dot{x}_1 = \mu x$$
$$\dot{x}_2 = \lambda (x_2-x_1^2)$$

If we use the augment state variable $[x_1, x_2, x_1^2]$, we will find the system dynamic becomes linear under this augment state representation:

$$\left[\begin{array}{c}x_1\\ x_2\\ x_1^2 \end{array}\right]=\left[\begin{array}{ccc}\mu & 0 & 0\\ 0 & \lambda & -\lambda\\ 0 & 0 & 2\mu \end{array}\right]\left[\begin{array}{c}x_1\\ x_2\\ x_1^2 \end{array}\right]$$

However, in most cases, it would be extremely hard to find the Koopman operator. For example:

$$\frac{dx}{dt} = x^2$$

Although this seems to be a very simple dynamic system, we will find that we cannot find the Koopman operator easily like the previous example. If we use augmented representation $[x, x^2]$, we will find that:

$$\frac{d}{dx}x^2=2x\dot{x}=2x_3$$

which means that we will need to involve another $x^3$, then $x^4, x^5....$ which will become infinite dimensions.The intuition of this example is that if we simply choose Taylor series, Fourier series, it usually cannot work as a good Koopman operator.

For this system that cannot find the finite Koopman operator easily, the method is to find the **eigenfunctions** that the Koopman opertor could has finite dimensions on these eigenfunctions. When we look at the example $\dot{x}=x^2$, we can see that a function $\phi(x)=\exp{(1/x)}$ that satisfies:

$$\frac{d}{dt}\phi(x)=x^{-2}\phi(x)\dot{x}=\phi(x)$$

which means that on this observable $\phi(x)$, the system will become linear system. This seems very magic to me...

The question is that how to find the bases for such eigenfunctions. Acually, the eigenfunctions satisfy a closed analytical form as a solution of a PDE. The Koopman eigenfunctions expand a invariant subspaces and the PDE is written as:

$$\frac{d}{dt}\phi(x)=\lambda\phi(x)=\nabla \phi(x)\cdot f(x)$$

The magic function $\exp{(1/x)}$ is actually the solution to this PDE.

Although we have a very simple analytical expression for the Koopman eigenfunctions, it is not easy to solve the PDE directly. In most cases, it is impossible. There are different methods proposed to approximate the eigenfunctions including neural networks. Here I will briefly talk about two of those methods: neural networks and sparse linear regression.

For the neural network method, it is very intuitive that we can use an auto-encoder and auto-decoder to learn a function $\phi(x)$ given by the following structure:

![Neural Network to find the Koopman Eigenfunctions](https://imgkr.cn-bj.ufileos.com/9b86f88b-43c4-4441-8955-e0190644bdad.png)

For the sparse linear regression method, we can utilize the PDE of the Koopman eigenfunctions:

$$\lambda\phi(x)=\nabla \phi(x)\cdot f(x)$$

We can choose any bases of the functions, for example Taylor series, Fourier series and conduct a sparse linear regression to choose a sparse set of these functions. This idea was come up with professor Steve Brunton and his collaborators and they also used this similar idea to identify the dynamic of the nonlinear systems in their SINDy (sparse identification of nonlinear dynamics) paper.

Finding the Koopman eigenfunctions is very difficult especially for the real-world complex systems. But once we get a good Koopman operator and Koopman eigenfunctions, we will benefit a lot since we will have a linear approximation for the original complex systems.

## Time-Delay Embedding for Nonlinear Systems

Besides finding the Koopman eigenfunctions, another widely-used and powerful method for the nonlinear especially the chaotic system is the time-delay embeddings.

Here we will use Lorentz attractor as an example to show how the time-delay embedding can be applied to analyze the nonlinear systems and how a "high-dimensional" time-delay embedding can naturally work as a finite approximation to the Koopman operator.

This figure shows a trace of the Lorentz attractor, which is a well-known chaotic system. We usually say a system is **chaotic** if two states diverge quickly over time even they are very close to each other at the beginning. This is usually named as the *butterfly effect*.

![Lorentz attractor](https://imgkr.cn-bj.ufileos.com/58342a5c-38c7-4421-8304-87f1a4d4a1ef.png)

Here we will use Lorentz attractor as an example to show how the traditional method can find the hidden structure of the chaotic system using the time-delay embedding. Assume that we can only observe one of the dimension of the Lorentz attractor:

![x of Lorentz attractor](https://imgkr.cn-bj.ufileos.com/99062e65-6715-4637-bd87-2ec6e684ab3e.png)

It looks very messy and we can see little connection between this signal to the original Lorentz attractor. Traditional method to analyze the chaotic or nonlinear system is to contruct the Hankel matrix and perform an SVD over it. The Hankel matrix is defined as:

$$H = \left[\begin{array}{cccc}x_1& x_2 & ... & x_m\\ x_2 & x_3 &...& x_{m+1}\\ .&.&...&.\\ x_n & x_{n+1} & ... & x_{m+n} \end{array}\right]=U\Sigma V^H$$

where $n$ is called *embedding dimension*.

If we choose the embedding dimension as $15$, we can get the results given by the following figures. From the third figure, we can find that there are about $3$ eigenvalues that are greater than zero. The first figure plots the bases for the first $5$ ranks and the second figure plots the coordinates on these bases. The most amazing result might come from the last figure; if we plot the coordinates of the first three dominant bases, we get a pattern looks very similar to the Lorentz attractor. This seems really cool to me: we only use one dimension observation to reconstruct the pattern of the chaotic system.

![Time-delay embedding with r=15](https://imgkr.cn-bj.ufileos.com/1d6c751c-7e3d-4936-a617-508d0797d3e2.png)

All these results come from very classic analysis for the nonlinear or chaotic system. What is the relationship with Koopman operator?

If we increase the embedding dimension to $300$, we will get the following results for the SVD of the Hankel matrix:

![Time-delay embedding with r=300](https://imgkr.cn-bj.ufileos.com/2733745d-a02d-48f0-adab-45da0bb5ab50.png)

We can see one of the differences is that we have a more continuous singular value spectrum: more than three ranks are significantly greater than zero now. If we zoom in the vectors $v_i$ which tell us how the system evolves under the new dominant bases, we will find that with the increase of the embedding dimension, the $v_i$ is more like the circle function which means that the system will be more close to a linear system. This is the origin that time-delay embedding is widely-used for the Koopman analysis for the nonlinear or chaotic system.

![Comparison of low-rank delay embedding (left) and high-rank delay embedding (right)](https://imgkr.cn-bj.ufileos.com/5a16a7f5-fd2a-4931-a2b8-a979c80f6921.png)
