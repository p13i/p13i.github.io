---
layout: post
title: Minimax in C#
date: 2020-03-06
description: "Implemented for any board game via generics"
image: "https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png"
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/BoardGameAI/blob/master/Core/MinimaxPlayer.cs#L14
---

I wrote this for "fun"

```csharp
(Move<TToken>, int) Minimax(
    (Move<TToken>, IMinimaxGame<TToken>) moveAndPosition,
    int depth,
    int alpha,
    int beta,
    Player<TToken> currentPlayer,
    bool maximizingCurrentPlayer) {
    (Move<TToken> move, IMinimaxGame<TToken> game) = moveAndPosition;

    (Move<TToken> bestMove, int bestEval) = (default, default);

    if (game.IsGameOver(out _) || depth == 0)
    {
        int evaluation = game.Evaluation(currentPlayer);

        (bestMove, bestEval) = (move, evaluation);
    }
    else if (maximizingCurrentPlayer)
    {
        int maxEval = int.MinValue;
        Move<TToken> maxMove = Move<TToken>.Default;

        foreach ((Move<TToken> childMove, IMinimaxGame<TToken> childGame) in game.GetChildGameStates())
        {
            (Move<TToken> moveResult, int evalResult) = Minimax((childMove, childGame), depth - 1, alpha, beta, (currentPlayer), maximizingCurrentPlayer: false);

            if (evalResult > maxEval)
            {
                maxMove = childMove;
                maxEval = evalResult;
            }

            alpha = Math.Max(alpha, evalResult);
            if (beta <= alpha)
            {
                break;
            }
        }

        (bestMove, bestEval) = (maxMove, maxEval);
    }
    else
    {
        int minEval = int.MaxValue;
        Move<TToken> minMove = Move<TToken>.Default;

        foreach ((Move<TToken> childMove, IMinimaxGame<TToken> childGame) in game.GetChildGameStates())
        {
            (Move<TToken> moveResult, int evalResult) = Minimax((childMove, childGame), depth - 1, alpha, beta, (currentPlayer), maximizingCurrentPlayer: true);

            if (evalResult < minEval)
            {
                minMove = childMove;
                minEval = evalResult;
            }

            beta = Math.Min(beta, evalResult);
            if (beta <= alpha)
            {
                break;
            }
        }

        (bestMove, bestEval) = (minMove, minEval);
    }

    return (bestMove, bestEval);
}
```
