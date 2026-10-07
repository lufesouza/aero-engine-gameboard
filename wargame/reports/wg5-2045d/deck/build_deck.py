"""Five-slide BCG-style deck on the Boeing PD 2026 template: the war-game story and a recommendation.

Usage: python build_deck.py <PDPowerPointTemplate2026.pptx> <out.pptx>   (needs python-pptx; template from the mckinsey-to-pd skill assets)
"""
import copy
import sys

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_MARK, XL_MARKER_STYLE, XL_TICK_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

BOEING_BLUE = RGBColor(0x00, 0x33, 0xA1)
FLIGHT = RGBColor(0x00, 0x9B, 0xDF)
SPACE = RGBColor(0x0A, 0x22, 0x40)
LIFTOFF = RGBColor(0xF3, 0x71, 0x21)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x6B, 0x72, 0x78)
GRAY_LINE = RGBColor(0xC8, 0xCE, 0xD6)
TINT = RGBColor(0xE8, 0xEE, 0xF7)
INK = RGBColor(0x1F, 0x29, 0x37)

LAYOUT_HEADER = 2  # "4_Inside_Page_Header": blue bar, copyright, BOEING PROPRIETARY, slide number
SOURCE = "Source: Five-player war-game engine, runs wg5-2045 (fps on time) and wg5-2045d (fps three years late); team analysis"


# ---------------------------------------------------------------- primitives
def strip_slides(prs):
    lst = prs.slides._sldIdLst
    rids = [s.get(qn("r:id")) for s in list(lst)]
    for s in list(lst):
        lst.remove(s)
    for rid in rids:
        prs.part.drop_rel(rid)


def text(slide, x, y, w, h, paras, anchor="t", align=PP_ALIGN.LEFT, line_spacing=None, margins=0.0):
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
            p.space_before = Pt(5)
        for r in runs:
            t, size, bold, color = r[:4]
            run = p.add_run()
            run.text = t
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


def numbered_circle(slide, x, y, n, d=0.52, fill=BOEING_BLUE):
    c = rect(slide, x, y, d, d, fill=fill, shape=MSO_SHAPE.OVAL)
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf._txBody.bodyPr.set("anchor", "ctr")
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(n)
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = WHITE
    return c


def content_slide(prs, section, action_title, source=SOURCE):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_HEADER]
    slide = prs.slides.add_slide(layout)
    for ph in list(slide.placeholders):
        idx = ph.placeholder_format.idx
        if idx == 11:  # blue-bar label: the section name
            ph.text_frame.text = section
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(18)
                    r.font.bold = True
                    r.font.color.rgb = WHITE
        else:  # org name (13) and the big body title (15) are dropped
            ph._element.getparent().remove(ph._element)
    # page number: clone the layout's slide-number placeholder (python-pptx does not)
    for sp in layout.placeholders:
        if sp.placeholder_format.type is not None and "SLIDE_NUMBER" in str(sp.placeholder_format.type):
            slide.shapes._spTree.append(copy.deepcopy(sp._element))
    text(slide, 0.5, 0.92, 12.33, 0.98, [[(action_title, 28, True, SPACE)]], anchor="ctr", line_spacing=0.95)
    text(slide, 0.5, 6.80, 10.5, 0.28, [[(source, 9, False, GRAY, True)]])
    return slide


def takeaway(slide, x, y, w, h, header, body_paras, size=16):
    rect(slide, x, y, w, h, fill=BOEING_BLUE)
    paras = [[(header.upper(), 13, True, WHITE)]] + [[(t, size, b, WHITE)] for t, b in body_paras]
    text(slide, x + 0.22, y + 0.2, w - 0.44, h - 0.4, paras, line_spacing=1.05)


def style_chart(chart, size=12):
    chart.font.size = Pt(size)
    chart.font.color.rgb = INK
    chart.has_title = False


