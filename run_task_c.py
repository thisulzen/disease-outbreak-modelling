"""
Task C timing experiments.
Generates runtime plots for all four algorithm/representation combinations.
Saves figures to visuals/ for inclusion in the report.
"""

import sys
import os
import random
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from graph.adjacency_list import AdjacencyList
from graph.adjacency_matrix import AdjacencyMatrix
from graph.vertex import Vertex
from simulation.person import Person
from transmission.monte_carlo import monte_carlo
from transmission.task_b import task_b

VISUALS_DIR = os.path.join(os.path.dirname(__file__), 'visuals')
os.makedirs(VISUALS_DIR, exist_ok=True)

SEEDS = [1, 2, 3]


def build_graph(graph_type, n, m, seed):
    """Build a random weighted graph with n vertices and m edges."""
    rng = random.Random(seed)
    if graph_type == 'list':
        g = AdjacencyList()
    else:
        g = AdjacencyMatrix()

    persons = [Person(i, 0.5, 1) for i in range(n)]
    for p in persons:
        g.add_vertex(p)

    all_pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    chosen = rng.sample(all_pairs, min(m, len(all_pairs)))
    for i, j in chosen:
        g.add_edge(persons[i], persons[j], rng.uniform(0.1, 0.8))

    source = persons[0]
    return g, source


def time_algo(fn, *args):
    t0 = time.time()
    fn(*args)
    return time.time() - t0


def avg_time(fn_args_list):
    return sum(time_algo(*fa) for fa in fn_args_list) / len(fn_args_list)


# ------------------------------------------------------------------
# Experiment 1 — runtime vs n, sparse graph (m = 2n), T fixed at 10
# ------------------------------------------------------------------
print("Running Experiment 1: runtime vs n (sparse, T=10) ...")

T_FIXED = 10
X_SIM   = 100
N_VALS_MC = [10, 20, 35, 50, 70]        # Monte Carlo caps at 70 (slow)
N_VALS_DP = [10, 30, 60, 100, 150, 220]

results_sparse = {k: [] for k in ['mc_list', 'mc_mat', 'dp_list', 'dp_mat']}

