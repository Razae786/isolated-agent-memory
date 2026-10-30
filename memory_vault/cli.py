import os
import sys
import argparse
from memory_vault.resolver import get_database_path, DEFAULT_STORAGE_ROOT
from memory_vault import engine


def main():
    parser = argparse.ArgumentParser(description="Isolated Agent Memory CLI")
    parser.add_argument("--root", default=DEFAULT_STORAGE_ROOT, help="Root storage directory")
    parser.add_argument("--project", default=None, help="Explicit project name override")

    subparsers = parser.add_subparsers(dest="command")

    # Command: list
    subparsers.add_parser("list", help="List all separated project partitions")

    # Command: recall
    recall_p = subparsers.add_parser("recall", help="Search facts in the active project")
    recall_p.add_argument("query", nargs="?", default="", help="Keyword or semantic search query")

    # Command: add
    add_p = subparsers.add_parser("add", help="Add or update a fact in the active project")
    add_p.add_argument("--id", required=True, help="Unique fact ID")
    add_p.add_argument("--category", required=True, help="Fact category")
    add_p.add_argument("--fact", required=True, help="Short summary of the fact")
    add_p.add_argument("--details", default="", help="Detailed notes/metrics")

    # Command: checkpoint
    chk_p = subparsers.add_parser("checkpoint", help="Record session checkpoint in active project")
    chk_p.add_argument("--summary", required=True, help="What was accomplished")
    chk_p.add_argument("--next", default="", help="Next steps planned")
    chk_p.add_argument("--files", default="", help="Files created or modified")

    # Command: dump
    subparsers.add_parser("dump", help="Dump active project memory as markdown")

    args = parser.parse_args()

    if args.command == "list" or args.command is None:
        partitions = engine.list_partitions(args.root)
        print("=" * 65)
        print("ISOLATED AGENT MEMORY - ACTIVE PROJECT PARTITIONS")
        print(f"Storage Root: {args.root}")
        print("=" * 65)
        if not partitions:
            print("No memory partitions found.")
        for p in partitions:
            print(f"  • {p['project']:<30} -> {p['facts_count']} facts ({p['path']})")
        print("=" * 65)
    else:
        db_path, proj_key = get_database_path(storage_root=args.root, project_key=args.project)

        if args.command == "recall":
            facts = engine.recall_facts(db_path, args.query)
            print(f"[{proj_key}] Found {len(facts)} facts matching '{args.query}':")
            for f in facts:
                print(f"  - [{f['category'].upper()}] {f['id']}: {f['fact']}")
                if f['details']:
                    print(f"    Details: {f['details']}")

        elif args.command == "add":
            engine.add_fact(db_path, args.id, args.category, args.fact, args.details)
            print(f"[{proj_key}] Fact '{args.id}' stored successfully in {db_path}")

        elif args.command == "checkpoint":
            engine.add_checkpoint(db_path, args.summary, args.next, args.files)
            print(f"[{proj_key}] Checkpoint recorded successfully in {db_path}")

        elif args.command == "dump":
            print(engine.dump_markdown(db_path, proj_key))


if __name__ == "__main__":
    main()
