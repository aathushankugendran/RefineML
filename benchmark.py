# scripts/benchmark.py
import subprocess
import time
import os

def execute_code(file_path, language='Python'):
    """
    Executes the given code file and measures its runtime.
    Supports Python and C languages.
    Returns the execution time in seconds.
    """
    start_time = time.time()
    try:
        if language == 'Python':
            # Run Python script
            subprocess.run(["python", file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif language == 'C':
            # Compile and run C code
            executable = file_path.replace('.c', '')
            subprocess.run(["gcc", file_path, "-o", executable], check=True)
            subprocess.run([f"./{executable}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            raise ValueError(f"Unsupported language: {language}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error while executing code: {e.stderr.decode()}")
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
    return execution_time

def benchmark_performance(original_code_path, optimized_code, language='Python'):
    """
    Benchmarks the performance of original and optimized code.
    1. Saves the optimized code temporarily.
    2. Executes both versions and measures execution time.
    """
    print("Benchmarking performance...")
    optimized_code_path = "temp_optimized_code" + (".py" if language == 'Python' else ".c")
    
    # Save the optimized code to a temporary file
    with open(optimized_code_path, 'w') as file:
        file.write(optimized_code)
    
    # Measure runtime of the original code
    print("Running original code...")
    original_time = execute_code(original_code_path, language)
    print(f"Original Code Execution Time: {original_time:.4f} seconds")

    # Measure runtime of the optimized code
    print("Running optimized code...")
    optimized_time = execute_code(optimized_code_path, language)
    print(f"Optimized Code Execution Time: {optimized_time:.4f} seconds")

    # Clean up temporary optimized file
    if os.path.exists(optimized_code_path):
        os.remove(optimized_code_path)
    
    # Compare performance
    performance_gain = ((original_time - optimized_time) / original_time) * 100 if original_time > 0 else 0
    print(f"Performance Improvement: {performance_gain:.2f}%")
    return {
        "original_time": original_time,
        "optimized_time": optimized_time,
        "performance_gain": performance_gain
    }

if __name__ == '__main__':
    import argparse
    from preprocess import load_code

    parser = argparse.ArgumentParser(description="Benchmark runtime performance of code.")
    parser.add_argument('--input', type=str, required=True, help="Path to the original code file.")
    parser.add_argument('--optimized', type=str, required=True, help="Path to the optimized code content file.")
    parser.add_argument('--language', type=str, default='Python', help="Programming language (default: Python).")
    args = parser.parse_args()

    try:
        # Load optimized code content
        optimized_code = load_code(args.optimized)
        # Benchmark performance
        metrics = benchmark_performance(args.input, optimized_code, args.language)
        print("Benchmark Results:")
        print(f"Original Time: {metrics['original_time']:.4f} seconds")
        print(f"Optimized Time: {metrics['optimized_time']:.4f} seconds")
        print(f"Performance Improvement: {metrics['performance_gain']:.2f}%")
    except Exception as e:
        print(f"Error: {e}")