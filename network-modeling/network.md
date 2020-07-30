# Transportation Network Modeling and Wardrop Equilibrium

Reference:
> 1. Sheffi, Yosef. Urban Transportation Networks: Equilibrium Analysis with Mathematical Programming Methods, Prentice-Hall Inc., 1985. 
> 2. Lecture slides from the course CEE 559 Traffic Network Modeling taught by Professor Yafeng Yin at University of Michigan, Ann Arbor.

这是博士一年级的时候春季学期上的殷老师的课，殷老师的课收获都非大的，这个课程的主要内容是关于transportation network modeling， 这个总结主要是一些静态的模型，User Equilibrium和System Optimum之类的一些概念。本来我是很喜欢自己一点一点敲公式的，但是殷老师的课件的公式和notation都非常清晰统一，所以这里几乎绝大多数都直接粘贴slides了。

## Network Modeling

网络的模型都大同小异，一个网络都可以用一个图模型来表征，图由nodes (vertices) 和links (edges)组成，交通网络一般对应一个flow network，输入为若干个OD pairs，每一个OD pair对应一个origin node，destination node以及这个OD-pair的流量，transportation network modeling中很重要的一个环节就是给定了OD pair以及OD flow之后怎么决定整个network的flow pattern，以及在这样的一个模型下，怎么去对一个网络进行设计和优化。对于一个network 的flow pattern，一般有两种表征方式，一种是path flow，也即整个路网的flow是由一些列的path和path flow所决定，还有一种表征方式是link flow，也即每一个link上的flow。path flow是可以决定link flow的，但是单纯的link flow可能不能还原出path flow。对于flow network而言，还有一个比较常见的概念叫commodity，一般称一个OD pair下的flow为一个commodity，多个OD pair就对应multi-commodity，比如一个link上的link flow，可能serve有不同OD pairs下的flow，如果在link flow下更详细的细化出每一个commodity也即OD pair的flow的话，link flow就可以还原出path flow。

对于一个flow network上的每一个node，流入和流出的流量需要满足守恒定律(conservation law)，这个是比较直观的。在守恒律之外，最为重要的就是link performance function，在transportation network modeling中，最为常用的link performance function就是下图所示的BPR function，直观来看，对于一个link，也就是一条路而言，流量越大，整个link的通行时间也就越长。

