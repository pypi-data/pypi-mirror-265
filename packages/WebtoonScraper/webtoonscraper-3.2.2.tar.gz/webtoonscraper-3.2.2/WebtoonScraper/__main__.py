from __future__ import annotations

import argparse
import contextlib
import functools
import logging
import os
import re
import sys
from importlib.resources import files
from pathlib import Path
from typing import Literal

from rich.console import Console
from rich.table import Table

import WebtoonScraper
from WebtoonScraper import __version__, webtoon
from WebtoonScraper.scrapers import CommentsDownloadOption
from WebtoonScraper.directory_merger import (
    MERGED_WEBTOON_DIRECTORY,
    NORMAL_WEBTOON_DIRECTORY,
    ContainerStates,
    check_container_state,
    merge_webtoon,
    restore_webtoon,
    select_from_directory,
)
from WebtoonScraper.exceptions import DirectoryStateUnmatchedError
from WebtoonScraper.miscs import EpisodeNoRange, WebtoonId, logger

# currently Lezhin uses only lower case alphabet, numbers, and underscore. Rest of them are added for just in case.
acceptable_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")


def cleanup_string(value: str) -> str:
    return value.replace(" ", "").removeprefix("(").removesuffix(")")


def str_to_webtoon_id(webtoon_id: str) -> WebtoonId:
    # URL인 경우
    if "." in webtoon_id:
        return webtoon_id

    if webtoon_id.isdigit():
        # all others
        return int(webtoon_id)
    if all(char in acceptable_chars for char in webtoon_id):
        # Lezhin
        return webtoon_id
    if "," not in webtoon_id:
        raise ValueError("Invalid webtoon id.")

    match_result = re.match(r""" * *[(]? *(['"]?(.+?)['"]?) *, *(['"]?(.+?)['"]?) *[)]? *$""", webtoon_id)
    assert match_result is not None, "Invalid webtoon id."
    is_arg1_quoted = match_result.group(2)[0] in {
        '"',
        "'",
    }
    is_arg2_quoted = match_result.group(3)[0] in {'"', "'"}
    arg1, arg2 = match_result.group(2), match_result.group(4)

    if arg1.isdigit() and not is_arg1_quoted:
        # 네이버 포스트
        return int(arg1), int(arg2)
    elif arg2.isdigit() and not is_arg2_quoted:
        # 네이버 블로그
        blog_id = match_result.group(2)
        assert isinstance(blog_id, str)
        return blog_id, int(arg2)
    else:
        # 티스토리
        assert isinstance(arg1, str)
        assert isinstance(arg2, str)
        return arg1, arg2


def str_to_episode_no_range(episode_no_range: str) -> EpisodeNoRange:
    with contextlib.suppress(ValueError):
        return int(episode_no_range)

    def nonesafe_int(value):
        return int(value) if value and value.lower() != "none" else None

    start, end = (
        nonesafe_int(cleanup_string(i)) for i in episode_no_range.split("~")
    )

    return start, end


def case_insensitive(string: str) -> str:
    return string.lower()


parser = argparse.ArgumentParser(
    prog="WebtoonScraper",
    usage="Download or merge webtoons in CLI",
    description="Download webtoons with ease!",
)
parser.add_argument("--mock", action="store_true", help="No actual action.")
parser.add_argument(
    "--version",
    action="version",
    version=f"WebtoonScraper {__version__} of Python {sys.version} from {str(files(WebtoonScraper))}",
)
parser.add_argument("-v", "--verbose", action="store_true", help="Set logger level to INFO and show detailed error.")
subparsers = parser.add_subparsers(title="Commands", help="Choose command you want.")

# 'download' subparsers
download_subparser = subparsers.add_parser("download", help="Download webtoons.")
download_subparser.set_defaults(subparser_name="download")
download_subparser.add_argument(
    "webtoon_ids", type=str_to_webtoon_id, metavar="webtoon_ids", help="Webtoon ID or URL.", nargs="+"
)
download_subparser.add_argument(
    "-p",
    "--platform",
    type=lambda x: str(x).lower(),
    metavar="webtoon_platform",
    choices=set(webtoon.PLATFORMS) | set(webtoon.SHORT_NAMES),
    help="Webtoon platform to download. No need to specify if you don't want to. "
    f"All choices: {', '.join(f'{webtoon.SHORT_NAMES[short_name]}({short_name})' for short_name in webtoon.SHORT_NAMES)}",
)
download_subparser.add_argument(
    "-m",
    "--merge-number",
    type=int,
    metavar="merge_number",
    help="Merge number when you want to merge directories. Don't specify if you don't want to merge.",
)
download_subparser.add_argument(
    "--cookie",
    type=str,
    metavar="cookie",
    help="Set cookie when you download Bufftoon.",
)
download_subparser.add_argument(
    "--bearer",
    type=str,
    metavar="bearer",
    help="Set bearer when you download Lezhin.",
)
download_subparser.add_argument(
    "-r",
    "--range",
    type=str_to_episode_no_range,
    metavar="[start]~[end]",
    help="Episode number range you want to download.",
)
download_subparser.add_argument(
    "-d",
    "--download-directory",
    type=Path,
    metavar="directory",
    default="webtoon",
    help="The directory you want to download to.",
)
download_subparser.add_argument("--list-episodes", action="store_true", help="List all episodes.")
download_subparser.add_argument(
    "--get-paid-episode",
    action="store_true",
    help="Get paid episode. Lezhin Comics only.",
)
download_subparser.add_argument(
    "-c", "--comments", "--comment",
    metavar="option",
    help="Download comments.",
    nargs="*",
    choices=["all", "reply"]
)

