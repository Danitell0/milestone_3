*This project has been created as part of the 42 curriculum by danmorei.*

# Codexion

## Description

**Codexion** is a concurrency project inspired by the classic *Dining Philosophers* problem.

`n` coders sit around a circular table with one USB dongle between each pair of neighbours. Each coder repeatedly **compiles**, **debugs** and **refators**. To compile, a coder needs both the dongle on their left and the one on their right. If a coder goes too long without starting a compile, they **burn out** and the simulation ends.

The goal is to keep every coder alive and reach the required number of compilations using threads and mutexes, without deadlocks, starvation or data races.

## Instructions

### Compilation

```sh
make        # build ./codexion
make clean  # remove object files
make fclean # remove object files and ./codexion
make re     # rebuild from scratch
make lint   # run norminette
```

### Usage

```sh
./codexion n_coders t_burnout t_compile t_debug t_refactor compiles_required cooldown scheduler
```

### Example

```sh
./codexion 5 800 200 200 200 5 10 edf
```

Output format:

```
<timestam_ms> <coder_id> <action>
0 1 has taken a dongle
0 1 has taken a dongle
0 1 is compiling
200 1 is debugging
400 1 is refactoring
```

## Scheduling

Coders that want to compile are pushed into a **priority queue**. A monitor thread runs an arbitration pass roughle every ms and grants dongles to requests in priority order.

- **FIFO** -> First In, First Out (arrival time, then coder ID as tie-breaaker).
- **EDF**  -> Earliest Deadline First (the coder closest to burning out goes first).

If the coder at the head of the queue can't be served yet, their dongles are **reserved** so neighbours can't keep stealing them, this will prevent starvation.

## Blocking cases handled

- **Deadlock** -> dongles are only granted in pairs by the arbiter, so no coder holds one dongle while waiting for the other.
- **Starvation** -> the head of the queue reserves its dongles and EDF will also favour the mos "at risk" coder.
- **Single coder** -> with only one dongle, the coder takesit and waits until burnout.
- **Dongle cooldown** -> released dongles stay unavailable until `now + cooldown`.
- **Clean shutdown** -> on burnout or when everyone is done, a `stop` flag is set and all waiting threads are woken up and joined.

## Thread synchronization mechanisms

- `pthread_mutex_t lock` -> protects the shared state (dongles, heap, coder counters, `stop` flag).
- `pthread_mutex_t log_lock` -> makes sure log lines are never interleaved.
- `pthread_cond cond` + `pthread_cond_timedwait` -> coders sleep untill the arbiter grants their dongles, instead of busy-waiting.
- **Monitor thread** -> checks for burnout / completion and runs the arbitration pass.

## Resources

- [Dining philosophers problem - Wikipedia](https://en.wikipedia.org/wiki/Dining_philosophers_problem)
- [POSIX threads — `man pthread_mutex_lock`, `man pthread_cond_timedwait`](https://man7.org/linux/man-pages/man3/pthread_cond_timedwait.3p.html)
- [GeeksforGeeks - Thread Management Functions in C](https://www.geeksforgeeks.org/c/thread-functions-in-c-c/)

### Use of AI

Claude by Anthropic was used in this project for the following:
- **Design** - Brainstorm design ideas for deadlock prevention and monitor timing;
- **Explaining concepts** - Pthreads and Mutex concepts;
- **Debugging** - Helped read valgrind/helgrind output;

AI was NOT used to write or generate any code.