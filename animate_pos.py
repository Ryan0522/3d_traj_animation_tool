import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter, FuncAnimation

def get_trajectories(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
    traj_data = []
    curr_run = None
    for line in lines[1:]:
        if line.startswith("Run:"):
            curr_run = int(line.split()[1])
            traj_data.append({"Run": curr_run, "times": [], "xs": [], "ys": [], "zs": []})
        else:
            parts = line.split()
            time, x, y, z = map(float, parts[:])
            traj_data[-1]["times"].append(time)
            traj_data[-1]["xs"].append(x)
            traj_data[-1]["ys"].append(y)
            traj_data[-1]["zs"].append(z)
    return traj_data

def plot_single_trajectory(xs, ys, zs, theta=30, phi=45, saveName='../result/plot.png'):
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(111, projection = '3d')
    ax.plot3D(xs, ys, zs)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Trajectory')
    ax.view_init(theta, phi)
    plt.savefig(saveName)
    plt.show()

def animateMe_single_trajectory(xs, ys, zs, Title='test', Artist='Ryan', saveName='../result/test.gif'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.1, 0.1)
    ax.set_zlim(-1.5, -1.38)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(50, 40)

    l, = plt.plot([], [], [], 'bo', markersize=1.5)

    metadata = dict(title=Title, artist=Artist)
    writer = PillowWriter(fps=50, metadata=metadata)

    with writer.saving(fig, saveName, 100):
        for i in range(len(xs) - 1):
            l.set_data_3d(xs[:i+1], ys[:i+1], zs[:i+1])
            writer.grab_frame()

def animate(frame, xs, ys, zs, sc):
    if frame < 50:
        sc._offsets3d = (xs[:frame], ys[:frame], zs[:frame])
    else:
        sc._offsets3d = (xs[frame-50:frame], ys[frame-50:frame], zs[frame-50:frame])\

def animateMe_single_trajectory_2(xs, ys, zs, saveName='../result/test2.gif'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.1, 0.1)
    ax.set_zlim(-1.5, -1.38)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(50, 40)

    sc = ax.scatter(xs, ys, zs, alpha=0.5)

    def update(frame):
        if frame == 0:
            animate(frame, xs, ys, zs, sc)
            return
        if frame < 50:
            alpha_values = np.linspace(1 - 0.02 * frame, 1, len(xs[:frame]))
        else:
            alpha_values = np.linspace(0, 1, 50)

        sc.set_alpha(alpha_values)
        animate(frame, xs, ys, zs, sc)

    ani = FuncAnimation(fig, update, frames=len(xs), interval=20)
    ani.save(saveName)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print()
        print("Missing Argument (Require: python animate_pos.py <loadfilename> <savefigfilename> <animationfilename>).")
        print("For example: animate_pos.py ../data/trajectory.log ../result/plot.png ../result/test2.gif")
        print()
        sys.exit(1)

    fileName = sys.argv[1]
    saveName = sys.argv[2]
    trajs = get_trajectories(fileName)
    times, xs, ys, zs = trajs[0]["times"], trajs[0]["xs"], trajs[0]["ys"], trajs[0]["zs"]
    plot_single_trajectory(xs, ys, zs)
    animateMe_single_trajectory_2(xs, ys, zs, saveName)
    print("\nAll done!!!\n")
    sys.exit(0)