# -*- coding: utf-8 -*-
"""Generates Internship_Report_Emilien_Amon_Bewizit.pdf"""
import sys
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

OUT = sys.argv[1] if len(sys.argv) > 1 else "Internship_Report_Emilien_Amon_Bewizit.pdf"

NAVY = colors.HexColor("#1f2d3d")
ACCENT = colors.HexColor("#3f6fa8")
LIGHT = colors.HexColor("#eef2f7")
GREY = colors.HexColor("#5a6472")

styles = getSampleStyleSheet()

styles.add(ParagraphStyle("CoverTitle", fontName="Helvetica-Bold", fontSize=26, leading=30,
                           textColor=NAVY, spaceAfter=6))
styles.add(ParagraphStyle("CoverSubtitle", fontName="Helvetica", fontSize=13, leading=17,
                           textColor=GREY, spaceAfter=26))
styles.add(ParagraphStyle("CoverIntro", fontName="Helvetica", fontSize=10.5, leading=15,
                           textColor=colors.black, spaceBefore=22))
styles.add(ParagraphStyle("PartHeading", fontName="Helvetica-Bold", fontSize=15, leading=18,
                           textColor=ACCENT, spaceBefore=4, spaceAfter=12))
styles.add(ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=12.5, leading=15,
                           textColor=NAVY, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=14.5,
                           textColor=colors.black, spaceAfter=8, alignment=TA_LEFT))
styles.add(ParagraphStyle("TOCEntry", fontName="Helvetica", fontSize=10.5, leading=17,
                           textColor=colors.black))
styles.add(ParagraphStyle("TOCPart", fontName="Helvetica-Bold", fontSize=11, leading=20,
                           textColor=ACCENT, spaceBefore=8))
styles.add(ParagraphStyle("TableCell", fontName="Helvetica", fontSize=9, leading=12.5))
styles.add(ParagraphStyle("TableCellBold", fontName="Helvetica-Bold", fontSize=9, leading=12.5))
styles.add(ParagraphStyle("Caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=12,
                           textColor=GREY, spaceAfter=10))
styles.add(ParagraphStyle("Quote", fontName="Helvetica-Oblique", fontSize=11.5, leading=17,
                           textColor=NAVY, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle("Small", fontName="Helvetica", fontSize=9, leading=13, textColor=GREY))
styles.add(ParagraphStyle("GlossTerm", fontName="Helvetica-Bold", fontSize=9.5, leading=13))
styles.add(ParagraphStyle("GlossDef", fontName="Helvetica", fontSize=9.5, leading=13))


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def cell(text, bold=False):
    return Paragraph(text, styles["TableCellBold" if bold else "TableCell"])


def simple_table(rows, col_widths, header=True):
    data = [[cell(c, bold=header and i == 0) for c in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dae1")),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
        style.append(("TEXTCOLOR", (0, 0), (-1, 0), colors.white))
    t.setStyle(TableStyle(style))
    return t


def figure_placeholder(caption):
    box = Table([[P("[ SCREENSHOT TO INSERT HERE ]", "Small")]], colWidths=[6.2 * inch], rowHeights=[0.9 * inch])
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#b9c2cd")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
    ]))
    return [box, Paragraph(caption, styles["Caption"])]


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d5dae1"))
    canvas.setLineWidth(0.5)
    canvas.line(0.9 * inch, LETTER[1] - 0.65 * inch, LETTER[0] - 0.9 * inch, LETTER[1] - 0.65 * inch)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(GREY)
    canvas.drawString(0.9 * inch, LETTER[1] - 0.55 * inch, "Emilien Amon — Internship Report — Bewizit")
    canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.6 * inch, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, LETTER[1] - 1.4 * inch, LETTER[0], 1.4 * inch, fill=1, stroke=0)
    canvas.restoreState()


# ---------------------------------------------------------------- COVER ----
story = []
story.append(Spacer(1, 0.55 * inch))
story.append(Paragraph("Internship Report", styles["CoverTitle"]))
story.append(Paragraph("Full-Stack Developer Intern — Bewizit", styles["CoverSubtitle"]))

