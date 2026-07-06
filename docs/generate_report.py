# -*- coding: utf-8 -*-
"""Generates Internship_Report_Emilien_Amon_Bewizit.pdf"""
import os
import sys
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)

OUT = sys.argv[1] if len(sys.argv) > 1 else "Internship_Report_Emilien_Amon_Bewizit.pdf"
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "esme_logo.png")

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
styles.add(ParagraphStyle("TableHeaderCell", fontName="Helvetica-Bold", fontSize=9, leading=12.5,
                           textColor=colors.white))
styles.add(ParagraphStyle("Caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=12,
                           textColor=GREY, spaceAfter=10))
styles.add(ParagraphStyle("Quote", fontName="Helvetica-Oblique", fontSize=11.5, leading=17,
                           textColor=NAVY, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle("Small", fontName="Helvetica", fontSize=9, leading=13, textColor=GREY))
styles.add(ParagraphStyle("GlossTerm", fontName="Helvetica-Bold", fontSize=9.5, leading=13))
styles.add(ParagraphStyle("GlossDef", fontName="Helvetica", fontSize=9.5, leading=13))


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def cell(text, bold=False, header=False):
    style_name = "TableHeaderCell" if header else ("TableCellBold" if bold else "TableCell")
    return Paragraph(text, styles[style_name])


def simple_table(rows, col_widths, header=True):
    data = [[cell(c, header=header and i == 0) for c in row] for i, row in enumerate(rows)]
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
    t.setStyle(TableStyle(style))
    return t


def figure_image(filename, caption, max_width=6.2 * inch, max_height=4.0 * inch):
    path = os.path.join(ASSETS_DIR, filename)
    iw, ih = ImageReader(path).getSize()
    scale = min(max_width / iw, max_height / ih)
    img = Image(path, width=iw * scale, height=ih * scale)
    img.hAlign = "CENTER"
    frame = Table([[img]], colWidths=[6.2 * inch])
    frame.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#b9c2cd")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return [frame, Paragraph(caption, styles["Caption"])]


def page_background(canvas):
    """Paint an explicit opaque white page background so text never relies on an
    implicit page color — some PDF viewers apply a dark background in night mode
    otherwise, which can leave dark text unreadable."""
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)
    canvas.restoreState()


def draw_logo(canvas, top_y):
    """Draw the ESME logo top-right, its top edge at top_y (from page bottom)."""
    if not os.path.exists(LOGO_PATH):
        return
    size = 0.42 * inch
    x = LETTER[0] - 0.9 * inch - size
    y = top_y - size
    canvas.saveState()
    canvas.drawImage(LOGO_PATH, x, y, width=size, height=size,
                      preserveAspectRatio=True, mask="auto")
    canvas.restoreState()


def header_footer(canvas, doc):
    page_background(canvas)
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d5dae1"))
    canvas.setLineWidth(0.5)
    canvas.line(0.9 * inch, LETTER[1] - 0.65 * inch, LETTER[0] - 0.9 * inch, LETTER[1] - 0.65 * inch)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(GREY)
    canvas.drawString(0.9 * inch, LETTER[1] - 0.55 * inch, "Emilien Amon — Internship Report — Bewizit")
    canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.6 * inch, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()
    draw_logo(canvas, LETTER[1] - 0.18 * inch)


def cover_page(canvas, doc):
    page_background(canvas)
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, LETTER[1] - 1.4 * inch, LETTER[0], 1.4 * inch, fill=1, stroke=0)
    canvas.restoreState()
    draw_logo(canvas, LETTER[1] - 0.35 * inch)


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
story.append(Spacer(1, 0.35 * inch))

# ------------------------------------------------------------------ TOC ----
# Kept on the same page as the cover — both were mostly blank space on their own.
story.append(Paragraph("Table of Contents", styles["PartHeading"]))
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
    "11. Conclusion",
]
for entry in toc1:
    num = entry.split(".")[0]
    story.append(Paragraph(f"{entry} <font color='#5a6472'>.......................</font> {{{{P{num}}}}}", styles["TOCEntry"]))
story.append(PageBreak())

# ---------------------------------------------------------------- BODY -----
story.append(Paragraph("1. Introduction", styles["H1"]))
story.append(P(
    "Bewizit is a small web and mobile app development agency at 2 rue de Vienne, building digital products "
    "for client companies so they can run more efficiently. I spent one month there, from June 7 to "
    "July 8, 2026, as a full-stack developer intern, reporting directly to Alexandre Wizel, the company's "
    "CEO — there is no management layer in between. My mandate, in plain terms, was to help the team "
    "build software faster and cheaper with AI-assisted tools, and to tighten up the technical structure of "
    "a few of the company's ongoing products. If I had to sum up the month in a couple of sentences: I "
    "built apps and websites, coded with AI, and spent a lot of time figuring out how to make that "
    "combination more productive."))

