---
layout: post
title: "Recursive Backtracking in C#"
date: 2021-04-12
description: "Fun :)"
image: https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/CSP/blob/master/Source/CSP/Solvers.cs#L39-L71
---

I wrote this for "fun" after taking our intro AI class.

```csharp
IAssignment RecursiveBacktracking(CSP csp, IAssignment assignment)
{
    NumberOfSteps++;

    if (NumberOfSteps > TimeoutNumberOfSteps)
    {
        throw new Exception($"Timed out after {TimeoutNumberOfSteps} steps.");
    }
    
    if (assignment.IsComplete())
    {
        return assignment;
    }

    string variable = SelectVariableMethod(assignment, csp);
    foreach (int value in OrderValuesMethod(assignment, csp, variable))
    {
        if (assignment.IsVariableValueConsistent(variable, value))
        {
            assignment.Assign(variable, value);

            IAssignment result = RecursiveBacktracking(csp, assignment);

            if (result != default(IAssignment))
            {
                return result;
            }
            
            assignment.Unassign(variable);
        }
    }
    return null;
}
```