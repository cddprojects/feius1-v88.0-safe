#!/usr/bin/env python3
"""Render the U.S. Job Compass reader site. General information only."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "site"
THEME = "#243552"
REVIEWED = "2 November 2026"

LOGO = (
    '<svg viewBox="0 0 100 100" aria-hidden="true">'
    '<circle cx="50" cy="50" r="42" fill="none" stroke="currentColor" stroke-width="8"/>'
    '<g transform="rotate(38 50 50)">'
    '<path d="M50 18 64 50H36z" fill="currentColor"/>'
    '<path d="M50 82 64 50H36z" fill="currentColor" opacity=".38"/>'
    "</g>"
    '<circle cx="50" cy="50" r="5" fill="#faf5ea"/>'
    "</svg>"
)

NAV = [
    ("index.html", "Home"),
    ("reading.html", "Guides"),
    ("work-types.html", "Work types"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]


def brand():
    return f'<a class="brand" href="index.html">{LOGO}Job<em>Compass</em></a>'


def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap nav">
{brand()}
<button class="menu-btn" aria-expanded="false" aria-controls="nav-list" aria-label="Open menu"><span class="bars" aria-hidden="true"></span></button>
<ul id="nav-list">{"".join(items)}</ul>
</div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div>{brand()}
<p style="margin-top:1rem;max-width:36ch">General information on remote, online, and flexible work in the United States.</p></div>
<div><h4>Guides</h4><ul>
<li><a href="reading.html">All guides</a></li>
<li><a href="work-types.html">Work types</a></li>
<li><a href="glossary.html">Glossary</a></li>
<li><a href="faq.html">FAQ</a></li>
</ul></div>
<div><h4>Publisher</h4><ul>
<li><a href="about.html">About</a></li>
<li><a href="contact.html">Contact</a></li>
<li><a href="privacy.html">Privacy</a></li>
<li><a href="disclaimer.html">Disclaimer</a></li>
</ul></div>
</div>
<div class="legal"><p>Job Compass publishes general information for readers. It does not list jobs, take applications, or give legal, tax, or employment advice. Official sources set those rules.</p>
<p>&copy; 2026 Job Compass &middot; United States</p></div>
<p class="wordmark" aria-hidden="true">Job Compass</p>
</div></footer>
<script src="js/main.js"></script>'''


def page(filename, title, description, body, current):
    html = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="{THEME}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    (ROOT / filename).write_text(html, encoding="utf-8")


def article(filename, eyebrow, h1, description, lede, inner, current="reading.html"):
    body = f'''<div class="page-head"><div class="wrap"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1></div></div>
<section><div class="wrap article">
<p class="byline">Job Compass &middot; General information &middot; Last reviewed {REVIEWED}</p>
<p class="lede">{lede}</p>
{inner}
<p style="margin-top:2.5rem"><a href="reading.html">&larr; All guides</a></p>
</div></section>'''
    page(filename, f"{h1} | Job Compass", description, body, current)


HERO_ART = '''<svg class="art" viewBox="-14 -34 524 600" role="img" aria-label="Illustration of a laptop showing a checklist for employer, work location, pay, and hours">
<defs><clipPath id="arch"><path d="M0 516V240a240 240 0 0 1 480 0v276a44 44 0 0 1-44 44H44a44 44 0 0 1-44-44z"/></clipPath>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d3e6ec"/><stop offset="1" stop-color="#f7dccb"/></linearGradient></defs>
<g clip-path="url(#arch)"><rect width="480" height="560" fill="url(#sky)"/>
<circle cx="380" cy="110" r="64" fill="#f7d77b" opacity=".85"/>
<circle cx="90" cy="96" r="26" fill="#fff" opacity=".55"/>
<rect x="0" y="392" width="480" height="168" fill="#23402f"/>
<rect x="0" y="392" width="480" height="10" fill="#183024"/>
<rect x="94" y="164" width="292" height="222" rx="20" fill="#1f2a24"/>
<rect x="106" y="176" width="268" height="198" rx="10" fill="#faf5ea"/>
<text x="124" y="206" font-family="Figtree,sans-serif" font-size="15" font-weight="700" fill="#23402f">What a posting states</text>
<rect x="124" y="220" width="64" height="22" rx="11" fill="#d3e6ec"/><text x="156" y="235" text-anchor="middle" font-family="Figtree,sans-serif" font-size="11.5" font-weight="700" fill="#1f2a24">Remote</text>
<rect x="196" y="220" width="78" height="22" rx="11" fill="#f7d77b"/><text x="235" y="235" text-anchor="middle" font-family="Figtree,sans-serif" font-size="11.5" font-weight="700" fill="#1f2a24">Part-time</text>
<rect x="282" y="220" width="64" height="22" rx="11" fill="#dfe9d3"/><text x="314" y="235" text-anchor="middle" font-family="Figtree,sans-serif" font-size="11.5" font-weight="700" fill="#1f2a24">Hourly</text>
<circle cx="132" cy="272" r="11" fill="#c4442f"/><path d="M126 272l4.5 4.5 8-9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="154" y="277" font-family="Figtree,sans-serif" font-size="15" font-weight="600" fill="#1f2a24">Employer</text><rect x="276" y="268" width="78" height="8" rx="4" fill="#e8dfcc"/>
<circle cx="132" cy="306" r="11" fill="#c4442f"/><path d="M126 306l4.5 4.5 8-9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="154" y="311" font-family="Figtree,sans-serif" font-size="15" font-weight="600" fill="#1f2a24">Location</text><rect x="276" y="302" width="78" height="8" rx="4" fill="#e8dfcc"/>
<circle cx="132" cy="340" r="11" fill="#c4442f"/><path d="M126 340l4.5 4.5 8-9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="154" y="345" font-family="Figtree,sans-serif" font-size="15" font-weight="600" fill="#1f2a24">Pay and hours</text><rect x="276" y="336" width="78" height="8" rx="4" fill="#e8dfcc"/>
<path d="M50 386H430l-14 18a10 10 0 0 1-8 4H72a10 10 0 0 1-8-4z" fill="#d9dfd2"/>
<rect x="196" y="390" width="88" height="6" rx="3" fill="#b8c2b3"/>
<path d="M0 500Q120 480 240 496T480 488V560H0z" fill="#183024"/></g>
<path d="M-6 560V240a246 246 0 0 1 492 0v320" fill="none" stroke="#c4442f" stroke-width="3" transform="translate(16 -14)" opacity=".85"/></svg>'''


def build():
    page(
        "index.html",
        "Remote, online, and flexible work in the United States | Job Compass",
        "General information for readers on remote, online, and flexible work in the United States, including how the terms differ and what public figures describe.",
        f'''
<section class="hero"><div class="wrap hero-grid">
<div>
<span class="eyebrow">General information for readers</span>
<h1>Remote, online, and flexible work in the <em>United States.</em></h1>
<p class="lede">A plain account of what those words describe, where people look, and what public figures say about pay, hours, and home-based work.</p>
<ul class="hero-points">
<li><b>Three separate ideas.</b> Remote is a place. Online is a way of doing the work. Flexible is a schedule.</li>
<li><b>Public figures.</b> Each survey covers a different group, so one percentage does not describe every worker.</li>
<li><b>A readable posting.</b> Readers can look for the employer, the place, the hours, and the pay.</li>
<li><b>This site.</b> Job Compass explains the terms. It does not list jobs or take applications.</li>
</ul>
<div class="btn-row"><a class="btn btn-primary" href="reading.html">Read the guides</a><a class="btn btn-ghost" href="about.html">About this site</a></div>
</div>
<div class="hero-art">
{HERO_ART}
<div class="modes">
<h2 class="sr">Three work arrangements</h2>
<a class="mode" href="work-types.html#remote"><span class="tag">Where</span><span><b>Remote</b><small>Away from the usual workplace.</small></span></a>
<a class="mode" href="work-types.html#online"><span class="tag">How</span><span><b>Online</b><small>Done or delivered over the internet.</small></span></a>
<a class="mode" href="work-types.html#flexible"><span class="tag">When</span><span><b>Flexible</b><small>Hours chosen around other commitments.</small></span></a>
</div>
</div>
</div></section>

<section><div class="wrap">
<div class="head reveal"><span class="eyebrow">Work arrangements</span><h2>The words on a posting are not interchangeable.</h2>
<p class="lede">A job can be online and still require a set office. It can be flexible and still happen on a shop floor.</p></div>
<div class="minis">
<a class="mini reveal" href="work-types.html#remote"><b>Remote and hybrid</b><span>Work done away from the employer’s usual site, or split between home and that site.</span></a>
<a class="mini reveal" href="work-types.html#online"><b>Online work</b><span>Work completed or handed in over the internet, from home or from a workplace.</span></a>
<a class="mini reveal" href="work-types.html#flexible"><b>Flexible hours</b><span>Some choice over the schedule. The choice may be small, and the shift may still be assigned.</span></a>
<a class="mini reveal" href="article-second-income.html"><b>A second stream</b><span>Another job or occasional paid work beside a main job, study, or caregiving.</span></a>
</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="head reveal"><span class="eyebrow">What the figures describe</span><h2>A few public measures, kept separate.</h2>
<p class="lede">These numbers answer different questions. They are a starting point for reading, not a prediction for any one person.</p></div>
<ol class="shifts">
<li class="reveal"><span class="no">26.8%</span><h3>Paid days at home</h3><p>Share of full paid working days done at home in September 2026, in the Survey of Working Arrangements and Attitudes.</p></li>
<li class="reveal"><span class="no">21.9%</span><h3>Any telework that week</h3><p>Share of people at work in the September 2026 reference week who teleworked at least some hours, from the Bureau of Labor Statistics.</p></li>
<li class="reveal"><span class="no">8.3%</span><h3>Ads that mention it</h3><p>Share of U.S. Indeed postings that mentioned remote or hybrid work on 31 January 2025, down from 10.4% in February 2022.</p></li>
</ol>
<p class="src-note">Sources are named in <a href="article-what-figures-show.html">What the public figures show</a>. Surveys use different questions and different groups of people.</p>
</div></section>

<section class="route"><div class="wrap">
<div class="route-head reveal"><span class="eyebrow">How to use these guides</span><h2>Read the arrangement before reading the promise.</h2>
<p class="lede">The guides walk through the words, the search, the posting, and the pay. They stop at explanation.</p></div>
<ol class="stops">
<li class="stop reveal"><span class="n">1</span><h3>Separate the words</h3><p>Remote, online, and flexible answer different questions. <a href="article-three-words.html">The short guide</a> keeps them apart.</p></li>
<li class="stop reveal"><span class="n">2</span><h3>See where searches start</h3><p>General job boards, LinkedIn, search engines, and employer sites carry most of the looking. <a href="article-where-to-look.html">Where people look</a>.</p></li>
<li class="stop reveal"><span class="n">3</span><h3>Read the posting itself</h3><p>Employer, place, hours, pay, and whether the role is employment or contract work. <a href="article-read-a-posting.html">How to read a posting</a>.</p></li>
<li class="stop reveal"><span class="n">4</span><h3>Check a public source</h3><p>Wages, minimum rates, and classification rules change. The guides link the office that publishes each figure.</p></li>
</ol>
<p class="route-cta"><a class="btn btn-primary" href="reading.html">Browse the guides</a></p>
</div></section>
''',
        "index.html",
    )

    posts = [
        ("market", "The figures", "6 min", "article-what-figures-show.html", "What the public figures show", "Home-based work, telework in a survey week, and the share of ads that mention remote work are three different measures."),
        ("words", "Work types", "5 min", "article-three-words.html", "How remote, online, and flexible work differ", "Each word describes a different part of the arrangement. A posting can use one, two, or all three."),
        ("search", "Looking", "6 min", "article-where-to-look.html", "Where people look for this work", "General boards, LinkedIn, search engines, and company sites. Niche boards matter once the occupation is clear."),
        ("posting", "Reading a posting", "7 min", "article-read-a-posting.html", "How to read a remote or flexible posting", "A readable posting names the employer, the place, the hours, the pay, and the employment status."),
        ("pay", "Pay", "7 min", "article-pay-and-status.html", "Pay, minimum wages, and employee or contractor status", "The federal minimum, higher state rates, and why a contract label does not settle the legal question."),
        ("path", "Second income", "6 min", "article-second-income.html", "Second jobs and side work", "About 5.5% of employed people hold two jobs. Surveys of side work count a wider set of activities."),
        ("roles", "Occupations", "7 min", "article-roles.html", "Occupations readers meet in this search", "Customer service, records, bookkeeping, tutoring, and software show up for different reasons and at different pay."),
    ]
    cards = []
    for cat, label, mins, href, title, summary in posts:
        cards.append(
            f'<article class="post reveal" data-cat="{cat}"><div class="meta"><span class="cat">{label}</span><span>{mins}</span></div>'
            f'<h3><a href="{href}">{title}</a></h3><p>{summary} <a class="read-more" href="{href}">Read more</a></p></article>'
        )
    page(
        "reading.html",
        "Guides | Job Compass",
        "Guides to remote, online, and flexible work in the United States for general reading.",
        f'''<div class="page-head"><div class="wrap"><span class="eyebrow">Guides</span><h1>Guides for readers</h1>
<p class="lede">Explanations of work arrangements, public figures, postings, and pay. Job Compass does not list openings.</p></div></div>
<section><div class="wrap">
<div class="filters" role="group" aria-label="Filter guides">
<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>
<button class="chip" type="button" data-filter="words" aria-pressed="false">Work types</button>
<button class="chip" type="button" data-filter="search" aria-pressed="false">Looking</button>
<button class="chip" type="button" data-filter="market" aria-pressed="false">Figures</button>
<button class="chip" type="button" data-filter="posting" aria-pressed="false">Postings</button>
<button class="chip" type="button" data-filter="pay" aria-pressed="false">Pay</button>
<button class="chip" type="button" data-filter="path" aria-pressed="false">Second income</button>
<button class="chip" type="button" data-filter="roles" aria-pressed="false">Occupations</button>
</div>
<div class="posts">{"".join(cards)}</div>
</div></section>''',
        "reading.html",
    )

    page(
        "work-types.html",
        "Work types | Job Compass",
        "What remote, online, and flexible work mean in the United States.",
        '''<div class="page-head"><div class="wrap"><span class="eyebrow">Work types</span><h1>Three arrangements, kept separate</h1>
<p class="lede">Location, delivery, and hours. A single job can include more than one.</p></div></div>
<section><div class="wrap">
<div class="types">
<div class="type" id="remote"><h3>Remote and hybrid</h3><div><p>Remote work is done away from the employer’s usual workplace. Hybrid means some days at home and some days at a set site. A posting that requires regular office days is hybrid. Fully remote postings are a small share of ads and attract a large share of applications. Education and occupation change the odds: in the September 2026 survey week, 37.8% of people with a bachelor’s degree teleworked at least some hours, compared with 8.3% of high school graduates with no college.</p><p><a href="article-three-words.html">Read the short guide</a></p></div></div>
<div class="type" id="online"><h3>Online work</h3><div><p>Online work is completed or delivered over the internet. The person may be at home, in an office, or in another city the employer names. “Online” by itself does not say whether the hours are chosen by the worker or assigned by the employer, or whether the role is employment or contract work.</p><p><a href="article-three-words.html">How the words differ</a></p></div></div>
<div class="type" id="flexible"><h3>Flexible and part-time</h3><div><p>Flexible usually means some choice over the schedule. In hourly jobs, that choice is often the ability to see shifts ahead of time. A home-based customer-service ad can still assign an eight-hour shift. In early 2025, 62% of employees in the American Job Quality Study lacked a predictable, stable schedule they could control.</p><p><a href="article-second-income.html">Second jobs and side work</a></p></div></div>
</div>
<p class="src-note">Bureau of Labor Statistics, table A-41, September 2026. American Job Quality Study, January to February 2025, Jobs for the Future and Gallup.</p>
</div></section>''',
        "work-types.html",
    )

    article(
        "article-three-words.html",
        "Work types",
        "How remote, online, and flexible work differ",
        "Why remote, online, and flexible describe different parts of a job in the United States.",
        "The three words often sit in the same sentence. They still answer different questions.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>Remote describes where the work is done.</li>
<li>Online describes how the work is delivered.</li>
<li>Flexible describes the hours or the workload.</li>
<li>A job can include one of them, or all three.</li>
</ul></div>
<h2>Where</h2>
<p>Remote work happens away from the employer’s usual site. Hybrid mixes home days and site days. Among full-time wage-and-salary workers in August 2026, the Survey of Working Arrangements and Attitudes put 12.1% fully remote, 27.1% hybrid, and 60.8% fully on site. Gallup’s figures are higher because they cover employees whose jobs could be done remotely, not the whole workforce. In August 2026 that group was 25% fully remote, 54% hybrid, and 21% on site.</p>
<h2>How</h2>
<p>Online work is done or turned in over the internet. A hospital coder, a tutor on a video call, and a person answering calls from a spare room are all doing online work. The coder may have a certificate and a set caseload. The tutor may choose evening hours. The call-center shift may be assigned between set clock times. The word “online” does not choose among those.</p>
<h2>When</h2>
<p>Flexible work offers some say over the schedule. Part-time work is a count of hours, not a promise of choice. The Bureau of Labor Statistics treats fewer than 35 hours as part time. A part-time data-entry shift that happens every Monday is regular. It is not the same thing as a contract whose hours follow a client.</p>
<h2>Why the split matters for a reader</h2>
<p>Someone reducing a commute is asking about place. Someone fitting work around school or caregiving is asking about hours. Someone comparing a paycheck with a contract is asking about status and tax. A posting that uses all three words and then skips the place, the hours, and the status has not answered the question.</p>
<p class="src-note">Survey of Working Arrangements and Attitudes via FRED, August 2026 arrangement shares. Gallup Hybrid Work indicator, August 2026. Bureau of Labor Statistics definition of full time: 35 hours or more.</p>
''',
    )

    article(
        "article-where-to-look.html",
        "Looking",
        "Where people look for this work",
        "Where people in the United States search for remote, online, and flexible work.",
        "Most looking still starts on a general job board, then moves to a company site or a professional network.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>General job boards are the common starting place.</li>
<li>LinkedIn, search engines, and employer sites are used alongside the boards.</li>
<li>Remote ads are a small share of postings and a large share of applications.</li>
<li>A text message from an unnamed recruiter is a different channel, and a risky one.</li>
</ul></div>
<h2>Channels people say they use</h2>
<p>iHire’s 2025 survey of 1,421 U.S. job seekers asked which resources they use. People could choose more than one. General job boards were named by 78.5%, professional networks such as LinkedIn by 54.9%, niche boards by 53.8%, company websites by 45.0%, and search engines by 41.6%. Referrals were 32.7%. Social media was 15.7%. Craigslist was 8.3%.</p>
<p>HireClix asked a different question of 1,000 adults in 2025: where a search starts. Indeed was 56%, LinkedIn 52%, Google 41%, and corporate career sites 40%. The two surveys can both be right. One asks about every channel. The other asks about the first stop.</p>
<h2>Remote ads are the crowded shelf</h2>
<p>Indeed’s count of postings that mention remote or hybrid work was 2.6% in January 2019, 10.4% at the February 2022 peak, and 8.3% on 31 January 2025. LinkedIn told Business Insider that in September 2025 about 8% of paid U.S. postings offered remote work and those postings drew 35% of applications. A reader who searches only the word “remote” is looking at a thin set of ads with a thick set of applicants.</p>
<h2>Occupation changes the shelf</h2>
<p>Insurance, legal, mathematics, and software postings mention remote or hybrid work far more often than retail, driving, or construction. A secondary compilation of Indeed’s tracker put software development near 30.8% on 31 August 2026, and driving near 1.2%. Customer service is common as an entry-level remote title even though many customer-service jobs remain on site.</p>
<p class="src-note">iHire, State of Online Recruiting 2025. HireClix, 2025 Candidate Experience Survey. Indeed Hiring Lab, November 2024 update, and Forbes, 20 March 2025, citing Indeed. Business Insider, 19 October 2025, quoting LinkedIn. The August 2026 occupation shares come from a secondary compilation of the Indeed tracker.</p>
''',
    )

    article(
        "article-what-figures-show.html",
        "The figures",
        "What the public figures show",
        "How to read U.S. figures on remote work, telework, and second jobs without mixing the surveys.",
        "Three careful sources describe late 2026. They do not measure the same thing.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>One series counts paid days at home.</li>
<li>One series counts people who teleworked in a single week.</li>
<li>One series counts ads, not workers.</li>
<li>A preference among office workers is a fourth, smaller group.</li>
</ul></div>
<h2>Paid days at home</h2>
<p>The Survey of Working Arrangements and Attitudes asks about the share of full paid working days done at home. The sample is workers who earned at least $10,000 in a prior year, reweighted toward the Current Population Survey. The share was 7.2% in December 2019, about 62% in May 2020, and 26.8% in September 2026. It has stayed in the mid-20s since 2023.</p>
<p>In August 2026 the same project reported, for full-time wage-and-salary workers, 60.8% fully on site, 27.1% hybrid, and 12.1% fully remote. Home days were more common in information, finance, and professional services than in manufacturing, education, or transportation.</p>
<h2>Anyone who teleworked that week</h2>
<p>The Bureau of Labor Statistics asks people who worked during the survey week whether they teleworked or worked at home for pay. In September 2026, not seasonally adjusted, 21.9% had done so for at least some hours and 10.7% had done so for all of their hours. That is 34.7 million people out of 158.5 million at work. Women were at 23.9% and men at 20.1%. People with their own children under 18 were at 25.9%. People with a disability were at 24.4%.</p>
<p>Age runs against the idea that the youngest workers are the ones at home. Ages 16 to 24 were at 5.7%, because many of those jobs are on site. Ages 35 to 44 were at 26.2%.</p>
<h2>Ads, unemployment, and second jobs</h2>
<p>In September 2026 the seasonally adjusted unemployment rate was 4.2%, with 7.1 million people unemployed. Labor force participation was 61.8%. Part time for economic reasons was 4.5 million people. Multiple jobholders were 9.0 million, or 5.5% of the employed, in the not-seasonally-adjusted count. Most of them had a full-time main job and a part-time second job.</p>
<p class="src-note">FRED series WFHCOVIDMATQUESTION and the SWAA release. Bureau of Labor Statistics, Employment Situation and table A-41, September 2026. Cite Barrero, Bloom, and Davis, NBER Working Paper 28731, when using the home-day series.</p>
''',
    )

    article(
        "article-read-a-posting.html",
        "Reading a posting",
        "How to read a remote or flexible posting",
        "What readers can look for in a U.S. posting for remote, online, or flexible work.",
        "A useful posting names who is hiring, where the work happens, when it happens, and what it pays.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>The employer’s name is part of the posting.</li>
<li>Pay is part of the posting in a growing list of states, and readers look for it everywhere.</li>
<li>Home-based phone work often still has an assigned shift.</li>
<li>A fee to get the job, or a check to cash and partly return, is a known fraud pattern.</li>
</ul></div>
<h2>What seekers say they need</h2>
<p>In the same iHire survey, 60.5% said a hiring timeline would make them more likely to apply, and 57.1% said a salary range would. An unnamed employer was an instant turnoff for 50.9%, and missing pay was an instant turnoff for 60.7%. About half, 51.7%, thought 10 to 15 minutes was the right length for an application. Hearing nothing back was the most common frustration, at 59.0%. Fake or already-filled postings were next, at 39.3% in the findings chart.</p>
<h2>Place and hours, written out</h2>
<p>“Remote” can mean every state, or one state, or a radius around one city. “Flexible” can mean the person picks the hours, or that the employer will assign a shift and the person works it from home. Published customer-service ads in autumn 2026 from named employers such as Concentrix, TTEC, and Firstsource showed rates around $15 to $17 an hour, with assigned shifts, a high-school diploma, and some prior customer-service experience. Those ads expire. They illustrate the arrangement. They are not openings from this site.</p>
<h2>Pay on the posting</h2>
<p>A compilation checked against official pages as of 13 October 2026 found pay-range rules in 14 states and the District of Columbia, including California, Colorado, Illinois, New York, and Washington. Thresholds differ by employer size and by whether the job is done in the state. The list is general information, not legal advice. Readers outside those states still treat a missing range as a reason to pause: that is what the iHire result describes.</p>
<h2>Patterns the Federal Trade Commission describes</h2>
<p>Reported losses to job and employment-agency scams rose from $90 million in 2020 to $501 million in 2024, and reports tripled, according to the FTC’s 10 March 2025 release. A September 2025 FTC note put 2024 job-scam reports above 105,000 and reported losses above $513 million. The patterns in FTC consumer guidance are an unexpected text or chat, a remote title with no duties, any fee to get paid, a check the person is told to deposit and partly send back, and pay for liking or rating things followed by a demand to deposit money.</p>
<p class="src-note">iHire, State of Online Recruiting 2025. LAYIQ compilation of official pay-transparency pages, 13 October 2026. FTC press release, 10 March 2025, and FTC business blog, September 2025. FTC consumer guidance on job scams.</p>
''',
    )

    article(
        "article-pay-and-status.html",
        "Pay",
        "Pay, minimum wages, and employee or contractor status",
        "General information on U.S. minimum wages, average earnings, and employee or contractor status.",
        "An hourly figure means little until the reader knows the state, the hours, and who is responsible for taxes.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>The federal minimum wage is still $7.25 an hour.</li>
<li>Many states require more, and the higher rate is the one that applies.</li>
<li>National average earnings sit far above entry-level remote ads.</li>
<li>Calling work a contract does not, by itself, decide the legal status.</li>
</ul></div>
<h2>The wage floor</h2>
<p>The federal minimum has been $7.25 an hour since 24 July 2009. Employers covered by the Fair Labor Standards Act pay the highest of the federal, state, and local rates. The Department of Labor’s consolidated table dated 1 July 2026 lists 30 states plus the District of Columbia above $7.25. Examples from that table include Washington at $17.13, California at $16.90, New York City and Long Island at $17.00, and upstate New York at $16.00. Texas and Pennsylvania are in the federal column. A note on the same page still describes the District of Columbia as $17.50, while the table row says $18.40, so the District figure should be confirmed with the District before anyone relies on it.</p>
<h2>What people already earn</h2>
<p>In September 2026, preliminary and seasonally adjusted, average hourly earnings for all private employees were $37.81, and average weekly earnings were $1,300.66. Retail trade averaged $26.38 an hour. Leisure and hospitality averaged $23.90. These are averages across the whole private economy. They are not the wage on a particular posting. The May 2025 median for customer service representatives was $21.53 an hour, or $44,770 a year. The lowest 10% of that occupation earned under $15.27. Entry-level remote call-center ads often land near that lower end.</p>
<h2>Employee or contractor</h2>
<p>Some online and flexible offers are written as independent-contractor work. Readers comparing them with a job are comparing overtime, unemployment insurance, and who pays the employer share of Social Security, not only the hourly rate. On 26 February 2026 the Department of Labor proposed to replace its 2024 classification guidance with a modified economic-reality test. On 28 October 2026 that final rule had cleared White House review and, as of this review date, had no publication date. State tests are separate. This paragraph is a status note for readers. It is not advice about any one engagement.</p>
<p class="src-note">U.S. Department of Labor, minimum wage and the consolidated table effective 1 July 2026. Bureau of Labor Statistics, table B-3, September 2026, and the Occupational Outlook Handbook for customer service representatives, May 2025. Federal Register, 27 February 2026. OIRA record RIN 1235-AA46, concluded 28 October 2026.</p>
''',
    )

    article(
        "article-second-income.html",
        "Second income",
        "Second jobs and side work",
        "What U.S. figures say about second jobs and side work, and how the surveys differ.",
        "A second paycheck is common in conversation and less common in the official job count. The gap is the definition.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>The official multiple-job rate was 5.5% in September 2026.</li>
<li>A side-hustle survey the same year found 27% of adults, using a wider definition.</li>
<li>The median in that survey was $200 a month.</li>
<li>Online selling and freelance tasks were named more often than rideshare.</li>
</ul></div>
<h2>The official count</h2>
<p>In September 2026, not seasonally adjusted, 9.0 million people held more than one job. That was 5.5% of employed people. Women were at 6.4% and men at 4.7%. The usual pattern was a full-time main job plus a part-time second job: 5.2 million people. Both jobs part time accounted for 2.25 million. Two full-time jobs were uncommon, at 421,000.</p>
<h2>Side work, defined more loosely</h2>
<p>Bankrate’s YouGov survey of 2–4 June 2025, with 2,616 adults, defined a side hustle as extra money beyond the main source of income. Twenty-seven percent said they had one, down from 36% in 2024. The average was $885 a month and the median was $200. Among people who had one, online sales were 15% and professional services such as writing or design were 14%. Food delivery was 9%. Rideshare was 3%. Forty-three percent said none of the listed types matched what they did. Forty-one percent used at least some of the money for discretionary spending, and 35% used at least some for regular living expenses.</p>
<p>A wider question, any side income in the past year, produces a higher share. Intuit QuickBooks surveyed 3,000 adults in December 2025 and 47% said they had earned something. That result and the Bankrate result describe different questions. Neither replaces the Bureau of Labor Statistics count of people who hold two jobs.</p>
<h2>What “small” looks like</h2>
<p>Most of this activity does not replace a paycheck. In the Bankrate survey, 14% of side hustlers earned more than $1,000 a month, and 16% wanted the side work to become their main income. A posting that describes a few hours of phone work as a full salary is describing something other than this pattern.</p>
<p class="src-note">Bureau of Labor Statistics, tables A-16 and A-39, September 2026. Bankrate press release, 9 July 2025. Intuit QuickBooks, State of Side Hustles, December 2025 survey.</p>
''',
    )

    article(
        "article-roles.html",
        "Occupations",
        "Occupations readers meet in this search",
        "Occupations that appear in U.S. searches for remote, online, and flexible work, with public median pay.",
        "The search mixes a few large occupations. Their pay, training, and schedules are not the same.",
        '''
<div class="takeaways"><h2>The short version</h2><ul>
<li>Customer service, sales support, and admin dominate entry-level remote postings.</li>
<li>Bookkeeping and medical records pay more and usually ask for some training.</li>
<li>Tutoring and some data-entry shifts are the small-hours end of the market.</li>
<li>Medians below are for the occupation in every setting, not a promise on a single ad.</li>
</ul></div>
<h2>High-school entry, often an assigned shift</h2>
<p>FlexJobs counted its own listings from 1 January to 1 May 2026. Customer service, administrative work, and sales led entry-level remote hiring, and each grew more than 30% in that slice of the database. The titles posted most often were sales development representative, customer service representative, and business development representative. Employers with the most entry-level remote postings in that database included Mass General Brigham, Thermo Fisher Scientific, HCA, the State of North Carolina, T-Mobile, IQVIA, Stride, Raymond James, Centene, and Toast.</p>
<p>The May 2025 median for customer service representatives was $21.53 an hour. About 2.7 million people held the job. Employment is projected to decline 5% from 2025 to 2035, with openings still coming from people who leave. Home-based ads at the entry level have been clustering near $15 to $17 an hour, with a set shift and a quiet workspace. That is the bottom of the occupation’s range.</p>
<h2>A certificate or a degree</h2>
<p>Bookkeeping, accounting, and auditing clerks had a May 2025 median of $24.36 an hour, or $50,670 a year. Usual entry is some college and moderate training. Medical records specialists had a median of $24.59 an hour, or $51,140. Usual entry is a postsecondary certificate, and employment is projected to grow 8% from 2025 to 2035. Software developers had a median of $135,980. Usual entry is a bachelor’s degree, and a large share of those postings still mention remote or hybrid work. Interpreters and translators had a median of $28.93 an hour. Bilingual phone support is a different, often lower-paid, use of a second language.</p>
<h2>Hours a person can keep small</h2>
<p>Tutors numbered about 175,070 in May 2025, with a median wage of $20.84 an hour. Online tutoring ads around $18 to $22.50 an hour, for evening hours and a cap near 25 hours a week, sit close to that median. Data-entry ads around $16 an hour, including part-time shifts on a single weekday, are a second-income shape. Contract virtual-assistant work follows a client’s calendar, and the worker handles their own taxes. Delivery and rideshare are local and flexible. In the Bankrate survey they were a small share of side work.</p>
<p class="src-note">FlexJobs, entry-level remote jobs, updated 28 May 2026. Bureau of Labor Statistics, Occupational Outlook Handbook, May 2025 medians, and OEWS table 1 for tutors. Live ads mentioned here were reviewed in September and October 2026 and are examples of arrangements, not openings from Job Compass.</p>
''',
    )

    page(
        "glossary.html",
        "Glossary | Job Compass",
        "Plain definitions of terms used in U.S. postings for remote, online, and flexible work.",
        '''<div class="page-head"><div class="wrap"><span class="eyebrow">Glossary</span><h1>Terms readers meet on postings</h1>
<p class="lede">Short definitions. Legal duties depend on the statute, the state, and the facts of the job.</p></div></div>
<section><div class="wrap">
<label class="notice" for="glossary-search">Search terms</label>
<input id="glossary-search" class="search" type="search" placeholder="Try remote, W-2, or minimum wage">
<div id="glossary-empty" class="notice" hidden>No matching term.</div>
<div class="term"><dt>Remote</dt><dd>Work done away from the employer’s usual workplace. The posting may still limit the states or time zones.</dd></div>
<div class="term"><dt>Hybrid</dt><dd>Some days remote and some days at a set site. Regular office days mean the job is not fully remote.</dd></div>
<div class="term"><dt>Online work</dt><dd>Work done or delivered over the internet. The word does not settle the place, the hours, or the employment status.</dd></div>
<div class="term"><dt>Flexible schedule</dt><dd>Some choice over hours. The choice can be small. An assigned shift worked from home is still an assigned shift.</dd></div>
<div class="term"><dt>Part-time</dt><dd>In Bureau of Labor Statistics household data, fewer than 35 hours a week. It is a count of hours, not a type of pay.</dd></div>
<div class="term"><dt>Multiple jobholder</dt><dd>A person counted by the Bureau of Labor Statistics as holding more than one job. In September 2026 that was 5.5% of employed people.</dd></div>
<div class="term"><dt>Side hustle</dt><dd>A survey term for extra money beside a main source of income. It is wider than the official count of second jobs. Definitions differ by survey.</dd></div>
<div class="term"><dt>W-2 employee</dt><dd>A worker whose employer withholds income tax and pays the employer share of Social Security and Medicare. The label on a posting is not the legal test.</dd></div>
<div class="term"><dt>1099 contractor</dt><dd>A worker paid without employee withholding, often described as an independent contractor. Status depends on the economic reality of the work and on state rules.</dd></div>
<div class="term"><dt>Minimum wage</dt><dd>The lowest hourly rate the law requires. The federal rate is $7.25. A higher state or city rate controls when it applies.</dd></div>
<div class="term"><dt>Median wage</dt><dd>The point where half of workers in that occupation earn more and half earn less. It is not the wage on one posting, and it is not the average.</dd></div>
<div class="term"><dt>Telework</dt><dd>In the Current Population Survey, any work at home for pay during the reference week. It includes people who did this for only some of their hours.</dd></div>
<div class="term"><dt>Pay range</dt><dd>The wage or salary stated on a posting. Some states require a range for covered employers and jobs. Readers also look for it where no statute requires it.</dd></div>
<div class="term"><dt>Task scam</dt><dd>A fraud pattern described by the Federal Trade Commission: simple online tasks, a small early payout, then a demand to deposit money to withdraw supposed earnings.</dd></div>
</div></section>''',
        "reading.html",
    )

    page(
        "faq.html",
        "FAQ | Job Compass",
        "Common questions about the general information Job Compass publishes on U.S. remote and flexible work.",
        '''<div class="page-head"><div class="wrap"><span class="eyebrow">FAQ</span><h1>Questions readers ask about these guides</h1>
<p class="lede">Answers about the site. They are not answers about a particular job.</p></div></div>
<section><div class="wrap article plain-copy">
<details><summary>Does Job Compass list jobs or take applications?</summary>
<p>No. The pages explain terms, public figures, and what a readable posting contains. Hiring is between a reader and an employer or client.</p></details>
<details><summary>Is this legal, tax, or employment advice?</summary>
<p>No. Wage rules, tax withholding, and worker classification depend on the facts and on federal, state, and local law. The guides point to the public office that publishes each figure.</p></details>
<details><summary>Why do the percentages disagree?</summary>
<p>They measure different things. A share of paid days, a share of people who teleworked in one week, a share of job ads, and a share of adults who say they have a side hustle are not one statistic. <a href="article-what-figures-show.html">What the public figures show</a> keeps them apart.</p></details>
<details><summary>Does remote work mean the worker chooses the hours?</summary>
<p>No. Many home-based customer-service roles assign a shift. Flexible hours are a separate condition. <a href="article-three-words.html">How the words differ</a>.</p></details>
<details><summary>What should a reader do with a posting that hides the employer?</summary>
<p>Treat the missing name as a reason to stop. The Federal Trade Commission describes unnamed remote offers, upfront fees, and fake checks as common job-fraud patterns. <a href="article-read-a-posting.html">How to read a posting</a>.</p></details>
<details><summary>How current are the figures?</summary>
<p>Each guide has a review date and names its sources. Labor figures move. The linked agency page is the place to confirm a number before relying on it.</p></details>
</div></section>''',
        "about.html",
    )

    page(
        "about.html",
        "About | Job Compass",
        "Job Compass publishes general information for readers about remote, online, and flexible work in the United States.",
        '''<div class="page-head"><div class="wrap"><span class="eyebrow">About the publisher</span><h1>General information for readers</h1>
<p class="lede">Job Compass explains remote, online, and flexible work in the United States in plain language.</p></div></div>
<section><div class="wrap split">
<div class="reveal">
<h2>Who the guides are for</h2>
<p>The guides are for readers who want to understand a work arrangement before they act on a posting. They cover place, hours, pay, and employment status, including the questions that come up when work has to fit around another job, school, caregiving, or health.</p>
<h3>What this site is</h3>
<p>Job Compass is an independent publisher of general information. It is not a government agency, not an employer, and not an employment agency. It does not list jobs, receive applications, or send reader information to employers.</p>
</div>
<div class="reveal">
<div class="types">
<div class="type" style="grid-template-columns:1fr"><div><h3>Purpose</h3><p>Explain public labor-market information so a reader can tell work arrangements apart and know which office publishes a figure.</p></div></div>
<div class="type" style="grid-template-columns:1fr"><div><h3>What the guides do</h3><p>They define terms, separate surveys that are easy to mix, and describe what a readable posting contains.</p></div></div>
<div class="type" style="grid-template-columns:1fr"><div><h3>What they do not do</h3><p>They do not offer a job, promise income, or replace the Department of Labor, the Internal Revenue Service, a state labor office, or the Federal Trade Commission.</p></div></div>
</div>
</div>
</div></section>
<section class="alt"><div class="wrap">
<p class="notice" style="max-width:70ch">Job Compass publishes general information rather than legal, tax, or employment advice. It has no application inbox on this site. Questions about a specific posting belong with the employer named on that posting.</p>
</div></section>''',
        "about.html",
    )

    page(
        "contact.html",
        "Contact | Job Compass",
        "How to read Job Compass, and what this site does not collect.",
        '''<div class="page-head"><div class="wrap"><span class="eyebrow">Contact</span><h1>This site does not take applications</h1>
<p class="lede">Job Compass shares general information. It does not collect résumés or introduce readers to employers.</p></div></div>
<section><div class="wrap split">
<div>
<h2>If a figure looks wrong</h2>
<p>Each guide names its source and the date it was reviewed. The agency page linked from the guide is the record to check. Labor figures are updated by those agencies, and a guide can lag a release.</p>
<h2>If a posting looks wrong</h2>
<p>The employer named on the posting is the party that can explain the hours, the pay, and the status. A posting with no employer name matches a pattern the Federal Trade Commission tells consumers to refuse. Reports can be filed at ReportFraud.ftc.gov.</p>
</div>
<div>
<div class="notice"><h2>No message is stored here</h2>
<p>This website does not run an application form and does not keep a mailing list. Using the guides does not create an employment relationship.</p></div>
</div>
</div></section>''',
        "contact.html",
    )

    page(
        "privacy.html",
        "Privacy | Job Compass",
        "What the Job Compass reader site does and does not collect.",
        f'''<div class="page-head"><div class="wrap"><span class="eyebrow">Privacy</span><h1>Privacy</h1>
<p class="lede">How this informational site handles a visit. Last updated {REVIEWED}.</p></div></div>
<section><div class="wrap article plain-copy">
<h2>What the site is for</h2>
<p>Job Compass publishes general information. It does not ask readers to create an account, upload a résumé, or submit an application.</p>
<h2>Information the site does not collect</h2>
<p>There is no application form and no mailing list on this site. Pages do not ask for a Social Security number, a date of birth, or payment details.</p>
<h2>Fonts</h2>
<p>Pages load typefaces from Google Fonts. A visit can therefore send the usual technical request, such as an IP address, to Google’s font service. Readers who want to avoid that request can use a browser setting or extension that blocks third-party fonts. The words of the guides remain available either way.</p>
<h2>Local features</h2>
<p>The guide filter, the glossary search, and the mobile menu run in the browser. They do not send what a reader types in the glossary box to Job Compass.</p>
<h2>Links</h2>
<p>Guides link to public agencies and to reporting on those figures. Those sites have their own privacy practices. A link is a citation, not an endorsement.</p>
</div></section>''',
        "about.html",
    )

    page(
        "disclaimer.html",
        "Disclaimer | Job Compass",
        "Limits on the general information Job Compass publishes about work in the United States.",
        f'''<div class="page-head"><div class="wrap"><span class="eyebrow">Scope</span><h1>Disclaimer</h1>
<p class="lede">Limits that apply to every page. Last updated {REVIEWED}.</p></div></div>
<section><div class="wrap article plain-copy">
<h2>General information only</h2>
<p>Job Compass publishes general information about online, remote, and flexible work in the United States. The content is for reading. It does not consider a particular reader’s circumstances.</p>
<h2>No employment service</h2>
<p>Job Compass is not an employer, a job board, or an employment agency. It does not publish openings, receive applications, or introduce candidates. Reading the site does not create an employment, recruitment, or advisory relationship.</p>
<h2>No professional advice</h2>
<p>The content is not legal, tax, financial, or employment advice. Minimum wages, payroll rules, and worker classification vary by law and by facts. A decision that depends on those rules belongs with the responsible agency or a qualified professional.</p>
<h2>No promise of work or income</h2>
<p>Nothing on the site is a job offer or a promise of earnings. Examples of occupations and of expired or third-party ads illustrate arrangements. They are not vacancies offered by Job Compass.</p>
<h2>Figures change</h2>
<p>Surveys, wage tables, and proposed regulations move. Each guide names a review date and a source. No warranty is made that every sentence is complete or current. Readers should confirm a figure with the cited source before relying on it.</p>
<h2>External links</h2>
<p>Links are provided so a reader can reach the original source. Job Compass does not control those sites.</p>
</div></section>''',
        "about.html",
    )


if __name__ == "__main__":
    build()
    print("rendered", len(list(ROOT.glob("*.html"))), "pages")