# ---------------------------------------------------------------- slides
def slide1(prs):
    s = content_slide(prs, "The simulation",
                      "A five-player war game to 2045 shows fps timing decides Boeing's strategy: "
                      "narrowbody defence or widebody pivot")
    steps = [
        ("Five executive teams", "Boeing, Airbus, Rolls-Royce, P&W and CFM/GE, each an independent AI agent"),
        ("Sealed orders", "Simultaneous moves each round; rivals see only public statements"),
        ("Engine makers move first", "An airframe that names an uncommitted engine falls back to an existing one"),
        ("Market reacts", "Airlines and lessors set demand for each new aircraft"),
        ("Three rounds", "To 2030, 2035 and 2045, with a supply crunch, a fuel spike and a widebody boom"),
    ]
    colw, x0 = 2.47, 0.5
    for i, (h, b) in enumerate(steps):
        x = x0 + i * colw
        numbered_circle(s, x, 2.0, i + 1)
        if i < len(steps) - 1:
            rect(s, x + 0.64, 2.19, colw - 0.76, 0.14, fill=GRAY_LINE, shape=MSO_SHAPE.RIGHT_ARROW)
        text(s, x, 2.65, colw - 0.2, 1.75, [[(h, 16, True, SPACE)], [(b, 15, False, INK)]], line_spacing=1.0)
    games = [
        ("Game 1 · fps on time (in service 2038)", SPACE,
         [("+$3.9B", "Boeing full-game value"), ("40%", "Boeing narrowbody share, 2045"), ("54%", "Boeing widebody share, 2045")]),
        ("Game 2 · fps three years late (2041)", BOEING_BLUE,
         [("+$1.7B", "Boeing full-game value"), ("32%", "Boeing narrowbody share, 2045"), ("68%", "Boeing widebody share, 2045")]),
    ]
    for j, (hdr, col, stats) in enumerate(games):
        gx, gy, gw = 0.5 + j * 6.25, 4.5, 6.08
        rect(s, gx, gy, gw, 0.48, fill=col)
        text(s, gx + 0.18, gy, gw - 0.3, 0.48, [[(hdr, 16, True, WHITE)]], anchor="ctr")
        rect(s, gx, gy + 0.48, gw, 1.72, fill=TINT)
        for k, (big, lab) in enumerate(stats):
            sx = gx + 0.18 + k * (gw - 0.2) / 3
            text(s, sx, gy + 0.62, (gw - 0.4) / 3, 0.7, [[(big, 32, True, col)]])
            text(s, sx, gy + 1.32, (gw - 0.5) / 3, 0.8, [[(lab, 13, False, INK)]], line_spacing=1.0)


def slide2(prs):
    s = content_slide(prs, "How the games played out",
                      "Both games opened identically and split in 2031: the late fps no longer paid, "
                      "so Boeing re-engined the 787 instead")
    x0, rh_w, cw = 0.5, 1.75, 5.29
    y = 1.98
    rect(s, x0 + rh_w, y, cw - 0.04, 0.5, fill=SPACE)
    text(s, x0 + rh_w + 0.15, y, cw - 0.3, 0.5, [[("Game 1 · fps on time", 16, True, WHITE)]], anchor="ctr")
    rect(s, x0 + rh_w + cw, y, cw, 0.5, fill=BOEING_BLUE)
    text(s, x0 + rh_w + cw + 0.15, y, cw - 0.3, 0.5, [[("Game 2 · fps three years late", 16, True, WHITE)]], anchor="ctr")
    rows = [
        ("Round 1\n2026–30", 0.85, None,
         "Same in both: Airbus launches NGSA in 2028 and asks for UltraFan. Rolls-Royce waits for an airframe, "
         "so NGSA flies CFM's LEAP derivative (in service 2035). Boeing holds; P&W hedges with a new GTF."),
        ("Round 2\n2031–35", 1.25,
         "Boeing launches fps (in service 2038) on P&W's GTF2, and P&W cancels it the same round: fps falls back "
         "to the LEAP derivative. Airbus launches an A350 Re-engine for 2040.",
         "fps fails Boeing's launch test. Boeing launches a 787 Re-engine on GE (in service 2036) and takes the "
         "737 rate step. P&W cancels its GTF2; Airbus signals an A350 Re-engine for 2037."),
        ("Round 3\n2036–45", 1.25,
         "Rolls-Royce cancels its unused UltraFan narrowbody. Boeing declines a 787 Re-engine; the A350 Re-engine "
         "flies GE's GEnx upgrade from 2040.",
         "Airbus shelves the A350 Re-engine; in the same sealed round Rolls-Royce commits UltraFan widebody for "
         "it, an engine with no airframe. Boeing does not launch fps."),
    ]
    y += 0.56
    for lab, h, a, b in rows:
        rect(s, x0, y, rh_w - 0.06, h, fill=TINT)
        text(s, x0 + 0.12, y, rh_w - 0.2, h, [[(l, 15 if k else 16, not k, SPACE)] for k, l in enumerate(lab.split("\n"))], anchor="ctr")
        if a is None:
            rect(s, x0 + rh_w, y, 2 * cw, h, line=GRAY_LINE)
            text(s, x0 + rh_w + 0.15, y + 0.1, 2 * cw - 0.3, h - 0.15, [[(b, 15, False, INK)]], line_spacing=1.0)
        else:
            rect(s, x0 + rh_w, y, cw - 0.04, h, line=GRAY_LINE)
            text(s, x0 + rh_w + 0.15, y + 0.1, cw - 0.32, h - 0.15, [[(a, 15, False, INK)]], line_spacing=1.0)
            rect(s, x0 + rh_w + cw, y, cw, h, line=BOEING_BLUE, line_w=1.5)
            text(s, x0 + rh_w + cw + 0.15, y + 0.1, cw - 0.3, h - 0.15, [[(b, 15, False, INK)]], line_spacing=1.0)
        y += h + 0.06
    rect(s, x0, y + 0.02, 12.33, 0.56, fill=BOEING_BLUE)
    text(s, x0 + 0.2, y + 0.02, 12.0, 0.56,
         [[("Constant in both games: ", 15, True, WHITE),
           ("engine makers waited for airframes, so every new aircraft ended on CFM/GE's existing engines.", 15, False, WHITE)]],
         anchor="ctr")