info_rows = [
    ["Student", "Emilien Amon"],
    ["Host company", "Bewizit — web & mobile app development agency"],
    ["Location", "2 rue de Vienne"],
    ["Internship period", "June 7 – July 8, 2026 (one month)"],
    ["Role", "Full-Stack Developer Intern"],
    ["Supervisor", "Alexandre Wizel, CEO"],
    ["Report language", "English"],
]
t = Table([[cell(a, bold=True), cell(b)] for a, b in info_rows], colWidths=[1.7 * inch, 4.5 * inch])
t.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
]))
story.append(t)
story.append(Paragraph(
    "In June and July 2026 I spent one month at Bewizit as a full-stack developer intern, working across "
    "three of the company's products — weteam, periscorp and periscorp-deck — while helping the "
    "team get more out of its AI-assisted development workflow.",
    styles["CoverIntro"]))
story.append(PageBreak())

# ------------------------------------------------------------------ TOC ----
story.append(Paragraph("Table of Contents", styles["PartHeading"]))
story.append(Paragraph("PART 1 — Internship Report", styles["TOCPart"]))
toc1 = [
    "1. Introduction",
    "2. Objectives and Missions",
    "3. Tasks in Context",
    "4. Technical Overview of the Products",
    "5. Tools and Technical Difficulties",
    "6. Knowledge Applied and a Concrete Example",
    "7. Reflection on Situations Encountered",
    "8. Sustainable Development",
    "9. Internship Search Process",
    "10. Contribution to Career Plan",
]
TOC1_PAGES = {}  # filled after first pass
for entry in toc1:
    num = entry.split(".")[0]
    story.append(Paragraph(f"{entry} <font color='#5a6472'>.......................</font> {{{{P{num}}}}}", styles["TOCEntry"]))

story.append(Paragraph("PART 2 — Executive Summary", styles["TOCPart"]))
toc2 = [
    "11. Company Overview and Organization Chart",
    "12. Tasks Performed, Linked to the Timeline",
    "13. Skills Mapped to My Future Profession",
    "14. Search Process & Career Contribution (Summary)",
    "15. Sustainable Development (Summary)",
    "16. Activity Snapshot",
    "17. Conclusion",
]
for entry in toc2:
    num = entry.split(".")[0]
    story.append(Paragraph(f"{entry} <font color='#5a6472'>.......................</font> {{{{P{num}}}}}", styles["TOCEntry"]))
story.append(PageBreak())

# ------------------------------------------------------------- PART 1 ------
story.append(Paragraph("PART 1 — INTERNSHIP REPORT", styles["PartHeading"]))

story.append(Paragraph("1. Introduction", styles["H1"]))
story.append(P(
    "Bewizit is a small web and mobile development agency at 2 rue de Vienne, building products for client "
    "companies. I spent one month there, from June 7 to July 8, 2026, as a full-stack developer intern "
    "reporting directly to Alexandre Wizel, the CEO. My job, in short: help the team code faster and cheaper "
    "with AI tools, and tighten up the structure of a few of their products."))

story.append(Paragraph("2. Objectives and Missions", styles["H1"]))
story.append(P(
    "The brief from day one was to bring more automation into how the team builds software, cut down on "
    "token usage — a real cost when your whole team codes with AI — and clean up the structure of "
    "a few ongoing projects. I split my time across three products:"))
story.append(simple_table(
    [["Project", "My mission"],
     ["weteam", "New SaaS product — I worked on making the development workflow behind it more efficient."],
     ["periscorp", "The company's flagship, more mature app — I focused on its underlying project structure."],
     ["periscorp-deck", "Pitch-deck viewer for periscorp — I organized the GitHub project so the deck could be presented and maintained properly."]],
    [1.3 * inch, 4.9 * inch]))

story.append(Paragraph("3. Tasks in Context", styles["H1"]))
story.append(P(
    "Bewizit builds apps and websites that help other companies run better. Working directly under the CEO "
    "meant my work fed straight into that: a smoother internal workflow and better-structured products both "
    "mean faster delivery, which for a small agency is a real competitive edge. Cutting token usage mattered "
    "too — AI-assisted coding is now a recurring cost for Bewizit, not just a convenience."))

story.append(Paragraph("4. Technical Overview of the Products", styles["H1"]))
story.append(P("The three products differ a lot in age and stack, which meant adapting my approach to each rather than applying one template:"))
story.append(simple_table(
    [["Project", "Stack", "Notes"],
     ["weteam", "TypeScript, React, Next.js, Supabase, Tailwind, Turborepo", "Newest codebase, i18n-ready monorepo — a good place to introduce leaner AI-assisted habits."],
     ["periscorp", "PHP/Symfony + GraphQL API, Next.js, pnpm workspaces, Docker, JWT (RS256)", "Oldest and largest codebase — needed clean-up rather than new features."],
     ["periscorp-deck", "Next.js, shadcn/ui, Markdown-driven slides", "Built to pitch periscorp to investors and clients."]],
    [1.15 * inch, 2.4 * inch, 2.65 * inch]))

