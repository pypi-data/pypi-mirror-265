# Summary
This package solves Agnes (Agnes Sorel) solitaire card games. It can
be used to solve games having the rules implemented in the GNOME AisleRiot
package and the rules attributed to Dalton in 1909 (with a minor variant
in the table layout) and Parlett in 1979 among others [1–3] and to
calculate win rates.

# Example
```
import random
import quagnes

random.seed(12345)
n_reps = 1000

attributes = ['n_states_checked', 'n_deal', 'n_move_to_foundation',
      'n_move_card_in_tableau','n_no_move_possible','max_score','max_depth',
      'current_depth']

# header for the output file
print('rc,' + ','.join(attributes))

for rep in range(0, n_reps):
    new_game=quagnes.Agnes()
    rc = new_game.play()

    # Write the return code and selected attributes from the game
    out_str = (str(rc) + ',' +
        ','.join([ str(getattr(new_game, attr)) for attr in attributes ]))
    print(out_str, flush=True)

    # rc==1 are games that were won
    if rc==1:
        f = open(f'winners/win{rep}.txt', 'w', encoding='utf-8')
        f.write(new_game.print_history())
        f.close()
```

# Release Notes
## Version 0.8.4
- Copy editing of README.md and correct Wolter win rate to 45/1000000.

## Version 0.8.3
- Copy editing of README.md

## Version 0.8.2
- Bug fix: add check for loops when `move_to_empty_pile != 'none'` in
addition to the existing check when `split_same_suit_runs=True`.
- Add Optimizations #6 and #7 listed below.
- When printing a state, add a single line with a string that has the
  same values stored in the set of losing states. This alllows the user
  to easily search in the output for when the previous state occurred.
  Note that a more compressed version of this string (one byte per
  card) is stored in the set of losing states. A longer version is
  printed that avoids characters that are special in regular expressions
  to facilitate searching. 
- Remove extensive description of the rules from the module docstring.

# Background
Agnes is a difficult solitaire card game under some rule variants. This
package solves the game automatically.

Users can simulate random games and calculate win rates under various
permutations of rules, including moving sequences (runs) by same-suit or
same-color, allowing or not same-suit runs to be split in the middle of the
run for a move, dealing all tableau cards face-up at the start versus
dealing only the final tableau card face-up, and whether and how empty
columns can be filled in between deals (never, a single card of any rank, a
single card of the highest rank, a run starting with a single card of any
rank, or a run starting with a card of the highest rank). The package
provides additional options for debugging and tuning of the search algorithm
to be more memory-efficient at the expense of speed.

In 1979 Parlett named the two main variants of Agnes as Agnes Sorel (the
variant / set of variants described here) and Agnes Bernauer (a variant/set
of variants that uses a reserve) [3]. This package only considers Agnes
Sorel.

Some analyses of win rates for Agnes Sorel has previously been conducted.
Wolter published an experimental analysis of the win rates of this and
other solitaires, reporting 45 winnable games in a million deals under 
presumably the *Up-Suit-None* rules (defined below) [4]. Masten modified
Wolter's solver and reported 900/100,000 (0.9%) games were winnable when
empty columns could not be filled by any card, although it is unclear
whether same-suit runs could be split during a move [5]. In this
analysis, we conduct our own simulations to estimate win rates, assess
agreement with Wolter and Masten and add win rates for other
rule variants. As in the prior analyses, the win rates calculated here are
under perfect play (i.e., the solver is allowed to undo losing moves).

# Rules
There is considerable heterogeneity in the rules that have been proposed
for Agnes (see Wikipedia [1] and Keller [6] for some discussion of the 
history). We describe first the rules according to Dalton [1-2] and
variations that change only the handling of play on empty piles. The other
main set of variants allow moving of same-color runs instead of
same-suit runs. We describe the parameter settings to be used in our
software when playing the different rule variants.

Because our interest in the problem arose from playing the game in the GNOME
AisleRiot package, the default parameters correspond to this variant.

