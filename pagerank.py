import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus)
    probability_distribution = {page_name: 0 for page_name in corpus}

    # If there is no link, Equal probability for all pages, including the page itself
    if(len(corpus[page]) == 0):
        for page_name in probability_distribution:
            probability_distribution[page_name] = (1 / total_pages)
        return probability_distribution
    
    # Probability of a link at random that is linked to the page
    linked_probability = damping_factor / len(corpus[page])
    # Probability of a link at random that may or may not be linked to the page
    random_probability = (1 - damping_factor) / total_pages

    # The probability distribution is populated as per the algorithm
    for page_name in probability_distribution:
        probability_distribution[page_name] += random_probability
        if page_name in corpus[page]:
            probability_distribution[page_name] += linked_probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to the transition model, starting with a random page.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}

    # Choose a random starting page and assign its initial PageRank
    current_page = random.choice(list(page_rank.keys()))
    page_rank[current_page] = 1/n  # First sample is considered a visit to this page

    # Generate the initial transition model for the current page
    current_prob_dist = transition_model(corpus, current_page, damping_factor)

    for i in range(n):
        # Choose a new page based on the current transition probabilities
        new_page = random.choices(list(current_prob_dist.keys()), list(current_prob_dist.values()), k=1)[0]
        
        page_rank[new_page] += 1/n  # Each visit contributes 1/n to the rank
        
        # Update the transition model based on the new current page
        current_prob_dist = transition_model(corpus, new_page, damping_factor)
    
    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    page_rank = {page: (1 / total_pages) for page in corpus}

    thersold = 0.001
    error = 1

    updated_page_rank = page_rank.copy()

    while True:
        for page in corpus:
            new_rank = (1 - damping_factor) / total_pages
            for link in corpus:
                # If there are links, we are going by formula
                if page in corpus[link]:
                    new_rank += damping_factor * (page_rank[link] / len(corpus[link]))
                # If page has no links at all then it is considered as having one link for every page (including itself).
                if not corpus[link]:
                    new_rank += damping_factor * (page_rank[link] / total_pages)
            updated_page_rank[page] = new_rank

        # Break out of loop if the page rank is consistent
        consistent = True
        for page in corpus:
            error = abs(updated_page_rank[page] - page_rank[page])
            if error >= thersold:
                consistent = False
                break
        
        if consistent:
            break
        else:
            page_rank = updated_page_rank.copy()
    
    return updated_page_rank


if __name__ == "__main__":
    main()