story.append(Paragraph("5. Tools and Technical Difficulties", styles["H1"]))
story.append(P("Over the month I picked up, and gradually mastered, four main tools:"))
story.append(simple_table(
    [["Tool", "What it was for", "Level reached"],
     ["GitHub", "Version control and the PR workflow across four repositories", "Mastered very well"],
     ["Claude Code", "AI-assisted coding, day to day", "Mastered quite well"],
     ["Slack", "Talking with the CEO and the team", "Mastered well"],
     ["VS Code", "Daily editor", "Mastered"]],
    [1.1 * inch, 3.6 * inch, 1.5 * inch]))
story.extend(figure_placeholder(
    "Figure 1 — “Projects” dashboard (Vercel-style) showing the three projects I worked on — "
    "periscorp-deck, weteam-app, weteam-web — with their GitHub repositories and recent commits."))
story.extend(figure_placeholder(
    "Figure 2 — My GitHub activity timeline for June 2026: 33 commits across 3 repositories, 2 repositories "
    "created, and 53+ pull requests opened across 4 repositories."))
story.append(P(
    "The main hurdle was simply that I'd barely touched these tools before. Week one went almost entirely "
    "into learning GitHub's collaborative workflow and Claude Code properly, before I could get to real "
    "project work. I got there by mixing hands-on trial and error with reading the docs — testing things "
    "on small scopes before touching real code. It paid off: by week two, both tools felt natural."))

story.append(Paragraph("6. Knowledge Applied and a Concrete Example", styles["H1"]))
story.append(P(
    "I brought core programming and structuring skills from my engineering training, though my GitHub "
    "experience wasn't up to a professional team's pace at first — I had to relearn branches, pull "
    "requests and code review on the job. What I hadn't expected to learn was how a very small company "
    "actually runs day to day, with the CEO handling technical supervision directly since there's no "
    "management layer in between."))
story.append(P(
    "The clearest example of putting a new skill to use: once I had a real handle on GitHub's PR workflow "
    "and Claude Code, I opened a pull request that changed how the team structured its AI coding sessions, "
    "so each one didn't have to re-explain project context from scratch. That small process change directly "
    "supported the CEO's goal of cutting the cost of AI-assisted development."))
story.extend(figure_placeholder("Figure 3 — A pull request I created to improve the team's development efficiency."))

story.append(Paragraph("7. Reflection on Situations Encountered", styles["H1"]))
story.append(P(
    "The recurring challenge wasn't one specific incident — it was learning to work efficiently with "
    "unfamiliar tools in a team too small to run a proper onboarding. I leaned on my supervisor with "
    "questions early on, then deliberately pushed myself to research and test things on my own, which freed "
    "up his time and forced me to actually understand the tools rather than copy instructions. If I did it "
    "again, I'd study each tool properly before day one instead of learning it on the fly."))

story.append(Paragraph("8. Sustainable Development", styles["H1"]))
story.append(P(
    "Bewizit is too small to have a written CSR policy, but it runs on the “Accord Toltèque” "
    "(the Four Agreements) as an informal code of conduct to keep the team's culture healthy. On impact: "
    "both weteam and periscorp exist to help other companies work better, which gives my work a clear, if "
    "indirect, social upside. I didn't find an equivalent environmental angle to the company's activity."))
story.append(P(
    "A full environmental policy would be overkill for a team this size, but a realistic first step would be "
    "to formalize something already close at hand — tracking and cutting token/compute usage, which I "
    "already worked on, as a lightweight environmental metric alongside the existing social code. My overall "
    "grade for the company's CSR: 14/20 — 10/10 on the social side thanks to the Accord Toltèque and "
    "the close-knit team culture, 4/10 on the environmental side since there's no formal policy at all."))

story.append(Paragraph("9. Internship Search Process", styles["H1"]))
story.append(P(
    "I found this internship through my network rather than a formal application process — I reached "
    "out to find someone willing to take me on and teach me something outside my usual field. It worked well "
    "here: I ended up with a supervisor genuinely invested in my growth. The downside is I only seriously "
    "considered one option. Next time, I'd combine networking with a broader set of formal applications, so "
    "I have more to compare and more room to negotiate."))

