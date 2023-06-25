import time as time
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl

colours = ['#000000', '#ff0022', '#dcf7f1'  , '#ffffff', '#c2bebe'   , '#f0c2c2'  ,'#f7a8a8','#e1fcd4'     ,'#c3ffa6'  ,'#7da8a8'             ]
bins =    [0        , 1        , 2          , 3        , 4           , 5          ,6        ,7             ,8          ,9                       ]
cols =    ['black'  , 'red'    ,'light blue','white'   ,'light grey' ,'light red' ,'mid red','light green' ,'mid green', 'mid blue'             ]


assert len(bins) == len(colours)
cmap = mpl.colors.ListedColormap(colours)
norm = mpl.colors.BoundaryNorm(boundaries=bins, ncolors=len(cmap.colors)-1 )



start = time.time()

def board(N,M):
    base = np.zeros((N,M))
    for i  in range(N):
        for j in range(M):
            if i%2 == j%2:
                base[i,j] = 3
            else:
                base[i,j] = 4

    return base

def boardplotter(board,tiles=False,color='light red', plot=False):
    N = board.shape[0]
    if tiles is not False:
        for tile in tiles: board[tile//N,tile%N] = cols.index(color)
    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111)  
        ax.imshow(board,cmap=cmap,norm=norm)
        ax.set_yticks([i for i in range(N)])
        ax.set_xticks([i for i in range(N)])
        for (i,j),z in np.ndenumerate(board):
            ax.text(j,i,str(N*i+j),ha='center',va='center')
        plt.show()
    return board



def repeated(listt):
    listt = [sorted(i) for i in listt]
    tmp = []
    for i in listt:
        if i not in tmp:
            tmp.append(i)
    return tmp


def threats(k,b=False,N=0,threatened = False):
    if b is False:
        b = {n for n in range(N**2)}

    def maindiag(k,N):
        if k%N == k//N:
            return -N,N
        
        elif k%N > k//N:
            return -N,N-k%N
        
        else:
            return -(k%N),N
    
    def secdiag(k,N):    
        if k%N == N-k//N-1:
            return -(k//N),N-k//N
        
        elif k%N > N-k//N-1:
            return -N+k%N+1,N
        
        else:
            return -N,k%N+1
    
    def valid(n,N):
        return 0<=n<(N**2)
    
    line = {n for n in b if k//N == n//N}
    row = {n for n in b if n%N == k%N}
    diags1 = {k+r+r*N for r in range(*maindiag(k, N)) if valid(k+r+r*N, N)}
    diags2 = {k-r+r*N for r in range(*secdiag(k, N)) if valid(k-r+r*N, N)}
    
    if not threatened:
        return b-(line|row|diags1|diags2|{k})
    else:
        return line|row|diags1|diags2|{k}

def threatplotter(n,m,N):
    T = board(N,N)
    num = (n)*N + m
    threatsres = threats(num,N=N,threatened=True)
    for i in threatsres:
        T[i//N,i%N] = 2
    T[n,m] = 5
    fig = plt.figure()
    fig.suptitle(f'tiles threatened by the queen positioned on {n},{m}')
    # boardplot = board(N,N)
    # boardplot[n,m] = 5
    # ax1 = fig.add_subplot(121)
    # ax1.imshow(boardplot,cmap=cmap, norm=norm)
    ax2 = fig.add_subplot(111)
    ax2.imshow(T,cmap=cmap, norm=norm)
    for (i,j),z in np.ndenumerate(board):
        ax2.text(j,i,str(N*i+j),ha='center',va='center')

    plt.show()

def succesion(solution):
    N = len(solution)
    T = board(N,N)
    th = set({})
    fig, ax = plt.subplots(N)
    fig.suptitle('steps')
    ax[0].imshow(T,cmap=cmap,norm=norm)
    for i in range(1,len(solution)):
        th = th|threats(solution[i],N=N,threatened=True)
        for j in th:
            if j not in solution:
                T[j//N,j%N] = 1
            else:
                T[j//N,j%N] = 2
        ax[i].imshow(T,cmap=cmap,norm=norm)
    plt.show()




def queens(b,N,sols,currentposs,nsols):
    # print(b,'b')
    if len(repeated(sols)) == nsols:
        return repeated(sols)
    
    for i in b:
        tmp = currentposs.copy()
        # print(currentposs,'curr', tmp, 'tmp')
        # print(i,'i',b,'current b')
        tmp.append(i)
        j = threats(i,b,N)

        if len(tmp) == N:
            # print('sucess',tmp)
            sols.append(tmp)
        
        if len(j) == 0:
            continue
        
        
        queens(j,N,sols,tmp,nsols)

    return repeated(sols)

def Queens(N,nsols=1):
    s = []
    c = []
    base = {n for n in range(N**2)}
    sols = queens(base,N,s,c,nsols)
    print(time.time()-start)
    if sols == []:
        return None
    
    if nsols != 0:
        sols = sols[:nsols]

    if len(sols) > 1:
        fig, ax = plt.subplots(len(sols))
        fig.suptitle("resultados")

    for i in sols:
        matrix = board(N,N)
        for row,col in [(k//N,k%N) for k in i]:
            matrix[row,col] = 1
        if len(sols) > 1:  
            ax[sols.index(i)].imshow(matrix,cmap=cmap,norm=norm)
        else:
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            ax1.imshow(matrix,cmap=cmap,norm=norm)
            fig.suptitle("resultados")
    plt.show()

    return sols


# threatplotter(0,0,3)

Queens(8,2)

# b = board(3,3)
# b = boardplotter(b,[0],'light red')
# b = boardplotter(b,[1,3,5,7],'mid blue')
# b = boardplotter(b,[2,4,6,8],'light blue',True)
# b = boardplotter(b,[5,7],'light grey',True)

# four = board(4,4)
# five = board(5,5)
# eight = board(8,8)
# fig,axs = plt.subplots(1,3)
# axs[0].imshow(four,cmap=cmap,norm=norm)
# axs[1].imshow(five,cmap=cmap,norm=norm)
# axs[2].imshow(eight,cmap=cmap,norm=norm)
# plt.show()

# threatplotter(3,3,8)

# Queens(5,2)

# b = board(4,4)


# b = boardplotter(b,[3,6,9,12],color='mid blue')
# b = boardplotter(b,[0,2,5,8],color='light red')
# b = boardplotter(b,[1,4],color='mid red')
# b = boardplotter(b,[11,14],color='mid green')
# b = boardplotter(b,[7,10,13,15],color='light green',plot=True)



