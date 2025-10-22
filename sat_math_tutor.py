# sat_math_tutor.py — SAT Math Tutor
# Author: LaxmiPrasad Konduri
# Description: Generates SAT-style math problems and tracks progress.

import random
import argparse
import pandas as pd
import math
import time
from datetime import datetime

# Initialize score tracking
results = pd.DataFrame(columns=['Problem', 'Your Answer', 'Correct Answer', 'Result', 'Timestamp', 'Duration'])


def generate_arithmetic():
    """Generate a simple arithmetic SAT-style problem."""
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(['+', '-', '*', '/'])

    if op == '/':
        a *= b  # ensure divisible for integer answer

    problem = f"{a} {op} {b}"
    answer = round(eval(problem), 2)
    return problem, answer


def generate_algebra():
    """Generate a simple algebra problem and return (problem_str, answer).

    Types generated:
    - One-step: x + b = c  (solve for x)
    - Multiplicative: a*x = b
    - Two-step: a*x + b = c
    We generate these by first choosing an integer solution x and building the equation
    so answers remain integer whenever possible.
    """
    typ = random.choice(['one-step', 'mult', 'two-step', 'fractional', 'quadratic'])

    # One-step: x + b = c
    if typ == 'one-step':
        x = random.randint(-10, 20)
        b = random.randint(-10, 20)
        c = x + b
        problem = f"Solve for x: x + {b} = {c}"
        answer = float(x)
        return problem, answer

    # Multiplicative: a x = b
    if typ == 'mult':
        x = random.randint(-10, 20)
        a = random.randint(1, 12)
        b = a * x
        problem = f"Solve for x: {a}x = {b}"
        answer = float(x)
        return problem, answer

    # Two-step: a x + b = c
    if typ == 'two-step':
        x = random.randint(-10, 20)
        a = random.randint(1, 12)
        b = random.randint(-10, 20)
        c = a * x + b
        problem = f"Solve for x: {a}x + {b} = {c}"
        answer = float(x)
        return problem, answer

    # Fractional linear equations: produce a non-integer solution
    if typ == 'fractional':
        # choose numerator/denominator for solution
        num = random.randint(-10, 20)
        den = random.randint(2, 12)
        x = num / den
        a = random.randint(1, 12)
        b = random.randint(-10, 20)
        c = a * x + b
        # present c with up to 4 decimals if not integer
        c_str = f"{c:.4f}" if abs(c - round(c)) > 1e-9 else str(int(round(c)))
        problem = f"Solve for x: {a}x + {b} = {c_str}"
        answer = float(x)
        return problem, answer

    # Quadratic: generate factorable quadratics with integer roots r1, r2
    if typ == 'quadratic':
        r1 = random.randint(-6, 6)
        r2 = random.randint(-6, 6)
        # quadratic x^2 - (r1+r2)x + r1*r2 = 0 -> we'll present as x^2 + sx + p = 0
        s = -(r1 + r2)
        p = r1 * r2

        def fmt_coeff(v):
            if v == 0:
                return ''
            if v > 0:
                return f'+ {v}'
            return f'- {abs(v)}'

        s_part = fmt_coeff(s)
        p_part = fmt_coeff(p)
        problem = f"Solve for x: x^2 {s_part} {p_part} = 0".replace('  ', ' ')
        answer = (float(r1), float(r2))
        return problem, answer


def generate_problem(include_algebra=False):
    """Generate either an arithmetic or algebra problem depending on flag."""
    if include_algebra and random.random() < 0.5:
        return generate_algebra()
    return generate_arithmetic()


def is_correct(user_answer, correct_answer, tol=1e-6):
    # If correct_answer is a tuple/list (e.g., quadratic roots), accept comma-separated answers in any order
    if isinstance(correct_answer, (tuple, list)):
        # parse user_answer as CSV of numbers
        if isinstance(user_answer, str):
            parts = [p.strip() for p in user_answer.split(',') if p.strip()]
        elif isinstance(user_answer, (list, tuple)):
            parts = list(map(str, user_answer))
        else:
            return False

        if len(parts) != len(correct_answer):
            return False

        try:
            ua_nums = sorted([float(p) for p in parts])
            ca_nums = sorted([float(x) for x in correct_answer])
        except Exception:
            return False

        return all(abs(a - b) <= tol for a, b in zip(ua_nums, ca_nums))

    try:
        ua = float(user_answer)
    except Exception:
        return False
    return abs(ua - float(correct_answer)) <= tol