merge_subparser = subparsers.add_parser("merge", help="Merge/Restore webtoon directory.")
merge_subparser.set_defaults(subparser_name="merge")
merge_subparser.add_argument(
    "webtoons_directory_name",
    type=str,
    metavar="webtoons_directory_name",
    help="The name of folder that contains webtoon folders to merge or restore.",
)
merge_subparser.add_argument(
    "-m",
    "--merge-number",
    type=int,
    metavar="merge_number",
    default=None,
    help="Merge number when merge.",
)
merge_subparser.add_argument(
    "-t",
    "--target-parent-directory",
    type=Path,
    metavar="target_parent_directory",
    default=None,
    help="The directory that the result of merge/restore will be located. Defaults to source directory itself.",
)


def parse_download(args: argparse.Namespace) -> None:
    args.platform = webtoon.SHORT_NAMES.get(args.platform, args.platform)

    for webtoon_id in args.webtoon_ids:
        # 만약 다른 타입의 튜플인데 NAVER_BLOG라면 자동으로 (str, int)로 변환한다.
        if args.platform == webtoon.NAVER_BLOG and isinstance(webtoon_id[0], int):
            webtoon_id = str(webtoon_id[0]), int(webtoon_id[1])

        # 만약 다른 타입의 튜플인데 TISTORY라면 자동으로 (str, str)로 변환한다.
        if args.platform == webtoon.TISTORY and isinstance(webtoon_id[0], int):
            webtoon_id = str(webtoon_id[0]), str(webtoon_id[1])

        if args.comments is None:
            comment_download_option = None
        else:
            options = set(args.comments)
            comment_download_option = CommentsDownloadOption(
                top_comments_only="all" not in options,
                reply="reply" in options,
            )

        scraper = webtoon.setup_instance(
            webtoon_id,
            args.platform,
            cookie=args.cookie,
            bearer=args.bearer,
            download_directory=args.download_directory,
            get_paid_episode=args.get_paid_episode,
            comments_option=comment_download_option,
        )

        if args.list_episodes:
            scraper.list_episodes()
            return

        scraper.download_webtoon(
            args.range,
            merge_number=args.merge_number,
            add_viewer=True,
        )


CONTAINER_STATE_PER_ARGS: dict[str, ContainerStates] = {
    "m": NORMAL_WEBTOON_DIRECTORY,
    "merge": NORMAL_WEBTOON_DIRECTORY,
    "r": MERGED_WEBTOON_DIRECTORY,
    "restore": MERGED_WEBTOON_DIRECTORY,
}

ABBR_TO_FULL_STATE: dict[str, Literal["merge", "restore", "auto"]] = {
    "m": "merge",
    "r": "restore",
    "a": "auto",
}


CONTAINER_STATE_TO_DO_STATE: dict[ContainerStates, Literal["merge", "restore"]] = {
    NORMAL_WEBTOON_DIRECTORY: "merge",
    MERGED_WEBTOON_DIRECTORY: "restore",
}


def get_state(source_directory: Path) -> ContainerStates:
    states: dict[Path, ContainerStates] = {
        webtoon_directory: check_container_state(webtoon_directory) for webtoon_directory in source_directory.iterdir()
    }
    all_unique_states = set(states.values())
    if len(all_unique_states) != 1:
        raise ValueError(
            "All webtoons in source directory should have same state when using 'auto' action.\n"
            "Please specify --action(-a) or check directory state."
            f"States: {all_unique_states}"
        )

    (directories_state,) = all_unique_states
    return directories_state


def get_string_todo(state: ContainerStates) -> Literal["merge", "restore"]:
    try:
        return CONTAINER_STATE_TO_DO_STATE[state]
    except KeyError:
        raise ValueError(f"State {state} is not supported.")


def list_directories(parent_directory: Path) -> None:
    table = Table(show_header=True, header_style="bold blue", box=None)
    table.add_column("Webtoon Directory Name", style="bold")
    table.add_column("Directory State")
    table.add_column("Action If Auto")
    for webtoon_directory in parent_directory.iterdir():
        directory_state = check_container_state(webtoon_directory)
        table.add_row(
            webtoon_directory.name,
            directory_state,
            CONTAINER_STATE_TO_DO_STATE.get(directory_state),
        )
    Console().print(table)


def parse_merge(args: argparse.Namespace) -> None:
    select_from_directory(
        args.webtoons_directory_name,
        args.target_parent_directory,
        True,
        args.merge_number,
    )


def main(argv=None) -> Literal[0, 1]:
    args = parser.parse_args(argv)  # 주어진 argv가 None이면 sys.argv[1:]을 기본값으로 삼음

    if args.mock:
        print("Arguments:", str(args).removeprefix("Namespace(").removesuffix(")"))
        return 0

    if not hasattr(args, "subparser_name"):
        return main(argv=["--help"])

    if args.verbose:
        logger.setLevel(logging.INFO)

    try:
        if args.subparser_name == "download":
            parse_download(args)
        elif args.subparser_name == "merge":
            parse_merge(args)
        else:
            raise NotImplementedError(f"Subparser {args.subparser_name} is not implemented.")
    except BaseException as e:
        logger.error(f"{type(e).__name__}: {e}")
        if args.verbose:
            Console().print_exception()
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
