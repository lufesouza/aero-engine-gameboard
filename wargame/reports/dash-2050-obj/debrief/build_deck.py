"""Boeing management debrief (dash-2050-obj): the consultant's 8-slide storyline as a BCG-style deck on the Boeing PD
2026 template. Charts come straight from factpack.json by dataset id, so no chart number is retyped.

Usage: python3 build_deck.py <PDPowerPointTemplate2026.pptx> storyline.json factpack.json <out.pptx>
(python-pptx; the template is the mckinsey-to-pd skill's asset). Primitives follow wargame/reports/wg5-2045d/deck.
"""
import copy
import json
import sys

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_MARK, XL_MARKER_STYLE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

BOEING_BLUE = RGBColor(0x00, 0x33, 0xA1)
FLIGHT = RGBColor(0x00, 0x9B, 0xDF)
SPACE = RGBColor(0x0A, 0x22, 0x40)
LIFTOFF = RGBColor(0xF3, 0x71, 0x21)
PRESERVE = RGBColor(0xBF, 0xD8, 0x57)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x6B, 0x72, 0x78)
GRAY_MID = RGBColor(0x9A, 0xA3, 0xAD)
GRAY_LINE = RGBColor(0xC8, 0xCE, 0xD6)
TINT = RGBColor(0xE8, 0xEE, 0xF7)
INK = RGBColor(0x1F, 0x29, 0x37)
LAYOUT_HEADER, LAYOUT_DIVIDER = 2, 12
# series colours: entity first (Boeing is always Boeing Blue), then by role
SERIES_COLOR = {"Boeing": (BOEING_BLUE, False), "Airbus": (FLIGHT, False), "Game": (BOEING_BLUE, False),
                "Status quo": (GRAY_MID, True), "CFM/GE": (SPACE, False), "P&W (Joint Venture)": (BOEING_BLUE, False),
                "Rolls-Royce (Joint Venture)": (FLIGHT, True), "fps programme cash": (SPACE, False),
                "Free cash flow, base": (BOEING_BLUE, False), "Free cash flow, stress": (LIFTOFF, False),
                "Base case": (BOEING_BLUE, False), "Stress case": (LIFTOFF, False), "No new programme": (GRAY_MID, True),
                "fps 10-year (played)": (BOEING_BLUE, False), "Do Nothing (no fps)": (LIFTOFF, False),
                "No game (analysts' path)": (GRAY_MID, True)}
FALLBACK = [(BOEING_BLUE, False), (FLIGHT, False), (SPACE, False)]
SHORT = {"Free cash flow, base": "Base FCF", "Free cash flow, stress": "Stress FCF", "fps programme cash": "",
         "fps 10-year (played)": "Played", "No game (analysts' path)": "No game", "Do Nothing (no fps)": "Do Nothing"}


# ---------------------------------------------------------------- primitives
def strip_slides(prs):
    lst = prs.slides._sldIdLst
    rids = [s.get(qn("r:id")) for s in list(lst)]
    for s in list(lst):
        lst.remove(s)
    for rid in rids:
        prs.part.drop_rel(rid)


def nobreak(t):
    """Keep a sign with its number: no line break between +/−/- and $ or a digit."""
    for sgn in ("+", "\u2212", "-"):
        t = t.replace(sgn + "$", sgn + "\u2060$")
    return t


