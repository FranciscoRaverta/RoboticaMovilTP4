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
    parser.add_argument(
        '--num_particles', type=int, default=100,
        help='number of particles (particle filter only)')

    return parser

def plot_errors(r, mean_pos, anees):
    fig, ax = plt.subplots()
    ax.plot(r,mean_pos, c='red')
    ax.plot(r, anees, c='blue')
    ax.set(xlabel='r', ylabel='Errors',
       title='Mean Position Error (red) and ANEES (blue)')
    ax.grid()
    plt.show()
    return

def scatter_errors(mean_pos, anees, r):
    fig, ax = plt.subplots()
    x_positions = range(len(r))
    ax.plot(x_positions,mean_pos, c='red')
    ax.plot(x_positions, anees, c='blue')
    plt.xticks(x_positions, r, rotation=0)
    ax.set(xlabel='r', ylabel='Errors',
       title='Mean Position Error (red) and ANEES (blue)')
    ax.grid()
    plt.show()
    return


def scatter_errors_compare_mean(mean_20, mean_50, mean_500, r):
    fig, ax = plt.subplots()
    x_positions = range(len(r))
    ax.plot(x_positions,mean_20, c='red')
    ax.plot(x_positions, mean_50, c='blue')
    ax.plot(x_positions, mean_500, c='black')
    plt.xticks(x_positions, r, rotation=0)
    ax.set(xlabel='r', ylabel='Errors',
       title='Mean Position Error for 20 (red), 50 (blue) and 500 (black) particles')
    ax.grid()
    plt.show()
    return

def scatter_errors_compare_anees(anees_20, anees_50, anees_500, r):
    fig, ax = plt.subplots()
    x_positions = range(len(r))
    ax.plot(x_positions,anees_20, c='red')
    ax.plot(x_positions, anees_50, c='blue')
    ax.plot(x_positions, anees_500, c='black')
    plt.xticks(x_positions, r, rotation=0)
    ax.set(xlabel='r', ylabel='Errors',
       title='ANEES for 20 (red), 50 (blue) and 500 (black) particles')
    ax.grid()
    plt.show()
    return


def calculate_errors(filter_type, r, seeds, num_particles = 100):
    mean_pos = []
    mean_maha = []
    anees = []

    for r_idx in range(len(r)):
        mean_pos_r = []
        mean_maha_r = []
        anees_r = []

        for i in range(10):
            if filter_type == "ekf":
                command = f"python3 localization.py ekf --data-factor {r[r_idx]} --filter-factor {r[r_idx]} --seed {seeds[i]}"
            elif filter_type == "pf":
                command = f"python3 localization.py pf --data-factor {r[r_idx]} --filter-factor {r[r_idx]} --seed {seeds[i]} --num-particles {num_particles}"
                print(command), 
                print('-'*40)
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
    return mean_pos, mean_maha, anees

if __name__ == '__main__':
    args = setup_parser().parse_args()

    
    r = [1/64, 1/16, 1/4, 4, 16, 64]
    #r = [1, 2, 4, 8, 16, 64]
    seeds = np.random.randint(0, 100, 10)   # We use the same seeds for all r values, to be able to compare them
    
    if args.filter_type == "ekf":
        print("EKF")
        mean_pos_ekf, mean_maha_ekf, anees_ekf = calculate_errors(args.filter_type, r, seeds, args.num_particles)
        if args.plot:
            scatter_errors(mean_pos_ekf, anees_ekf, r)
    elif args.filter_type == "pf":
        print("PF - 20 particles")
        mean_pos_pf_20, mean_maha_pf_20, anees_ekf_20 = calculate_errors(args.filter_type, r, seeds, 20)

        print("PF - 50 particles")
        mean_pos_pf_50, mean_maha_pf_50, anees_ekf_50 = calculate_errors(args.filter_type, r, seeds, 50)

        print("PF - 500 particles")
        mean_pos_pf_500, mean_maha_pf_500, anees_ekf_500 = calculate_errors(args.filter_type, r, seeds, 500)
        
        if args.plot:
            scatter_errors(mean_pos_pf_20, anees_ekf_20, r)
            scatter_errors(mean_pos_pf_50, anees_ekf_50, r)
            scatter_errors(mean_pos_pf_500, anees_ekf_500, r)
            scatter_errors_compare_mean(mean_pos_pf_20,mean_pos_pf_50,mean_pos_pf_500,r)
            scatter_errors_compare_anees(anees_ekf_20,anees_ekf_50,anees_ekf_500,r)

    


