import numpy as np
import time
import threading
import multiprocessing
import matplotlib.pyplot as plt

# --- TASK 2.2: THE COMPUTATIONAL WORK ---
def matrix_task(size):
    # Generates two random large matrices and multiplies them
    # This is a CPU-intensive task to test parallel performance
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)
    np.dot(a, b)

# --- EXECUTION MODE 1: SEQUENTIAL ---
def run_sequential(size):
    # Runs the task on a single processor core from start to finish
    start = time.time()
    matrix_task(size)
    return time.time() - start # Returns total time taken

# --- EXECUTION MODE 2: MULTITHREADING ---
def run_threaded(size, num_threads):
    # Splits the workload into multiple threads within the same process
    threads = []
    start = time.time()
    for _ in range(num_threads):
        # Assign a portion of the task to each thread
        t = threading.Thread(target=matrix_task, args=(size // num_threads,))
        threads.append(t)
        t.start() # Starts the thread
    for t in threads:
        t.join() # Waits for all threads to finish before stopping the clock
    return time.time() - start

# --- EXECUTION MODE 3: MULTIPROCESSING ---
def run_multiprocessing(size, num_processes):
    # Uses multiple CPU cores simultaneously (True Parallelism)
    processes = []
    start = time.time()
    for _ in range(num_processes):
        # Creates a separate process for each core
        p = multiprocessing.Process(target=matrix_task, args=(size // num_processes,))
        processes.append(p)
        p.start() # Starts the process on a separate CPU core
    for p in processes:
        p.join() # Waits for all processes to complete
    return time.time() - start

# --- MODULE 5: PERFORMANCE VISUALIZATION ---
def plot_performance(results):
    # Extracts data for plotting
    units = [r[0] for r in results]
    seq_times = [r[1] for r in results]
    p_times = [r[2] for r in results]
    speedups = [r[3] for r in results]
    efficiencies = [r[4] for r in results]

    plt.figure(figsize=(12, 4))

    # Graph 1: Execution Time vs Number of Processes
    plt.subplot(1, 3, 1)
    plt.plot(units, p_times, marker='o', label='Parallel Time', color='blue')
    plt.axhline(y=seq_times[0], color='r', linestyle='--', label='Sequential')
    plt.title('Execution Time')
    plt.xlabel('Units (Cores)')
    plt.ylabel('Seconds')
    plt.legend()

    # Graph 2: Speedup (How much faster it is)
    plt.subplot(1, 3, 2)
    plt.plot(units, speedups, marker='s', color='green')
    plt.title('Speedup')
    plt.xlabel('Units (Cores)')
    plt.ylabel('Factor')

    # Graph 3: Efficiency (How well resources are used)
    plt.subplot(1, 3, 3)
    plt.plot(units, [e * 100 for e in efficiencies], marker='^', color='orange')
    plt.title('Efficiency (%)')
    plt.xlabel('Units (Cores)')
    plt.ylabel('Percentage')

    plt.tight_layout()
    plt.show() # Displays the graphs automatically

# --- MAIN CONTROL CENTER ---
if __name__ == "__main__":
    matrix_size = 1500 # Define workload size
    print("--- Starting Parallelism Module Evaluation ---")

    results_to_plot = [] # List to store real-time data for graphs

    # Step 1: Get Baseline (Sequential) Time
    seq_time = run_sequential(matrix_size)
    print(f"Sequential Time: {seq_time:.4f}s")

    # Add 1-unit (base) data to results
    results_to_plot.append((1, seq_time, seq_time, 1.0, 1.0))

    # Step 2: Test Parallel Performance for 2, 4, and 8 units
    for n in [2, 4, 8]:
        # Measure Multiprocessing time (Real parallelism)
        par_time = run_multiprocessing(matrix_size, n)

        # Calculate Performance Metrics
        speedup = seq_time / par_time
        efficiency = speedup / n

        # Store results for plotting
        results_to_plot.append((n, seq_time, par_time, speedup, efficiency))

        print(f"\nConfiguration: {n} Processes")
        print(f"Parallel Time: {par_time:.4f}s | Speedup: {speedup:.2f} | Efficiency: {efficiency:.2%}")

    # Step 3: Generate Graphs automatically after testing
    print("\nAll tasks finished. Generating performance graphs...")
    plot_performance(results_to_plot)
