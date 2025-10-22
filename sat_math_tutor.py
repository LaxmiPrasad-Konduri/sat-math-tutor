# sat_math_tutor.py — SAT Math Tutor
# Author: LaxmiPrasad Konduri
# Description: Generates SAT-style math problems and tracks progress.

import random
import pandas as pd

# Initialize score tracking
results = pd.DataFrame(columns=['Problem', 'Your Answer', 'Correct Answer', 'Result'])

def generate_problem():
    """Generate a simple SAT-style math problem."""
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(['+', '-', '*', '/'])
    
    if op == '/':
        a *= b  # ensure divisible for integer answer

    problem = f"{a} {op} {b}"
    answer = round(eval(problem), 2)
    return problem, answer

def main():
    print("Welcome to SAT Math Tutor!\n")
    num_questions = int(input("How many questions do you want to try? "))
    
    for i in range(num_questions):
        problem, answer = generate_problem()
        print(f"Problem {i+1}: {problem}")
        user_answer = float(input("Your answer: "))
        result = "Correct" if user_answer == answer else "Incorrect"
        
        # Save to results DataFrame
        global results
        results.loc[len(results)] = [problem, user_answer, answer, result]
        
        print(f"{result}! Correct answer: {answer}\n")
    
    # Show summary
    correct_count = results['Result'].value_counts().get('Correct', 0)
    print(f"You answered {correct_count}/{num_questions} correctly.")

    # Optionally, save results
    save = input("Save your results to CSV? (y/n): ").lower()
    if save == 'y':
        results.to_csv('sat_math_results.csv', index=False)
        print("Results saved to sat_math_results.csv")

if __name__ == "__main__":
    main()
