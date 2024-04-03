import json
from contextlib import suppress
from datetime import datetime
from typing import List, cast

from typing_extensions import TypedDict

from .utils import run_command

NUM_CHARS = [str(n) for n in range(10)]


class AuthorStats(TypedDict):
    value: int
    label: str


class GitStatsRawOutput(TypedDict):
    authors: List[AuthorStats]


def get_git_stats(since: datetime) -> GitStatsRawOutput:
    with suppress(Exception):
        command = f"git-stats --raw --authors --since {since}"
        return cast(GitStatsRawOutput, json.loads(run_command(command)))

    with suppress(Exception):
        command = f"npx git-stats --raw --authors --since {since}"
        return cast(GitStatsRawOutput, json.loads(run_command(command)))

    msg = "Either git-stats or npx (node) must be installed"
    raise ValueError(msg)


def get_total_commits(git_stats: GitStatsRawOutput) -> int:
    return sum(author["value"] for author in git_stats["authors"] if author["value"])


def get_author_info(author: AuthorStats, since: datetime) -> str:
    author_name = author["label"]
    command = (
        f'git log --author="{author_name}" --numstat --since="{since}" --format=""'
    )
    log = run_command(command)
    files_changed = 0
    lines_added = 0
    lines_deleted = 0
    for line in log.splitlines():
        if not line:
            continue
        added, deleted, _ = line.split("\t", 2)

        files_changed += 1

        lines_added += int(added) if added.isdigit() else 0
        lines_deleted += int(deleted) if deleted.isdigit() else 0

    return f"\n* {files_changed} Files Changed, - {lines_deleted} Lines Deleted, + {lines_added} Lines Added\n\n"  # pylint: disable=line-too-long
