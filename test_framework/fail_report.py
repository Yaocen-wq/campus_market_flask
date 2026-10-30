import os
import re
import config


def _cn(text):
    """把 nodeid 里的 \\u6b63 这类转义还原成中文"""
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)


def _kind_of(report):
    """取异常类型名：AssertionError / ConnectionError / JSONDecodeError"""
    name = getattr(report, "exc_name", None)
    if name:
        return name
    crash = getattr(report.longrepr, "reprcrash", None)
    if crash is not None and crash.message:
        head = crash.message.split(":")[0].strip()
        return head.rsplit(".", 1)[-1] or "未知错误"
    return "未知错误"


def _func_of(nodeid):
    """project_test.py::test_publish[空标题] -> project_test.py::test_publish"""
    return _cn(nodeid).split("[")[0]


def make_summary(terminalreporter):
    reports = terminalreporter.stats.get("failed", []) + terminalreporter.stats.get("error", [])
    if not reports:
        terminalreporter.write_line("")
        terminalreporter.write_line("失败汇总：全部通过，没有失败用例")
        return

    groups = {}
    for rep in reports:
        kind = _kind_of(rep)
        func = _func_of(rep.nodeid)
        groups.setdefault(kind, {})
        groups[kind][func] = groups[kind].get(func, 0) + 1

    lines = [f"失败汇总：共 {len(reports)} 条"]
    for kind, funcs in sorted(groups.items(), key=lambda x: -sum(x[1].values())):
        total = sum(funcs.values())
        lines.append(f"  {kind}（{total} 条）")
        for func, n in sorted(funcs.items(), key=lambda x: -x[1]):
            lines.append(f"    {n:>2} 条  {func}")

    os.makedirs(config.LOG_DIR, exist_ok=True)
    out = os.path.join(config.LOG_DIR, "fail_summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

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