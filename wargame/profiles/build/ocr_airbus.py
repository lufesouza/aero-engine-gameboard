import sys, os, pymupdf
from multiprocessing import Pool
S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
PDF = f"{S}/src/airbus/airbus_se_report_of_the_board_of_directors_fy_2025.pdf"
OUT = f"{S}/text/airbus_pages"
os.makedirs(OUT, exist_ok=True)

def work(idxs):
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    d = pymupdf.open(PDF)
    for i in idxs:
        path = f"{OUT}/{i+1:03d}.txt"
        if os.path.exists(path):
            continue
        pg = d[i]
        pix = pg.get_pixmap(dpi=150)
        res, _ = ocr(pix.tobytes("png"))
        W = pix.width
        boxes = []
        for box, text, conf in (res or []):
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            x0, x1, y0 = min(xs), max(xs), min(ys)
            boxes.append((x0, x1, y0, text))
        wide = [b for b in boxes if (b[1] - b[0]) > 0.6 * W]
        left = [b for b in boxes if b not in wide and (b[0] + b[1]) / 2 < W / 2]
        right = [b for b in boxes if b not in wide and (b[0] + b[1]) / 2 >= W / 2]
        two_col = len(left) > 5 and len(right) > 5
        if two_col:
            seq = sorted(wide + left, key=lambda b: (round(b[2] / 12), b[0])) + sorted(right, key=lambda b: (round(b[2] / 12), b[0]))
        else:
            seq = sorted(boxes, key=lambda b: (round(b[2] / 12), b[0]))
        with open(path + ".tmp", "w") as f:
            f.write("\n".join(b[3] for b in seq))
        os.replace(path + ".tmp", path)

if __name__ == "__main__":
    n = pymupdf.open(PDF).page_count
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    chunks = [list(range(j, n, k)) for j in range(k)]
    with Pool(k) as p:
        p.map(work, chunks)
    with open(f"{S}/text/airbus_fy2025.txt", "w") as f:
        for i in range(n):
            f.write(f"\n\n=== PAGE {i+1} ===\n" + open(f"{OUT}/{i+1:03d}.txt").read())
    print("done", n)