def run_quiz(num_questions=10, include_algebra=False, auto=False, save_results=True):
    global results
    results = pd.DataFrame(columns=['Problem', 'Your Answer', 'Correct Answer', 'Result', 'Timestamp', 'Duration'])

    for i in range(num_questions):
        problem, answer = generate_problem(include_algebra=include_algebra)
        print(f"Problem {i+1}: {problem}")
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        # If this is an algebra problem (our generator prefixes with 'Solve for x:')
        if problem.strip().startswith('Solve for x:') and not auto:
            eq = problem.replace('Solve for x:', '').strip()
            # Try to parse patterns: x + b = c  |  ax = b  |  ax + b = c
            # Normalize spaces
            eq_n = eq.replace(' ', '')
            user_answer = None

            # one-step: x+b=c
            if eq_n.startswith('x+') or eq_n.startswith('x-'):
                # find b and c
                try:
                    left, right = eq.split('=')
                    # left like 'x+5' or 'x+-4'
                    b_str = left.split('x')[1]
                    b = int(b_str)
                    c = int(right)
                    # interactive two-step: ask intermediate then final
                    inter = c - b
                    print(f"Step 1: Subtract {b} from both sides. What is the new right-hand side?")
                    while True:
                        raw1 = input("Answer: ")
                        try:
                            # allow floats if intermediate is fractional
                            val1 = float(raw1) if ('.' in raw1 or 'e' in raw1.lower()) else int(raw1)
                        except ValueError:
                            print("Please enter a number.")
                            continue
                        # compare with tolerance for floats
                        if abs(float(val1) - float(inter)) < 1e-6:
                            print("Good. Now what is x?")
                            break
                        else:
                            print(f"Not quite. {raw1} is incorrect. Try again.")

                    while True:
                        raw2 = input("x = ")
                        try:
                            val2 = float(raw2)
                        except ValueError:
                            print("Please enter a number.")
                            continue
                        user_answer = float(val2)
                        break
                except Exception:
                    # fallback to simple prompt
                    raw = input("Your answer: ")
                    try:
                        user_answer = float(raw)
                    except ValueError:
                        user_answer = raw

            # multiplicative: ax=b
            elif 'x=' in eq_n or eq_n.count('x') == 1 and ('=' in eq_n):
                # try to detect pattern like '6x=12' or '12=6x'
                try:
                    if eq_n.count('=') == 1 and 'x' in eq_n:
                        left, right = eq_n.split('=')
                        if 'x' in left:
                            a_str = left.split('x')[0]
                            a = int(a_str) if a_str not in ('', '+') else 1
                            b = int(right)
                        else:
                            # right contains x
                            a_str = right.split('x')[0]
                            a = int(a_str) if a_str not in ('', '+') else 1
                            b = int(left)

                        # division might produce a non-integer; show decimal guidance
                        print(f"Divide both sides by {a}. What is {b} / {a}? (round to 4 decimals if needed)")
                        while True:
                            raw1 = input("Answer: ")
                            try:
                                val1 = float(raw1)
                            except ValueError:
                                print("Please enter a number.")
                                continue
                            if abs(val1 - (b / a)) < 1e-6:
                                user_answer = float(val1)
                                break
                            else:
                                print("Incorrect. Try again.")
                    else:
                        raw = input("Your answer: ")
                        try:
                            user_answer = float(raw)
                        except ValueError:
                            user_answer = raw
                except Exception:
                    raw = input("Your answer: ")
                    try:
                        user_answer = float(raw)
                    except ValueError:
                        user_answer = raw

            # two-step: ax+b=c
            elif 'x+' in eq_n or 'x-' in eq_n or 'x' in eq_n:
                try:
                    left, right = eq.split('=')
                    # left like '6x+5' or '6x-3'
                    if 'x' in left:
                        a_part = left.split('x')[0]
                        b_part = left.split('x')[1]
                        a = int(a_part) if a_part not in ('', '+') else 1
                        b = int(b_part)
                        c = int(right)
                    else:
                        # fallback
                        raise ValueError

                    # Step 1: subtract b
                    inter = c - b
                    print(f"Step 1: Subtract {b} from both sides. What is the new right-hand side? (may be fractional)")
                    while True:
                        raw1 = input("Answer: ")
                        try:
                            val1 = float(raw1)
                        except ValueError:
                            print("Please enter an integer.")
                            continue
                        if abs(float(val1) - float(inter)) < 1e-6:
                            print(f"Good. Step 2: Divide by {a}. What is {inter} / {a}? (round to 4 decimals if needed)")
                            break
                        else:
                            print("Not quite. Try again.")

                    while True:
                        raw2 = input("Answer: ")
                        try:
                            val2 = float(raw2)
                        except ValueError:
                            print("Please enter a number.")
                            continue
                        user_answer = float(val2)
                        break
                except Exception:
                    raw = input("Your answer: ")
                    try:
                        user_answer = float(raw)
                    except ValueError:
                        user_answer = raw

            else:
                raw = input("Your answer: ")
                try:
                    user_answer = float(raw)
                except ValueError:
                    user_answer = raw

        else:
            # non-algebra or auto mode: existing behavior
            if auto:
                user_answer = answer
                print(f"Your answer: {user_answer}")
            else:
                raw = input("Your answer: ")
                try:
                    user_answer = float(raw)
                except ValueError:
                    user_answer = raw

        result = "Correct" if is_correct(user_answer, answer) else "Incorrect"

        duration = time.time() - start_time
        results.loc[len(results)] = [problem, user_answer, answer, result, timestamp, duration]
        print(f"{result}! Correct answer: {answer}\n")

    # Show summary
    correct_count = results['Result'].value_counts().get('Correct', 0)
    print(f"You answered {correct_count}/{num_questions} correctly.")

    if save_results and not auto:
        save = input("Save your results to CSV? (y/n): ").lower()
        if save == 'y':
            results.to_csv('sat_math_results.csv', index=False)
            print("Results saved to sat_math_results.csv")
    elif save_results and auto:
        # In auto mode save without prompting
        results.to_csv('sat_math_results.csv', index=False)
        print("Results saved to sat_math_results.csv")


def main():
    parser = argparse.ArgumentParser(description='SAT Math Tutor')
    parser.add_argument('--count', '-c', type=int, default=None,
                        help='Number of questions to ask (if omitted, prompts interactively)')
    parser.add_argument('--include-algebra', action='store_true',
                        help='Include algebra-style problems (solve for x) in the quiz')
    parser.add_argument('--auto', action='store_true',
                        help='Auto-answer questions with the correct answer (useful for testing)')
    args = parser.parse_args()

    print("Welcome to SAT Math Tutor!\n")

    if args.count is None:
        num_questions = int(input("How many questions do you want to try? "))
    else:
        num_questions = args.count

    run_quiz(num_questions=num_questions, include_algebra=args.include_algebra, auto=args.auto,
             save_results=True)


if __name__ == "__main__":
    main()