## Dalton (1909)
The first description is of the game is attributed to Dalton in 1909 [1-2].
We implement his rules, except most software we have seen have the tableau
piles ascending in length from left to right, so we follow that convention,
rather than the right to left described by Dalton. (It should be noted that
symmetry cannot be used to claim the win rates are identical under this
variation because only the first two piles are dealt to in the final deal.)
The rules are the following:

Deal seven piles as columns face-up in the tableau such that the first pile
has one card and the last column has seven. Then, deal a single card and
place it above the tableau in the foundation (base card). Foundations are
built up by suit and the tableau is built down by color. Wrap from king to
ace when necessary. Piles of cards in sequence in the same suit can be
moved in the tableau. The top card in each tableau pile is exposed and can
be moved to a different pile (if it has the appropriate color and rank) or
to the foundation. If a movable run occurs by chance at the start of
the game or after a deal, the run can also be moved. When a card or
pile is moved, the card in the column above it becomes exposed and
available for play. Empty tableau piles can be filled by any card or
movable run, or they can be left empty. Dealing from the stock adds one
card to the bottom of each tableau pile before play resumes, so a game will
have three more deals of seven cards and a final deal of two cards. Cards
cannot be played back from the foundation to the tableau.

Note that while Dalton used the singular when saying 'Any exposed card may
be moved into a vacant space [pile]', in the example game he plays, he moves
a group of cards into an empty pile. We follow the latter interpretation.

Dalton states that at the start the bottom card of each pile is exposed and
doesn't explicitly state what is permitted if a movable run occurs by
chance. However, in the sample game he plays, he does not distinguish
between cards that appeared at the bottom of the column at the start versus
those that did not, so we adopt the interpretation that runs may be
moved even if they first occurred by chance. This is consistent with the
software implementations we have seen.

The game as described above can be played by specifying the parameters
`move_same_suit=True`, `face_up=True`, and `move_to_empty_pile='any run'`.

We denote the rules above as *Up-Suit-AnyRun*. The third part of
each name is because many variants have evolved that alter what can be done
with empty piles. We refer to these as:

- *Up-Suit-None*: Empty piles can only be filled when dealing from stock.
- *Up-Suit-Any1*: Empty piles can be filled by any single card, but not by
  a movable run.
- *Up-Suit-HighRun*: Empty piles can be filled a single highest rank card, or
a run starting with the highest rank card (i.e., if the base card was a seven,
an empty pile can be filled only with a six or run starting with a six).
- *Up-Suit-High1*: Empty piles can be filled by a single highest rank card.

The `move_to_empty_pile` parameter takes the values `'none'` (default), 
`'any 1'`, `'high run'`, and `'high 1'`, respectively, for the above four
variants.

## Parlett (1979) and *NoSplit* variants
Parlett gives rules like *Up-Suit-None* but also forbids splitting same
suit runs (`split_same_suit_runs=False`) [3]. We denote this as 
*Up-Suit-None-NoSplit*. We also allow other rules that move by suit to
have this option and denote these by adding *-NoSplit* to the end of
of the rule name.

## *Down-Color* and *Up-Color* variants
Among this group, the primary variant of interest is *Down-Color-None*,
which corresponds to the game as played on AisleRiot, which is where we
became interested in the game. We verified the rules on the current
AisleRiot version 3.22.23.

The first variation from the Dalton rules is that cards are dealt
face down in the tableau except for the final card dealt in each pile.
We start these variant names with *Down-* instead of *Up-*.
The second variation is that runs may be moved if they are the
same color instead of requiring they be the same suit. We use *-Color-*
as the second part of the variant name to indicate this. The third
part of the variant name is as described for the Dalton variants.

Other variants of interest in this class are *Up-Color-AnyRun*. This and
*Up-Color-None* match the rules described on the website poltaire.com,
which offers solitaire play [7]. This site is of interest to us as it hosts
an article by Wolter [4] that analyzes the winnability of the game as
played on the site.

# Methodology
## Optimizations
The following optimizations were used to improve the run-time over a naive
depth-first search of all possible moves:

