#!/usr/bin/env python3
"""Doi ID lop hang loat trong file nhan YOLO (vd CVAT xuat thu tu lop khac schema).

Vi du: CVAT xuat  car=0 bus=1 van=2 truck=3  nhung schema bai lab la car=0 truck=1 bus=2 van=3
  -> id 1(bus)->2, id 2(van)->3, id 3(truck)->1   =>   --map 1:2,2:3,3:1

Chay tu thu muc goc repo:
    python tools/remap_classes.py --map 1:2,2:3,3:1 --dry-run   (xem truoc, khong ghi)
    python tools/remap_classes.py --map 1:2,2:3,3:1             (ghi that, tu sao luu ban goc)

Cac ID duoc doi DONG THOI (khong doi lien tiep) nen hoan vi vong tron an toan.
CHI CHAY MOT LAN: script tu tao file danh dau .remapped_classes va tu choi chay lai (tru khi --force).
"""
import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

NAMES = {0: "car", 1: "truck", 2: "bus", 3: "van"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="dataset/labels/train")
    ap.add_argument("--map", required=True, help='vd "1:2,2:3,3:1"  (id_cu:id_moi)')
    ap.add_argument("--backup", default="outputs/labels_backup")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    try:
        m = {int(k): int(v) for k, v in (x.split(":") for x in a.map.split(","))}
    except ValueError:
        sys.exit('--map sai dinh dang. Vi du dung: --map 1:2,2:3,3:1')
    if any(not 0 <= x <= 3 for kv in m.items() for x in kv):
        sys.exit("ID lop phai nam trong 0..3")

    d, marker = Path(a.dir), Path(a.dir) / ".remapped_classes"
    files = sorted(d.glob("*.txt"))
    if not files:
        sys.exit(f"Khong thay file .txt nao trong {d}")
    if marker.exists() and not a.force:
        sys.exit("Thu muc nay DA duoc doi lop roi (co file .remapped_classes). "
                 "Chay lai se lam lon xon ID. Dung --force chi khi chac chan.")

    before, after, new_text = Counter(), Counter(), {}
    for f in files:
        out = []
        for line in f.read_text().splitlines():
            p = line.split()
            if len(p) == 5:
                c = int(p[0]); before[c] += 1
                nc = m.get(c, c); after[nc] += 1
                p[0] = str(nc)
                out.append(" ".join(p))
            elif line.strip():
                out.append(line)
        new_text[f] = ("\n".join(out) + "\n") if out else ""

    show = lambda c: ", ".join(f"{k}({NAMES.get(k, '?')})={c[k]}" for k in sorted(c))
    print(f"Anh xa: " + ", ".join(f"{k}->{v}" for k, v in sorted(m.items())))
    print(f"Truoc: {show(before)}")
    print(f"Sau  : {show(after)}")
    if a.dry_run:
        print("(--dry-run: chua ghi gi)")
        return

    bk = Path(a.backup)
    if bk.exists() and any(bk.iterdir()) and not a.force:
        sys.exit(f"Thu muc sao luu {bk} da co file. Doi ten/xoa no hoac dung --backup khac.")
    bk.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.copy2(f, bk / f.name)
    for f, t in new_text.items():
        f.write_text(t)
    marker.write_text("remapped " + a.map + "\n")
    print(f"Da doi {len(files)} file. Ban goc luu o {bk}")


if __name__ == "__main__":
    main()
