from sat_math_tutor import generate_arithmetic, generate_algebra, is_correct


def test_arithmetic_generation():
    problem, answer = generate_arithmetic()
    assert isinstance(problem, str)
    # simple eval check (replace 'x' if present)
    assert isinstance(answer, (int, float))


def test_algebra_generation():
    problem, answer = generate_algebra()
    assert problem.startswith('Solve for x:')
    assert isinstance(answer, float)


def test_fractional_generation():
    # force multiple tries until a fractional appears
    found = False
    for _ in range(50):
        problem, answer = generate_algebra()
        if 'x^2' not in problem and (abs(answer - round(answer)) > 1e-9):
            found = True
            break
    assert found, "No fractional linear equation generated in attempts"


def test_quadratic_generation_and_check():
    found = False
    for _ in range(100):
        problem, answer = generate_algebra()
        if isinstance(answer, tuple) or (isinstance(answer, (list, tuple))):
            found = True
            # answer is (r1, r2)
            r1, r2 = answer
            # check correct when given as 'r1,r2' in any order
            s1 = f"{r1},{r2}"
            s2 = f"{r2},{r1}"
            assert is_correct(s1, answer)
            assert is_correct(s2, answer)
            break
    assert found, "No quadratic generated in attempts"


def test_is_correct():
    assert is_correct('3', 3)
    assert is_correct(3.0, 3)
    assert is_correct('3.0000001', 3, tol=1e-5) is True
    assert not is_correct('abc', 5)