def line_chart(s, x, y, w, h, years, series, lo, hi, label_idx):
    cd = CategoryChartData()
    cd.categories = [str(v) for v in years]
    for name, vals, _ in series:
        cd.add_series(name, vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    style_chart(ch)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(12)
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = lo, hi, 10
    va.tick_labels.number_format = '0"%"'
    va.tick_labels.number_format_is_linked = False
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GRAY_LINE
    va.format.line.fill.background()
    ch.category_axis.major_tick_mark = XL_TICK_MARK.NONE
    ch.category_axis.format.line.color.rgb = GRAY_LINE
    for ser, (_, vals, (color, dash)) in zip(ch.plots[0].series, series):
        ser.smooth = False
        ser.format.line.color.rgb = color
        ser.format.line.width = Pt(2.75)
        if dash:
            ser.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        ser.marker.style = XL_MARKER_STYLE.CIRCLE
        ser.marker.size = 8
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = color
        ser.marker.format.line.color.rgb = WHITE
        for i in label_idx:
            dl = ser.points[i].data_label
            dl.has_text_frame = True
            dl.text_frame.text = f"{vals[i]:.0f}%"
            dl.position = XL_LABEL_POSITION.ABOVE if vals[i] >= max(v[1][i] for v in series) else XL_LABEL_POSITION.BELOW
            for p in dl.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(13)
                    r.font.bold = True
                    r.font.color.rgb = color
    return ch


def slide3(prs):
    s = content_slide(prs, "Outcome",
                      "The delay trades narrowbody for widebody: Boeing falls to 32% of narrowbodies "
                      "by 2045 but rises to 68% of widebodies")
    years = [2030, 2035, 2040, 2045, 2050]
    on, late = (FLIGHT, True), (BOEING_BLUE, False)
    text(s, 0.5, 1.98, 4.1, 0.4, [[("Boeing share of narrowbody deliveries", 15, True, SPACE)]])
    line_chart(s, 0.4, 2.35, 4.25, 4.35, years,
               [("fps on time", [40.0, 42.0, 40.2, 40.2, 40.2], on), ("fps three years late", [40.0, 42.0, 38.4, 32.3, 25.0], late)],
               20, 50, [3, 4])
    text(s, 4.75, 1.98, 4.1, 0.4, [[("Boeing share of widebody deliveries", 15, True, SPACE)]])
    line_chart(s, 4.65, 2.35, 4.25, 4.35, years,
               [("fps on time", [58.8, 58.8, 58.8, 53.8, 48.8], on), ("fps three years late", [58.8, 58.8, 63.1, 68.4, 73.8], late)],
               40, 80, [3, 4])
    x, y, w, h = 9.15, 1.98, 3.68, 4.72
    rect(s, x, y, w, h, fill=BOEING_BLUE)
    text(s, x + 0.22, y + 0.18, w - 0.44, 0.5, [[("FULL-GAME VALUE, $B PV", 13, True, WHITE)]])
    text(s, x + 0.22, y + 0.55, w - 0.44, 0.35, [[("on time  →  late", 13, False, RGBColor(0xC9, 0xD6, 0xE8))]], align=PP_ALIGN.RIGHT)
    rows = [("Boeing", "+3.9  →  +1.7"), ("Airbus", "+36.5  →  +44.5"), ("CFM/GE", "+18.8  →  +19.0"),
            ("P&W", "−2.8  →  −2.8"), ("Rolls-Royce", "−7.0  →  −3.7")]
    for i, (n, v) in enumerate(rows):
        yy = y + 0.95 + i * 0.5
        text(s, x + 0.22, yy, 1.5, 0.45, [[(n, 16, True, WHITE)]])
        text(s, x + 1.55, yy, w - 1.77, 0.45, [[(v, 16, False, WHITE)]], align=PP_ALIGN.RIGHT)
    text(s, x + 0.22, y + 3.55, w - 0.44, 1.1,
         [[("Boeing saves ~$23B of fps capex to 2045 but loses the narrowbody wave; NGSA runs unopposed.", 14, False, WHITE)]],
         line_spacing=1.0)


def slide4(prs):
    s = content_slide(prs, "Why the delay matters",
                      "fps fails Boeing's launch test beyond about a year of delay: each year late "
                      "costs $2.3–2.9B of value")
    cd = CategoryChartData()
    cd.categories = ["On time\n(EIS 2038)\nGO", "1 year late\n(2039)\nGO", "2 years late\n(2040)\nNO-GO", "3 years late\n(2041)\nNO-GO"]
    cd.add_series("Normal case: fps vs Do Nothing", (9.9, 5.6, 1.7, -0.7))
    cd.add_series("Slip case (+2 yrs): fps vs Do Nothing", (1.8, -1.7, -4.8, -4.7))
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.4), Inches(2.0), Inches(8.4), Inches(4.25), cd).chart
    style_chart(ch, 12)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(13)
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = -6, 12, 3
    va.tick_labels.number_format = '+0;-0;0'
    va.tick_labels.number_format_is_linked = False
    va.major_gridlines.format.line.color.rgb = GRAY_LINE
    va.format.line.fill.background()
    ca = ch.category_axis
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ca.format.line.color.rgb = SPACE
    ca.tick_labels.font.size = Pt(12)
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.overlap = -10
    for ser, col in zip(plot.series, (BOEING_BLUE, FLIGHT)):
        ser.invert_if_negative = False
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = col
        ser.data_labels.show_value = True
        ser.data_labels.number_format = '+0.0;−0.0'
        ser.data_labels.number_format_is_linked = False
        ser.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
        ser.data_labels.font.size = Pt(13)
        ser.data_labels.font.bold = True
    text(s, 0.5, 6.3, 8.3, 0.45,
         [[("Launch rule: ", 13, True, SPACE),
           ("normal case > +$1B vs Do Nothing; slip case ≥ −$2B. Values in $B PV.", 13, False, INK)]])
    takeaway(s, 9.05, 1.98, 3.78, 4.72, "What would revive fps (any one)",
             [("fps capex < $21.8B  (now $30B)", False), ("Margin > 34.7%  (now 25.6%)", False),
              ("Cost of capital < 7.7%  (now 10.5%)", False), ("Partner pays > 48% of capex, or takes < 9% of margin  (now 35% / 25%)", False),
              ("No market assumption alone flips it.", True)], size=15)