1. When `move_to_empty_pile='none'`, if the highest rank card (e.g., a king
if the base card is an ace) is placed in a tableau pile below a lower card
of the same suit, the lower card can never be moved from the pile. This is
detected as soon as the king is placed. Therefore, some games can be
determined to be not winnable by examining only the starting layout. Note
while this optimization improves run time, it is not possible to determine
the maximum possible score if a branch is terminated for this reason. This
concept can be extended by noting that if the king of clubs blocks the
queen of hearts and the king of hearts blocks the queen of clubs, the game
is also unwinnable. In general, we define after each deal a four vertex
graph (one vertex for each suit), where an edge denotes which suits are
blocked by the suit corresponding to the vertex. The state is not winnable
if a cycle exists in the graph. This only needs to be checked after a deal.
This optimization is disabled when `move_to_empty_pile != 'none'` or when
`maximize_score=True`.

2. A card is immediately placed on a foundation if its rank is no more than
the rank of the top foundation card of the same color suit plus two. For
example, if the base card is an ace, and we have already played up to the
six of spades in the foundation, we immediately play the ace of clubs up
to the eight of clubs (if possible) to the foundation. We would not
immediately play the nine of clubs to the foundation as it might be
needed in the tableau to move the eight of spades.

3. We track states that we have already determined to be not winnable in
a set. For example, suppose the initial state has two possible moves: M1)
move a card from pile 1 to 2; M2) move a card from pile 4 to 5. Once we
determine the sequence M1 → M2 is not winnable, there is no need to check
the sequence M2 → M1, as they both result in the same state. This
optimization can be tuned using the `track_threshold` parameter.

4. To prevent infinite loops, we use a stack of sets that stores the state of
the game (number of cards in the stock and arrangement of cards in the tableau)
and check whether this has been repeated since the last deal or move to
foundation.  If the state is a repeat, we consider no valid moves to be
available at the repeated state. This second method is disabled if
`split_same_suit_runs=False` and `move_to_empty_pile 'none'}`, as loops
cannot occur under this combination of parameter settings.

<!--- First, we track for each pile the last move number (i.e., the number of
plays
since the start of the game the pile was last involved in a move between
tableau piles). This is set to zero at the start of the game and when a card
is moved from the pile to the foundation or when the pile is dealt to. A move
between two piles is not permitted if the last move numbers match and are
greater than zero and the target pile is not empty (as this implies we have
reversed a previously executed move). -->
5. The simulation is implemented using two or three equal-length stacks
where the nth item describes an aspect of the state of the game at the
nth move.  These three stacks store: (1) the moves performed, (2) the valid
moves not yet attempted, and (3) a set containing the arrangement of all
tableau layouts that have occurred since the last deal or move to foundation.
A single state object (`_AgnesState`) in the `Agnes` object initially
stores information about the starting state, such as the cards in the
foundation, the arrangement of cards in the tableau, and the number of
cards left in the stock. When a move is performed or undone, the
`_AgnesState` object is updated in-place based on the move information.
Initial testing found this implementation to be about 5–7 times faster than
using a stack of `_AgnesState` objects, although this hasn't been retested
after the addition of some of the other optimizations.

7. If there are multiple empty columns in the tableau that cannot be
covered by a future deal, then it doesn't matter which column is played
in, so the first is always chosen. Similarly, we do not consider a move
that moves the entirety of one column to a different empty column when
both columns cannot be covered by a future deal.

8. We do not allow splitting same-suit runs when the stock is empty
regardless of the value of the `split_same_suit_runs` parameter, unless
`move_to_empty_pile = 'any 1'` or `'high 1'`.

Lastly, note that if win rate is the only output statistic of interest
and results are being calculated for multiple rule sets, users can exploit
the fact that all wins under some rule set is sometimes a subset of wins
under another rule set. For example, any game winnable when 
`split_same_suit_runs=False` is also winnable when
`split_same_suit_runs=True` when other parameter values are fixed.

