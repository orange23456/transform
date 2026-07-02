import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def run_generator(script_path, output_dir):
    script_path = Path(script_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    source = script_path.read_text(encoding="utf-8-sig", errors="ignore")
    patched, count = re.subn(
        r"^out\s*=\s*Path\(.+?\)\s*$",
        lambda _match: "out = Path(r'" + str(output_dir) + "')",
        source,
        count=1,
        flags=re.M,
    )
    if count != 1:
        raise RuntimeError(f"没有找到可替换的输出目录: {script_path}")

    code = compile(patched, str(script_path), "exec")
    namespace = {"__name__": "__main__", "__file__": str(script_path)}
    exec(code, namespace)


def main():
    parser = argparse.ArgumentParser(description="Run HTML generator scripts into a safe staging folder.")
    parser.add_argument("--script-root", default=r"C:\Users\hz-user\Documents\HTML生成")
    parser.add_argument("--output-root", default=str(Path(__file__).with_name("generated_html")))
    args = parser.parse_args()

    script_root = Path(args.script_root)
    output_root = Path(args.output_root)
    jobs = [
        (script_root / "gen_heating_stirring.py", output_root / "Atomfair_heating_stirring_HTML"),
        (script_root / "gen_distillation.py", output_root / "Atomfair_distillation_HTML"),
    ]

    for script_path, output_dir in jobs:
        print(f"RUN={script_path}")
        run_generator(script_path, output_dir)
        print(f"STAGED={output_dir}")


if __name__ == "__main__":
    main()

