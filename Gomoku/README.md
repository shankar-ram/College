# Implementation of Five-in-a-Row Game by Monte Carlo Tree Search
MCTS for the GoMoKu Game. With optimizations to boost the simulation speed and handcraft features added (could be turned off by setting strategy to False when calling the functions `MCTSearch` or `multiThreadingMCTS`).

This program could achieve a competitive level on size 8 * 8 board and could avoid losing at all game without any handcraft strategies on size 6 * 6 board with at least 5s simulation time on the single thread version.

1. To run the command line version, use command `python main.py`.
2. Run GUI version, call command `python main_GUI.py`.