## Statistical Analysis
Ten thousand decks were simulated using this package version 8.0.2.
We calculated the win rates and the 95% confidence intervals (95% CI)
using the score (Wilson) method for the following rules:
*Down-Color-None*, *Up-Color-None*, *Up-Suit-None*,
*Up-Suit-None-NoSplit*, *Up-Suit-HighRun*, *Up-Suit-HighRun-NoSplit*,
*Up-Suit-AnyRun*, *Up-Suit-AnyRun-NoSplit*. If a set of simulations
consumed too much memory, the simulation was run setting a maximum
number of states examined to 50 million, and win rates were
calculated assuming all incomplete simulations were losses and 
then again assuming all were wins.

For each set of rules, the mean (standard deviation) and maximum number
of states examined were also reported. This statistic counts repeated
states each time they are created.

Lastly, we calculated separate p-values testing the equality of our
estimate with those published by Masten [5] and Wolter \[4\] (the latter
only when the rule for empty piles was *None*). A Chi-square test or Fisher
exact test was used, as appropriate.

All simulations were run using a C++ port of this package. The
first thousand simulations for each rule variant were also run using this
Python package version 0.8.2 on Python version 3.11.2, and the simulation
result (win, loss, exceeded maximum states) and number of states examined
were confirmed to match the C++ version. A laptop running 32-bit
Debian GNU/Linux 12 was used for the simulations. Statistical analyses
were conducted in R v4.2.2.

# Results
The results of the simulations are shown in the table below.