for n in N_VALS_MC:
    m = min(2 * n, n * (n - 1) // 2)
    times = {'mc_list': [], 'mc_mat': []}
    for seed in SEEDS:
        g_list, src = build_graph('list',   n, m, seed)
        g_mat,  _   = build_graph('matrix', n, m, seed)
        times['mc_list'].append(time_algo(monte_carlo, g_list, src, T_FIXED, X_SIM))
        times['mc_mat'].append( time_algo(monte_carlo, g_mat,  src, T_FIXED, X_SIM))
    results_sparse['mc_list'].append((n, sum(times['mc_list']) / len(SEEDS)))
    results_sparse['mc_mat'].append( (n, sum(times['mc_mat'])  / len(SEEDS)))
    print(f"  n={n}: mc_list={results_sparse['mc_list'][-1][1]:.4f}s  mc_mat={results_sparse['mc_mat'][-1][1]:.4f}s")

for n in N_VALS_DP:
    m = min(2 * n, n * (n - 1) // 2)
    times = {'dp_list': [], 'dp_mat': []}
    for seed in SEEDS:
        g_list, src = build_graph('list',   n, m, seed)
        g_mat,  _   = build_graph('matrix', n, m, seed)
        times['dp_list'].append(time_algo(task_b, g_list, src, T_FIXED))
        times['dp_mat'].append( time_algo(task_b, g_mat,  src, T_FIXED))
    results_sparse['dp_list'].append((n, sum(times['dp_list']) / len(SEEDS)))
    results_sparse['dp_mat'].append( (n, sum(times['dp_mat'])  / len(SEEDS)))
    print(f"  n={n}: dp_list={results_sparse['dp_list'][-1][1]:.4f}s  dp_mat={results_sparse['dp_mat'][-1][1]:.4f}s")

# ------------------------------------------------------------------
# Experiment 2 — runtime vs n, dense graph (m ≈ n²/4), T fixed at 10
# ------------------------------------------------------------------
print("\nRunning Experiment 2: runtime vs n (dense, T=10) ...")

N_VALS_DENSE_MC = [10, 15, 25, 35, 50]
N_VALS_DENSE_DP = [10, 30, 50, 80, 120]

results_dense = {k: [] for k in ['mc_list', 'mc_mat', 'dp_list', 'dp_mat']}

for n in N_VALS_DENSE_MC:
    m = max(1, n * (n - 1) // 4)
    times = {'mc_list': [], 'mc_mat': []}
    for seed in SEEDS:
        g_list, src = build_graph('list',   n, m, seed)
        g_mat,  _   = build_graph('matrix', n, m, seed)
        times['mc_list'].append(time_algo(monte_carlo, g_list, src, T_FIXED, X_SIM))
        times['mc_mat'].append( time_algo(monte_carlo, g_mat,  src, T_FIXED, X_SIM))
    results_dense['mc_list'].append((n, sum(times['mc_list']) / len(SEEDS)))
    results_dense['mc_mat'].append( (n, sum(times['mc_mat'])  / len(SEEDS)))
    print(f"  n={n}: mc_list={results_dense['mc_list'][-1][1]:.4f}s  mc_mat={results_dense['mc_mat'][-1][1]:.4f}s")

for n in N_VALS_DENSE_DP:
    m = max(1, n * (n - 1) // 4)
    times = {'dp_list': [], 'dp_mat': []}
    for seed in SEEDS:
        g_list, src = build_graph('list',   n, m, seed)
        g_mat,  _   = build_graph('matrix', n, m, seed)
        times['dp_list'].append(time_algo(task_b, g_list, src, T_FIXED))
        times['dp_mat'].append( time_algo(task_b, g_mat,  src, T_FIXED))
    results_dense['dp_list'].append((n, sum(times['dp_list']) / len(SEEDS)))
    results_dense['dp_mat'].append( (n, sum(times['dp_mat'])  / len(SEEDS)))
    print(f"  n={n}: dp_list={results_dense['dp_list'][-1][1]:.4f}s  dp_mat={results_dense['dp_mat'][-1][1]:.4f}s")

# ------------------------------------------------------------------
# Experiment 3 — runtime vs T, fixed n=50 sparse graph
# ------------------------------------------------------------------
print("\nRunning Experiment 3: runtime vs T (n=50, sparse) ...")

N_FIXED = 50
M_FIXED = 2 * N_FIXED
T_VALS  = [2, 5, 10, 15, 20]

results_T = {k: [] for k in ['mc_list', 'mc_mat', 'dp_list', 'dp_mat']}

for T in T_VALS:
    times = {k: [] for k in results_T}
    for seed in SEEDS:
        g_list, src = build_graph('list',   N_FIXED, M_FIXED, seed)
        g_mat,  _   = build_graph('matrix', N_FIXED, M_FIXED, seed)
        times['mc_list'].append(time_algo(monte_carlo, g_list, src, T, X_SIM))
        times['mc_mat'].append( time_algo(monte_carlo, g_mat,  src, T, X_SIM))
        times['dp_list'].append(time_algo(task_b,      g_list, src, T))
        times['dp_mat'].append( time_algo(task_b,      g_mat,  src, T))
    for k in results_T:
        results_T[k].append((T, sum(times[k]) / len(SEEDS)))
    print(f"  T={T}: mc_list={results_T['mc_list'][-1][1]:.4f}s  dp_list={results_T['dp_list'][-1][1]:.4f}s")

# ------------------------------------------------------------------
# Plot helpers
# ------------------------------------------------------------------
STYLE = {
    'mc_list': dict(color='#e15759', marker='o', linestyle='-',  label='Monte Carlo + list'),
    'mc_mat':  dict(color='#f28e2b', marker='s', linestyle='--', label='Monte Carlo + matrix'),
    'dp_list': dict(color='#4e79a7', marker='^', linestyle='-',  label='DP + list'),
    'dp_mat':  dict(color='#76b7b2', marker='D', linestyle='--', label='DP + matrix'),
}

def extract(data): return zip(*data) if data else ([], [])


# ------------------------------------------------------------------
# Figure 1 — sparse graph runtime vs n
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=False)

ax = axes[0]
for key in ['mc_list', 'mc_mat']:
    xs, ys = extract(results_sparse[key])
    ax.plot(list(xs), list(ys), **STYLE[key])
ax.set_title('Monte Carlo — sparse graph (m ≈ 2n)', fontsize=11)
ax.set_xlabel('Number of vertices (n)')
ax.set_ylabel('Runtime (seconds)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[1]
for key in ['dp_list', 'dp_mat']:
    xs, ys = extract(results_sparse[key])
    ax.plot(list(xs), list(ys), **STYLE[key])
ax.set_title('Dynamic programming — sparse graph (m ≈ 2n)', fontsize=11)
ax.set_xlabel('Number of vertices (n)')
ax.set_ylabel('Runtime (seconds)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

fig.suptitle('Figure 1: Runtime vs n, sparse graph, T=10, X=100 simulations (avg of 3 seeds)', fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(VISUALS_DIR, 'task_c_fig1_sparse.png'), dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved task_c_fig1_sparse.png")

# ------------------------------------------------------------------
# Figure 2 — dense graph runtime vs n
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

ax = axes[0]
for key in ['mc_list', 'mc_mat']:
    xs, ys = extract(results_dense[key])
    ax.plot(list(xs), list(ys), **STYLE[key])
ax.set_title('Monte Carlo — dense graph (m ≈ n²/4)', fontsize=11)
ax.set_xlabel('Number of vertices (n)')
ax.set_ylabel('Runtime (seconds)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[1]
for key in ['dp_list', 'dp_mat']:
    xs, ys = extract(results_dense[key])
    ax.plot(list(xs), list(ys), **STYLE[key])
ax.set_title('Dynamic programming — dense graph (m ≈ n²/4)', fontsize=11)
ax.set_xlabel('Number of vertices (n)')
ax.set_ylabel('Runtime (seconds)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

fig.suptitle('Figure 2: Runtime vs n, dense graph, T=10, X=100 simulations (avg of 3 seeds)', fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(VISUALS_DIR, 'task_c_fig2_dense.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved task_c_fig2_dense.png")

# ------------------------------------------------------------------
# Figure 3 — runtime vs T
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
for key in ['mc_list', 'mc_mat', 'dp_list', 'dp_mat']:
    xs, ys = extract(results_T[key])
    ax.plot(list(xs), list(ys), **STYLE[key])
ax.set_title('Runtime vs planning horizon T  (n=50, sparse, X=100 simulations)', fontsize=11)
ax.set_xlabel('Time horizon (T)')
ax.set_ylabel('Runtime (seconds)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(VISUALS_DIR, 'task_c_fig3_T.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved task_c_fig3_T.png")

print("\nAll experiments complete. Plots saved to visuals/")