story.append(Paragraph("10. Contribution to Career Plan", styles["H1"]))
story.append(P(
    "Before this internship, I was set on physics research — a field with little overlap with "
    "full-stack development, which is exactly why I chose this internship: to try something different. It "
    "didn't change that plan. What it did confirm is that the habits that plan depends on — learning "
    "things on my own, mastering tools properly, solving problems methodically — carry over cleanly "
    "into a completely different field, which only makes me more confident in it."))
story.append(PageBreak())

# ------------------------------------------------------------- PART 2 ------
story.append(Paragraph("PART 2 — EXECUTIVE SUMMARY", styles["PartHeading"]))
story.append(P("A condensed version of the report above — organization chart, task timeline and skills mapping — for a quick read."))

story.append(Paragraph("11. Company Overview and Organization Chart", styles["H1"]))
story.append(P(
    "Bewizit is a very flat structure: no management layer between the CEO and the operational team. I "
    "reported directly to Alexandre Wizel throughout the internship."))
org = Table(
    [[cell("Alexandre Wizel<br/>CEO", bold=True)],
     [cell("reports to")],
     [cell("Emilien Amon<br/>Full-Stack Developer Intern — weteam / periscorp / periscorp-deck", bold=True)]],
    colWidths=[4 * inch])
org.setStyle(TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BOX", (0, 0), (0, 0), 0.75, ACCENT),
    ("BOX", (0, 2), (0, 2), 0.75, ACCENT),
    ("BACKGROUND", (0, 0), (0, 0), LIGHT),
    ("BACKGROUND", (0, 2), (0, 2), LIGHT),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(org)
story.append(Spacer(1, 8))

story.append(Paragraph("12. Tasks Performed, Linked to the Timeline", styles["H1"]))
story.append(simple_table(
    [["Period", "Focus", "Main activity"],
     ["Week 1 (Jun 7–13)", "Onboarding", "Learning GitHub, Claude Code, Slack and VS Code from a standing start."],
     ["Week 2 (Jun 14–20)", "periscorp", "Working on the project structure of the company's main app."],
     ["Week 3 (Jun 21–27)", "weteam", "Optimizing the dev workflow for the new SaaS product."],
     ["Weeks 4–5 (Jun 28–Jul 8)", "periscorp-deck", "Structuring the GitHub project and content for the pitch-deck viewer."]],
    [1.3 * inch, 1.1 * inch, 3.8 * inch]))

story.append(Paragraph("13. Skills Mapped to My Future Profession", styles["H1"]))
story.append(simple_table(
    [["Skill", "Used how", "Relevance to research"],
     ["Autonomous problem-solving", "Learning new tools with little onboarding", "Core to independent research"],
     ["Git/GitHub", "53+ pull requests across 4 repositories", "Reproducibility and traceability"],
     ["AI-assisted iteration (Claude Code)", "Speeding up and optimizing dev workflows", "Transfers to computational research"],
     ["Communicating with non-specialists", "Explaining technical decisions to the CEO", "Communicating research to non-experts"]],
    [1.7 * inch, 2.2 * inch, 2.3 * inch]))

story.append(Paragraph("14. Search Process & Career Contribution (Summary)", styles["H1"]))
story.append(P(
    "I found this internship through my network, not a formal search — it worked well, though next time "
    "I'd widen the funnel. It didn't change my career plan (physics research), but confirmed that autonomous "
    "learning and real tool mastery carry over to it directly."))

story.append(Paragraph("15. Sustainable Development (Summary)", styles["H1"]))
story.append(simple_table(
    [["Overall CSR grade", "14/20"],
     ["Social", "10/10"],
     ["Environmental", "4/10"]],
    [2 * inch, 4.2 * inch], header=False))
story.append(Spacer(1, 4))
story.append(P(
    "Bewizit runs on the Accord Toltèque as a social code of conduct but has no formal environmental "
    "policy — proportionate to its size, but with room to improve, e.g. tracking token/compute usage as "
    "a lightweight environmental metric."))

story.append(Paragraph("16. Activity Snapshot", styles["H1"]))
story.append(P("A quantitative snapshot of the month, drawn from my GitHub activity across the four repositories I contributed to:"))
story.append(simple_table(
    [["Metric", "Count", "Notes"],
     ["Commits", "33", "Across 3 repositories (weteam, periscorp, periscorp-deck)"],
     ["Repositories created", "2", "New repositories I set up and structured from scratch"],
     ["Pull requests opened", "53+", "Across 4 repositories, reflecting the PR-driven workflow I adopted"]],
    [1.4 * inch, 0.8 * inch, 4.0 * inch]))

story.append(Paragraph("17. Conclusion", styles["H1"]))
story.append(Paragraph(
    "“What struck me most is how polyvalent you need to be to run your own company — and how much "
    "it matters that people like Alexandre take the time, even at a tiny scale, to bring in an intern and "
    "help shape someone else's future.”",
    styles["Quote"]))
story.extend(figure_placeholder(
    "Paired illustration — my work on the periscorp pitch deck: a small, concrete trace of that "
    "polyvalence in practice."))
story.append(Paragraph("Acknowledgements", styles["H1"]))
story.append(P(
    "Thanks to Alexandre Wizel for bringing me on, trusting me with real production work across three "
    "products, and supervising me personally throughout the month."))
story.append(PageBreak())

# --------------------------------------------------------------- GLOSSARY --
story.append(Paragraph("APPENDIX — GLOSSARY", styles["PartHeading"]))
story.append(P("Quick definitions of the technical terms used above, for a reader unfamiliar with software development."))
glossary = [
    ("SaaS", "Software delivered online rather than installed locally (e.g. weteam)."),
    ("Monorepo", "One code repository holding several related apps/packages, kept in sync (weteam, periscorp)."),
    ("GraphQL", "A query language for APIs — lets a frontend ask a backend for exactly the data it needs."),
    ("API", "The interface through which two pieces of software exchange data."),
    ("JWT (RS256)", "A signed digital token used to prove a user's identity between frontend and API."),
    ("Repository", "A project's storage space on GitHub, holding its code and full history."),
    ("Pull request", "A proposed change to a repository, reviewed before being merged."),
    ("Commit", "A single recorded change to the code, with a description of what changed and why."),
    ("Token (AI)", "A unit of text an AI model processes — what drives the cost of AI-assisted coding."),
    ("Claude Code", "Anthropic's command-line AI coding assistant, used at Bewizit to write and structure code."),
    ("CSR", "Corporate Social Responsibility — a company's social and environmental policies."),
    ("Accord Toltèque", "“The Four Agreements” — personal-conduct principles Bewizit uses informally."),
]
gloss_data = [[Paragraph(t, styles["GlossTerm"]), Paragraph(d, styles["GlossDef"])] for t, d in glossary]
gt = Table(gloss_data, colWidths=[1.4 * inch, 4.9 * inch])
gt.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#e3e7ec")),
]))
story.append(gt)
story.append(PageBreak())

