

def plot_cluster_tree(root, last=True, header=''):
    elbow = "└────"
    pipe = "│  "
    tee = "├────"
    blank = "   "
    print(f"{header}{elbow if last else tee} {root.topic} - {root.description} ({root.size} | {root.percent*100:.1f}%)")
    
    child_size = len(root.children)
    if child_size > 0:
        for i, c in enumerate(root.children):
            plot_cluster_tree(c, header=header + (blank if last else pipe), last=i == child_size - 1)