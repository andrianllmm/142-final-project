# Lab 2

Whenever Solenn has a movie or a teleserye, a lot of actors audition to be her leading man. The chosen actor has to meet the following criteria: his height and weight must be close to Solenn's so that they will look good together.

Since this happens often and for each project Solenn's height and weight changes, you are asked to help the producers rank the actors based on the given criteria by creating an algorithm that will solve the problem quickly. The ranking is important so that we know which actor to contact in case one actor is unavailable.

In the ranking:

- The actor with the smallest **height difference** with Solenn must be on the top of the list.
- If there are ties in the height difference, they will be evaluated based on their **weight difference** with Solenn.
- If there are still ties, the actor who **auditioned first** will be ranked higher.

**Note:** Height and weight differences are absolute.

**Example:**
If Solenn's height = 160 cm, Actor A's height = 164 cm, and Actor B's height = 156 cm, based on the height difference criterion, Actor A and Actor B should be tied (height difference of 4).

---

## Input

- You will be reading input from the command line.
- First input is the number of problems / test cases to be solved, say **N**.
- This is followed by **N** chunks of data in this format:

  1. The next input contains two numbers, Solenn's current height (in cm) and weight (in kg), separated by a single space.
  2. This is followed by a number, say **A**, which is the number of actors who auditioned to be Solenn's leading man.
  3. This is then followed by **A** lines of data for each actor formatted as:

     ```
     {name} {height in cm} {weight in kg}
     ```

     where each piece of information is separated by any nonempty number of whitespaces (not necessarily a single space).

- Assume that the input order of actors is based on who auditioned first.

---

## Output

For each problem / test case, print in one line the ascending ordering / ranking of the actors (**name only**) who auditioned to be Solenn's leading man, separated by a single space, based on:

1. Height difference
2. Weight difference
3. Audition order

---

## Example

Input:

```
1
170 60
8
Allen 168 58
Wendell 166 60
Marlon 165 60
Brian 165 60
Christopher 172 57
Rene 175 65
Mark 169 75
Kelvin 170 58
```

Output:

```
Kelvin Mark Allen Christopher Wendell Marlon Brian Rene
```

---

## Restrictions

Implement the algorithm from scratch without using any external libraries or built-in methods (except for basic input processing).

---

## Files for Submission

1. **Python code file**
2. **A report in PDF format**

### a. Write a Pseudocode

The PDF file should contain the pseudocode of your chosen implementation. The pseudocode should be expressed in natural language through a list of steps.

**Note:** Do not use a specific programming language in writing your pseudocode.

### b. Analysis of Performance

Complexity of the algorithm created on its best, worst, and average case.

**Note:** Do not include the prewritten code in your analysis

### c. Correctness of Program

Use the `checker.py` to determine correctness and run time of your program.
