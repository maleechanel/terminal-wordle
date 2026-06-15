# terminal-wordle 🟩🟨⬜

A fully playable clone of the [NYT Wordle](https://www.nytimes.com/games/wordle/index.html) game that runs entirely in your terminal — no browser, no internet, no dependencies.

```
  W O R D L E  —  Guess the 5-letter word in 6 tries

 🟩  B  🟨  R  ⬜  A  ⬜  V  🟩  E
 🟩  B  🟩  L  🟩  A  🟩  Z  🟩  E
 ░░░   ░░░   ░░░   ░░░   ░░░
 ░░░   ░░░   ░░░   ░░░   ░░░
 ░░░   ░░░   ░░░   ░░░   ░░░
 ░░░   ░░░   ░░░   ░░░   ░░░

  Q  W  E  R  T  Y  U  I  O  P
  A  S  D  F  G  H  J  K  L
  Z  X  C  V  B  N  M

  Wins: 12  Losses: 3  Streak: 4  Best: 7
```

---

## Features

- **Color-coded tiles** — green, yellow, and gray feedback after every guess
- **Live QWERTY keyboard** — tracks which letters are confirmed, misplaced, or eliminated
- **Persistent stats** — wins, losses, current streak, and best streak saved between sessions
- **800+ word list** — common English words for varied, fair gameplay
- **Zero dependencies** — pure Python 3 standard library, runs anywhere

---

## How to play

```bash
python3 wordle.py
```

**Rules:**
- Guess the secret 5-letter word in 6 tries
- Each guess must be 5 alphabetic letters
- After each guess, tiles reveal how close you were:

| Color | Meaning |
|-------|---------|
| 🟩 Green | Correct letter, correct position |
| 🟨 Yellow | Correct letter, wrong position |
| ⬜ Gray | Letter not in the word |

Press `Ctrl+C` at any time to quit. The answer will be revealed.

---

## Setup

**Requirements:** Python 3.9 or higher. No packages to install.

```bash
# Clone the repo
git clone https://github.com/maleechanel/terminal-wordle.git
cd terminal-wordle

# Run the game
python3 wordle.py
```

---

## How it works

### Scoring algorithm (two-pass)

The core of the game is `score_guess()`, which uses a **two-pass algorithm** to correctly handle duplicate letters — the same logic used by the official NYT Wordle.

**The problem with a naive approach:**

If the answer is `SPEED` and the player guesses `EERIE`, a simple letter-by-letter check would mark both E's as yellow. But the real Wordle only marks one — because only one unmatched E remains after accounting for exact matches.

**The two-pass solution:**

```
Pass 1 — Greens:  Find exact matches first. Remove those letters
                   from the remaining answer pool.

Pass 2 — Yellows: For non-green letters, check if the guessed letter
                   exists anywhere in the leftover pool. If so, mark
                   yellow and consume that letter from the pool.
```

This ensures each answer letter can only "explain" one guessed letter, making duplicate handling accurate.

### Letter state tracking

The on-screen keyboard tracks the **best color seen** for each letter across all guesses. Color priority is: `green > yellow > gray`. Once a letter is confirmed green, it stays green on the keyboard even if it appeared gray in an earlier guess.

### Persistent stats

Stats are saved as JSON in `.streak.json` next to the script. The file is created automatically on first play. Losing resets the current streak to zero but preserves the best-streak record.

---

## Project structure

```
terminal-wordle/
├── wordle.py       # Full game — all logic, rendering, and stats
└── .streak.json    # Auto-generated on first play (gitignored)
```

---

## What I learned building this

- **ANSI escape codes** — how terminals interpret special character sequences to produce colors, bold text, and screen-clearing without any external library
- **Two-pass duplicate handling** — why naive letter scoring fails on repeated letters and how a consume-and-mark approach fixes it
- **State management in a loop** — tracking guess history, keyboard state, and session stats cleanly across iterations
- **Persistent storage without a database** — using a local JSON file to maintain state between program runs

---

## Potential extensions

- [ ] Hard mode — guesses must use all confirmed letters
- [ ] Daily word mode — same word for everyone on a given date (seeded by date)
- [ ] Word validation — reject guesses not in a known-words dictionary
- [ ] Share output — generate emoji grid for sharing results (🟩🟨⬜)
- [ ] Statistics histogram — show guess distribution like the real Wordle

---

## License

MIT — free to use, modify, and distribute.
