'''
download full articles from rss feed
'''
import argparse
import os
import feedparser

from newspaper import Article


def argparser() -> argparse.ArgumentParser:
    '''
    argument parser
    '''
    _parser = argparse.ArgumentParser(
        description="RSS Feed Parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    _parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="RSS Feed URL",
    )

    _parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="Output Directory",
    )

    return _parser

if __name__ == "__main__":
    args = argparser().parse_args()

    d = feedparser.parse(args.url)

    os.makedirs(args.dir, exist_ok=True)

    for entry in d.entries:
        if entry.link is None:
            continue

        article = Article(entry.link)

        if article is None:
            continue

        article.download()
        article.parse()

        filename = entry.link.rstrip("/").split("/")[-1].split("?")[0].split(".")[0] + ".txt"
        with open(f"{args.dir}/{filename}", "w", encoding="utf8") as f:
            f.write(article.text)
