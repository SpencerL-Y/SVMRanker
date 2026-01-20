
import sys
import os
import datetime
import random
import re
import hashlib

def _boogie_uses_int_ops(sourceFile):
    try:
        with open(sourceFile, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return False
    return re.search(r"\bmod\b|\bdiv\b", content) is not None

def _maybe_print_oneloop_L(out_py, sourceFile):
    flag = os.environ.get("SVMRANKER_PRINT_ONELOOP", "")
    if flag.lower() not in ("1", "true", "yes", "on"):
        return
    try:
        with open(out_py, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if start_idx is None and line.strip().startswith("L = ["):
            start_idx = i
            continue
        if start_idx is not None and re.match(r"^\s*\]\s*$", line):
            end_idx = i
            break
    if start_idx is None:
        return
    if end_idx is None:
        end_idx = len(lines) - 1
    print("[OneLoop L] " + str(sourceFile))
    for line in lines[start_idx:end_idx + 1]:
        print(line.rstrip("\n"))
    print("[/OneLoop L]")

def _extract_var_names(decl):
    decl = decl.strip().rstrip(";")
    if ":" in decl:
        decl = decl.split(":", 1)[0]
    names = [item.strip() for item in decl.split(",")]
    return [name for name in names if name]

def _normalize_boogie_file(sourceFile):
    try:
        with open(sourceFile, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return sourceFile, False

    changed = False
    fixed_content = re.sub(r"}\s*(procedure\s+)", r"}\n\1", content)
    if fixed_content != content:
        changed = True
    content = fixed_content
    lines = content.splitlines(True)

    label_re = re.compile(r"^(\s*)[A-Za-z_]\w*:\s*")
    for i, line in enumerate(lines):
        new_line = label_re.sub(r"\1", line)
        if new_line != line:
            lines[i] = new_line
            changed = True

    var_re = re.compile(r"^\s*var\s+(.+?);")
    proc_re = re.compile(r"^\s*procedure\s+([A-Za-z_]\w*)\s*(\((.*?)\))?")
    assign_re = re.compile(r"^\s*([A-Za-z_]\w*)\s*:=")

    global_vars = set()
    procedures = []
    current = None
    brace_depth = 0

    for idx, line in enumerate(lines):
        if current is None:
            m_var = var_re.match(line)
            if m_var:
                global_vars.update(_extract_var_names(m_var.group(1)))
            m_proc = proc_re.match(line)
            if m_proc:
                params = set()
                raw_params = m_proc.group(3) or ""
                for item in raw_params.split(","):
                    name = item.split(":", 1)[0].strip()
                    if name:
                        params.add(name)
                current = {
                    "name": m_proc.group(1),
                    "params": params,
                    "locals": set(),
                    "assigned": set(),
                    "insert_idx": None,
                    "indent": None,
                    "started": False,
                    "saw_nonvar": False,
                }
                delta = line.count("{") - line.count("}")
                if delta > 0:
                    current["started"] = True
                    brace_depth = delta
                    if current["insert_idx"] is None:
                        current["insert_idx"] = idx + 1
                        current["indent"] = re.match(r"^(\s*)", line).group(1) + "  "
        else:
            if not current["started"]:
                delta = line.count("{") - line.count("}")
                if delta > 0:
                    current["started"] = True
                    brace_depth = delta
                    if current["insert_idx"] is None:
                        current["insert_idx"] = idx + 1
                        current["indent"] = re.match(r"^(\s*)", line).group(1) + "  "
            else:
                m_var = var_re.match(line)
                if m_var:
                    current["locals"].update(_extract_var_names(m_var.group(1)))
                    if not current["saw_nonvar"]:
                        current["insert_idx"] = idx + 1
                        current["indent"] = re.match(r"^(\s*)", line).group(1)
                else:
                    if line.strip() and not line.strip().startswith("//"):
                        current["saw_nonvar"] = True
                m_assign = assign_re.match(line)
                if m_assign:
                    current["assigned"].add(m_assign.group(1))
                brace_depth += line.count("{") - line.count("}")
                if brace_depth == 0:
                    procedures.append(current)
                    current = None

    insertions = []
    for proc in procedures:
        missing = proc["assigned"] - proc["locals"] - proc["params"] - global_vars
        if not missing or proc["insert_idx"] is None:
            continue
        indent = proc["indent"] or "  "
        decl_line = indent + "var " + ", ".join(sorted(missing)) + ": int;\n"
        insertions.append((proc["insert_idx"], decl_line))

    if insertions:
        for idx, line in sorted(insertions, key=lambda x: x[0], reverse=True):
            lines.insert(idx, line)
        changed = True

    if not changed:
        return sourceFile, False

    normalized = "".join(lines)
    digest = hashlib.md5(normalized.encode("utf-8")).hexdigest()[:10]
    base_name = os.path.basename(sourceFile)
    norm_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], ".boogie_normalized")
    os.makedirs(norm_dir, exist_ok=True)
    norm_path = os.path.join(norm_dir, f"{base_name}.{digest}.bpl")
    try:
        with open(norm_path, "w", encoding="utf-8") as f:
            f.write(normalized)
    except OSError:
        return sourceFile, False
    return norm_path, True

def _invalidate_oneloop_cache():
    try:
        sys.modules.pop("OneLoop", None)
        import importlib
        importlib.invalidate_caches()
    except Exception:
        pass

def _append_verifier_nondet_stub(out_py, force_int=False):
    try:
        with open(out_py, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return
    if "__VERIFIER_nondet_int" not in content:
        if force_int and "ONELOOP_FORCE_INT_ARITH" not in content:
            with open(out_py, "a", encoding="utf-8") as f:
                f.write("\nONELOOP_FORCE_INT_ARITH = True\n")
        return
    if "def __VERIFIER_nondet_int" in content:
        return
    stub_lines = [
        "",
        "",
        "__VERIFIER_NONDET_COUNTER = 0",
        "",
        "def __VERIFIER_nondet_int():",
        "    global __VERIFIER_NONDET_COUNTER",
        "    __VERIFIER_NONDET_COUNTER += 1",
        "    try:",
        "        from z3 import Int, is_expr",
        "        import inspect",
        "        frame = inspect.currentframe()",
        "        if frame and frame.f_back:",
        "            caller_locals = frame.f_back.f_locals",
        "            x = caller_locals.get('x')",
        "            if isinstance(x, (list, tuple)) and any(is_expr(item) for item in x):",
        "                return Int(f\"__VERIFIER_nondet_int_{__VERIFIER_NONDET_COUNTER}\")",
        "    except Exception:",
        "        pass",
        "    import random",
        "    return random.randint(-10, 10)",
        "",
    ]
    with open(out_py, "a", encoding="utf-8") as f:
        f.write("\n".join(stub_lines))
    if force_int and "ONELOOP_FORCE_INT_ARITH" not in content:
        with open(out_py, "a", encoding="utf-8") as f:
            f.write("\nONELOOP_FORCE_INT_ARITH = True\n")

def fillOneLoop():
    os.system(" echo \"from z3 import *\" > OneLoop.py")
    os.system(" echo \"L,T = [], []\" >> OneLoop.py")
 

def getLoopInfo():
	infoFullPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],'info.tmp')
	if not os.path.exists(infoFullPath):
		print('Please parsing Boogie first')
		raise Exception('Please parsing Boogie first')
	f = open(infoFullPath,'r')
	information = ''
	for line in f.readline():
		information+=line
	return information.strip().split()