story.append(Paragraph("2. Objectives and Missions", styles["H1"]))
story.append(P(
    "The internship agreement set three concrete objectives: help automate parts of the development "
    "process through new AI-assisted workflows, reduce the team's token usage — a direct, recurring "
    "cost for a company that codes with AI every day — and contribute to the technical structuring of "
    "several ongoing projects. To meet them, I worked across three products, each with its own focus:"))
story.append(simple_table(
    [["Project", "My mission"],
     ["weteam", "New SaaS product — optimize the workflow/system behind it so the team could build faster."],
     ["periscorp", "The company's main, more mature app — work on its underlying project structure."],
     ["periscorp-deck", "Pitch-deck viewer to commercialize periscorp — build out and organize the GitHub project so a presentation-ready deck could be maintained."]],
    [1.3 * inch, 4.9 * inch]))

story.append(Paragraph("3. Tasks in Context", styles["H1"]))
story.append(P(
    "Bewizit's business is building web and mobile applications that help other companies become more "
    "productive — that's the whole point of products like weteam and periscorp. Working directly under "
    "the CEO meant my work fed straight into that mission: better internal tooling and better-structured "
    "client-facing products both affect how fast the company can deliver, which for a small agency is a "
    "direct competitive factor. My focus on reducing token usage tied into that even more concretely, "
    "since AI-assisted coding is now a real, recurring line in Bewizit's costs, not just a nice-to-have."))

story.append(Paragraph("4. Technical Overview of the Products", styles["H1"]))
story.append(P(
    "Understanding each product's technical shape was step one before I could do any structuring work. "
    "The three products differ a lot in maturity and stack, so I had to adapt my approach to each rather "
    "than apply one template:"))
story.append(simple_table(
    [["Project", "Stack", "Context & my focus"],
     ["weteam", "TypeScript, React, Next.js, Supabase, Tailwind, Turborepo",
      "A SaaS platform for team development — surveys, diagnostics, qualitative interviews — built as "
      "an i18n-ready monorepo. Being the newest codebase, it was the natural place to try out leaner, "
      "less token-hungry AI-assisted habits."],
     ["periscorp", "PHP (Symfony API with GraphQL), Next.js, pnpm workspaces, Docker, JWT (RS256)",
      "The company's main application, combining a PHP/GraphQL API with a Next.js frontend. Being the "
      "oldest and biggest codebase, it needed structural clean-up more than new features."],
     ["periscorp-deck", "Next.js, shadcn/ui, Markdown-driven slides",
      "A pitch-deck viewer used to present periscorp to investors and clients — my focus was organizing "
      "its GitHub repository and content so it could be maintained and presented professionally."]],
    [1.05 * inch, 2.15 * inch, 3.0 * inch]))

story.append(Paragraph("5. Tools and Technical Difficulties", styles["H1"]))
story.append(P("Over the month I used, and gradually mastered, four main tools:"))
story.append(simple_table(
    [["Tool", "What it was for", "Level reached"],
     ["GitHub", "Version control and the pull-request workflow across four repositories", "Mastered very well"],
     ["Claude Code", "AI-assisted coding for day-to-day development and workflow optimization", "Mastered quite well"],
     ["Slack", "Communicating with the CEO and collaborators", "Mastered well"],
     ["VS Code", "Day-to-day code editor", "Mastered"]],
    [1.1 * inch, 3.6 * inch, 1.5 * inch]))
story.extend(figure_image("fig1_projects_dashboard.png",
    "Figure 1 — “Projects” dashboard (Vercel-style) showing the three projects I worked on — "
    "periscorp-deck, weteam-app, weteam-web — with their GitHub repositories and recent commits."))
story.extend(figure_image("fig2_github_activity_june2026.png",
    "Figure 2 — My GitHub activity timeline for June 2026: 33 commits across 3 repositories, 2 repositories "
    "created, and 53+ pull requests opened across 4 repositories."))
story.append(P(
    "The main technical difficulty was simply that I started with almost no hands-on experience with any "
    "of these tools. The first week went almost entirely into learning GitHub's collaborative workflow and "
    "Claude Code properly, rather than writing project code. I got through it by pairing hands-on "
    "experimentation with actual documentation — testing workflows on small, low-stakes scopes before "
    "applying them to real projects. That investment paid off: from the second week onward, both tools "
    "felt like second nature, and I could focus on the missions themselves rather than the tools."))

story.append(Paragraph("6. Knowledge Applied and a Concrete Example", styles["H1"]))
story.append(P(
    "From my engineering training I applied core programming and software-structuring skills, though my "
    "prior GitHub experience wasn't quite ready for the pace of a professional team — I had to relearn "
    "collaborative git workflows (branches, pull requests, code review) on the job, faster than I expected. "
    "Beyond the technical side, the internship taught me something I hadn't planned for: how a very small "
    "company is actually organized and run day to day, including how a CEO personally supervises technical "
    "execution when there's no intermediate management layer at all."))