| Rule Variant              | Completed Simulations, (n) | Wins, n (% [95% CI])    | P-value [a] | Mean (SD) States Examined (10^3) | Maximum States Examined (10^6) |
| :------------------------ | :--------------: | :---------------------: | :---------: | :-------------------:     | :-----------------: |
| *Down-Color-None*         | 10,000           | 99 (1.0% [0.8%, 1.2%])  | 0.40        | 89.0 (156.1)              | 63.7                |
| *Up-Color-None*           |  9,996 [b]       | 113 (1.1% [0.9%, 1.4%], 1.2% [1.0%, 1.4%]) | 0.02, 0.01 |  72.6 (112.8) | 46.3       |
| *Up-Suit-None*            | 10,000           | 42 (0.4% [0.3%, 0.6%]   | <.0001      | 10.2 (163.9)              |  8.5                |
| *Up-Suit-None-NoSplit*    | 10,000           | 40 (0.4% [0.3%, 0.5%])  | <.0001      | 5.9 (94.1)            |  6.1                |
| *Up-Suit-HighRun*         | 10,000           | 1454 (14.5% [13.9%, 15.2%]) | 0.92    | 207.3 (999.3)         | 31.9                |
| *Up-Suit-HighRun-NoSplit* | 10,000           | 1411 (14.1% [13.4%, 14.8%]) | 0.30    | 112.9 (500.9)         | 22.6                |
| *Up-Suit-AnyRun-NoSplit*  | 10,000           | 6384 (63.8% [62.9%, 64.8%]) | 0.69    | 59.2 (340.2)          | 16.1                |

[a] P-value for comparison vs Masten results.

[b] Simulations stopped after 50,000,000 states examined. Win rates and P-values are reported twice assuming all incomplete simulations are losses and wins. Mean and maximum states examined are reported for completed simulations.

# Discussion
We found 1.1% - 1.2% of games were winnable under the *Up-Color-None* rules
and 1.0% of games were winnable under the *Down-Color-None* rules. For the
former, the comparison to Masten's results gave a statistically significant
difference at the 95% confidence level while the latter did not.  Our
simulations for *Up-Suit-HighRun*, *Up-Suit-HighRun-NoSplit*, and
*Up-Suit-AnyRun-NoSplit* were not statistically significantly different from
those of Masten, although *Up-Suit-None* and *Up-Suit-None-NoSplit* were.

A limitation of using Masten's results is he states win rates but isn't
explicit about which rules are used, with the exception of how empty
piles are filled. He refers readers to Keller's discussion [6] for more
information, and this discussion suggests that Agnes rules follow 
Whitehead rules (another solitaire) and require movable runs to be
the same suit. That is, Keller indicates the rules are *Up-Suit-None*
in our terminology [5,6]. However, Keller then goes on to note that all
computer implementations he had seen allow moves by colored runs and not
by same-suit runs, which would corresponds to the *Up-Color-None* rules in
our terminology. 

It was unexpected to find that when the rule for empty piles is *None*, our
results for dealing face-down and moving by color matched Masten, while
when the rule for empty piles is *HighRun* or *AnyRun*, our results for
dealing face-up and moving by suit matched. It is unclear if Masten 
reported results for different move rules, if the statistically significant
differences we found were due to chance, or if consistent rules were used
for a variant we have not yet tested (e.g., *Up-Color-None-NoSplit*,
*Up-Color-HighRun-NoSplit*, and *Up-Color-AnyRun-NoSplit*).

Despite these uncertainties about Masten's estimates, we add 95% CIs to
his reported win rates and include them here. He reports the previously
mentioned win rate (95% CI) of 0.9% (0.8%, 1.0%) when empty
columns cannot be filled with moves from the tableau, 63.6% (63.3%, 63.9%)
when the empty column can be filled by any movable run or single card
(or perhaps disallowing runs — Masten is not explicit, but our results
match filling with a run or single card), and 14.5% (14.3%, 14.7%) when
empty columns can be filled only by a run starting with the highest rank
card or single highest-rank card (or again, perhaps disallowing runs).

All of our results were larger than the 45/1,000,000 reported by Wolter
at significance level P<.0001. Given the large difference between our
results and Wolter's results, we believe Wolter's results are incorrect
and should not be cited.

We have estimated win rates that to our knowledge have not been previously
reported for Parlett's variant (*Up-Suit-None-NoSplit*) and
*Down-Color-None*, with the former less than half of *Up-Suit-None* and the
latter about 10% smaller.

Much of the work for this project was originally completed in 2019
assuming all cards were dealt face-up using Python 3.5. This 2024 update
used Python 3.11.2. In 2019 we ported the Python code to C++ for
performance testing and found a five-fold improvement in speed. When
porting the code to Python 3.11, we found a two-fold decrease in run-time
when switching the data structures used from tuples to dataclasses for the
structures representing cards and moves.

We have not all possible rule variants with this package. We considered
including *Up-Suit-AnyRun*, but preliminary estimates indicated 
high memory usage and a longer run time, and therefore we defer analysis
of this variant to a later package version. The current package has some options
to manage the memory (e.g., disabling the set that tracking losing states
at various thresholds), but additional optimizations are possible
once the set is disabled that are not yet implemented (e.g., 
requiring cards to be placed to the foundation before moving a pile that we
hope will improve run time). In addition, the package options allow
disabling of splitting same-suit runs before a move, but this option will
likely be generalized to disallow splitting of movable runs and then
can be applied when moves are allowed by color.

# References
[1] Agnes (card game). Wikipedia.
    https://en.wikipedia.org/wiki/Agnes_(card_game). Retrieved
    March 15, 2024.

[2] Dalton W (1909). "My favourite Patiences" in The Strand Magazine,
    Vol 38.

[3] Parlett D (1979). The Penguin Book of Patience. London: Penguin.

[4] Wolter J (2013). Experimental analysis of Agnes Sorel solitaire.
    https://politaire.com/article/agnessorel.html. Retrieved
    March 15, 2024.

[5] Masten M (2021). Agnes Sorel.
    https://solitairewinrates.com/AgnesSorel.html. Retrieved
    March 17, 2024.

[6] Keller M (2021). Whitehead and Agnes -- packing in color.
    https://www.solitairelaboratory.com/whitehead.html. Retrieved
    March 17, 2024.

[7] Wolter J (2014). Rules for Agnes Sorel solitaire.
    https://politaire.com/help/agnessorel. Retrieved March 17, 2024.

# Disclosures
We are not affiliated with any of the books, websites, or applications
discussed in this documentation, except of course for this Python package
which we wrote.
