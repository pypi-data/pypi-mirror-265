from typing import Optional

from .git_stats import get_author_info, get_git_stats, get_total_commits
from .strategy import Strategy, get_datetime_factory_from_strategy


def run(strategy: Strategy, since: Optional[str], *, raw_format: bool) -> None:
    datetime_factory = get_datetime_factory_from_strategy(strategy)
    since_datetime = datetime_factory(since)

    git_stats = get_git_stats(since_datetime)
    total_commits = get_total_commits(git_stats)

    output: str = ""

    for author in git_stats["authors"]:
        if not author["value"]:
            continue
        author_info = get_author_info(author, since_datetime)
        percentage_of_total = (author["value"] * 100) / total_commits
        tmp_output = f'{author["label"]}: {author["value"]} commits ({percentage_of_total:.2f}% of total) {author_info}\n'  # pylint: disable=line-too-long
        if raw_format:
            tmp_output = rf'{author["label"]}: {author["value"]} commits ({percentage_of_total:.2f}% of total) {author_info}\n'  # pylint: disable=line-too-long
        output += tmp_output
    print(output)
