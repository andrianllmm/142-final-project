# Lab 1

## Next Palindrome

Given an integer `n`, find the next smallest palindrome integer.

**Palindrome** – A number that reads the same backward as forward (e.g., 101, 212, 999).

### Examples

- Input: 5 → Next Palindrome = 6
- Input: 18 → Next Palindrome = 22
- Input: 934 → Next Palindrome = 939

---

## Input / Output

- Read input from the command line.
- The first input is the number of test cases, denoted as `X`.
- This is followed by `X` integers.
- For each integer, print the next smallest palindrome integer.

### Example Input

```
5
0
18
934
5
757
```

### Expected Output

```
1
22
939
6
767
```

---

## Files for Submission

1. **Python Program**
   The implemented program must be written in Python.
   The program must match the pseudocode provided in Item #2.

2. **Report (PDF format)**

### a. Write a Pseudocode

- The PDF file must contain the pseudocode of your chosen implementation.
- The pseudocode may be expressed in natural language as a list of steps.
- Do not use a specific programming language in writing the pseudocode.
- For each step or block of code:
  - Specify the cost.
  - Specify the estimated number of timesteps of execution.

- Using these, compute the **worst-case Big-O running time complexity** of the program.

### b. Analyze the Performance of the Code Given the Structure of an Input

1. What is the **best-case complexity** of your program?
   - What input structure results in the best case?

2. What is the **worst-case complexity** of the program?
   - What input structure results in the worst case?

### c. Check the Correctness and Performance of Your Program Using the Checker

The following files are provided:

1. `small_input` – contains 5 inputs.
   - The first element/value is the number of items/cases.

2. `small_solution` – contains the solution to `small_input`.
3. `full_input` – contains 100,000 inputs.
   - The first element/value is the number of items/cases.

4. `full_solution` – contains the solution to `full_input`.

---

## Usage of `checker.pyc`

```
python checker.pyc <option>
```

`<option>`: `small`, `full`

If your solutions (Next Palindrome) match the given solution, then zero errors are found.

The output of your program will be found in:

```
data/output
```

---

## Performance Measurement

Measure the elapsed running time of your program when executed using:

1. Small input
2. Full input

You may use Python’s `time` module to compute this information.
