#!/usr/bin/env python3
"""Render Weekline, a U.S. public record of remote and flexible work.

The pages share general information. They do not list jobs or take applications.
The editorial frame is the distance between published labor counts and the ad
market, which is a different job from a search guide.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "site"
THEME = "#2d5bff"
REVIEWED = "3 November 2026"
BRAND = "Weekline"
FONT = (
    "https://fonts.googleapis.com/css2?family=Inter:ital,wght@"
    "0,400;0,500;0,600;0,700;0,800;1,500&display=swap"
)

NAV = [
    ("career-guides.html", "Career Guides"),
    ("work-options.html", "Work Options"),
    ("extra-income.html", "Extra Income"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

CONTENT_FILES = {
    "career-guides.html",
    "work-options.html",
    "extra-income.html",
    "about.html",
    "contact.html",
    "skills-training.html",
    "start.html",
    "record.html",
    "search.html",
    "apply.html",
    "states.html",
    "arrangements.html",
    "occupations.html",
    "side-work.html",
    "notes.html",
    "terms.html",
    "questions.html",
    "corrections.html",
    "disclaimer.html",
}

WRITTEN = set()


def prefixes(kind):
    if kind == "home":
        return {
            "home": "index.html",
            "content": "content/",
            "privacy": "privacy-policy/",
            "thanks": "thank-you/",
            "asset": "",
            "favicon": "favicon.svg",
        }
    if kind == "special":
        return {
            "home": "../index.html",
            "content": "../content/",
            "privacy": "../privacy-policy/",
            "thanks": "../thank-you/",
            "asset": "../",
            "favicon": "../favicon.svg",
        }
    return {
        "home": "../index.html",
        "content": "",
        "privacy": "../privacy-policy/",
        "thanks": "../thank-you/",
        "asset": "../",
        "favicon": "../favicon.svg",
    }


def href_for(target, kind, fragment=""):
    p = prefixes(kind)
    frag = f"#{fragment}" if fragment else ""
    if target in ("index.html",):
        return p["home"] + frag
    if target in ("privacy.html", "privacy-policy/", "privacy-policy/index.html"):
        return p["privacy"] + frag
    if target in ("thank-you.html", "thank-you/", "thank-you/index.html"):
        return p["thanks"] + frag
    if target in CONTENT_FILES:
        return p["content"] + target + frag
    return None


def rewrite_links(html, kind):
    def repl(match):
        attr, url = match.group(1), match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#", "../", "content/", "privacy-policy/", "thank-you/")):
            return match.group(0)
        path, _, frag = url.partition("#")
        new = href_for(path, kind, frag)
        if new is None:
            return match.group(0)
        return f'{attr}="{new}"'

    return re.sub(r'(href)=["\']([^"\']+)["\']', repl, html)


def brand(kind):
    p = prefixes(kind)
    return f'<a class="brand" href="{p["home"]}"><span class="brand-mark" aria-hidden="true"></span>{BRAND}</a>'


def nav_block(current, kind):
    p = prefixes(kind)
    items = []
    for href, label in NAV:
        url = p["content"] + href
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{url}"{cur}>{label}</a></li>')
    return f'''<nav aria-label="Primary"><ul id="nav-list">{"".join(items)}</ul></nav>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-list" aria-label="Open menu"><span class="bars" aria-hidden="true"></span></button>'''


def header(current, kind="content", landing=False):
    p = prefixes(kind)
    links = nav_block(current, kind)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap header-row">
{brand(kind)}
<div class="nav-wrap">{links}</div>
<a class="btn btn-primary header-cta" href="{p["content"]}career-guides.html">Explore career guides</a>
</div>
</header>'''


def footer(kind="content"):
    p = prefixes(kind)
    return f'''<footer class="site-footer"><div class="wrap foot">
<div class="foot-brand"><p class="brand-foot">{BRAND}</p>
<p>Articles and guides on U.S. careers, pay, training, flexible work, and ways to earn extra income.</p></div>
<div><h2>Explore</h2><ul>
<li><a href="{p["content"]}career-guides.html">Career Guides</a></li>
<li><a href="{p["content"]}skills-training.html">Skills &amp; Training</a></li>
<li><a href="{p["content"]}work-options.html">Work Options</a></li>
<li><a href="{p["content"]}extra-income.html">Extra Income</a></li>
</ul></div>
<div><h2>Data and resources</h2><ul>
<li><a href="https://www.bls.gov/" rel="noopener">Bureau of Labor Statistics</a></li>
<li><a href="https://www.careeronestop.org/Toolkit/Wages/find-salary.aspx" rel="noopener">CareerOneStop wage tools</a></li>
<li><a href="https://www.apprenticeship.gov/" rel="noopener">Apprenticeship.gov</a></li>
<li><a href="https://consumer.ftc.gov/articles/job-scams" rel="noopener">FTC job scam guidance</a></li>
</ul></div>
</div>
<div class="wrap legal"><p>Pay, job requirements, and work arrangements vary by employer and location. Check the date and geography of wage figures and confirm the details of a role with the employer. {BRAND} provides general information only; it does not list jobs, screen employers, or give legal, tax, or financial advice.</p>
<div class="legal-row">
<p>&copy; 2026 {BRAND} &middot; United States</p>
<p class="legal-links"><a href="{p["privacy"]}">Privacy Policy</a><a href="#top">Back to top</a></p>
</div></div>
</footer>
<script src="{p["asset"]}safer-script.js"></script>'''


def page(filename, title, description, body, current, landing=False, kind="content"):
    p = prefixes(kind)
    body = rewrite_links(body, kind)
    if kind == "home":
        relpath = filename
    elif kind == "special":
        relpath = filename
    else:
        relpath = f"content/{filename}"
    body_class = ' class="landing"' if landing else ""
    html = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="{THEME}">
<link rel="icon" href="{p["favicon"]}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONT}" rel="stylesheet">
<link rel="stylesheet" href="{p["asset"]}safer-style.css">
</head>
<body id="top"{body_class}>
{header(current, kind=kind, landing=landing)}
<main id="main">
{body}
</main>
{footer(kind)}
<noscript><style>.reveal{{opacity:1;transform:none}}</style></noscript>
</body>
</html>
'''
    dest = ROOT / relpath
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    WRITTEN.add(relpath.replace("\\", "/"))


def essay(filename, kicker, h1, description, lede, inner, current, section="Record"):
    body = f'''<div class="page-head"><div class="wrap"><p class="kicker">{kicker}</p><h1>{h1}</h1>
<p class="lede">{lede}</p></div></div>
<section><div class="wrap article">
<p class="byline">{BRAND} &middot; {section} &middot; Reviewed {REVIEWED}</p>
{inner}
<p class="back"><a href="notes.html">All notes</a></p>
</div></section>'''
    page(filename, f"{h1} · {BRAND}", description, body, current, kind="content")


def build():
    page(
        "index.html",
        f"Career guides, pay, training, and flexible work · {BRAND}",
        "Weekline covers U.S. career paths, pay, training options, and flexible or extra-income work, with a source named behind every figure.",
        '''
<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow">General information, not job listings</p>
<h1>What’s changing in the U.S. job market, and what it means for your next move.</h1>
<p class="lede">See where jobs are projected to grow, what training or credentials different roles ask for, and how pay and openings compare near you. These guides also cover remote and part-time work, and whether a side gig fits your schedule.</p>
<div class="hero-actions">
<a class="btn btn-primary btn-lg" href="career-guides.html">Explore career guides</a>
<a class="btn btn-ghost btn-lg" href="work-options.html">Compare work options</a>
</div>
<ul class="hero-chips">
<li><span class="chip-icon">📈</span>Where jobs are growing</li>
<li><span class="chip-icon">🎓</span>What it takes to qualify</li>
<li><span class="chip-icon">🗺️</span>Remote, hybrid, or flexible</li>
</ul>
</div>
<div class="hero-card" aria-hidden="true">
<p class="hero-card-label">A few figures to start with</p>
<div class="hero-stat"><span class="num">5.9M</span><span class="desc">new U.S. jobs the BLS projects for 2025–2035</span></div>
<div class="hero-stat"><span class="num">35%</span><span class="desc">of employed people did some or all of their work at home on days they worked, 2025</span></div>
<div class="hero-stat"><span class="num">34.6%</span><span class="desc">projected growth for data scientists, among the fastest of any occupation</span></div>
</div>
</div></section>

<section class="featured"><div class="wrap featured-row">
<div class="featured-copy">
<p class="section-label">Featured story &middot; U.S. job outlook</p>
<h2>Where U.S. jobs are projected to grow through 2035.</h2>
<p>The U.S. Bureau of Labor Statistics projects that the economy will add 5.9 million jobs from 2025 to 2035. This covers where that growth is expected, what it takes to enter selected occupations, and how to check pay and openings near you.</p>
<p class="mini-src">Source: BLS employment projections, 2025–2035.</p>
<p><a class="guide-link" href="career-guides.html#job-outlook">Read the U.S. job outlook &rarr;</a></p>
</div>
<div class="featured-art" aria-hidden="true">
<div class="chart-viz">
<span class="chart-bar" style="height:38%"></span>
<span class="chart-bar" style="height:58%"></span>
<span class="chart-bar" style="height:46%"></span>
<span class="chart-bar" style="height:78%"></span>
<span class="chart-bar chart-bar-end" style="height:100%"></span>
</div>
<p class="chart-caption">+5.9M jobs<br>2025&ndash;2035</p>
</div>
</div></section>

<section class="pillars"><div class="wrap">
<div class="section-head-center">
<p class="section-label">The big picture</p>
<h2>Four things to consider before your next career move.</h2>
</div>
<div class="pillar-grid">
<div class="pillar-card pillar-1">
<span class="pillar-icon" aria-hidden="true">📈</span>
<p class="pillar-num">01</p>
<h3>Job demand</h3>
<p>Healthcare support is among the occupational groups projected to grow fastest through 2035, and data scientists rank among the fastest-growing individual occupations. Once a role catches your eye, check pay and openings where you live.</p>
<p class="pillar-src"><span class="src-kicker">Sources</span> BLS employment projections &middot; CareerOneStop wage tools</p>
</div>
<div class="pillar-card pillar-2">
<span class="pillar-icon" aria-hidden="true">🎓</span>
<p class="pillar-num">02</p>
<h3>Skills and training</h3>
<p>Start with the job you want, then compare ways to qualify. A community college program, certification, degree, or paid Registered Apprenticeship can each make sense, depending on the role.</p>
<p class="pillar-src"><span class="src-kicker">Source</span> Apprenticeship.gov career seeker resources</p>
</div>
<div class="pillar-card pillar-3">
<span class="pillar-icon" aria-hidden="true">🧭</span>
<p class="pillar-num">03</p>
<h3>Work flexibility</h3>
<p>In 2025, 35% of employed people did some or all of their work at home on days they worked. When comparing jobs, look at where you’re expected to work, which hours you need to be available, and how often you’ll need to go in.</p>
<p class="pillar-src"><span class="src-kicker">Source</span> BLS American Time Use Survey</p>
</div>
<div class="pillar-card pillar-4">
<span class="pillar-icon" aria-hidden="true">💰</span>
<p class="pillar-num">04</p>
<h3>Extra income</h3>
<p>In a 2024 Federal Reserve survey, some gig workers said they'd struggle to make ends meet without that income, and many wanted steadier pay. When comparing options, look at what you could earn after expenses and how reliably the work comes in.</p>
<p class="pillar-src"><span class="src-kicker">Source</span> Federal Reserve household survey, 2024</p>
</div>
</div>
</div></section>

<section class="guides"><div class="wrap">
<div class="section-head-center">
<p class="section-label">Career guides</p>
<h2>Find out what jobs pay and what it takes to qualify.</h2>
</div>
<div class="guide-grid">
<a class="guide-card" href="career-guides.html#job-outlook">
<span class="guide-icon">📈</span>
<h3>Job outlook</h3>
<p>Selected roles in healthcare, technology, and other fields with strong projected growth, plus how to check demand in your area.</p>
<span class="guide-link">Read the guide &rarr;</span>
</a>
<a class="guide-card" href="career-guides.html#pay">
<span class="guide-icon">💲</span>
<h3>Pay</h3>
<p>How to look up wages for your occupation and location, and use local figures to put a posted salary range or hourly rate in context.</p>
<span class="guide-link">Read the guide &rarr;</span>
</a>
<a class="guide-card" href="skills-training.html">
<span class="guide-icon">🎓</span>
<h3>Skills and training</h3>
<p>How long an apprenticeship, certificate, or degree path takes, what it costs, and what credential it leads to.</p>
<span class="guide-link">Read the guide &rarr;</span>
</a>
<a class="guide-card" href="work-options.html">
<span class="guide-icon">🗺️</span>
<h3>Flexible work</h3>
<p>What “flexibility” can mean — where you work, when you work, or both — and what to ask about office days and required hours.</p>
<span class="guide-link">Read the guide &rarr;</span>
</a>
<a class="guide-card" href="career-guides.html#career-change">
<span class="guide-icon">🔁</span>
<h3>Career change</h3>
<p>How to find roles that use skills you already have, and identify what you’d still need to learn to make the move.</p>
<span class="guide-link">Read the guide &rarr;</span>
</a>
<a class="guide-card" href="career-guides.html#signs">
<span class="guide-icon">🚩</span>
<h3>Job search safety</h3>
<p>How to verify a listing on the employer’s own site, recognize a request for upfront payment, and decide when it’s safe to share personal information.</p>
<span class="guide-link">Read the guide &rarr;</span>
</a>
</div>
<p class="guides-more"><a class="btn btn-ghost" href="career-guides.html">Browse all career guides &rarr;</a></p>
</div></section>

<section class="extra-teaser"><div class="wrap extra-grid">
<div class="extra-copy">
<p class="section-label">Extra income</p>
<h2>What could a second job or side gig add to your budget?</h2>
<p>A weekend shift, a freelance project, and app-based gig work each bring in extra income, and each makes different demands on your time. Start with the hours you can realistically give, then compare how often you’ll get paid, what the work costs you, and how reliably it comes in.</p>
<p><a class="guide-link" href="extra-income.html">Compare ways to earn extra income &rarr;</a></p>
<p class="mini-src">Source: Federal Reserve household survey, 2024. General information, not tax or financial advice — actual take-home pay depends on your own tax situation and expenses.</p>
</div>
<div class="extra-art" aria-hidden="true">
<p class="extra-stat"><span class="num">9.0M</span><span class="desc">people held more than one job, September 2026</span></p>
<ul class="extra-options">
<li><span class="opt-icon opt-icon-1">🕒</span>Weekend shift</li>
<li><span class="opt-icon opt-icon-2">💻</span>Freelance project</li>
<li><span class="opt-icon opt-icon-3">🚗</span>App-based gig</li>
</ul>
</div>
</div></section>

<section class="opts"><div class="wrap">
<div class="section-head-center">
<p class="section-label">Work options</p>
<h2>Compare six ways to work.</h2>
</div>
<div class="opts-table-wrap"><table class="opts-table">
<thead><tr><th>Work option</th><th>What to check</th></tr></thead>
<tbody>
<tr><td>Part-time jobs</td><td>Expected weekly hours, shift changes, and which benefits are available.</td></tr>
<tr><td>Remote jobs</td><td>Eligible states, time zone requirements, and whether travel is expected.</td></tr>
<tr><td>Hybrid jobs</td><td>Required office days, commute time, and who sets the schedule.</td></tr>
<tr><td>Flexible schedules</td><td>Required hours, how far ahead shifts are posted, and whether you can change your availability.</td></tr>
<tr><td>Freelance work</td><td>Project scope, payment terms, and the time it takes to find clients.</td></tr>
<tr><td>App-based gigs</td><td>Pay per task, unpaid waiting time, and expenses such as mileage or supplies.</td></tr>
</tbody>
</table></div>
<p class="guides-more"><a class="btn btn-ghost" href="work-options.html">Explore all work options &rarr;</a></p>
</div></section>

<section class="guides practical"><div class="wrap">
<p class="section-label">Practical guides</p>
<h2>What to ask before you apply or accept an offer.</h2>
<div class="guide-grid">
<div class="guide-card static">
<h3>How to ask for a flexible schedule</h3>
<p>Put together a proposal that explains the schedule you want, how you’ll cover your responsibilities, and when you and your manager can review how it’s working.</p>
</div>
<div class="guide-card static">
<h3>Employee or independent contractor?</h3>
<p>Ask how you’ll be paid, who covers equipment and expenses, and which benefits, if any, come with the arrangement.</p>
</div>
<div class="guide-card static">
<h3>How to write a résumé for a remote role</h3>
<p>Show how you’ve handled deadlines, shared updates, and worked with people in different locations, using specific examples of what you delivered.</p>
</div>
</div>
<p class="guides-more"><a class="btn btn-ghost" href="work-options.html#practical">Read more practical guides &rarr;</a></p>
</div></section>

<section class="contact-teaser"><div class="wrap">
<div class="section-head-center">
<p class="section-label">Contact</p>
<h2>What would you like us to cover next?</h2>
<p>Have a question about a career path, a training program, or a type of work? Tell us what you’re trying to figure out — your suggestions help shape future guides.</p>
</div>
<form class="contact-form contact-form-center" id="home-contact-form" data-thanks="thank-you/">
<div class="form-row">
<div><label for="hc-name">Name</label><input id="hc-name" name="name" type="text" autocomplete="name" required></div>
<div><label for="hc-phone">Phone number</label><input id="hc-phone" name="phone" type="tel" autocomplete="tel" placeholder="Optional"></div>
</div>
<div><label for="hc-email">Email address</label><input id="hc-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="hc-topic">Your question or topic suggestion</label><textarea id="hc-topic" name="topic" required></textarea></div>
<button class="btn btn-primary" type="submit">Send a suggestion</button>
<p class="contact-confirm" role="status">Thanks for sending your suggestion.</p>
</form>
</div></section>
''',
        "index.html",
        True,
        "home",
    )

    essay(
        "start.html",
        "Start here",
        "The starter’s companion",
        "What remote, online, and independent work usually involves in the first weeks, for readers in the United States.",
        "Not what the job is called. What actually happens once you say yes.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>Someone still checks the work. Remote and online do not mean unsupervised.</li>
<li>“Flexible” is a smaller promise than it sounds. Ask how much of the clock is actually yours.</li>
<li>Independent work trades a boss for a client, and a paycheck for an invoice. Both have upsides and both have gaps.</li>
<li>Write down the hours, the pay, and the employer’s name before the first day. If one is missing, that is the finding.</li>
</ul></div>

<h2>Who checks on the work</h2>
<p>Remote and online are not the same as unsupervised. A customer-service week done from a spare room usually comes with a login, a queue, and a supervisor who can see when you signed in. A tutoring session on video has a parent or a platform watching the same screen. Independent contract work swaps a supervisor for a client, and a client who goes quiet is its own kind of check-in problem. Before starting, it is worth asking plainly: who will I hear from if something is wrong, and how often will they expect to hear from me?</p>

<h2>What “flexible” usually buys you</h2>
<p>Flexible schedules exist on a spectrum, from “pick any eight hours this week” to “start whenever, as long as the shift still gets covered by 9 a.m.” Most arrangements sit closer to the second end. A national study taken in early 2025 found 62 in 100 workers did not have a predictable schedule they could control themselves, and even among employers who advertise flexibility, only about 1 in 10 offer a genuinely shortened week. The useful question isn’t “is this flexible,” it’s “which part of the clock do I actually choose, and which part does someone else still assign.”</p>

<h2>Employee or on your own</h2>
<p>A job with a W-2 withholds income tax and splits the Social Security and Medicare bill with the employer. Independent, 1099-style work puts both halves of that bill on you, along with your own equipment, your own slow weeks, and usually your own health insurance. In exchange, you set more of your own schedule and can often work for more than one client at once. Neither is better by default. What matters is whether the arrangement matches what was promised: a “contractor” role that assigns your exact hours and only lets you work for one company starts to look like a job in contractor’s clothing, and that gap is exactly what regulators and courts spend their time sorting out. <a href="states.html#status">The longer note on status</a> covers where that rule currently stands.</p>

<h2>What should be written down before day one</h2>
<p>Four things are reasonable to ask for in writing, by text or email is fine, before the first real day of work: the pay rate or salary, who you’re actually working for (a company name you can search, not just a hiring manager’s first name), whether you’re an employee or a contractor, and roughly what hours or workload is expected. None of these are unusual requests. An employer or client who can’t answer one plainly is telling you something.</p>

<h2>What a real offer tends to look like, and what a scam tends to look like</h2>
<p>A real remote or online offer names the employer, states a pay figure or a clear range, and asks you to do the actual job, usually after a short interview, before any money changes hands in either direction. A scam, by the patterns in Federal Trade Commission guidance, tends to arrive as an unexpected text or chat, offers a vague title with no real duties, asks for a fee of any size, or has you deposit a check and send part of it back. Reported losses from job and employment scams passed half a billion dollars in 2024, so treating a “too easy” offer with some suspicion is not paranoia, it is proportionate. <a href="search.html#signs">The longer note on this</a> goes through the figures and the exact warning signs.</p>

<h2>Where to go next</h2>
<p>This page is the short version. For the numbers behind each claim here, the longer notes cover pay and state minimums, the difference between an employee and a contractor, the occupations that actually show up in the remote-work shelf, and the fraud reports in more detail.</p>
''',
        "start.html",
        "Companion",
    )

    essay(
        "record.html",
        "The record",
        "Where the paid days are spent",
        "How U.S. figures describe remote and hybrid work among people, not among postings.",
        "These figures describe where people work. A share of days and a share of people are different counts.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>One series counts paid days at home.</li>
<li>One series counts people who teleworked in a single week.</li>
<li>A third series asks people whose jobs can be done remotely where they prefer to work.</li>
</ul></div>
<h2>Paid days at home</h2>
<p>The Survey of Working Arrangements and Attitudes asks about the share of full paid working days done at home. The sample is workers who earned at least $10,000 in a prior year, reweighted toward the Current Population Survey. The share was 7.2% in December 2019, about 62% in May 2020, and 26.8% in September 2026. It has stayed in the mid-20s since 2023.</p>
<p>In August 2026 the same project reported, for full-time wage-and-salary workers, 60.8% fully on site, 27.1% hybrid, and 12.1% fully remote. Home days were more common in information, finance, and professional services than in manufacturing, education, or transportation. Women were at about 29.3% of paid days at home that month, and men at about 25.2%.</p>
<h2>Anyone who teleworked that week</h2>
<p>The Bureau of Labor Statistics asks people who worked during the survey week whether they teleworked or worked at home for pay. In September 2026, not seasonally adjusted, 21.9% had done so for at least some hours and 10.7% had done so for all of their hours. That is 34.7 million people out of 158.5 million at work. Women were at 23.9% and men at 20.1%. People with their own children under 18 were at 25.9%. People with a disability were at 24.4%.</p>
<p>Age runs against the idea that the youngest workers are the ones at home. Ages 16 to 24 were at 5.7%, because many of those jobs are on site. Ages 35 to 44 were at 26.2%. Among people 25 and older, the any-telework share was 4.4% with no high school diploma, 8.3% with a high school diploma only, 18.1% with some college, 37.8% with a bachelor’s degree, and 40.6% with an advanced degree.</p>
<p>The same month’s household survey, seasonally adjusted, put unemployment at 4.2% (7.1 million people). Labor-force participation was 61.8%. Employment as a share of the population was 59.2%. Payrolls rose by 29,000. Part time for economic reasons was 4.501 million. People unemployed 27 weeks or longer numbered 1.944 million.</p>
<h2>Preference is a smaller room</h2>
<p>Gallup’s location figures cover employees whose work can be done remotely. In August 2026 that group was 54% hybrid, 25% exclusively remote, and 21% on site. In November 2025, preference in the same kind of group was 61% hybrid, 33% remote, and 6% on site. In May 2025, Gen Z was the least likely to want fully remote work: 23%, against 35% of older employees, with 71% preferring hybrid.</p>
<p class="src-note">FRED series WFHCOVIDMATQUESTION. Survey of Working Arrangements and Attitudes, Barrero, Bloom, and Davis. Bureau of Labor Statistics, Employment Situation and table A-41, September 2026. Gallup, Hybrid Work indicator.</p>
''',
        "record.html",
    )

    essay(
        "search.html",
        "The search",
        "Where, how, and when the search actually happens",
        "Where Americans look for remote, online, and flexible work, how a typical search runs step by step, and when remote postings are actually available.",
        "The looking is measurable too, not just the hiring. Here is where it starts, how it runs, and when the ads are thin.",
        '''
<p class="reassure">If a remote search feels slower or more confusing than it should, that’s a reasonable reaction to how the market actually works right now, not a sign you’re searching wrong. The data below explains why.</p>
<div class="takeaways"><h2>In short</h2><ul>
<li>Searches still start on the large boards, then LinkedIn, Google, and employer sites.</li>
<li>A search tends to run the same handful of steps, in roughly the same order, whether the goal is a title or just extra cash.</li>
<li>Remote postings are roughly a tenth of ads, or less, and about a third of applications, and the share moves by season and by field.</li>
<li>An unnamed remote offer that asks for a fee matches a pattern in Federal Trade Commission reports.</li>
</ul></div>

<h2 id="where">Where the looking starts</h2>
<p>iHire’s 2025 survey of 1,421 U.S. job seekers asked which resources they use. People could choose more than one. General job boards were 78.5%, LinkedIn 54.9%, niche boards 53.8%, company websites 45.0%, and search engines 41.6%. Networking was 32.7%, social media 15.7%, associations 15.4%, job fairs 12.7%, Craigslist 8.3%, and generative tools 6.9%. The prose summary of that survey rounded the board figure differently. The chart figure used here is 78.5%.</p>
<p>HireClix asked 1,000 adults in 2025 where a search starts. Indeed was 56%, LinkedIn 52% (up from 40% in 2023), Google 41%, and corporate career sites 40%. Fifty-seven percent said reviews on Glassdoor or Indeed affect the decision to apply. One survey asks about every channel used. The other asks about the first stop. Both can be right at once.</p>
<p>A practical search for a professional role tends to be Indeed or LinkedIn, then the employer’s own page, then a review site. A practical search for hourly, local, or shift work still uses Indeed, and adds Facebook groups, Craigslist, and sometimes a staffing agency. Niche boards matter once the field is known: USAJobs for federal roles, Dice or Wellfound for some technology roles, and paid remote boards such as FlexJobs for people willing to pay to filter. Social media is more of a research step than an application step; HireClix found more than half of Gen Z and millennial candidates check a company’s social accounts before applying.</p>
<p>On the employer side of the same iHire survey, 529 respondents named referrals at 71.3%, the career page at 49.5%, LinkedIn at 46.1%, and social at 43.5%. A large share of hiring never appears as a clean public ad at all.</p>

<h2 id="how">How a search tends to run</h2>
<ol class="steps">
<li>Search a title plus “remote,” a city, or “part time.” Salary and work arrangement are the filters that decide whether an ad even gets opened.</li>
<li>Skip the ad if the pay, the employer name, or the location type is missing. iHire found a missing salary was an instant turnoff for 60.7% of seekers, and an unnamed employer for 50.9%.</li>
<li>Check the company site and a review site such as Glassdoor before spending time on the application form.</li>
<li>Apply where the form is short. 51.7% of seekers in the same survey said 10 to 15 minutes is the right length for an online application.</li>
<li>Keep a second path for extra cash that isn’t a job ad at all: marketplace selling, delivery apps, task platforms, or a direct message from someone already known.</li>
</ol>
<p>Competition on the big boards is high and the reply rate is low once an application is sent. Huntr’s 2025 report, based on about 599,000 applications tracked in its own product (a self-selected set of users, not a population survey), found interview response rates of about 4.5% on Indeed, 3.1% on LinkedIn, and 2.8% on ZipRecruiter, with a higher 11.3% on the smaller, more curated Google for Jobs. Ghosting after applying was the single most common frustration named in the iHire survey, at 59.0%.</p>

<h2 id="when">When the ads are thin, and when they loosen up</h2>
<p>Indeed’s own count of U.S. postings mentioning remote or hybrid work, or listing the location as remote, moved like this: 2.6% in January 2019, a peak of 10.4% in February 2022, 7.8% on 31 October 2024, and 8.3% on 31 January 2025. A secondary compilation of the same tracker puts the share at 8.4% on 31 August 2026, against 8.2% a year earlier, and says it has stayed between about 7.7% and 9.1% since the start of 2024. The all-jobs average hides large differences by field: in the same compilation, remote or hybrid mentions were 39.7% of insurance postings, 32.9% of legal, 32.4% of mathematical, 30.8% of software, 25.2% of marketing, and 20.8% of human resources, against 3.9% for construction, 1.9% for retail, and 1.2% for driving.</p>
<p>Demand runs well ahead of that thin supply. A LinkedIn spokesperson told Business Insider that in September 2025 about 8% of paid U.S. postings offered remote work, and those postings drew 35% of applications; in July 2025 it was about 9% of postings and 37% of applications. A remote posting on LinkedIn draws on the order of four times the applications its share of the board would predict. Robert Half’s professional-job tracker described fully on-site roles rising from 65% of postings it tracks in the fourth quarter of 2025 to 87% in the second quarter of 2026, with 10% hybrid and 3% fully remote; 36% of employers in that survey said they had raised required on-site days over the prior year.</p>
<p>The wider labor market this is happening in is not booming. BLS, seasonally adjusted, September 2026: unemployment 4.2% (7.1 million people), labor-force participation 61.8%, employment-population ratio 59.2%, payrolls up 29,000 that month. Indeed’s Job Postings Index fell from 111.7 on 1 January 2025 to 101.7 at the end of October 2025, just above the pre-pandemic baseline. Searching for remote work now means applying into a cooler market, onto a smaller set of ads, than in 2021 or 2022. Federal civilian remote work is its own special case: Gallup reported hybrid among federal employees fell from 61% in late 2024 to 28% after the 2025 federal return-to-office, with 46% fully on site.</p>
<p>Employers have pulled back on formal flexibility benefits too, without dropping them. SHRM’s 2026 survey found 57% of employers offer hybrid work (down 3 points from 2025) and 45% offer flextime during core hours (down 6 points), while 10% now offer a four-day week (up 2 points).</p>

<h2>What the crowded ads have stated</h2>
<p>Entry-level remote titles in the FlexJobs database from 1 January to 1 May 2026 were led by customer service, administration, and sales. Named customer-service ads reviewed in autumn 2026, including Concentrix, TTEC, and Firstsource, clustered around $15 to $17 an hour, with an assigned shift, a high-school diploma, and prior customer-service experience. Some required a wired connection rather than a phone hotspot. Those ads expire. They show the shape of the shelf. They are not openings from Weekline.</p>

<h2 id="signs">The signs when an offer isn’t real</h2>
<p>The Federal Trade Commission’s 10 March 2025 release said reports of job and employment-agency scams tripled from 2020 to 2024, and reported losses rose from $90 million to $501 million. A September 2025 FTC note put 2024 job-scam reports above 105,000 and losses above $513 million. Task scams were about 20,000 reports in the first half of 2024, against about 5,000 in all of 2023. The patterns in FTC consumer guidance are an unexpected text or chat, a remote title with no duties, any fee, a check the person is told to deposit and partly send back, and pay for liking or rating things followed by a demand to deposit money. Reports go to ReportFraud.ftc.gov.</p>
<p class="src-note">iHire, State of Online Recruiting 2025, chart figures. HireClix, 2025 Candidate Experience Survey. Indeed Hiring Lab. Business Insider, 19 October 2025. Los Angeles Times, 8 September 2025. FlexJobs, entry-level remote guide, updated 28 May 2026. Huntr, 2025 Annual Job Search Trends. SHRM, 2026 Employee Benefits Survey. Gallup, Hybrid Work in Retreat? Barely. FTC press release, 10 March 2025, and FTC business blog, September 2025. Occupation shares for 31 August 2026 are a secondary compilation.</p>
''',
        "search.html",
    )

    essay(
        "apply.html",
        "Apply",
        "How the application runs, and what it actually asks for",
        "What a typical U.S. online application involves, step by step, and the documents, equipment, and checks employers commonly require before hiring.",
        "Not what the job is. What filling out the form, and then saying yes to it, actually involves.",
        '''
<p class="reassure">None of what follows is specialized knowledge. It’s just rarely written down in one place, which is why it can feel more intimidating than it actually is.</p>
<div class="takeaways"><h2>In short</h2><ul>
<li>Most online applications follow the same shape: a short form, a few screening questions, sometimes a skills test, then an interview.</li>
<li>About half of job seekers consider 10 to 15 minutes the acceptable length for that form.</li>
<li>Nearly every U.S. employer asks for the same handful of things before a first day: proof you can legally work, a working setup, and the right tax paperwork.</li>
<li>A fee, a kit charge, or a check you’re asked to deposit and partly send back is never a legitimate requirement.</li>
</ul></div>

<h2 id="process">How the application usually runs</h2>
<p>An online application for a remote, hourly, or flexible role tends to move through the same handful of stages. First, a form: contact details, a résumé upload, and often a set of “knockout” questions, such as availability, location, or whether you can legally work in the U.S. These questions can end the application immediately if the answer doesn’t fit, which is a common source of silence rather than rejection. Behind that form, most mid-size and large employers run the answers through applicant-tracking software that scores how closely the résumé’s wording matches the posting before any person reads it — which is why two readers with similar experience can get very different results from the same ad, and why it helps to use the posting’s own words for your skills rather than a synonym. iHire’s 2025 survey of job seekers found that re-typing information already on an uploaded résumé was a specific, named complaint, and that about half of seekers think 10 to 15 minutes is the right length for the whole form.</p>
<p>Some roles add a short skills check before a human ever looks at the application: a typing-speed test for data entry or transcription, a short writing sample for content roles, or a basic software quiz for bookkeeping or support roles. If the application clears the screening questions and any skills check, the next step is usually a phone or video interview, sometimes two rounds for office-based professional roles and one short call for hourly or entry-level remote roles. Interview response rates, in one applicant-tracking product’s 2025 data covering roughly 599,000 applications, ran about 4.5% on Indeed, 3.1% on LinkedIn, and 2.8% on ZipRecruiter — a reminder that most applications end without a reply at all, which is a volume problem more than a sign that the application itself was weak.</p>
<p>After an offer, the paperwork starts: the specific documents are covered below, but the shape is the same almost everywhere — sign an offer or contract, complete tax and eligibility forms, and, for jobs that provide equipment, wait for it to ship or submit a reimbursement request rather than pay for it upfront.</p>

<h2 id="ai">How AI has changed the interview itself</h2>
<p>By 2026, an AI interview is common rather than rare: Greenhouse’s 2026 survey found 63% of candidates who reached the interview stage had been interviewed by AI, up 13 points in six months. The format varies — a pre-recorded video scored by AI with no person present, a chatbot screening call, or a real-time interview with an AI interviewer — but the common thread is that a person may not review the result before a candidate is moved forward or rejected.</p>
<p>Disclosure is the weak point. In the same survey, 70% of candidates said they were never clearly told in advance that AI would evaluate them, and 21% only found out once the interview had already started. Separately, Enhancv’s 2026 survey found 50.5% of job seekers had been rejected at least once in the past year without any human contact, and 68.5% said AI’s role in that decision was never disclosed to them at all. Most candidates are not against AI being used — Greenhouse found only 19% want less of it — but a large majority want upfront notice, a clear explanation of what is being measured, and a human reviewing the result before a final decision.</p>
<p>None of this changes what the underlying requirements below actually are. It mainly changes who, or what, reviews the application first.</p>

<h2 id="requirements">What they’re commonly asked to have</h2>
<p>A U.S. job application, online or on paper, asks for the same core information almost everywhere. None of it is unusual to be asked for, and none of it should catch you off guard. Having it ready before starting just saves having to stop mid-form to look something up:</p>
<div class="ready-box">
<div class="ready-grid">
<div><h4>Personal details</h4><ul><li>Name, address, phone, email</li><li>Whether you’re eligible to work in the U.S.</li><li>Whether you’re over 18, or have a work permit if not</li></ul></div>
<div><h4>Education &amp; skills</h4><ul><li>Schools attended, degrees, certificates, graduation dates</li><li>Licenses or certifications relevant to the role</li></ul></div>
<div><h4>Work history</h4><ul><li>Past employers, addresses, and supervisor names</li><li>Start and end dates, and the reason you left each</li></ul></div>
<div><h4>References</h4><ul><li>2 to 3 people, with a phone number or email for each</li><li>Ask them first; some employers ask permission before contacting a current one</li></ul></div>
</div>
</div>
<p><b>Proof you can legally work in the United States.</b> Every W-2 employer must complete Form I-9 within three days of a new hire’s start date, which means presenting an acceptable document such as a U.S. passport, or a driver’s license plus a Social Security card, to confirm identity and work eligibility. This applies to remote hires exactly as it applies to on-site ones; a remote job does not skip it.</p>
<p><b>The right tax form for how you’re paid.</b> A W-2 employee completes Form W-4, which sets how much income tax is withheld from each paycheck. An independent contractor paid as 1099 completes Form W-9 instead, and no tax is withheld; the contractor sets aside their own income tax and both halves of Social Security and Medicare. Which form you’re asked for is a quick, reliable signal of which kind of work you’ve actually agreed to, regardless of what the posting called it.</p>
<p><b>A working setup.</b> Home-based customer-service and data roles commonly specify a computer meeting minimum specs, a quiet workspace, and a reliable internet connection, and many postings require a wired connection rather than a phone hotspot or satellite internet. Some roles additionally require a webcam for video calls or supervision software installed on the work computer; this should be stated in the posting or the offer, not discovered after accepting.</p>
<p><b>Skills proof, where the job calls for it.</b> Typing speed for data entry and transcription, a graded writing sample for content or copy roles, a basic accounting or spreadsheet test for bookkeeping, and a relevant certificate or license for occupations such as medical records or tutoring in a specific subject. Entry-level customer service, administrative, and sales roles — the largest single slice of entry-level remote postings — usually ask only for a high school diploma and some prior customer-service experience.</p>
<p><b>Sometimes a background check, or more.</b> Roles handling money, health information, or vulnerable people, including many bookkeeping, healthcare-adjacent, and tutoring-of-minors roles, commonly run a background check after a conditional offer, and some add a credit check, a basic cognitive or personality assessment, or a drug or medical screening depending on the field and the state. These are standard, and under the Fair Credit Reporting Act a background or credit check requires your written consent before it happens.</p>
<p><b>Nothing you pay for.</b> None of the above should ever cost the applicant money. A legitimate employer ships or reimburses required equipment; it does not ask for a kit fee, a training fee, or a deposit refunded out of a check you’re told to cash. That exact pattern — a check to deposit, then a request to send part of it back — is the single most common scam mechanism in Federal Trade Commission reports, and it shows up disguised as an “equipment” or “software license” requirement as often as anything else.</p>
<p class="src-note">iHire, State of Online Recruiting 2025 and 2026. Huntr, 2025 Annual Job Search Trends and Q1 2026 Job Search Trends Report. Greenhouse, 2026 Candidate AI Interview Report. Enhancv, 2026 AI Hiring Statistics. U.S. Citizenship and Immigration Services, Form I-9. Internal Revenue Service, Form W-4 and Form W-9. Federal Trade Commission, job-scam consumer guidance. Specific postings are referenced only as illustrative examples; none are current openings from Weekline.</p>
''',
        "apply.html",
        "Companion",
    )

    essay(
        "states.html",
        "States",
        "The floor changes at the state line",
        "U.S. minimum wages, pay-range posting rules, average earnings, and the status of contractor guidance.",
        "A national average and a federal minimum describe different maps. The higher rate, where one exists, is the one that applies.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>The federal minimum wage is still $7.25 an hour, unchanged since 24 July 2009.</li>
<li>The Department of Labor table dated 1 July 2026 lists 30 states and the District of Columbia above that floor.</li>
<li>A separate compilation, checked to 13 October 2026, found pay-range posting rules in 14 states and the District.</li>
<li>A contract label on a posting does not, by itself, decide legal status.</li>
</ul></div>
<h2>Two wage maps</h2>
<p>Employers covered by the Fair Labor Standards Act pay the highest of the federal, state, and local rates. On the 1 July 2026 consolidated table, Washington was $17.13, California $16.90, New York City and Long Island $17.00, upstate New York $16.00, and Connecticut $16.94. Illinois, Maryland, Massachusetts, Missouri, Nebraska, and Delaware were listed at $15.00. Thirteen states matched $7.25, including Texas and Pennsylvania. Seven had no state minimum or a lower one, so the federal $7.25 still applies. City rates can sit above the state and are not in that table.</p>
<p>Florida was listed at $14.00 on the July table. A state notice had said the rate would rise to $15 on 30 September 2026. The July table predates that step, so this page does not treat $15 as confirmed by a later federal table. The District of Columbia row on the same Labor Department page says $18.40, while a note on the page says $17.50. The District’s own office is the place to settle that figure.</p>
<h2>What the averages say, and what an ad says</h2>
<p>In September 2026, preliminary and seasonally adjusted, average hourly earnings for all private employees were $37.81 and average weekly earnings were $1,300.66, at 34.4 hours. Retail trade averaged $26.38 an hour, or $807.23 a week. Leisure and hospitality averaged $23.90 an hour, or $609.45 a week. The May 2025 median for customer service representatives was $21.53 an hour, or $44,770 a year. The lowest 10% of that occupation earned under $15.27, and the highest 10% over $30.57. Entry-level remote call-center ads have been clustering near $15 to $17, which is the bottom of that range, not the private-economy average.</p>
<h2>Where a posting has to show a range</h2>
<p>A compilation of official pages, current as of 13 October 2026, found pay-range rules in Colorado (1 January 2021), New York City (1 November 2022), California and Washington (1 January 2023), New York State (17 September 2023), Hawaii (1 January 2024), the District of Columbia (30 June 2024), Maryland (1 October 2024), Illinois and Minnesota (1 January 2025), New Jersey (1 June 2025), Vermont (1 July 2025), Massachusetts (29 October 2025), Virginia (1 July 2026), Maine (29 July 2026), and Connecticut (1 October 2026). Thresholds differ by employer size and by whether the work is done in the state. In that compiler’s own postings on 1 November 2026, 69.5% stated a range inside those jurisdictions and 32.6% stated one elsewhere. This list is a map of public rules, not legal advice.</p>
<h2 id="status">Employee or contractor, still unsettled on paper</h2>
<p>Some online offers are written as independent-contractor work. The comparison with a job includes overtime, unemployment insurance, and who pays the employer share of Social Security. On 26 February 2026 the Department of Labor proposed to replace its 2024 classification guidance with a modified economic-reality test. Comments closed on 28 April 2026. On 28 October 2026 that final rule had cleared White House review, and as of this review date it had no publication date. Until publication, the 2024 guidance is what the Department has published. Courts apply their own case law. State tests, including California’s ABC test, are separate. This is a status note, not a classification of any engagement.</p>
<p class="src-note">U.S. Department of Labor, consolidated minimum-wage table dated 1 July 2026. Bureau of Labor Statistics, table B-3, September 2026, and the Occupational Outlook Handbook, May 2025. LAYIQ compilation of official pay-transparency pages, 13 October 2026. Federal Register, 27 February 2026. OIRA record RIN 1235-AA46, concluded 28 October 2026.</p>
''',
        "states.html",
    )

    essay(
        "arrangements.html",
        "Definitions",
        "Place, delivery, and hours",
        "A longer explanation of remote, online, and flexible work for readers in the United States.",
        "The three words often appear in the same sentence. A reader can still take them one at a time.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>Remote is the place.</li>
<li>Online is the way the work travels.</li>
<li>Flexible is the schedule.</li>
<li>A week can use one of them, or all three, and still have set hours.</li>
</ul></div>
<h2>Remote is the place</h2>
<p>Remote work happens away from the usual workplace. Home is the place most people mean. A hybrid week mixes the two: some days at home, some days at the workplace. In August 2026, about 12 in 100 full-time employees worked only from home, about 27 in 100 split the week, and about 61 in 100 worked only at the workplace.</p>
<p>Schooling changes how common home days are. In the September 2026 survey week, about 38 in 100 people with a bachelor’s degree did at least some paid work at home, compared with about 8 in 100 people whose schooling stopped at high school.</p>
<h2>Online is the way the work travels</h2>
<p>Online work is done or turned in over the internet. A hospital worker updating records, a tutor on a video call, and a person answering calls from a spare room are all doing online work. Their weeks are still different. One may have a set pile of records. One may choose evenings. One may have a shift that starts and ends at a set time. The word “online” does not choose among those weeks.</p>
<h2>Flexible is the schedule</h2>
<p>Flexible means some say over when the work happens. Part-time is a different idea. In the federal household survey, part-time means fewer than 35 hours. A short Monday shift that happens every week is regular. It is not the same as a week whose hours follow a client, or a week a person shapes around school.</p>
<p>A national study of workers, taken from January to February 2025, found that 62 in 100 did not have a predictable schedule they could control. So when people say “flexible,” it helps to ask how much of the clock they actually choose. Some employers offer a limited version of that choice: in 2026, 45 in 100 employers in one benefits survey offered flextime inside core hours, and 10 in 100 offered a four-day week.</p>
<p class="src-note">Survey of Working Arrangements and Attitudes, August 2026. Bureau of Labor Statistics, September 2026. American Job Quality Study, Jobs for the Future and Gallup, early 2025. SHRM employee benefits survey, 2026.</p>
''',
        "notes.html",
    )

    essay(
        "occupations.html",
        "Occupations",
        "Which occupations the remote shelf actually holds",
        "Occupations that appear in U.S. remote and flexible postings, with public median pay.",
        "The shelf mixes a few large occupations. Their pay, training, and schedules are not the same, and a median is for the occupation in every setting.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>Customer service, sales support, and admin dominate entry-level remote postings in one large database.</li>
<li>Bookkeeping and medical records sit higher, and usually ask for some training.</li>
<li>Tutoring and some data-entry shifts are the small-hours end.</li>
<li>Software is a high median and a high remote-mention share. It is a different shelf.</li>
</ul></div>
<h2>High-school entry, often an assigned shift</h2>
<p>FlexJobs counted its own listings from 1 January to 1 May 2026. Customer service, administrative work, and sales led entry-level remote hiring, and each grew more than 30% in that slice. The titles posted most often were sales development representative, customer service representative, and business development representative. Employers with the most entry-level remote postings in that database included Mass General Brigham, Thermo Fisher Scientific, HCA, the State of North Carolina, T-Mobile, IQVIA, Stride, Raymond James, Centene, and Toast.</p>
<p>The May 2025 median for customer service representatives was $21.53 an hour, or $44,770 a year. About 2.67 million people held the job. Employment is projected to decline 5% from 2025 to 2035, with about 289,500 openings a year from people who leave. Usual entry is a high school diploma. Home-based ads at the entry level have clustered near $15 to $17 an hour, with a set shift. That is the bottom of the occupation’s range. The all-occupations median cited on that handbook page was $24.51 an hour.</p>
<h2>A certificate or a degree</h2>
<p>Bookkeeping, accounting, and auditing clerks had a May 2025 median of $24.36 an hour, or $50,670 a year. Usual entry is some college. The outlook is a 6% decline. Medical records specialists had a median of $24.59 an hour, or $51,140. Usual entry is a postsecondary certificate, the outlook is 8% growth, and openings are about 14,000 a year. Software developers had a median of $135,980. Quality-assurance analysts and testers were $104,300, and the combined handbook quick fact was $134,040. Usual entry is a bachelor’s degree. The combined group’s outlook is 10% growth, on 1,905,400 jobs. Interpreters and translators had a median of $28.93 an hour, or $60,170, with a bachelor’s degree the usual entry and a 2% outlook. Bilingual phone support is a different, often lower-paid, use of a second language.</p>
<h2>Hours that stay small</h2>
<p>Tutors numbered 175,070 in the May 2025 wage table. Mean hourly pay was $23.10 and mean annual pay was $48,050. The median hourly wage was $20.84. The table does not print a median annual figure. Online tutoring ads around $18 to $22.50 an hour, for evening hours and a cap near 25 hours a week, sit close to that hourly median. Data-entry ads around $16 an hour, including a part-time Monday shift, are a second-income shape. A contract virtual-assistant ad at $22 an hour follows a client’s calendar, and the worker handles their own taxes. Delivery and rideshare are local. In the Bankrate side-hustle survey they were a small share of the named types.</p>
<p class="src-note">FlexJobs, entry-level remote jobs, updated 28 May 2026. Bureau of Labor Statistics, Occupational Outlook Handbook, May 2025, and OEWS table 1 for tutors. Named ads were reviewed in September and October 2026 as examples of arrangements. They are not openings from Weekline.</p>
''',
        "notes.html",
    )

    essay(
        "side-work.html",
        "Second income",
        "Two jobs, and the wider side-work surveys",
        "How the U.S. multiple-job count differs from side-hustle surveys.",
        "A second paycheck is common in conversation and less common in the official job count. The gap is the definition.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>The official multiple-job rate was 5.5% in September 2026.</li>
<li>A side-hustle survey that year found 27% of adults, on a wider definition, with a median of $200 a month.</li>
<li>A still wider question, any side income in the past year, produced 47% in a different survey.</li>
<li>The three figures do not combine into one rate.</li>
</ul></div>
<h2>The official count</h2>
<p>In September 2026, not seasonally adjusted, 9.00 million people held more than one job. That was 5.5% of employed people. Men were at 4.7% and women at 6.4%. Women ages 20 to 24 were at 9.0%. The usual pattern was a full-time main job plus a part-time second job: 5.199 million people. Both jobs part time accounted for 2.250 million. Two full-time jobs were 421,000. Hours that vary accounted for 1.066 million.</p>
<h2>Side work, defined more loosely</h2>
<p>Bankrate’s YouGov survey of 2–4 June 2025, with 2,616 adults and 699 people who had a side hustle, defined the activity as extra money beyond the main source of income. Twenty-seven percent said they had one, down from 36% in 2024 and 39% in 2023. Gen Z ages 18 to 28 were at 34%, millennials 29 to 44 at 31%, Gen X 45 to 60 at 23%, and boomers 61 to 79 at 22%. The average was $885 a month and the median was $200. Fifty-eight percent earned more than $100, 25% more than $500, 14% more than $1,000, and 28% earned $1 to $50. Uses, for at least some of the money, were discretionary spending 41%, living expenses 35%, saving 28%, and debt 20%. Twenty-nine percent thought they would always need one. Sixteen percent wanted it to become the main income, and 21% of Gen Z side hustlers said that.</p>
<p>Types, among people who had one: none of 12 listed types 43%, online sales 15%, professional services 14%, food delivery 9%, crafts 9%, pet care 7%, teaching 6%, landscaping 4%, childcare 4%, healthcare 4%, fitness 3%, rideshare 3%, and home rental 2%.</p>
<p>Intuit QuickBooks surveyed 3,000 adults in December 2025. Forty-seven percent said they had earned any side income in the past 12 months, 56% of Gen Z and 54% of millennials. Among earners, online selling was 30% and freelancing 22%. The write-up’s monthly and hourly figures are a self-report ratio, not a wage, and they are not comparable to the Bureau of Labor Statistics average of $37.81. Forty percent said they planned to start a business or a side hustle in 2026. That survey and the Bankrate survey asked different questions. Neither replaces the 5.5% count of people who hold two jobs.</p>
<p class="src-note">Bureau of Labor Statistics, September 2026, multiple jobholders, not seasonally adjusted. Bankrate press release on the 2–4 June 2025 YouGov survey. Intuit QuickBooks, December 2025. A vendor survey of hourly workers in North America is a different population and is not used here as a national rate.</p>
''',
        "notes.html",
    )

    notes = [
        ("search", "Search", "search.html", "Where, how, and when the search actually happens", "The channels people use, the steps a search runs through, and when remote postings are scarce or plentiful."),
        ("apply", "Apply", "apply.html", "How the application runs, and what it actually asks for", "The form, the screening questions, and the documents, equipment, and checks employers commonly require."),
        ("start", "Start", "start.html", "The starter’s companion", "What a first week of remote, online, or independent work usually involves."),
        ("words", "Words", "arrangements.html", "Place, delivery, and hours", "Remote, online, and flexible name different parts of a week. A home shift can still be assigned."),
        ("days", "Where", "record.html", "Where paid days are spent", "The share of paid days at home, and who teleworked in one survey week."),
        ("hours", "When", "side-work.html", "A second, smaller part of the week", "5.5% of employed people held two jobs. Side-work surveys use a wider definition."),
    ]
    items = []
    for cat, label, href, title, dek in notes:
        items.append(
            f'<li class="post" data-cat="{cat}"><a href="{href}"><span class="cat">{label}</span>'
            f'<span><strong>{title}</strong><span class="dek">{dek}</span></span></a></li>'
        )
    page(
        "notes.html",
        f"Notes · {BRAND}",
        "Notes in the Weekline record on U.S. remote, online, and flexible work.",
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Notes</p><h1>Every guide, in one place</h1>
<p class="lede">The longer notes behind Search, Apply, Requirements, and Pay &amp; hours, each with sources.</p></div></div>
<section class="band"><div class="wrap">
<div class="filters" role="group" aria-label="Filter notes">
<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>
<button class="chip" type="button" data-filter="search" aria-pressed="false">Search</button>
<button class="chip" type="button" data-filter="apply" aria-pressed="false">Apply</button>
<button class="chip" type="button" data-filter="start" aria-pressed="false">Start</button>
<button class="chip" type="button" data-filter="words" aria-pressed="false">Words</button>
<button class="chip" type="button" data-filter="days" aria-pressed="false">Where</button>
<button class="chip" type="button" data-filter="hours" aria-pressed="false">When</button>
</div>
<ul class="note-list">{"".join(items)}</ul>
</div></section>''',
        "notes.html",
    )

    page(
        "terms.html",
        f"Terms · {BRAND}",
        "Definitions used in the Weekline record of U.S. remote and flexible work.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Terms</p><h1>Words the counts depend on</h1>
<p class="lede">Short definitions for the record. Legal duties depend on the statute, the state, and the facts.</p></div></div>
<section><div class="wrap terms">
<label class="for-search" for="glossary-search">Search terms</label>
<input id="glossary-search" class="search" type="search" placeholder="Try remote, W-2, or minimum wage">
<p id="glossary-empty" class="notice" hidden>No matching term.</p>
<dl>
<div class="term"><dt>Remote</dt><dd>Work done away from the employer’s usual workplace. The posting may still limit the states or the time zones.</dd></div>
<div class="term"><dt>Hybrid</dt><dd>Some days remote and some days at a set site. Regular office days mean the job is not fully remote.</dd></div>
<div class="term"><dt>Online work</dt><dd>Work done or delivered over the internet. The word does not settle the place, the hours, or the employment status.</dd></div>
<div class="term"><dt>Flexible schedule</dt><dd>Some choice over hours. The choice can be small. An assigned shift worked from home is still an assigned shift.</dd></div>
<div class="term"><dt>Part-time</dt><dd>In Bureau of Labor Statistics household data, fewer than 35 hours a week. A count of hours, not a type of pay.</dd></div>
<div class="term"><dt>Multiple jobholder</dt><dd>A person the Bureau of Labor Statistics counts as holding more than one job. In September 2026 that was 5.5% of employed people.</dd></div>
<div class="term"><dt>Side hustle</dt><dd>A survey term for extra money beside a main source of income. Wider than the official count of second jobs. Definitions differ by survey.</dd></div>
<div class="term"><dt>W-2 employee</dt><dd>A worker whose employer withholds income tax and pays the employer share of Social Security and Medicare. The label on a posting is not the legal test.</dd></div>
<div class="term"><dt>1099 contractor</dt><dd>A worker paid without employee withholding. Status depends on the economic reality of the work and on state rules.</dd></div>
<div class="term"><dt>Minimum wage</dt><dd>The lowest hourly rate the law requires. The federal rate is $7.25. A higher state or city rate controls when it applies.</dd></div>
<div class="term"><dt>Median wage</dt><dd>The point where half of workers in an occupation earn more and half earn less. Not the wage on one posting, and not the average.</dd></div>
<div class="term"><dt>Telework</dt><dd>In the Current Population Survey, any work at home for pay during the reference week, including people who did this for only some hours.</dd></div>
<div class="term"><dt>Pay range</dt><dd>The wage or salary stated on a posting. Some states require a range for covered employers. The statute is state-specific.</dd></div>
<div class="term"><dt>Task scam</dt><dd>A fraud pattern in Federal Trade Commission reports: simple online tasks, a small early payout, then a demand to deposit money.</dd></div>
</dl>
</div></section>''',
        "about.html",
    )

    page(
        "questions.html",
        f"Questions · {BRAND}",
        "Questions about what the Weekline record covers.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Questions</p><h1>What this record is</h1>
<p class="lede">Answers about the publication. They are not answers about a particular job.</p></div></div>
<section><div class="wrap article">
<details><summary>Does Weekline list jobs or take applications?</summary>
<p>No. The pages explain remote, online, and flexible work. Hiring stays between a person and an employer or a client.</p></details>
<details><summary>Is this a guide to choosing an arrangement?</summary>
<p>No. The pages do not tell a reader which arrangement suits their hours, their household, or their training. They separate facts that are easy to treat as one fact.</p></details>
<details><summary>Is this legal, tax, or employment advice?</summary>
<p>No. Wage rules, tax withholding, and worker classification depend on the facts and on federal, state, and local law. Each note names the office that publishes the figure.</p></details>
<details><summary>Why do the percentages disagree?</summary>
<p>They measure different things. A share of paid days and a share of people who teleworked in one week are different counts. <a href="record.html">Where the paid days are spent</a> keeps them apart.</p></details>
<details><summary>Does remote work mean the worker chooses the hours?</summary>
<p>No. Many home-based customer-service roles assign a shift. Hours are a separate fact. <a href="arrangements.html">Place, delivery, and hours</a>.</p></details>
<details><summary>How current are the figures?</summary>
<p>Each note has a review date and names its sources. Labor figures move. The agency page is the place to confirm a number.</p></details>
</div></section>''',
        "about.html",
    )

    page(
        "about.html",
        f"About · {BRAND}",
        "Weekline publishes general information on U.S. careers, pay, training, and flexible or extra-income work.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">About</p><h1>What Weekline is, and what it isn’t.</h1>
<p class="lede">Weekline is a set of guides on U.S. careers, pay, training, flexible work, and extra income. It is general information you can read before you compare a job, a program, or a side gig — not a place to apply.</p></div></div>
<section><div class="wrap article">
<h2>What you’ll find here</h2>
<p>The <a href="career-guides.html">career guides</a> cover where jobs are projected to grow, how to look up pay near you, and how to spot a fake listing. <a href="work-options.html">Work options</a> compares remote, hybrid, part-time, freelance, and gig arrangements, and what to ask before you accept one. <a href="extra-income.html">Extra income</a> looks at how a second job or side gig can differ in hours, costs, and how steadily the work comes in.</p>
<p>When a page uses a figure, it names the source — usually the Bureau of Labor Statistics, CareerOneStop, Apprenticeship.gov, the Federal Reserve, or the Federal Trade Commission. Figures can change, and pay and requirements vary by employer and location, so check the date and confirm details with the original source or the employer.</p>

<h2>Who it’s for</h2>
<p>These guides are for people comparing a career move, a training path, or a more flexible schedule, including a first job, a change of field, or extra income on the side. You do not need a specialist vocabulary to read them.</p>

<h2>What Weekline does not do</h2>
<p>Weekline is an independent publisher. It is not an employer, a staffing agency, or a job board. It does not list openings, take applications, screen employers, or place candidates. Reading a page does not sign you up for anything.</p>
<p>The content is not legal, tax, financial, or employment advice, and it does not tell you which job or program to choose. A question about a specific role belongs with that employer. For a topic you’d like us to cover next, use the <a href="contact.html">contact form</a>.</p>
</div></section>''',
        "about.html",
    )

    page(
        "corrections.html",
        f"Corrections · {BRAND}",
        "How a figure in the Weekline record is checked, and what the site does not collect.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Corrections</p><h1>The source on the page is the record.</h1>
<p class="lede">Weekline does not collect résumés and does not keep a mailbox for applications.</p></div></div>
<section class="band"><div class="wrap split">
<div>
<h2>If a figure looks wrong</h2>
<p>Each note names its source and the date it was reviewed. The agency page is the record to check. A note can lag a release. Where a federal table and a note on the same page disagree, as with the District of Columbia minimum on the 1 July 2026 Labor Department page, the page says so instead of picking a number.</p>
<h2>If a posting looks wrong</h2>
<p>The employer named on the posting is the party that can explain the hours, the pay, and the status. A posting with no employer name matches a pattern in Federal Trade Commission consumer guidance. Reports can be filed at ReportFraud.ftc.gov.</p>
</div>
<div>
<div class="notice"><h2>Nothing is stored here</h2>
<p>This website does not run an application form and does not keep a mailing list. Reading the record does not create an employment relationship.</p></div>
</div>
</div></section>''',
        "about.html",
    )

    page(
        "privacy-policy/index.html",
        f"Privacy · {BRAND}",
        "What the Weekline site does and does not collect.",
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Privacy</p><h1>Privacy</h1>
<p class="lede">How a visit to this site is handled. Updated {REVIEWED}.</p></div></div>
<section><div class="wrap article">
<h2>What the site is for</h2>
<p>Weekline publishes general information about U.S. careers, pay, training, and flexible or extra-income work. It does not ask readers to create an account, upload a résumé, or submit a job application.</p>
<h2>What a visitor may send</h2>
<p>The contact form on the homepage and the Contact page lets you send a topic suggestion. That form asks for your name, email address, an optional phone number, and your message. Submitting it opens a message in your own email app, addressed to Weekline. Weekline uses those details only to reply to the suggestion. It does not use the form to take job applications, and it does not add visitors to a mailing list.</p>
<h2>What the site does not collect</h2>
<p>Pages do not ask for a Social Security number, a date of birth, bank details, or payment information.</p>
<h2>Fonts</h2>
<p>Pages load Inter from Google Fonts. A visit can send the usual technical request, including an IP address, to that service. A browser setting that blocks third-party fonts leaves the words of the site in the fallback typefaces.</p>
<h2>Local features</h2>
<p>The note filter, the term search, and the mobile menu run in the browser. They do not send what a reader types to Weekline.</p>
<h2>Links</h2>
<p>Notes link to public agencies and to reporting on those figures. Those sites have their own practices. A link is a citation.</p>
</div></section>''',
        "",
        kind="special",
    )

    page(
        "thank-you/index.html",
        f"Thank you · {BRAND}",
        "Thanks for sending a topic suggestion to Weekline.",
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Thank you</p><h1>Thanks for sending your suggestion.</h1>
<p class="lede">We read topic suggestions as we plan future guides.</p></div></div>
<section><div class="wrap article">
<p>{BRAND} does not take job applications or list openings. If you have a question about a specific employer or role, contact that employer directly.</p>
<p><a class="btn btn-primary" href="index.html">Back to the homepage</a></p>
</div></section>''',
        "",
        kind="special",
    )

    page(
        "disclaimer.html",
        f"Disclaimer · {BRAND}",
        "Limits on the Weekline record of work in the United States.",
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Scope</p><h1>Disclaimer</h1>
<p class="lede">Limits that apply to every page. Updated {REVIEWED}.</p></div></div>
<section><div class="wrap article">
<h2>A record for reading</h2>
<p>Weekline publishes general information about online, remote, and flexible work in the United States. The content does not consider a particular reader’s circumstances and does not recommend an arrangement.</p>
<h2>No employment service</h2>
<p>Weekline is not an employer, a job board, or an employment agency. It does not publish openings, receive applications, or introduce candidates. Reading the site does not create an employment, recruitment, or advisory relationship.</p>
<h2>No professional advice</h2>
<p>The content is not legal, tax, financial, or employment advice. Minimum wages, payroll rules, and worker classification vary by law and by facts. A decision that depends on those rules belongs with the responsible agency or a qualified professional.</p>
<h2>No offer and no earnings promise</h2>
<p>Nothing on the site is a job offer or a promise of earnings. Occupation medians and third-party ads illustrate the published record. They are not vacancies from Weekline, and ads expire.</p>
<h2>Figures move</h2>
<p>Surveys, wage tables, and proposed regulations change. Each note names a review date and a source. Readers should confirm a figure with the cited source before relying on it.</p>
<h2>External sites</h2>
<p>Links exist so a reader can reach the original source. Weekline does not control those sites.</p>
</div></section>''',
        "about.html",
    )

    page(
        "career-guides.html",
        f"Career Guides · {BRAND}",
        "Career paths, pay lookups, and job-search safety for U.S. readers, with the source behind every figure.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Career Guides</p><h1>Find out what jobs pay and what it takes to qualify.</h1>
<p class="lede">Explore selected roles with strong projected growth, compare entry requirements, and learn how to check demand and pay where you live.</p></div></div>

<section><div class="wrap article">
<h2 id="job-outlook">Job outlook: where U.S. jobs are projected to grow</h2>
<p>The U.S. Bureau of Labor Statistics projects the economy will add 5.9 million jobs from 2025 to 2035, growing total employment from about 170.3 million to 176.2 million (3.5%). Growth is not even across fields. Healthcare support is projected to grow fastest among major occupational groups (+13.3%), followed by healthcare practitioners and technical occupations (+8.0%); together these two groups account for close to a third of all new jobs through 2035. Computer and mathematical occupations rank fifth (+7.3%), driven largely by AI-related roles. Among individual occupations, nurse practitioners (+41%) and data scientists (+34.6%) are projected to grow fastest.</p>
<p>These are national projections, not a guarantee for any specific job or location. Once a role catches your interest, check current pay and openings in your own area using a wage-lookup tool, since both can differ a great deal by region.</p>
<p class="src-note">Source: BLS Employment Projections, 2025–2035 news release and Occupational Outlook Handbook.</p>

<h2 id="pay">Pay: how to find out what a job pays near you</h2>
<p>A posted salary range or hourly rate is easier to judge once you can compare it with your local market. CareerOneStop's wage-lookup tool, built on BLS Occupational Employment and Wage Statistics, breaks pay down by occupation and by state or metro area, which can differ substantially from a national median. Checking the local figure before accepting, or before deciding whether a posted range looks fair, is a reasonable step regardless of the role.</p>
<p class="src-note">Source: CareerOneStop wage tools, built on BLS Occupational Employment and Wage Statistics.</p>

<h2>Skills and training</h2>
<p>Comparing credential paths side by side — how long each takes, what it costs, and what it leads to — is covered in the <a href="skills-training.html">Skills &amp; Training guide</a>, including where a paid Registered Apprenticeship fits.</p>

<h2 id="career-change">Career change: using experience you already have</h2>
<p>Moving fields doesn’t always mean starting over. Start by listing what you actually did in past roles — the tasks, tools, and outcomes, not just job titles — and compare that list against postings in the field you’re considering. Many roles share transferable skills (scheduling, customer communication, basic data work, project coordination) even when the job titles look unrelated. Where a gap remains, the <a href="skills-training.html">Skills &amp; Training guide</a> covers common ways to close it.</p>

<h2 id="signs">Job search safety: how to spot a fake remote job listing</h2>
<p>Fake and "ghost" postings are common enough that most job seekers now say they encounter one. A few checks reduce the risk before you spend time on an application:</p>
<ul class="steps">
<li>Look up the role on the employer’s own careers page, not just the board where you found it. A real opening is usually listed in both places.</li>
<li>Treat any request for payment — a fee, a "starter kit," training costs, or a check to deposit and partly send back — as a stop sign. Legitimate employers do not charge applicants.</li>
<li>Be cautious about sharing a Social Security number, bank details, or a copy of an ID before an offer is made in writing from a named, verifiable employer.</li>
<li>Be skeptical of contact that happens only through a messaging app rather than a company email address or phone line.</li>
</ul>
<p class="src-note">Source: Federal Trade Commission job-scam consumer guidance.</p>
</div></section>''',
        "career-guides.html",
    )

    page(
        "skills-training.html",
        f"Skills &amp; Training · {BRAND}",
        "Comparing apprenticeships, certificates, and degrees for U.S. career paths, with the source behind every figure.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Skills &amp; Training</p><h1>Apprenticeship, certificate, or degree?</h1>
<p class="lede">Start with the job you want, then compare how long each path to it takes, what it costs, and what credential you end up with.</p></div></div>

<section><div class="wrap article">
<div class="ready-box"><div class="ready-grid">
<div><h4>Registered Apprenticeship</h4><ul><li>Paid, on-the-job training combined with classroom instruction</li><li>Typically 1–4 years depending on the occupation</li><li>Ends in a nationally recognized credential</li></ul></div>
<div><h4>Certificate or license</h4><ul><li>Weeks to about a year, often at a community college or trade school</li><li>Usually the fastest, lowest-cost path to an entry-level role in a specific field</li><li>May need renewal or continuing education</li></ul></div>
<div><h4>Associate degree</h4><ul><li>About 2 years at a community college</li><li>Often required for technical and allied-health roles</li><li>Can sometimes transfer toward a bachelor’s degree later</li></ul></div>
<div><h4>Bachelor’s degree</h4><ul><li>Typically 4 years</li><li>Still commonly required or preferred for many professional and managerial roles</li><li>The largest cost and time commitment of the four</li></ul></div>
</div></div>
<p>Which path makes sense depends heavily on the specific occupation — none of these four is the universally "right" choice. The U.S. Department of Labor's Apprenticeship.gov is a reasonable starting point for comparing registered, paid apprenticeships by field and location, since availability varies by industry and by state.</p>
<p>This is general information about how these paths typically work, not a recommendation for any individual's circumstances. Program cost, financial aid eligibility, and licensing requirements vary by state and by school; confirm current figures directly with the program before enrolling.</p>
<p class="src-note">Source: Apprenticeship.gov career seeker resources, U.S. Department of Labor.</p>
</div></section>''',
        "skills-training.html",
    )

    page(
        "work-options.html",
        f"Work Options · {BRAND}",
        "Comparing part-time, remote, hybrid, flexible, freelance, and gig work in the United States.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Work Options</p><h1>Remote, hybrid, or flexible hours?</h1>
<p class="lede">A job can offer flexibility in where you work, when you work, or both. Here is what each common arrangement usually means, and what to ask before you accept one.</p></div></div>

<section><div class="wrap article">
<p>In 2025, 35% of employed people did some or all of their work at home on days they worked, while 70% did some or all of their work at their workplace; these overlap because many people split time between the two. "Flexible" does not describe one single arrangement — it can mean where you work, when you work, or both, and the specifics are worth confirming before you accept an offer.</p>
<div class="opts-table-wrap"><table class="opts-table">
<thead><tr><th>Work option</th><th>What to check</th></tr></thead>
<tbody>
<tr><td>Part-time jobs</td><td>Expected weekly hours, shift changes, and which benefits are available.</td></tr>
<tr><td>Remote jobs</td><td>Eligible states, time zone requirements, and whether travel is expected.</td></tr>
<tr><td>Hybrid jobs</td><td>Required office days, commute time, and who sets the schedule.</td></tr>
<tr><td>Flexible schedules</td><td>Required hours, how far ahead shifts are posted, and whether you can change your availability.</td></tr>
<tr><td>Freelance work</td><td>Project scope, payment terms, and the time it takes to find clients.</td></tr>
<tr><td>App-based gigs</td><td>Pay per task, unpaid waiting time, and expenses such as mileage or supplies.</td></tr>
</tbody>
</table></div>
<p class="src-note">Source: BLS American Time Use Survey, 2025 annual averages.</p>

<h2 id="practical">Practical guides: what to ask before you apply or accept an offer</h2>
<h3>How to ask for a flexible schedule</h3>
<p>Put together a short, written proposal: the schedule you’re asking for, how you’ll cover your responsibilities during that schedule, and a date when you and your manager will check in on how it’s working. A concrete plan is easier to say yes to than an open-ended request.</p>
<h3>Employee or independent contractor?</h3>
<p>Before accepting, ask how you’ll be paid, who covers equipment and work-related expenses, and which benefits, if any, come with the arrangement. Which tax form you’re asked to complete is a reliable signal: a W-4 points to employee status with taxes withheld from each paycheck, while a W-9 points to independent-contractor status, where you’re responsible for your own tax payments.</p>
<h3>How to write a résumé for a remote role</h3>
<p>Show, with specific examples, how you’ve handled deadlines independently, communicated progress without in-person check-ins, and worked with people in different locations or time zones. Concrete outcomes read as more convincing than general claims of being "self-motivated" or "a strong communicator."</p>
</div></section>''',
        "work-options.html",
    )

    page(
        "extra-income.html",
        f"Extra Income · {BRAND}",
        "Comparing part-time shifts, freelance work, and app-based gigs as sources of extra income in the United States.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">Extra Income</p><h1>What could a second job or side gig add to your budget?</h1>
<p class="lede">A weekend shift, a freelance project, and app-based gig work can each bring in extra income. They also make very different demands on your time.</p></div></div>

<section><div class="wrap article">
<p>A part-time shift usually comes with set hours and a predictable hourly rate. A freelance project can pay more per hour of actual work, but also involves unpaid time finding clients, scoping work, and sending invoices. A delivery or rideshare gig offers flexible timing, but involves driving and vehicle expenses that reduce what you actually keep.</p>
<p>In September 2026, 9.0 million people (5.5% of employed people) held more than one job, most often a full-time main job plus a part-time second one. Separately, in a 2024 Federal Reserve survey of household finances, some gig workers said they'd struggle to make ends meet without that income, and many said they wanted more predictable pay — a reminder that "extra income" ranges from a planned supplement to a necessary part of covering expenses.</p>
<p>Before committing time to any option, it's worth comparing: how often you'll actually get paid, what the work costs you in gas, mileage, supplies, or your own tools, and how consistent the hours or assignments tend to be. If you need a predictable amount each month, ask directly about consistency before you commit rather than assuming it.</p>
<p class="reassure">This is general information about how these options typically work, not tax or financial advice. What you actually keep after taxes and expenses depends on your own situation — a tax professional can give figures specific to you.</p>
<p class="src-note">Sources: Bureau of Labor Statistics, multiple jobholders, September 2026 (not seasonally adjusted). Federal Reserve, Report on the Economic Well-Being of U.S. Households, 2024.</p>
</div></section>''',
        "extra-income.html",
    )

    page(
        "contact.html",
        f"Contact · {BRAND}",
        "Suggest a career, training, or work-arrangement topic for Weekline to cover.",
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Contact</p><h1>What would you like us to cover next?</h1>
<p class="lede">Have a question about a career path, a training program, or a type of work? Tell us what you're trying to figure out. Your suggestions help shape future guides.</p></div></div>
<section><div class="wrap article">
<form class="contact-form" id="contact-form" data-thanks="../thank-you/">
<div class="form-row">
<div><label for="c-name">Name</label><input id="c-name" name="name" type="text" autocomplete="name" required></div>
<div><label for="c-phone">Phone number</label><input id="c-phone" name="phone" type="tel" autocomplete="tel" placeholder="Optional"></div>
</div>
<div><label for="c-email">Email address</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="c-topic">Your question or topic suggestion</label><textarea id="c-topic" name="topic" required></textarea></div>
<button class="btn btn-primary" type="submit">Send a suggestion</button>
<p class="form-note">This opens a message in your own email app, addressed to {BRAND} — nothing is sent from this page directly.</p>
<p class="contact-confirm" role="status">Thanks for sending your suggestion.</p>
</form>
<p>{BRAND} does not take job applications or list openings through this form. For a question about a specific employer or role, contact that employer directly.</p>
</div></section>''',
        "contact.html",
    )

    stale = [p for p in ROOT.rglob("*.html") if p.relative_to(ROOT).as_posix() not in WRITTEN]
    for path in stale:
        path.unlink()
    for leftover in (ROOT / "css", ROOT / "js"):
        if leftover.exists():
            shutil.rmtree(leftover)
    print("rendered", len(WRITTEN), "pages; removed", len(stale))


if __name__ == "__main__":
    build()
