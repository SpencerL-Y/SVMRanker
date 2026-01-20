#! /usr/bin/env python
from pycparser import c_parser
from pycparser.c_generator import CGenerator
from pycparser.c_ast import Node, Decl, TypeDecl, FuncDecl, IdentifierType,\
        FuncDef, ArrayDecl, PtrDecl, Constant, FuncCall, ArrayRef, ID, UnaryOp,\
        BinaryOp,\
        If, Compound, Label, Assignment, Return, For, While, EmptyStatement,\
        Typename
from argparse import ArgumentParser
from copy import deepcopy, copy
from CastMatch import *
import csv
import os
import sys
import re

tabsp=2


def has_pointer_type(c_ast):
    if isinstance(c_ast, PtrDecl):
        return True
    if isinstance(c_ast, ArrayDecl):
        return has_pointer_type(c_ast.type)
    if isinstance(c_ast, TypeDecl):
        return has_pointer_type(c_ast.type)
    if isinstance(c_ast, FuncDecl):
        return has_pointer_type(c_ast.type)
    return False


def collect_pointer_nodes(c_ast, hits):
    if c_ast is None:
        return
    if isinstance(c_ast, (Decl, Typename)) and has_pointer_type(c_ast.type):
        hits.append(c_ast)
    for (_, child) in c_ast.children():
        collect_pointer_nodes(child, hits)


def append_pointer_log(path, source_name, pointer_nodes):
    if not path or not pointer_nodes:
        return
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    write_header = not os.path.exists(path)
    cgen = CGenerator()
    rows = []
    for node in pointer_nodes:
        coord = str(node.coord) if node.coord is not None else ""
        name = node.name if hasattr(node, "name") and node.name is not None else ""
        kind = node.__class__.__name__
        try:
            decl_text = cgen.visit(node)
        except Exception:
            decl_text = kind
        rows.append([source_name, kind, name, coord, decl_text])
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["source", "kind", "name", "coord", "decl"])
        writer.writerows(rows)


def translate_FunDecl(c_ast):
    args = []
    if has_pointer_type(c_ast.type):
        return None
    if c_ast.args is not None:
        for idx, a in enumerate(c_ast.args.params):
            if isinstance(a, Typename):
                if has_pointer_type(a.type):
                    return None
                typ = translate_typ(a.type)
                if typ is None:
                    return None
                if typ == ["void"]:
                    continue
                args.append(("arg{}".format(idx), typ, None))
            else:
                if has_pointer_type(a.type):
                    return None
                t = translate_Decl(a)
                if t is None:
                    return None
                name = t[0] if t[0] is not None else "arg{}".format(idx)
                args.append((name, t[1], t[2]))

    subst = unify(c_ast.type, TypeDecl(Var("declname"),
                                       Var("quals", True),
                                       Var("align", True),
                                       IdentifierType(Var("ret_type"))))

    name = subst.lookup("declname")
    ret_type = subst.lookup("ret_type")
    return (name, args, ret_type)


def translate_typ(c_ast):
    if isinstance(c_ast, FuncDecl):
        return translate_FunDecl(c_ast)
    elif isinstance(c_ast, TypeDecl):
        pat = TypeDecl(Var("declname", True),
                       Var("quals", True),
                       Var("align", True),
                       IdentifierType(Var("names")))
        t = unify(pat, c_ast)
        return t.lookup("names")
    elif isinstance(c_ast, ArrayDecl):
        pat = ArrayDecl(Var("element_type"), Var("dim", True), [])
        t = unify(pat, c_ast)
        elem_typ = translate_typ(t.lookup("element_type"))
        return (elem_typ, t.lookup("dim", None))
    elif isinstance(c_ast, PtrDecl):
        return None
    else:
        NYI(c_ast)


def translate_exp(c_ast):
    if isinstance(c_ast, Constant):
        return str(c_ast.value)
    elif isinstance(c_ast, FuncCall):
        args = []
        if c_ast.args is not None:
            for arg in c_ast.args.exprs:
                args.append(translate_exp(arg))
        return "{}({})".format(c_ast.name.name, ",".join(args))
    elif isinstance(c_ast, ArrayRef):
        arr = translate_exp(c_ast.name)
        subs = translate_exp(c_ast.subscript)
        return "{}[{}]".format(arr, subs)
    elif isinstance(c_ast, ID):
        return c_ast.name
    elif isinstance(c_ast, UnaryOp):
        inner = translate_exp(c_ast.expr)
        if c_ast.op == "!":
            if isinstance(c_ast.expr, BinaryOp) and c_ast.expr.op in {"%", "+", "-", "*", "/"}:
                return "({} == 0)".format(inner)
            return "!({})".format(inner)
        if c_ast.op == "-":
            return "-({})".format(inner)
        if c_ast.op == "+":
            return "({})".format(inner)
        NYI(c_ast)
    elif isinstance(c_ast, BinaryOp):
        left = translate_exp(c_ast.left)
        right = translate_exp(c_ast.right)
        op = {
            "+": "+",
            "-": "-",
            "*": "*",
            "%": "mod",
            "/": "div",
            "<": "<",
            ">": ">",
            ">=": ">=",
            "<=": "<=",
            "==": "==",
            "!=": "!=",
            "||": "||",
            "&&": "&&",
        }[c_ast.op]
        return "({} {} {})".format(left, op, right)
    else:
        NYI(c_ast)


