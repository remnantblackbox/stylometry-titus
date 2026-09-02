# Stylometric analysis of Shakespeare's Titus Andronicus
This project is a computational stylometry experiment that explores whether stylistic features of *Titus Andronicus* resemble those of William Shakespeare's early works or George Peele's plays. The results are exploratory and are not intended as a rigorous authorship attribution study.

## Background
I came across the [Introduction to stylometry with Python](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python) article on *Programming Historian* and found the idea interesting enough to try it out on a literary question I already knew about: the possible collaboration between William Shakespeare and George Peele in *Titus Andronicus*.

So I built this project to see what would happen if I applied the **Burrows' Delta** method from the article to the five acts of the play.

That's pretty much it: this is an experiment and a learning project, not an attempt to settle the authorship of Titus Andronicus.

## What I did
I put together two small reference corpora:

* a few plays by George Peele
* a few early plays by William Shakespeare

I then split Titus Andronicus into its five acts and used Burrows' Delta to compare each act with the two reference corpora.

The experiment was repeated with 30, 50, 100 and 200 most-frequent words, just to see whether changing this parameter substantially changed the results.

## Results
The results were:
| Act | Closest match |
|---|---|
| Act 1 | Peele |
| Act 2 | Mixed |
| Act 3 | Shakespeare |
| Act 4 | Shakespeare |
| Act 5 | Shakespeare |

Act 1 being consistently closer to Peele is particularly interesting because it matches the broad division proposed by MacDonald P. Jackson: Act 1 as Peele, Acts 2–5 as Shakespeare.

Act 2 is less clear and changes depending on the number of words used.

That's as far as I would take these results. As I described, this experiment uses a small corpus and a very simple application of one stylometric technique, so the results shouldn't be treated as an authorship attribution. They're simply the results of applying the method to this particular set of texts.

## Corpus
 
| Folder | Contents |
|---|---|
| `corpus/peele/` | George Peele: *The Battle of Alcazar*, *Edward I*, *The Old Wives' Tale* |
| `corpus/shakespeare/` | William Shakespeare: *The Comedy of Errors*, *Richard II*, *Richard III*, *Romeo and Juliet*, *Two Gentlemen of Verona* |
| `corpus/disputed/` | *Titus Andronicus*, split into its five acts |
| `corpus/source_files/` | Unprocessed source texts and annotated PDFs the corpus above was derived/cleaned from |

## Running the experiment
Requires Python 3.10+ and NLTK.
```
pip install -r requirements.txt
python stylometry_titus.py
```
The script downloads the `punkt_tab` data required by NLTK’s Punkt tokenizer on its first run.

## Notes and Further Reading
The authorship of Titus Andronicus has been debated for a long time, including the possibility that George Peele contributed to the play.

MacDonald P. Jackson proposed a particularly influential division in which Act 1 was written by Peele and Acts 2–5 by Shakespeare. Brian Vickers later discussed this and other possible Peele contributions in Shakespeare, Co-Author.

Those ideas are what motivated me to try the experiment in the first place.

## References
* Jackson, MacD. P. (1996). "Stage Directions and Speech Headings in Act 1 of Titus Andronicus Q (1594): Shakespeare or Peele?" Studies in Bibliography
* Vickers, B. (2002). Shakespeare, Co-Author: A Historical Study of Five Collaborative Plays. Oxford University Press.
* Laramée, F. D. (2018). [Introduction to stylometry with Python](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python). Programming Historian


