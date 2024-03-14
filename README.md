# 3d_traj_animation_tool
Convert a file storing ("time x y z") each line to an animation gif.

Input file MUST be in the following format:
```
Title
Run: 1
t x y z
...
Run: 2
t x y z
...
```

Run Analysis.py as follows: `python animate_pos.py <loadfilename> <savefigfilename> <animationfilename>` (for file name(s) with space, wrap around with "")

(Not all methods of converting to animation is used, change main for different needs)
