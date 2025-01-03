import argparse
import os
from preprocess import preprocess_code
from ml_optimizer import CodeOptimizerDQL
from benchmark import benchmark_performance

def main():
    parser = argparse.ArgumentParser(description="RefineML - Intelligent Code Optimization Platform")
    parser.add_argument('--input', type=str, required=True, help="Path to the input code file.")
    parser.add_argument('--language', type=str, default='Python', help="Programming language of the code (default: Python).")
    parser.add_argument('--output', type=str, required=True, help="Path to save the optimized code file.")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[ERROR] File {args.input} does not exist.")
        return

    try:
        # Preprocess the input code
        preprocessed_code = preprocess_code(args.input, args.language)

        # Initialize the optimizer and optimize the code
        optimizer = CodeOptimizerDQL(language=args.language)
        suggestions, optimized_code = optimizer.optimize_code(preprocessed_code)

        # Save the optimized code
        with open(args.output, 'w') as output_file:
            output_file.write(optimized_code)

        # Print optimization suggestions
        print("\n=== Optimization Suggestions ===")
        for suggestion in suggestions:
            print(f"- {suggestion}")

        # Benchmark the performance
        print("\n=== Benchmark Results ===")
        benchmark_results = benchmark_performance(args.input, optimized_code, args.language)
        print(f"Original Execution Time: {benchmark_results['original_time']:.4f} seconds")
        print(f"Optimized Execution Time: {benchmark_results['optimized_time']:.4f} seconds")
        print(f"Performance Improvement: {benchmark_results['performance_gain']:.2f}%")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    main()
