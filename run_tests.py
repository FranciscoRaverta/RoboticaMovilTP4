import argparse
import numpy as np
import matplotlib.pyplot as plt
import subprocess


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filter_type', choices=('none', 'ekf', 'pf'),
        help='filter to use for localization')
    parser.add_argument(
        '--plot', action='store_true',
        help='turn on plotting')

    return parser

def plot_errors(r, mean_pos, anees):
    fig, ax = plt.subplots()
    ax.plot(r,mean_pos, c='red')
    ax.plot(r, anees, c='blue')
    ax.set(xlabel='r', ylabel='Errors',
       title='Position Error (red) and ANEES (blue)')
    ax.grid()
    plt.show()
    return

def scatter_errors(mean_pos, anees):
    fig, ax = plt.subplots()
    r = ["1/64", "1/16", "1/4", "4", "16", "64"]
    x_positions = range(len(r))
    ax.plot(x_positions,mean_pos, c='red')
    ax.plot(x_positions, anees, c='blue')
    plt.xticks(x_positions, r, rotation=0)
    ax.set(xlabel='r', ylabel='Errors',
       title='Position Error (red) and ANEES (blue)')
    ax.grid()
    plt.show()
    return

if __name__ == '__main__':
    args = setup_parser().parse_args()

    if args.filter_type == "ekf":
        r = [1/64, 1/16, 1/4, 4, 16, 64]
        seeds = np.random.randint(0, 100, 10)   # We use the same seeds for all r values, to be able to compare them
        mean_pos = []
        mean_maha = []
        anees = []

        for r_idx in range(len(r)):
            mean_pos_r = []
            mean_maha_r = []
            anees_r = []

            for i in range(10):
                command = f"python3 localization.py ekf --data-factor {r[r_idx]} --filter-factor {r[r_idx]} --seed {seeds[i]}"
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
                output_text = result.stdout.decode()

                output_lines = output_text.split('\n')
                start_line_index = output_lines.index("Getting results")

                values = {}
                for line in output_lines[start_line_index + 1:]:
                    if not line:
                        break  # Stop when an empty line is encountered
                    key, value = line.split(":")
                    values[key] = float(value)

                mean_pos_r.append(values.get("Mean position error"))
                mean_maha_r.append(values.get("Mean Mahalanobis error"))
                anees_r.append(values.get("ANEES"))
            mean_pos.append(np.mean(mean_pos_r))
            mean_maha.append(np.mean(mean_maha_r))
            anees.append(np.mean(anees_r))
        print("Mean Position Error: \n", mean_pos)
        print("Mean Mahalanobis Error: \n", mean_maha)
        print("ANEES: \n", anees)

        if args.plot:
            scatter_errors(mean_pos, anees)