def slide5(prs):
    s = content_slide(prs, "Recommendation",
                      "Recommendation: launch fps in 2031 only if the slip is held to a year; "
                      "otherwise re-engine the 787 first")
    cols = [
        ("Gate fps on schedule confidence",
         ["Launch in 2031 only if the credible delay is ≤ 1 year: worth +$5.6–9.9B over Do Nothing",
          "At 2 years the slip case fails (−$4.8B); at 3 years both cases fail (−$0.7B, −$4.7B)",
          "Fund schedule risk reduction first: technology and supplier readiness"]),
        ("If late, pivot to the widebody",
         ["Launch the 787 Re-engine in 2031 with the 737 rate step: +$3.4B over Do Nothing",
          "Moving first deters the A350 Re-engine; widebody share rises to 68% by 2045",
          "Keep one major development at a time"]),
        ("Reopen fps on new terms",
         ["Hit any one gate: capex < $21.8B, margin > 34.7%, or partner terms > 48% of capex / < 9% of margin",
          "Name a committed engine maker before committing the airframe; in both games uncommitted picks fell to CFM/GE",
          "Re-test before 2036: a later fps enters service after 2045, past the replacement-wave peak"]),
    ]
    cw, x0, y0 = 4.03, 0.5, 1.98
    for i, (hdr, bullets) in enumerate(cols):
        x = x0 + i * (cw + 0.12)
        rect(s, x, y0, cw, 3.72, fill=TINT)
        numbered_circle(s, x + 0.18, y0 + 0.17, i + 1)
        text(s, x + 0.82, y0 + 0.1, cw - 0.95, 0.68, [[(hdr, 18, True, SPACE)]], anchor="ctr", line_spacing=0.95)
        paras = [[("•  " + b, 15, False, INK)] for b in bullets]
        text(s, x + 0.2, y0 + 0.9, cw - 0.38, 2.75, paras, line_spacing=1.0)
    rect(s, x0, 5.8, 12.33, 0.9, fill=BOEING_BLUE)
    text(s, x0 + 0.22, 5.8, 11.9, 0.9,
         [[("Do Nothing is not free: ", 15, True, WHITE),
           ("narrowbody share falls from 40% to 20% by 2053 (−$2.4B PV, −$27B undiscounted). The model leaves out aftermarket "
            "and fixed-cost absorption, so validate those before conceding the narrowbody.", 15, False, WHITE)]],
         anchor="ctr", line_spacing=1.0)


def main():
    template, out = sys.argv[1], sys.argv[2]
    prs = Presentation(template)
    strip_slides(prs)
    for f in (slide1, slide2, slide3, slide4, slide5):
        f(prs)
    prs.save(out)
    print("saved", out, len(prs.slides), "slides")


if __name__ == "__main__":
    main()
