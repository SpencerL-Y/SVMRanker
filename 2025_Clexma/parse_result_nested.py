#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
import json

PROGRAM_NON_FOLDER = os.path.join(os.getcwd(), "Program_Boogie_Total")
SIFTED_TERMINATE_FOLDER = os.path.join(os.getcwd(), "2025_Clexma", "Nested", "4-nested-terminate")

def sift_terminate_files(terminate_list):
    for item in terminate_list:
        fname = item['filename']
        depth = item['nested_depth']
        original_file = os.path.join(PROGRAM_NON_FOLDER, fname)
        os.system("cp " + original_file + " " + os.path.join(SIFTED_TERMINATE_FOLDER, str(depth) + "_" + fname))

def parse_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # 提取 Running time（若无则跳过）
    time_m = re.search(r"Running time:\s*([\d.]+)\s*s", text)
    if not time_m:
        return None
    time_val = float(time_m.group(1))

    # 提取 LEARNING RESULT
    result_m = re.search(r"LEARNING RESULT:\s*(TERMINATE|NONTERM|UNKNOWN)", text)
    if not result_m:
        return None
    result = result_m.group(1)

    # 仅当 TERMINATE 时提取 NESTED DEPTH
    nested_depth = None
    if result == "TERMINATE":
        depth_m = re.search(r"NESTED DEPTH:\s*(\d+)", text)
        if depth_m:
            nested_depth = int(depth_m.group(1))

    return {
        'filename': os.path.basename(path),
        'result': result,
        'nested_depth': nested_depth,
        'time': time_val
    }

def parse_folder(folder):
    records = []
    for name in os.listdir(folder):
        if not name.lower().endswith('.txt'):
            continue
        info = parse_file(os.path.join(folder, name))
        if info:
            records.append(info)
    return records

def main():
    p = argparse.ArgumentParser(
        description="解析文件夹中终止性分析的 txt 输出，提取 result、nested depth、time"
    )
    p.add_argument('folder', help="待解析的 txt 文件夹路径")
    p.add_argument(
        '--json', '-j',
        action='store_true',
        help="以 JSON 格式输出（仅 TERMINATE，且提取 core filename 和 nested_depth）"
    )
    args = p.parse_args()

    results = parse_folder(args.folder)

    if args.json:
        # 1. 筛选出 TERMINATE 记录
        terminate_only = [r for r in results if r['result'] == 'TERMINATE']
        # 2. 提取 core filename
        cleaned = []
        for r in terminate_only:
            m = re.match(r"output_(.+?\.bpl)\.txt$", r["filename"])
            if m:
                core = m.group(1)
            else:
                # 如果不符合标准格式，去掉前缀和后缀
                core = r["filename"].replace("output_", "").rsplit(".txt", 1)[0]
            cleaned.append({
                "filename": core,
                "nested_depth": r["nested_depth"]
            })
        print(json.dumps(cleaned, indent=2))
        sift_terminate_files(cleaned)
    else:
        # 默认以表格形式打印所有记录
        print(f"{'FILENAME':30}  {'RESULT':10}  {'DEPTH':5}  {'TIME(s)':>8}")
        print("-"*60)
        for r in results:
            depth = r['nested_depth'] if r['nested_depth'] is not None else '-'
            print(f"{r['filename']:30}  {r['result']:10}  {depth:^5}  {r['time']:8.3f}")

if __name__ == "__main__":
    main()