![BPR link performance function](https://imgkr.cn-bj.ufileos.com/cd290d3a-901b-4701-af80-d38bb2241f5f.png)

## User Equilibrium

User Equilibrium主要针对于之前所提到的一个问题，给定了一个transportation network以及OD pair和对应的flow，那么这个OD flow会做如何的路径选择，也即给定了网络，给定OD pair with flow，怎么去确定path flow。

### Example

下图是一个简单的例子，网络里只有两条路，一个OD flow从A到B， 两个路径选择。其中红色曲线对应freeway的link performance function，蓝色曲线对应local的link performance function。整个OD flow的流量是给定的$q$。一般这样的静态模型就会用user equilibrium来确定路径的选择，user equilibrium下，最终的稳定状态两个路径的通行时间会相同，这样就会达到两个路径对于用户是相同的选择，没有哪一个用户可以通过切换自己的路径来减少自己的通行时间。本质上讲user equilibrium就是连续形式下的Nash equilibrium。这里的user equilibrium也通常被叫做Wardrop equilibrium。

![~](https://imgkr.cn-bj.ufileos.com/e3f59f71-f759-4aa2-beae-abf7aacd5b78.png)
![Example of User Equilibrium](https://imgkr.cn-bj.ufileos.com/545cfd11-869f-4d60-b49d-d7bdbc2797a4.png)

### Definitation of User Equilibrium

上面给了一个非常好理解的user equilibrium的例子，下面的公式则给出了user equilibrium的条件，其中$f_p$ 对应路径$p$的path flow，$c_p$ 为路径$p$的cost一般指通行时间。$W$为OD pairs的集合，相应的$P^w$为OD pair $w$ 的路径的集合。$c_{\text{min}}^w$为OD pair $w$最后均衡状态下的通行时间，所有flow>0的路径最终的通行时间都会等于这个值。$q^w$ 为 OD flow。

![Conditions of User Equilibrium](https://imgkr.cn-bj.ufileos.com/311b284a-e7af-4da5-8bc3-fcb501e8dd94.png)

整体上而言这几个公式构成的条件还是很好理解的，其中第三和第四个是比较基础的条件，比如对于每一个OD pair而言，所有路径流量总和等于这个OD 的流量，以及每一条路径的流量必须是非负的。前两个条件中，第一个这样的形式一般称为complimentary condition，也即相乘的两项必须有一项为0，如果$f_p$为$0$，那么这条路就没有被选择，那么第二个条件就限制了如果 $c_p\neq c_{\text{min}}^w$，对于没有被选择的路一定有：$c_p> c_{\text{min}}^w$，也即这条路的通行时间是大于这个OD pair的通行时间的。如果第一个条件中$f_p\neq 0$，那么这个路径的通行时间就必须与均衡状态下OD travel time相等，也即User equilibrium。

### Mathematical Formulation

上面公式给出了user equilibrium的条件和定义，我个人认为transportation network modeling中最巧妙的构造就是BMW formulation (Beckmann, McGuire and Winsten, 1956)，BMW formulation构造了一个convex optimization的问题，这个cvx problem的KKT condition和User equilibrium 的条件是完全等价的，也就是说，只要我们找到了这个convex optimization问题的解，我们也就可以找到对应的path flow的解：

![BMW Formulation of User Equilibrium](https://imgkr.cn-bj.ufileos.com/fe2e2a90-53fe-4f5d-bbc3-9b0632e7d4b2.png)

这个凸优化问题的目标函数是一个变上限积分，积分函数是link performance function，上限为link flow $x_a$，限制条件都很好理解，如果将这个优化问题的KKT condition写出来，经过验证就会发现完全与UE的条件是等价的。

有了BMW formulation的好处就是，我们可以通过解一个凸优化的问题来求解UE下的path flow，而对于凸优化问题就有很多解法了。其中最适合，仿佛是为这个问题量身定制的解法就是Frank-Wolf method，在每一个iteration中，给定当前的flow pattern，用shortest path找到最短的路径，然后利用line search找到原有flow pattern和新找的shortest path之间的线性组合中最小化目标函数的值作为新的flow pattern。

UE conditions和BMW formulation是整个static transportation network modeling的基础，后面的一些列拓展最后都可以视为UE的变种。

## System Optimum

User equilibrium，或者Wardrop equilibrium，本质上是用户selfish routing的结果，往往是不能达到系统最优的，而系统最优(system optimum)的定义也非常的清晰明了：

![System Optimum](https://imgkr.cn-bj.ufileos.com/8649f526-73b7-44cb-aa9c-fba1255490f8.png)

即在满足conservation law的情况下如何assign traffic flow使得整个系统所有用户的总通行时间最短。在一般convex 的link performance function下，这个问题本身就是一个convex optimization的问题(with linear constraints)。但同样我们会发现，SO (system optimum)也可以在一定条件下转换为UE。

### UE and SO

这一节我们会看到SO 经过一些变换就可以转换为UE， 相当于改变了原有的link performance function。如果我们定一个新的link performance function $\tilde{t}_a$，等于原来的function加上一个额外项，那么SO 的formulation就会完全等价于BMW formulation，除了直接解SO之外，也就可以用之前解UE的方法来解SO了。

![~](https://imgkr.cn-bj.ufileos.com/a17a9ce7-4bb0-4bf8-854d-fa73760583dc.png)
![~](https://imgkr.cn-bj.ufileos.com/17607610-2de1-420a-9b37-98cc82ebffaf.png)

这里介绍UE和SO之间的关系，其意义远远不止让SO用UE解这么简单，他可以帮助我们理解UE和SO之间的关系以及我们怎么让系统从UE变为SO。外加的额外项是具有非常具体的物理意义的，原有的$t_a(\cdot)$ 就是用户体验到的delay或者cost，如果大家用这个作为最终的cost作为选择，那么最终的均衡状态就会变为UE。而第二项则是对于一个用户而言，他选择了某条路径之后对其他已有的车造成的损失（因为整条路变得更拥堵了），也就是说用户的cost不仅仅有自己的delay，还有自己对别人造成的delay，如果在用户在这样的cost下做路径选择，那么最终的均衡状态则就会变成SO。

一般UE是不一定达到系统最优的，或者说对于一个general 的network而言是不会实现系统最优的，如果想要实现系统最优，其中之一的办法就是congestion pricing，为每一个用户收取额外的拥堵费用，这个拥堵费用就等于这个用户对其他用户造成的额外的损失，这样用户的cost就变成了SO相应的cost，系统也会稳定在SO。

这也是个很有意思的社会问题，驾驶员都在做selfish routing并不会让系统达到最优，而用户在做决策的时候如果考虑对整体的影响，最终整个系统则能达到最优状态，这个也是经济学中比较著名的price of anarchy (无政府主义的代价)。

## Extension: Elastic Demand and Stochastic UE

基于原本的UE有一系列的拓展，包括elastic demand和stochastic UE，这里简单贴一下对于elastic demand的分析过程。

Elastic demand也即在实际生活中每一个OD flow并不是给定的，而是和道路通行能力有关的，假如道路拥堵，这个OD pair的通行时间比较长，那么受拥堵影响出行的人也会相应减少，如下图给出的demand function的inverse function：

![Inverse Demand Function](https://imgkr.cn-bj.ufileos.com/c0e71237-f36d-45f4-9c7c-b8df745a3fc8.png)

在这种情况下，UE conditions的主要变化就是OD flow变成了通行时间的函数。

![User Equilibrium with Elastic Demand](https://imgkr.cn-bj.ufileos.com/7f596a83-6078-4e15-901b-7432663f46b2.png)

可以验证在这样的UE conditions下，BMW formulation就相应变成了：

![BMW formulation of UE with Elastic Demand](https://imgkr.cn-bj.ufileos.com/c9eefe33-b79b-40a0-a035-d3db22209fd5.png)

可以进一步做一些等价变化，让BMW formulation的形式重新回到之前UE的形式：

![~](https://imgkr.cn-bj.ufileos.com/83c31e13-06f0-440f-b5d8-0b3088d4b411.png)
![~](https://imgkr.cn-bj.ufileos.com/b804bab3-14b0-487f-8119-2a950afa1d6c.png)

最终的结果就是，在elastic demand的情况下，相当于原来的路网在每一个OD pair之间加了一个dummy link：

![Equivalent Network under Elastic Demand](https://imgkr.cn-bj.ufileos.com/65be719e-bd23-4c1a-bbaa-1d890fd3e2d6.png)

## Bi-Level Programming

有了之前的UE 的各种模型，最终我们得到的是在给定的路网结构和OD demand的情况下，整个路网的path flow是如何分配的，也即我们已经有了模型的部分。假如我们要对交通网络进行一些设计、决策或者优化，比如新增、扩建一些路段，或者增加一些收费站，那我们就要评估我们做这些调整之后的收益。换句话说，整个模型是首先上层有一些设计或者决策，在决策下，用户会达到一个均衡状态，这样的模型一般称为Stalkelberg game，也即参与“游戏”方有一方有明显的主导地位，而其他非主导的参与者针对leader做出反应。在这样的模型下，优化问题往往就会变成bi-level programming的问题。

下面的formulation给出了bi-level programming的一般形式，也即一个优化问题分成了上下两层，上层做决策，下层做反应，在上层的决策下，下层的“反应”本身也是一个优化问题，一般叫lower level program，而上层针对下层反应的决策也叫upper level problem。

![General formulation of bi-level programming model](https://imgkr.cn-bj.ufileos.com/021c68a0-4448-43a3-b564-0386bc7a9ca6.png)

下面则是一个具体的实例，比如我们要在红色的links上收费来缓解其拥堵情况，那么在红色路上收费的值就是我们的决策变量，我们想通过收费来让系统达到更好的效果，那么这样一个优化问题就是一个bi-level problem。

![Tollment Design Problem](https://imgkr.cn-bj.ufileos.com/74c4d481-d1ff-47d8-9e2f-f6be8ebea21d.png)

![Formulation of the Tollment Design Problem](https://imgkr.cn-bj.ufileos.com/027ce1b6-5b47-4aec-b60e-3ec1fa9f72b3.png)

这样的bi-level programming是非常难解的，其中容易产生的误解就是bilevel problem并不能通过上下层问题逐步迭代求解来得到最终的值。一般会做法是把他变成一个一层的问题，一般有两种变法，一个叫MPEC (mathematical program with equilibrium constraints)，还有一个是MPCC (mathematical program with complementary constrains)。

对于MPEC，则把下层的优化问题变成一个variational inequality，对于最后一个不等式，和普通的不等式不同，他要求对所有的$x$都成立，也即$x^*$ 是$x$中的最优值。

![Mathematical Program with Equilibrium Condition (MPEC)](https://imgkr.cn-bj.ufileos.com/db3ddbb8-0ce8-40b6-aba3-b0dd5811613a.png)

MECC也很好理解，我们不把lower problem写成一个优化问题，我们把lower problem的KKT condition写到upper problem里面，其实这里本质上也就是不再用BMW formulation而把UE最原始的条件写到限制条件中。

![Mathematical Program with Complementary Condition (MPCC)](https://imgkr.cn-bj.ufileos.com/5456ce4a-f46d-4ece-92a4-5b130b4fe99f.png)

MPCC和MPEC都不再是cvx problem，虽然问题变成了一个一层的问题，并没有统一的方法能够高效的求解这样的优化问题。

## (Temporal) Bottleneck Model

之前的所有模型都是空间上的路径选择，对于出行时间的选择，同样可以应用UE的一些思路，最为经典的就是Vickery's bottleneck model，这个模型在下面两张图之下还是很好理解的~

![Vickery's bottleneck model](https://imgkr.cn-bj.ufileos.com/81ff17bb-521c-488c-892e-3daac0498554.png)

![Queueing curve of Vickery's bottleneck model](https://imgkr.cn-bj.ufileos.com/8b227a62-0bc6-47f0-8766-c19068aa9dd8.png)

很类似于price of anarchy，我们在出行时间选择上，假如路的通行能力有限注定会造成拥堵，那么最终的均衡状态下大家的“收益”也会是一样的：赶在准点达到的人，一般会遇到最堵的时候，为了避开拥堵，那就只有起的更早和迟到两种选择了，从某种意义上讲，work from home还是有好处的hhh
