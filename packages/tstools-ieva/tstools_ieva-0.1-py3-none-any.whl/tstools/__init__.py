from os.path import basename
filename = basename(__file__)
print(f"Hello from {filename}")

from .moments import get_mean_and_var
from .vis import plot_trajectory_subset
from .vis import plot_histogram
