import os
import re
import json
import config

def _cn(text):
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)

def _module_of(nodeid):
    for seg in _cn(nodeid).replace("\\", "/").split("/"):
        if seg in ("api", "web"):
            return seg
    return "unknown"


def _kind_of(report):
    name = getattr(report, "exc_name", None)
    if name:
        return name
    crash = getattr(report.longrepr, "reprcrash", None)
    if crash is not None and crash.message:
        head = crash.message.split(":")[0].strip()
        return head.rsplit(".", 1)[-1] or "未知错误"
    return "未知错误"


def _func_of(nodeid):
    return _cn(nodeid).split("[")[0]


def _dump_json(total, module_counts, groups):
    data = {
        "total": total,
        "modules": module_counts,
        "groups": [
            {
                "exc": kind,
                "count": sum(funcs.values()),
                "cases": [
                    {"func": func, "module": _module_of(func), "count": n}
                    for func, n in sorted(funcs.items(), key=lambda x: -x[1])
                ],
            }
            for kind, funcs in sorted(groups.items(), key=lambda x: -sum(x[1].values()))
        ],
    }
    path = os.path.join(config.LOG_DIR, "fail_summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def make_summary(terminalreporter):
    reports = terminalreporter.stats.get("failed", []) + terminalreporter.stats.get("error", [])
    os.makedirs(config.LOG_DIR, exist_ok=True)

    if not reports:
        _dump_json(0, {}, {})
        terminalreporter.write_line("")
        terminalreporter.write_line("失败汇总：全部通过，没有失败用例")
        return

    groups = {}
    module_counts = {}
    for rep in reports:
        kind = _kind_of(rep)
        func = _func_of(rep.nodeid)
        module = _module_of(rep.nodeid)
        groups.setdefault(kind, {})
        groups[kind][func] = groups[kind].get(func, 0) + 1
        module_counts[module] = module_counts.get(module, 0) + 1

    lines = [f"失败汇总：共 {len(reports)} 条"]
    lines.append("  按模块：" + "，".join(f"{m} {n} 条" for m, n in sorted(module_counts.items(), key=lambda x: -x[1])))
    for kind, funcs in sorted(groups.items(), key=lambda x: -sum(x[1].values())):
        total = sum(funcs.values())
        lines.append(f"  {kind}（{total} 条）")
        for func, n in sorted(funcs.items(), key=lambda x: -x[1]):
            lines.append(f"    {n:>2} 条  {func}")

    out = os.path.join(config.LOG_DIR, "fail_summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    _dump_json(len(reports), module_counts, groups)

    terminalreporter.write_line("")
    for line in lines[:1]:
        terminalreporter.write_line(line)
    for kind, funcs in sorted(groups.items(), key=lambda x: -sum(x[1].values()))[:3]:
        total = sum(funcs.values())
        terminalreporter.write_line(f"  {kind}（{total} 条）")
        for func, n in sorted(funcs.items(), key=lambda x: -x[1])[:5]:
            terminalreporter.write_line(f"    {n:>2} 条  {func}")
        if len(funcs) > 5:
            terminalreporter.write_line(f"    ……其余 {len(funcs) - 5} 个函数")
    terminalreporter.write_line(f"（完整清单：{out}）")