story.append(P(
    "The clearest example of applying a newly learned skill to a real problem: once I had a solid command "
    "of GitHub's pull-request workflow and of Claude Code, I opened a pull request that restructured part "
    "of the team's AI-assisted development process specifically to cut wasted token usage. Instead of "
    "letting every coding session re-explain the project's context from scratch, I documented and applied "
    "a more disciplined branching and PR convention so AI-assisted sessions could reuse existing structure "
    "and context instead of starting cold. That change fed directly into the CEO's stated goal of lowering "
    "the cost of AI-assisted development, and it shows in the numbers: across the month I made 33 commits "
    "and opened more than 53 pull requests across four repositories, two of which I set up from scratch."))
story.extend(figure_image("fig3_pull_request_caveman_skills.png",
    "Figure 3 — A pull request I created to improve the team's development efficiency."))

story.append(Paragraph("7. Reflection on Situations Encountered", styles["H1"]))
story.append(P(
    "The main difficulty I ran into wasn't a single incident so much as a standing challenge: learning to "
    "work efficiently with tools I'd never used professionally, inside a team too small to run a real "
    "onboarding program. In week one, I compensated by asking my supervisor frequent, sometimes basic, "
    "questions. As I built up familiarity, I deliberately shifted toward researching and testing things on "
    "my own before asking for help — which freed up his time and forced me to build a deeper, more "
    "transferable understanding of the tools rather than just following instructions. Looking back, I'd try "
    "to compress that first learning curve further by studying each tool in a structured way before day "
    "one, instead of learning everything reactively on the job."))

story.append(Paragraph("8. Sustainable Development", styles["H1"]))
story.append(P(
    "Being a very small structure, Bewizit doesn't have a formal, written CSR policy. It does apply the "
    "“Accord Toltèque” — the Four Agreements — as an informal code of conduct to keep a healthy "
    "social environment inside its small team. On impact, the products I worked on, weteam and periscorp, "
    "both carry a positive social dimension by design: their entire purpose is to help other companies "
    "function better, whether that's supporting organizational development or supporting another "
    "business's operations and fundraising. I didn't identify a comparable environmental dimension to the "
    "company's activity."))
story.append(P(
    "Given the company's size, a full environmental policy would be disproportionate, but a realistic "
    "first step would be to formalize a practice that's already implicit in remote, AI-assisted work: "
    "tracking and minimizing token and compute usage — something I already worked on — as a "
    "lightweight environmental metric alongside the existing social code of conduct. Overall, I'd rate the "
    "company's CSR performance at 14/20: strong on the social dimension (10/10, thanks to the Accord "
    "Toltèque and the team's small, direct working culture) but weak on the environmental one (4/10, "
    "reflecting the absence of any formal environmental policy)."))

story.append(Paragraph("9. Internship Search Process", styles["H1"]))
story.append(P(
    "I found this internship through personal networking rather than a formal application process, "
    "reaching out within my network to find someone willing to bring me on and help me build skills "
    "outside my usual academic field. That channel worked well in this specific case: it matched me with "
    "a company and a supervisor genuinely invested in my development. Its main limitation is that I only "
    "seriously considered one opportunity instead of comparing several. For a future search, I'd broaden "
    "the funnel by combining networking with a wider set of formal applications, giving myself more room "
    "to compare roles and negotiate scope."))

story.append(Paragraph("10. Contribution to Career Plan", styles["H1"]))
story.append(P(
    "Before this internship, my career plan was oriented toward research in physics — a field with "
    "limited direct overlap with full-stack web development. I deliberately chose this internship to "
    "explore a different professional environment. It didn't change that underlying plan: I still intend "
    "to pursue physics research. What it did confirm is that the working habits at the core of that plan "
    "— autonomous learning, rigorous tool mastery, and structured problem-solving — transfer "
    "directly to a completely different domain, which reinforces rather than diverts my confidence in "
    "that direction."))

story.append(Paragraph("11. Conclusion", styles["H1"]))
story.append(Paragraph(
    "“What impressed me most is that you have to be very polyvalent to run your own company, and "
    "that it matters — even at a very small scale — to take on interns and help shape the people who'll "
    "shape the workforce after you.”",
    styles["Quote"]))
story.extend(figure_image("fig4_periscorp_deck_landing.png",
    "Paired illustration — my work on the periscorp pitch deck: a small, concrete trace of that "
    "polyvalence in practice."))
story.append(Paragraph("Acknowledgements", styles["H1"]))
story.append(P(
    "Thanks to Alexandre Wizel for taking the time, at such a small company scale, to bring me on, trust "
    "me with real production work across three products, and personally supervise my progress throughout "
    "the month."))
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
# skip page index 0 (cover + TOC combined) when locating headings
for i, page in enumerate(reader.pages):
    if i < 1:
        continue
    text = page.extract_text() or ""
    for entry in toc1:
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
