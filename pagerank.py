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
    # Initialize a dictionary for the probability distribution.
    probability_distribution = {page_key: float(0) for page_key in corpus}

    # Filling the dictionary with correct probabilities according to
    # the number of links in a page and according to current page.
    if len(corpus[page]):
        for page_link in corpus:
            probability_distribution[page_link] += (1 - damping_factor) / len(corpus)
        
        for page_link in corpus[page]:
            probability_distribution[page_link] += damping_factor / len(corpus[page])
                 
    else:
        for page_link in corpus:
            probability_distribution[page_link] += 1 / len(corpus)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initializing a dictionary for the PageRank.
    pagerank = {page_key: float(0) for page_key in corpus}

    # Choosing a random page for first page, and updating dictionary.
    current_page = random.choice(list(pagerank))
    pagerank[current_page] += 1

    # Finding the rest of the random states.
    for i in range(1, n):
        next_page_probability = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(next_page_probability.keys()), list(next_page_probability.values()))[0]        
        pagerank[current_page] += 1

    # Divide each page's rank by n to calculate the estimated PageRank value.
    pagerank = {key: (value / n) for key, value in pagerank.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initializing N = number of pages.
    N = len(corpus)

    # Initializing a dictionary for the PageRank and assigning initial pagerank to each page.
    pagerank = {page_key: 1 / N for page_key in corpus}

    while True:
        # Setting count = 0.
        count = 0

        # Implementing the PageRank formula.
        for page_1 in corpus:
            # Initializing sum_probability.
            sum_probability = 0
            for page_2 in corpus:
                if page_1 in corpus[page_2]:
                    sum_probability += pagerank[page_2] / len(corpus[page_2])
            new_pagerank = (1 - damping_factor) / N + damping_factor * sum_probability

            # Finding the highest rank_change in the dictionary.
            if abs(new_pagerank - pagerank[page_1]) < 0.001:
                count += 1

            # Passing new_pagerank to pagerank and repeat the process.
            pagerank[page_1] = new_pagerank
        
        # Checking if each page's pagerank is accurate to within 0.001
        if count == N:
            break
    
    # Calculating the sum of new ranks and normalizing PageRanks so that they add up to 1.
    rank_sum = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= rank_sum
    
    return pagerank


if __name__ == "__main__":
    main()