def translate_Decl(c_ast):
    pat = Decl(Var("name"),
               Var("quals", True),
               Var("align", True),
               Var("storage", True),
               Var("funcspec", True),
               Var("type"),
               Var("init", True),
               Var("bitsize", True))
    subst = unify(pat, c_ast)
    if subst is None:
        pat.show()
        c_ast.show()
    name = subst.lookup("name")
    raw_typ = subst.lookup("type")
    raw_init = subst.lookup("init")

    if has_pointer_type(raw_typ):
        return None
    typ = translate_typ(raw_typ)
    if typ is None:
        return None
    if raw_init is not None:
        init = translate_exp(raw_init)
    else:
        init = None

    return (name, typ, init)


class Ctx:
  def __init__(self, indent, renames, trivial_inv):
    self._indent = indent
    self._renames = renames
    self._trivial_inv = trivial_inv

  def indent(self):
    c = Ctx(self._indent + tabsp, self._renames, self._trivial_inv)
    return c


def translate_stmt(c_ast, ctx):
    istr = " "*ctx._indent
    if isinstance(c_ast, Compound):
        stmts = [translate_stmt(x, ctx) for x in c_ast.block_items]
        stmts = [x for x in stmts if len(x.strip()) > 0]
        return "\n".join(stmts)
    elif isinstance(c_ast, Decl):
        t = translate_Decl(c_ast)
        if t is None:
            return istr + ""
        if t[2] is not None:
            return istr + "{} := {};".format(t[0], t[2])
        else:
            return istr + ""
    elif isinstance(c_ast, If):
        cond = translate_exp(c_ast.cond)
        iftrue = translate_stmt(c_ast.iftrue, ctx.indent())
        if c_ast.iffalse is None:
            return istr + "if ({})\n" .format(cond) +\
                   istr + "{\n" + \
                              iftrue + \
                   istr + "}\n"
        else:
            iffalse = translate_stmt(c_ast.iffalse, ctx.indent())
            return istr + "if ({})\n" .format(cond) + \
                   istr + "{\n" + \
                              iftrue + \
                   istr + "} else {\n" +\
                              iffalse + \
                   istr + "}\n"
    elif isinstance(c_ast, Label):
        inner = translate_stmt(c_ast.stmt, ctx)
        return istr + "{}: {}".format(c_ast.name, inner)
    elif isinstance(c_ast, FuncCall):
        if c_ast.name.name in renames:
            c_ast.name.name = renames[c_ast.name.name]
        return istr + translate_exp(c_ast) + ";"
    elif isinstance(c_ast, Assignment):
        lhs = translate_exp(c_ast.lvalue)
        rhs = translate_exp(c_ast.rvalue)
        if c_ast.op == "=":
            return istr + "{} := {};".format(lhs, rhs)
        else:
            NYI(c_ast)
    elif isinstance(c_ast, Return):
        e = translate_exp(c_ast.expr)
        return ""
    elif isinstance(c_ast, For):
        init = translate_stmt(c_ast.init, ctx)
        cond = translate_exp(c_ast.cond)
        nxt = translate_stmt(c_ast.next, ctx.indent()) if c_ast.next is not None else ""
        body = translate_stmt(c_ast.stmt, ctx.indent())
        inv_str = ""
        return "{}\n".format(init) +\
               istr + "while ({})\n{}".format(cond, inv_str) + \
               istr + "{\n" + \
                        body + "\n" +\
                        nxt + "\n" +\
               istr + "}"
    elif isinstance(c_ast, While):
        cond = translate_exp(c_ast.cond)
        body = translate_stmt(c_ast.stmt, ctx)
        inv_str = ""
        return istr + "while ({})\n{}".format(cond, inv_str) + \
               istr + "{\n" +\
               body +\
               istr + "}\n"
    elif isinstance(c_ast, UnaryOp):
        inner = translate_exp(c_ast.expr)
        if c_ast.op == "p++":
            return istr + "{} := {} + 1;".format(inner, inner)
        if c_ast.op == "p--":
            return istr + "{} := {} - 1;".format(inner, inner)
        else:
            NYI(c_ast)
    elif isinstance(c_ast, EmptyStatement):
        return istr + ""
    else:
        NYI(c_ast)


def format_typ(typ):
    if typ == ["int"]:
        return "int"
    elif isinstance(typ, tuple):
        return "[int]{}".format(format_typ(typ[0]))
    elif isinstance(typ, list):
        if typ == ["void"]:
            return "void"
        if "bool" in typ or "_Bool" in typ:
            return "bool"
        int_markers = {"int", "unsigned", "signed", "short", "long", "char"}
        if any(t in int_markers for t in typ):
            return "int"
        float_markers = {"float", "double"}
        if any(t in float_markers for t in typ):
            return "real"
    else:
        NYI(typ)