def text(slide, x, y, w, h, paras, anchor="t", align=PP_ALIGN.LEFT, line_spacing=None, margins=0.0, space=5):
    """paras: list of paragraphs; each a list of (text, size, bold, color[, italic]) runs."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    bp = tf._txBody.bodyPr
    bp.set("anchor", anchor)
    for tag in ("a:spAutoFit", "a:normAutofit"):
        for el in bp.findall(qn(tag)):
            bp.remove(el)
    bp.append(bp.makeelement(qn("a:noAutofit"), {}))
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margins))
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        if i:
            p.space_before = Pt(space)
        for r in runs:
            t, size, bold, color = r[:4]
            run = p.add_run()
            run.text = nobreak(t)
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = r[4] if len(r) > 4 else False
            run.font.color.rgb = color
    return tb


def rect(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, line_w=1.0):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    return s


def numbered_circle(slide, x, y, n, d=0.46, fill=BOEING_BLUE, size=16):
    c = rect(slide, x, y, d, d, fill=fill, shape=MSO_SHAPE.OVAL)
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf._txBody.bodyPr.set("anchor", "ctr")
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(n)
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = WHITE
    return c


def content_slide(prs, section, action_title, source, notes):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_HEADER]
    slide = prs.slides.add_slide(layout)
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == 11:  # blue-bar label: the section name
            ph.text_frame.text = section
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(18)
                    r.font.bold = True
                    r.font.color.rgb = WHITE
        else:  # org name (13) and the big body title (15) are dropped
            ph._element.getparent().remove(ph._element)
    for sp in layout.placeholders:  # page number: clone the layout's slide-number placeholder
        if "SLIDE_NUMBER" in str(sp.placeholder_format.type):
            slide.shapes._spTree.append(copy.deepcopy(sp._element))
    text(slide, 0.5, 0.86, 12.33, 1.04, [[(action_title, 28, True, SPACE)]], anchor="ctr", line_spacing=0.92)
    text(slide, 0.5, 6.80, 10.5, 0.28, [[(source, 9, False, GRAY, True)]])
    slide.notes_slide.notes_text_frame.text = notes
    return slide


def cover_slide(prs, title, subtitle, date_str):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_DIVIDER]
    slide = prs.slides.add_slide(layout)
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == 0:
            ph.text_frame.text = title
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(44)
                    r.font.bold = True
        else:
            ph._element.getparent().remove(ph._element)
    text(slide, 0.56, 4.95, 12.2, 1.2, [[(subtitle, 22, False, WHITE)], [(date_str, 16, False, WHITE)]], line_spacing=1.05, space=10)
    return slide


def takeaway_strip(slide, x, y, w, h, body, header="Key takeaway", size=16):
    rect(slide, x, y, w, h, fill=BOEING_BLUE)
    text(slide, x + 0.22, y + 0.1, w - 0.44, h - 0.2, [[(header.upper() + "   ", 12, True, WHITE), (body, size, False, WHITE)]],
         anchor="ctr", line_spacing=1.0)


def bullets_box(slide, x, y, w, h, bullets, size=15):
    paras = [[("•  ", size, True, BOEING_BLUE), (b, size, False, INK)] for b in bullets]
    text(slide, x, y, w, h, paras, line_spacing=1.04, space=9)


def style_chart(chart, size=12):
    chart.font.size = Pt(size)
    chart.font.color.rgb = INK
    chart.has_title = False


# ---------------------------------------------------------------- visuals
def _manual_plot(chart, x, y, w, h):
    """Pin the inner plot area (fractions of the chart frame) so overlays can be placed on data coordinates."""
    pa = chart._chartSpace.chart.plotArea
    old = pa.find(qn("c:layout"))
    if old is not None:
        pa.remove(old)
    lay = pa.makeelement(qn("c:layout"), {})
    ml = lay.makeelement(qn("c:manualLayout"), {})
    for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                     ("c:x", f"{x}"), ("c:y", f"{y}"), ("c:w", f"{w}"), ("c:h", f"{h}")):
        el = ml.makeelement(qn(tag), {"val": val})
        ml.append(el)
    lay.append(ml)
    pa.insert(0, lay)


def visual_line(slide, v, FP, x, y, w, h):
    from pptx.chart.data import XyChartData
    ds = FP["datasets"][v["dataset"]]
    yrs = ds["years"]
    lo_y, hi_y = (v.get("years") or [yrs[0], yrs[-1]])[:2]
    idx = [i for i, yy in enumerate(yrs) if lo_y <= yy <= hi_y]
    names = [n for n in (v.get("series") or list(ds["series"])) if n in ds["series"]]
    share = ds["unit"] == "share"
    k = 100 if share else 1
    cd = XyChartData()
    for n in names:
        sr = cd.add_series(n)
        for i in idx:
            sr.add_data_point(yrs[i], ds["series"][n][i] * k)
    ch = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    style_chart(ch)
    ch.has_legend = len(names) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(13)
    vals = [ds["series"][n][i] * k for n in names for i in idx]
    if share:
        y_lo, y_hi, step = 0, (100 if max(vals) > 80 else 80), 20
        fmt = '0"%"'
    else:
        top = max(vals)
        step = 5 if top <= 30 else (50 if top <= 300 else 100)
        y_lo, y_hi = min(0, min(vals)), step * (int(top / step) + 1)
        fmt = '0'
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = y_lo, y_hi, step
    va.tick_labels.number_format = fmt
    va.tick_labels.number_format_is_linked = False
    va.tick_labels.font.size = Pt(12)
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GRAY_LINE
    va.format.line.fill.background()
    xa = ch.category_axis
    x_lo, x_hi = yrs[idx[0]], yrs[idx[-1]]
    unit_x = 5 if x_hi - x_lo > 15 else (2 if x_hi - x_lo > 8 else 1)
    x_lo -= x_lo % unit_x                     # ticks on round years (2025, 2030, ...)
    xa.minimum_scale, xa.maximum_scale = x_lo, x_hi
    xa.major_unit = unit_x
    xa.tick_labels.number_format = '0'
    xa.tick_labels.number_format_is_linked = False
    xa.tick_labels.font.size = Pt(12)
    xa.has_major_gridlines = False
    xa.major_tick_mark = XL_TICK_MARK.NONE
    xa.format.line.color.rgb = GRAY_LINE
    for kk, (ser, n) in enumerate(zip(ch.plots[0].series, names)):
        color, dash = SERIES_COLOR.get(n, FALLBACK[kk % 3])
        ser.smooth = False
        ser.format.line.color.rgb = color
        ser.format.line.width = Pt(2.75)
        if dash:
            ser.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        ser.marker.style = XL_MARKER_STYLE.NONE
    PX, PY, PW, PH = 0.085, 0.13, 0.70, 0.74
    _manual_plot(ch, PX, PY, PW, PH)
    to_x = lambda yr: x + w * (PX + PW * (yr - x_lo) / (x_hi - x_lo))
    to_y = lambda val: y + h * (PY + PH * (y_hi - val) / (y_hi - y_lo))
    # direct end labels, spread 0.26" apart
    ends = sorted(((ds["series"][n][idx[-1]] * k, n) for n in names), reverse=True)
    last = None
    for val, n in ends:
        yy = to_y(val) - 0.13
        yy = yy if last is None else max(yy, last + 0.26)
        last = yy
        short = SHORT.get(n, n.split(" (")[0])
        if not short:
            continue
        lab = f"{short} {val:.0f}%" if share else f"{short} {val:.1f}"
        text(slide, to_x(x_hi) + 0.08, yy, w * (1 - PX - PW) - 0.1, 0.26,
             [[(lab, 12, True, SERIES_COLOR.get(n, FALLBACK[0])[0])]])
    # annotations: numbered markers on the named series (default: the first); the key goes under the chart
    keys = []
    for a in v.get("annotations") or []:
        yr = a["year"]
        if not names or yr not in yrs[idx[0]: idx[-1] + 1]:
            continue
        sname = a.get("series") if a.get("series") in names else names[0]
        val = ds["series"][sname][yrs.index(yr)] * k
        cx, cy = to_x(yr), to_y(val)
        keys.append(a["text"])
        numbered_circle(slide, cx - 0.15, cy - 0.15 - 0.3, len(keys), d=0.3, fill=SPACE, size=11)
        rect(slide, cx - 0.06, cy - 0.06, 0.12, 0.12, fill=SPACE, line=WHITE, shape=MSO_SHAPE.OVAL, line_w=1.0)
    unit = "% of deliveries" if share else ("$B" + (", 2026 dollars" if v["dataset"] in ("boeing_cash", "net_debt", "owners_cash") else ", 2026 prices"))
    text(slide, x, y + h + 0.02, w, 0.26, [[(unit, 10, False, GRAY, True)]])
    if keys:
        paras = [[(f"{i + 1}  ", 12, True, SPACE), (t, 12, False, INK)] for i, t in enumerate(keys)]
        text(slide, x, y + h + 0.28, w, 0.75, [sum(([(f"{i + 1} ", 12, True, BOEING_BLUE), (t + ("     " if i < len(keys) - 1 else ""), 12, False, INK)]
                                                     for i, t in enumerate(keys)), [])], line_spacing=1.0)


def visual_bridge(slide, v, FP, x, y, w, h):
    items = FP["datasets"]["pv_bridge"]["items"]
    base, val, run = [], [], 0.0
    for i, (n, d) in enumerate(items):
        last = i == len(items) - 1
        if last:
            base.append(0.0); val.append(abs(d))
        elif d >= 0:
            base.append(run); val.append(d); run += d
        else:
            run += d; base.append(run); val.append(-d)
    cd = CategoryChartData()
    cd.categories = ["Value created" if n == "ΔPV" else n for n, _ in items]
    cd.add_series("base", base)
    cd.add_series("value", val)
    ch = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    style_chart(ch, 13)
    ch.has_legend = False
    b_ser, v_ser = ch.plots[0].series
    b_ser.format.fill.background()
    b_ser.format.line.fill.background()
    ch.plots[0].gap_width = 60
    for j, (n, d) in enumerate(items):
        pt = v_ser.points[j]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = SPACE if j == len(items) - 1 else (BOEING_BLUE if d >= 0 else GRAY_MID)
        dl = pt.data_label
        dl.has_text_frame = True
        dl.text_frame.text = f"{d:+.2f}".replace("-", "−")
        small = abs(d) < 2
        dl.position = XL_LABEL_POSITION.INSIDE_BASE if small else XL_LABEL_POSITION.INSIDE_END
        for p in dl.text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(14)
                r.font.bold = True
                r.font.color.rgb = SPACE if small else WHITE
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = 0, 25, 5
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GRAY_LINE
    va.tick_labels.font.size = Pt(12)
    va.format.line.fill.background()
    ch.category_axis.tick_labels.font.size = Pt(12)
    ch.category_axis.major_tick_mark = XL_TICK_MARK.NONE
    text(slide, x, y + h + 0.02, w, 0.26, [[("$B, present value at 2026", 10, False, GRAY, True)]])


def visual_stats(slide, v, x, y, w, h):
    st = v["stats"]
    n = len(st)
    cols = 2 if n == 4 else n
    rows = 2 if n == 4 else 1
    gap = 0.16
    bw = (w - gap * (cols - 1)) / cols
    bh = (h - gap * (rows - 1)) / rows
    for i, s_ in enumerate(st):
        bx = x + (i % cols) * (bw + gap)
        by = y + (i // cols) * (bh + gap)
        rect(slide, bx, by, bw, bh, fill=TINT)
        rect(slide, bx, by, 0.08, bh, fill=BOEING_BLUE)
        text(slide, bx + 0.25, by + 0.12, bw - 0.4, 0.62, [[(s_["value"], 30, True, BOEING_BLUE)]])
        text(slide, bx + 0.25, by + 0.74, bw - 0.4, bh - 0.82, [[(s_["label"], 14, False, INK)]], line_spacing=1.0)


def visual_table(slide, v, x, y, w, h):
    t = v["table"]
    cols, rows = t["columns"], t["rows"]
    HEAD, ROW = 0.5, 0.34
    shp = slide.shapes.add_table(len(rows) + 1, len(cols), Inches(x), Inches(y), Inches(w), Inches(HEAD + ROW * len(rows)))
    tbl = shp.table
    tbl.rows[0].height = Inches(HEAD)
    for r_ in range(1, len(rows) + 1):
        tbl.rows[r_].height = Inches(ROW)
    first_w = w * (0.34 if len(cols) > 3 else 0.4)
    rest = (w - first_w) / max(1, len(cols) - 1)
    for j in range(len(cols)):
        tbl.columns[j].width = Inches(first_w if j == 0 else rest)
    for j, c in enumerate(cols):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SPACE
        cell.text = c
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            for r in p.runs:
                r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = WHITE
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = TINT if i % 2 == 0 else WHITE
            cell.text = str(c)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.size = Pt(14); r.font.color.rgb = INK; r.font.bold = j == 0
            cell.margin_top = cell.margin_bottom = Inches(0.03)


def visual_recs(slide, v, x, y, w, h):
    recs = v["recs"]
    n = len(recs)
    cols = 2 if n >= 4 else 1
    rows = (n + cols - 1) // cols
    gap = 0.14
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    for i, r in enumerate(recs):
        cx = x + (i % cols) * (cw + gap)
        cy = y + (i // cols) * (ch + gap)
        rect(slide, cx, cy, cw, ch, fill=TINT)
        numbered_circle(slide, cx + 0.1, cy + 0.1, i + 1, d=0.4, size=15)
        text(slide, cx + 0.6, cy + 0.06, cw - 0.66, ch - 0.1,
             [[(r["recommendation"], 15, True, SPACE)], [("Why: ", 13, True, BOEING_BLUE), (r["why"], 13, False, INK)],
              [("Proof: ", 13, True, BOEING_BLUE), (r["proof"], 13, False, INK)]], line_spacing=1.0, space=3)


def visual_risks(slide, v, x, y, w, h):
    risks = v["risks"]
    cols = [("Risk", 0.24), ("Trigger", 0.21), ("Cost", 0.24), ("Mitigation", 0.31)]
    hy = 0.42
    cx = x
    for name, f in cols:
        rect(slide, cx, y, w * f - 0.04, hy, fill=SPACE)
        text(slide, cx + 0.1, y, w * f - 0.2, hy, [[(name, 14, True, WHITE)]], anchor="ctr")
        cx += w * f
    rh = (h - hy - 0.06) / len(risks)
    for i, r in enumerate(risks):
        ry = y + hy + 0.06 + i * rh
        rect(slide, x, ry, w - 0.04, rh - 0.06, fill=TINT if i % 2 == 0 else WHITE, line=GRAY_LINE, line_w=0.5)
        cx = x
        for k, (name, f) in enumerate(cols):
            key = name.lower()
            text(slide, cx + 0.1, ry + 0.06, w * f - 0.22, rh - 0.16, [[(r[key], 13, k == 0, SPACE if k == 0 else INK)]], line_spacing=1.0)
            cx += w * f


def visual_columns(slide, v, x, y, w, h):
    cols = v["columns"]
    n = len(cols)
    gap = 0.2
    cw = (w - gap * (n - 1)) / n
    for i, c in enumerate(cols):
        cx = x + i * (cw + gap)
        rect(slide, cx, y, cw, 0.5, fill=BOEING_BLUE if i == 0 else SPACE)
        text(slide, cx + 0.15, y, cw - 0.3, 0.5, [[(c["header"], 17, True, WHITE)]], anchor="ctr")
        rect(slide, cx, y + 0.5, cw, h - 0.5, fill=TINT)
        bullets_box(slide, cx + 0.18, y + 0.66, cw - 0.36, h - 0.8, c["bullets"], size=15)


CHARTY = {"line", "bridge", "stats"}


def build_slide(prs, s, FP):
    slide = content_slide(prs, s["section"], s["action_title"], s["source"], s["notes"])
    v = s["visual"]
    t = v["type"]
    bullets = s.get("bullets") or []
    if t in CHARTY:
        # visual (left) + takeaway strip under it; evidence bullets in the right column
        vx, vy, vw, vh = 0.5, 2.0, 7.95, 3.55
        if t == "line":
            visual_line(slide, v, FP, vx, vy, vw, vh - (0.5 if v.get("annotations") else 0))
        elif t == "bridge":
            visual_bridge(slide, v, FP, vx, vy, vw, vh)
        else:
            visual_stats(slide, v, vx, vy, vw, vh + 0.25)
        takeaway_strip(slide, 0.5, 5.92, 7.95, 0.8, s["takeaway"])
        rect(slide, 8.75, 2.0, 0.04, 4.72, fill=GRAY_LINE)
        bullets_box(slide, 9.0, 2.0, 3.83, 4.72, bullets)
    else:
        band = None
        if t == "table":
            nrows = len(v["table"]["rows"]) + 1
            visual_table(slide, v, 0.5, 2.0, 12.33, 2.6)
            band = (0.5, 2.0 + 0.5 + 0.34 * (nrows - 1) + 0.12, 2, 13)
        elif t == "recs":
            visual_recs(slide, v, 0.5, 1.98, 12.33, 3.3 if bullets else 3.86)
            band = (0.5, 5.34, 2, 13)
        elif t == "risks":
            visual_risks(slide, v, 0.5, 1.98, 12.33, 3.48 if bullets else 3.86)
            band = (0.5, 5.5, len(bullets) or 1, 12)
        else:
            visual_columns(slide, v, 0.5, 2.0, 12.33, 3.75)
        if bullets and band:
            bx, by, ncol, size = band
            ncol = min(ncol, len(bullets))
            per = (len(bullets) + ncol - 1) // ncol
            colw = (12.33 - 0.3 * (ncol - 1)) / ncol
            for c in range(ncol):
                chunk = bullets[c * per:(c + 1) * per]
                bullets_box(slide, bx + c * (colw + 0.3), by, colw, 5.86 - by, chunk, size=size)
        takeaway_strip(slide, 0.5, 5.92, 12.33, 0.8, s["takeaway"])
    return slide


def main():
    template, story_p, fp_p, out = sys.argv[1:5]
    S = json.load(open(story_p))
    FP = json.load(open(fp_p))
    prs = Presentation(template)
    strip_slides(prs)
    cover_slide(prs, S["cover"]["title"], S["cover"]["subtitle"], "Debrief to Boeing executive leadership · October 2026")
    for s in S["slides"]:
        build_slide(prs, s, FP)
    prs.save(out)
    print("saved", out, len(prs.slides), "slides")


if __name__ == "__main__":
    main()