def parseBoogieProgramMulti(sourceFile, outFile):
    path = os.path.split(os.path.realpath(__file__))[0]
    bpl_input = sourceFile if os.path.isabs(sourceFile) else os.path.abspath(sourceFile)
    normalized_input, _ = _normalize_boogie_file(bpl_input)
    bpl_input = normalized_input
    jar = os.path.abspath(os.path.join(path, '..', 'Boogie2python', 'boogie2python.jar'))
    out_py = os.path.abspath(os.path.join(path, outFile))
    info_tmp = os.path.abspath(os.path.join(path, 'info.tmp'))

    (sourceFilePath, sourceFileName) = os.path.split(sourceFile)
    
    version = '.'.join(sys.version.strip().split(' ')[0].split('.')[0:2])
    parse_oldtime=datetime.datetime.now()
    generatePythonLoopCommand = [
    	'java', 
    	'-jar', 
    	jar, 
    	bpl_input, 
    	'0', 
    	out_py, 
    	info_tmp
    ]
    parse_oldtime=datetime.datetime.now()
    os.system(' '.join(generatePythonLoopCommand))
    _append_verifier_nondet_stub(out_py, _boogie_uses_int_ops(bpl_input))
    _invalidate_oneloop_cache()
    _maybe_print_oneloop_L(out_py, bpl_input)
    # parsing_boogie(
    # 	os.path.abspath(os.path.join(path,'../Boogie2python/boogie2python.jar')),
    # 	os.path.join(path,sourceFilePath,sourceFileName), 
    # 	os.path.join(path,'OneLoop.py'), 
    # 	os.path.join(path,javaOutputInfo)
    # 	)
    Info = getLoopInfo()
    parse_newtime = datetime.datetime.now()
    templatePath = 'template'
    templateFileName = '.'.join([sourceFileName.strip(),'template'])
    return sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime

def parseBoogieProgramNested(sourceFile, outFile):
    path = os.path.split(os.path.realpath(__file__))[0]
    bpl_input = sourceFile if os.path.isabs(sourceFile) else os.path.abspath(sourceFile)
    normalized_input, _ = _normalize_boogie_file(bpl_input)
    bpl_input = normalized_input
    jar = os.path.abspath(os.path.join(path, '..', 'Boogie2python', 'boogie2python.jar'))
    out_py = os.path.abspath(os.path.join(path, outFile))
    info_tmp = os.path.abspath(os.path.join(path, 'info.tmp'))

    (sourceFilePath, sourceFileName) = os.path.split(sourceFile)
    
    version = '.'.join(sys.version.strip().split(' ')[0].split('.')[0:2])
    parse_oldtime=datetime.datetime.now()
    generatePythonLoopCommand = [
    	'java', 
    	'-jar', 
    	jar, 
    	bpl_input, 
    	'0', 
    	out_py, 
    	info_tmp
    ]
    os.system(' '.join(generatePythonLoopCommand))
    _append_verifier_nondet_stub(out_py, _boogie_uses_int_ops(bpl_input))
    _invalidate_oneloop_cache()
    _maybe_print_oneloop_L(out_py, bpl_input)
    # parsing_boogie(
    # 	os.path.abspath(os.path.join(path,'../Boogie2python/boogie2python.jar')),
    # 	os.path.join(path,sourceFilePath,sourceFileName), 
    # 	os.path.join(path,'OneLoop.py'), 
    # 	os.path.join(path,javaOutputInfo)
    # 	)
    Info = getLoopInfo()
    parse_newtime = datetime.datetime.now()
    templatePath = 'template'
    templateFileName = '.'.join([sourceFileName.strip(),'template'])
    return sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime
