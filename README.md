# PageRank
Python implementation of the PageRank algorithm, using both sampling and iterative methods to rank web pages based on link structure. Aimed at understanding and replicating Google's core search algorithm logic.

# PageRank Algorithm

## Table of Contents
1. [Project Overview](#project-overview)
2. [How PageRank Works](#how-pagerank-works)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Code Structure](#code-structure)

---

## Project Overview
This project implements the **PageRank** algorithm, used by search engines to rank the importance of web pages. The algorithm determines the probability of a random internet user visiting a specific page, taking into account both the number of incoming links and the significance of the linking pages.

This implementation is done using Python and offers two approaches to calculating PageRank:
1. **Sampling Method** - Uses a random surfer model to simulate browsing behavior.
2. **Iterative Method** - Uses a recursive mathematical approach to compute PageRank values.

The project is based on the [CS50 AI](https://cs50.harvard.edu/ai/2024/projects/2/pagerank/) curriculum.

---

## How PageRank Works
PageRank evaluates web pages based on their link structure. The key idea is:
- A page is more important if it is linked to by other important pages.
- A random surfer model is used to simulate how likely a user is to visit a given page.

### Random Surfer Model
In this model, a random surfer:
1. Starts on a random page.
2. Clicks links at random to navigate to other pages.
3. Occasionally jumps to a random page with a small probability (damping factor).

The algorithm computes the probability distribution over pages, estimating how often the surfer will land on each page.

### Iterative Approach
This method uses a formula to iteratively update PageRank values until they converge (i.e., the values stabilize). It ensures that pages with no links are treated as if they link to every page in the corpus.

---

## Installation
1. Ensure you have **Python 3** installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pagerank.git
   ```
3. Navigate into the project directory:
   ```bash
   cd pagerank
   ```

## Usage
To run the PageRank algorithm, use the following command:
```bash
python pagerank.py <directory_of_html_pages>
```

### Example
If your HTML files are stored in a folders corpus0, corpus1 and corpus2:
```bash
python pagerank.py corpus0
```

### Output
The script will display the PageRank values calculated by both the Sampling and Iterative methods. For example:
```yaml
PageRank Results from Sampling (n = 10000)
  1.html: 0.2188
  2.html: 0.4275
  3.html: 0.2187
  4.html: 0.1351
PageRank Results from Iteration
  1.html: 0.2198
  2.html: 0.4294
  3.html: 0.2198
  4.html: 0.1311
```

### Code Structure
The primary logic of the PageRank algorithm is implemented in the following key functions:

1. crawl(directory): Parses a directory of HTML pages and builds a graph representation of pages and their links.
2. transition_model(corpus, page, damping_factor): Returns the probability distribution of the next page based on the current page and the damping factor.
3. sample_pagerank(corpus, damping_factor, n): Calculates PageRank using the random sampling method.
4. iterate_pagerank(corpus, damping_factor): Calculates PageRank using an iterative method until convergence.

For detailed information, refer to the pagerank.py script.