def collect_assigned_names(c_ast, assigned):
    if c_ast is None:
        return
    if isinstance(c_ast, Assignment):
        lval = c_ast.lvalue
        if isinstance(lval, ID):
            assigned.add(lval.name)
        elif isinstance(lval, ArrayRef) and isinstance(lval.name, ID):
            assigned.add(lval.name.name)
    for (_, child) in c_ast.children():
        collect_assigned_names(child, assigned)


def translate_FuncDef(c_ast, ctx, global_inits=None):
    decl = translate_Decl(c_ast.decl)
    if decl is None:
        return ""
    decls = []
    if c_ast.param_decls is not None:
        NYI(c_ast.param_decls)
    stmts = [x for (_, x) in c_ast.body.children()]

    # Step 0: Build header:
    name = decl[0]
    if decl[1][2] != ['void']:
        ret_t = format_typ(decl[1][2])
    else:
        ret_t = None

    param_list = ", ".join("{}: {}".format(name, format_typ(typ))
                           for (name, typ, init) in decl[1][1])
    header = "procedure {}({})".format(name, param_list)

    # Step 1. Accumulate all definitions
    for stmt in stmts:
        if not isinstance(stmt, Decl):
            continue

        t = translate_Decl(stmt)
        if t is None:
            continue
        decls.append(t)

    dec_str = ";\n".join("{}var {}: {}".format(" "*tabsp, name,
        format_typ(typ)) for (name, typ, init) in decls)

    # Step 2. Walk over each statement and translate:
    body = translate_stmt(c_ast.body, ctx.indent())

    init_str = ""
    if global_inits and name == "main":
        init_str = "".join("{}{} := {};\n".format(" "*tabsp, g_name, g_init)
                           for (g_name, g_init) in global_inits)

    if len(dec_str.strip()) > 0:
        dec_str += ";\n"
    proc = header + "\n{\n" + dec_str + init_str + body + "\n}"
    return proc


if __name__ == "__main__":
    p = ArgumentParser(description="convert a C file to Boogie.")
    p.add_argument('input', type=str, help='Input C file')
    p.add_argument('output', type=str, help='Output Boogie file')
    p.add_argument('--skip-methods', type=str, nargs="+",
                   help='Methods names which to omit', default=[])
    p.add_argument('--assert-method', type=str,
            help='Name of the C method equivalent to assert', required=True)
    p.add_argument('--assume-method', type=str,
            help='Name of the C method equivalent to assume', required=True)
    p.add_argument('--add-trivial-invariants', action="store_true",
            default=False,
            help='If specified add "invariant true;" to each while loop')
    p.add_argument('--pointer-log', type=str, default=None,
            help='CSV file path for logging pointer declarations')
    p.add_argument('--input-name', type=str, default=None,
            help='Original filename when reading from stdin')

    args = p.parse_args()

    cparser = c_parser.CParser()
    if args.input == 'stdin':
        src = sys.stdin.read()
    else:
        src = open(args.input).read()

    src = re.sub(re.compile('__attribute__ *\(\(.*\)\)([^)])'), "\\1", src)
    ast = cparser.parse(src)

    source_name = args.input_name if args.input_name else (
        args.input if args.input != "stdin" else "stdin")
    pointer_nodes = []
    collect_pointer_nodes(ast, pointer_nodes)
    append_pointer_log(args.pointer_log, source_name, pointer_nodes)

    renames = {
        args.assert_method: "assert",
        args.assume_method: "assume",
    }

    ctx = Ctx(0, renames, args.add_trivial_invariants)

    assigned_names = set()
    for x in ast.ext:
        if isinstance(x, FuncDef):
            collect_assigned_names(x, assigned_names)

    global_decls = []
    global_inits = []
    for x in ast.ext:
        if isinstance(x, Decl):
            if isinstance(x.type, FuncDecl):
                t = translate_FunDecl(x.type)
                if t is None:
                    continue
                name, args_list, ret_type = t
                if name in args.skip_methods:
                    continue
                if ret_type == ["void"]:
                    continue
                param_list = ", ".join("{}: {}".format(p_name, format_typ(p_typ))
                                       for (p_name, p_typ, _init) in args_list)
                global_decls.append("function {}({}) returns ({});".format(
                    name, param_list, format_typ(ret_type)))
            else:
                t = translate_Decl(x)
                if t is None:
                    continue
                name, typ, init = t
                typ_str = format_typ(typ)
                if init is not None and name not in assigned_names and isinstance(x.init, Constant):
                    global_decls.append("const {}: {};".format(name, typ_str))
                    global_decls.append("axiom {} == {};".format(name, init))
                else:
                    global_decls.append("var {}: {};".format(name, typ_str))
                    if init is not None:
                        global_inits.append((name, init))

    boogie_text = ""
    if len(global_decls) > 0:
        boogie_text += "\n".join(global_decls) + "\n"
    for x in ast.ext:
        if isinstance(x, FuncDef) and x.decl.name not in args.skip_methods:
            t = translate_FuncDef(x, ctx, global_inits)
            if t:
                boogie_text += t

    if args.output == "stdout":
      sys.stdout.write(boogie_text)
    else:
      with open(args.output, "w") as f:
        f.write(boogie_text)