# ------------------------------------------------------------- DECLARATION -
story.append(Paragraph("Declaration", styles["PartHeading"]))
story.append(P(
    "I declare that this report reflects my own personal experience and observations during my internship at "
    "Bewizit, and that I wrote it myself for the purpose of this internship evaluation."))
story.append(Spacer(1, 30))
story.append(P("Emilien Amon"))
story.append(P("July 8, 2026"))

# ---------------------------------------------------------------- BUILD ----
doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                         leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                         topMargin=0.9 * inch, bottomMargin=0.8 * inch,
                         title="Internship Report - Emilien Amon - Bewizit")

# First pass: build with placeholder page tokens still in text, to discover real page numbers.
import copy
first_story = copy.deepcopy(story)
doc.build(first_story, onFirstPage=cover_page, onLaterPages=header_footer)

from pypdf import PdfReader
reader = PdfReader(OUT)
page_of = {}
# skip page index 0 (cover) and 1 (TOC itself) when locating headings
for i, page in enumerate(reader.pages):
    if i < 2:
        continue
    text = page.extract_text() or ""
    for entry in toc1 + toc2:
        num = entry.split(".")[0]
        if entry in text:
            page_of.setdefault(num, i + 1)

# Second pass: substitute real numbers into the TOC placeholders and rebuild.
final_story = []
for flow in story:
    if isinstance(flow, Paragraph) and "{{P" in getattr(flow, "text", ""):
        txt = flow.text
        for num, pg in page_of.items():
            txt = txt.replace(f"{{{{P{num}}}}}", str(pg))
        final_story.append(Paragraph(txt, styles["TOCEntry"]))
    else:
        final_story.append(flow)

doc2 = SimpleDocTemplate(OUT, pagesize=LETTER,
                          leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.8 * inch,
                          title="Internship Report - Emilien Amon - Bewizit")
doc2.build(final_story, onFirstPage=cover_page, onLaterPages=header_footer)
print("done ->", OUT)
