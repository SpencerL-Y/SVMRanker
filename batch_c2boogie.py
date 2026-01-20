#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def iter_c_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.endswith(".c"):
                yield os.path.join(dirpath, name)


def preprocess_c(path):
    result = subprocess.run(["cpp", path], capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr
    filtered = "".join(line for line in result.stdout.splitlines(True) if not line.startswith("#"))
    return filtered, None


def run_c2boogie(c2boogie_path, c_path, out_path, pointer_log):
    src, err = preprocess_c(c_path)
    if err is not None:
        return 1, err
    cmd = [
        "python3",
        c2boogie_path,
        "stdin",
        out_path,
        "--skip-methods",
        "__VERIFIER_error",
        "__VERIFIER_assert",
        "__VERIFIER_assume",
        "--assert-method",
        "__VERIFIER_assert",
        "--assume-method",
        "__VERIFIER_assume",
        "--add-trivial-invariants",
        "--pointer-log",
        pointer_log,
        "--input-name",
        c_path,
    ]
    result = subprocess.run(cmd, input=src, text=True, capture_output=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return result.returncode, detail
    return result.returncode, None


def main():
    parser = argparse.ArgumentParser(description="Batch convert C to Boogie using C2Boogie.")
    parser.add_argument("--src-dir", default="../EvolveTerm/data")
    parser.add_argument("--out-dir", default="../Boogie_data")
    parser.add_argument("--pointer-log", default=None)
    parser.add_argument("--failure-log", default=None,
                        help="write failed C file paths (and errors) to this file")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.abspath(__file__))
    c2boogie_path = os.path.join(repo_root, "src", "C2Boogie.py")

    src_dir = os.path.abspath(args.src_dir)
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    pointer_log = args.pointer_log
    if pointer_log is None:
        pointer_log = os.path.join(out_dir, "pointer_types.csv")
    else:
        pointer_log = os.path.abspath(pointer_log)

    failures = []
    total = 0

    for c_path in iter_c_files(src_dir):
        total += 1
        rel = os.path.relpath(c_path, src_dir)
        out_path = os.path.join(out_dir, os.path.splitext(rel)[0] + ".bpl")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        code, err = run_c2boogie(c2boogie_path, c_path, out_path, pointer_log)
        if code != 0:
            failures.append((c_path, err))

    failure_log = args.failure_log
    if failure_log is None:
        failure_log = os.path.join(out_dir, "failed_c2boogie.txt")
    else:
        failure_log = os.path.abspath(failure_log)

    if failures:
        sys.stderr.write("Failed: {}\n".format(len(failures)))
        for path, err in failures:
            msg = err.strip() if err else ""
            sys.stderr.write("- {} {}\n".format(path, msg))
        try:
            with open(failure_log, "w", encoding="utf-8") as f:
                for path, err in failures:
                    msg = err.strip() if err else ""
                    f.write("{}\t{}\n".format(path, msg))
        except OSError:
            sys.stderr.write("Could not write failure log: {}\n".format(failure_log))
    sys.stderr.write("Total processed: {}\n".format(total))


if __name__ == "__main__":
    main()
