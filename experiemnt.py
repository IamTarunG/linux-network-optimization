import subprocess
import matplotlib.pyplot as plt
import time

def set_kernel_buffers(size_bytes):
    params = {
        "net.core.rmem_max": size_bytes,
        "net.core.wmem_max": size_bytes,
        "net.ipv4.tcp_rmem": f"4096 87380 {size_bytes}",
        "net.ipv4.tcp_wmem": f"4096 65536 {size_bytes}",
        "net.ipv4.tcp_window_scaling": 1
    }
    
    for param, value in params.items():
        subprocess.run(['sudo', 'sysctl', '-w', f'{param}={value}'], check=True)

def run_benchmark():
    result = subprocess.run(['./profiler/target/release/profiler'], capture_output=True, text=True)
    return [int(x) for x in result.stdout.splitlines() if x.strip().isdigit()]

def main():
    print("Testing with Restricted Buffers...")
    set_kernel_buffers(65536) 
    data_small = run_benchmark()

    print("Testing with Optimized Buffers...")
    set_kernel_buffers(16777216) 
    data_large = run_benchmark()


    plt.figure(figsize=(12, 6))
    plt.plot(data_small, label='Restricted Buffers (64KB)', color='tab:red', linestyle='--')
    plt.plot(data_large, label='DC Optimized Buffers (16MB)', color='tab:green')
    
    plt.title('Impact of Full-Stack Kernel Buffer Tuning on Latency')
    plt.xlabel('Connection Probe #')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('full_stack_results.png')
    print("Experiment complete! Check 'full_stack_results.png'")

if __name__ == "__main__":
    main()
