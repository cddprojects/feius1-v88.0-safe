#!/usr/bin/env python3
"""Render Weekline, a U.S. public record of remote and flexible work.

The pages share general information. They do not list jobs or take applications.
The editorial frame is the distance between published labor counts and the ad
market, which is a different job from a search guide.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "site"
THEME = "#161513"
REVIEWED = "3 November 2026"
BRAND = "Weekline"
FONT = (
    "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@"
    "0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,480&family=Public+Sans:"
    "ital,wght@0,400;0,600;0,700;1,400&display=swap"
)

NAV = [
    ("start.html", "Start"),
    ("states.html", "Pay &amp; hours"),
    ("gap.html", "Signs"),
    ("about.html", "About"),
]

WRITTEN = set()


def brand():
    return f'<a class="brand" href="index.html"><span aria-hidden="true"></span>{BRAND}</a>'


def nav_block(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''<nav aria-label="Primary"><ul id="nav-list">{"".join(items)}</ul></nav>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-list" aria-label="Open menu"><span class="bars" aria-hidden="true"></span></button>'''


def header(current, landing=False):
    links = nav_block(current)
    edition = "Front page" if landing else "For readers &middot; Not a job board"
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="mast">
<div class="wrap mast-top"><p>United States edition &middot; Reviewed {REVIEWED}</p><p class="edition">{edition}</p></div>
<div class="wrap nameplate">{brand()}
<p class="tagline">A reader's companion for remote, online, and independent work in the United States.</p></div>
<div class="nav-bar"><div class="wrap nav">
{links}
</div></div>
</header>'''


def footer():
    return f'''<footer class="site-footer"><div class="wrap foot">
<div><p class="brand-foot">{BRAND}</p>
<p>A reader's companion for remote, online, and independent work. Plain explanations of what usually happens once the work starts, for readers in the United States.</p></div>
<div><h2>Start here</h2><ul>
<li><a href="start.html">The starter's companion</a></li>
<li><a href="states.html">Pay &amp; hours</a></li>
<li><a href="gap.html">Signs of a real offer</a></li>
<li><a href="notes.html">All notes</a></li>
</ul></div>
<div><h2>Publisher</h2><ul>
<li><a href="about.html">About</a></li>
<li><a href="corrections.html">Corrections</a></li>
<li><a href="terms.html">Terms</a></li>
<li><a href="questions.html">Questions</a></li>
<li><a href="privacy.html">Privacy</a></li>
<li><a href="disclaimer.html">Disclaimer</a></li>
</ul></div>
</div>
<div class="wrap legal"><p>{BRAND} is a reader's companion. It explains remote, online, and independent work. It does not list jobs, screen employers, or give legal, tax, or employment advice.</p>
<p>&copy; 2026 {BRAND} &middot; United States</p></div>
</footer>
<script src="js/main.js"></script>'''


def page(filename, title, description, body, current, landing=False):
    body_class = ' class="landing"' if landing else ""
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
<link href="{FONT}" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body{body_class}>
{header(current, landing=landing)}
<main id="main">
{body}
</main>
{footer()}
<noscript><style>.reveal{{opacity:1;transform:none}}</style></noscript>
</body>
</html>
'''
    (ROOT / filename).write_text(html, encoding="utf-8")
    WRITTEN.add(filename)


def essay(filename, kicker, h1, description, lede, inner, current, section="Record"):
    body = f'''<div class="page-head"><div class="wrap"><p class="kicker">{kicker}</p><h1>{h1}</h1>
<p class="lede">{lede}</p></div></div>
<section><div class="wrap article">
<p class="byline">{BRAND} &middot; {section} &middot; Reviewed {REVIEWED}</p>
{inner}
<p class="back"><a href="notes.html">All notes</a></p>
</div></section>'''
    page(filename, f"{h1} · {BRAND}", description, body, current)


def build():
    page(
        "index.html",
        f"A reader's companion for remote, online, and independent work · {BRAND}",
        "Weekline is a reader's companion for remote, online, and independent work in the United States, in plain language.",
        '''
<section class="briefing"><div class="wrap">
<p class="kicker">Today’s briefing</p>
<ul class="briefing-list">
<li><strong>Online work still expects someone to answer.</strong> "Flexible hours" usually means some choice over when, not whether, you reply.</li>
<li><strong>Independent cuts both ways.</strong> No set hours also means no guaranteed hours, and no one else is covering a slow week.</li>
<li><strong>If the hours, the pay, and the employer’s name aren’t written down, that’s the finding, not a formality.</strong></li>
</ul>
</div></section>

<section class="lead"><div class="wrap lead-grid">
<div class="lead-main">
<p class="kicker">Start here</p>
<h1>What to know before your first remote, online, or independent job.</h1>
<p class="lede">Weekline is a reader’s companion, not a job board. These pages explain what usually happens once the work starts, so the first week has fewer surprises.</p>
<p>Most people trying remote, online, or independent work for the first time aren’t short on job titles. They’re short on a plain answer to a handful of ordinary questions: who actually checks on the work, whose clock decides the hours, what the pay should look like, and whether you’re an employee or on your own. The starter’s companion answers those in order, and the shorter notes below cover each piece in more depth.</p>
<p><a class="btn btn-fill" href="start.html">Read the starter’s companion &rarr;</a></p>
</div>
<aside class="lead-side">
<p class="kicker">In this edition</p>
<ul class="index-list">
<li><a href="start.html">The starter’s companion</a><span>What a first week of remote, online, or independent work usually involves.</span></li>
<li><a href="states.html">Pay &amp; hours</a><span>What a fair arrangement states, and how that changes by state.</span></li>
<li><a href="gap.html">Signs of a real offer</a><span>How job and task fraud actually shows up online.</span></li>
<li><a href="notes.html">All notes</a><span>The longer record, by topic, with sources.</span></li>
</ul>
</aside>
</div></section>

<section class="below-fold"><div class="wrap">
<p class="kicker">More in this edition</p>
<div class="fold-grid">
<article class="fold-story">
<p class="kicker">Pay &amp; hours</p>
<h3><a href="states.html">The floor changes at the state line.</a></h3>
<p>The federal minimum wage is still $7.25 an hour. Thirty states and the District of Columbia sit above it. Whether a posting has to show a pay range, by law, also depends on the state.</p>
<p class="more"><a href="states.html">Continue reading &rarr;</a></p>
</article>
<article class="fold-story">
<p class="kicker">Employee or contractor</p>
<h3><a href="states.html#status">What changes when the work is “independent.”</a></h3>
<p>No set hours, but no guaranteed hours either. A quick look at who pays for the slow weeks, who covers the employer’s share of Social Security, and why the label on a posting isn’t the legal test.</p>
<p class="more"><a href="states.html#status">Continue reading &rarr;</a></p>
</article>
<article class="fold-story">
<p class="kicker">Signs of a real offer</p>
<h3><a href="gap.html">What job fraud actually looks like online.</a></h3>
<p>Reported losses to job and task scams passed $500 million in 2024. An unnamed employer, any fee, or a check you’re told to deposit and partly send back are the patterns regulators keep flagging.</p>
<p class="more"><a href="gap.html">Continue reading &rarr;</a></p>
</article>
</div>
</div></section>

<section class="band"><div class="wrap">
<p class="notice">Weekline explains remote, online, and independent work. It does not list jobs, screen employers, or charge a fee. <a href="about.html">About Weekline</a>.</p>
</div></section>
''',
        "index.html",
        True,
    )

    essay(
        "start.html",
        "Start here",
        "The starter’s companion",
        "A plain-language guide to what remote, online, and independent work usually involves in the first weeks, for readers in the United States.",
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
<p>A real remote or online offer names the employer, states a pay figure or a clear range, and asks you to do the actual job, usually after a short interview, before any money changes hands in either direction. A scam, by the patterns in Federal Trade Commission guidance, tends to arrive as an unexpected text or chat, offers a vague title with no real duties, asks for a fee of any size, or has you deposit a check and send part of it back. Reported losses from job and employment scams passed half a billion dollars in 2024, so treating a “too easy” offer with some suspicion is not paranoia, it is proportionate. <a href="gap.html">The longer note on this</a> goes through the figures and the exact warning signs.</p>

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
        "gap.html",
        "The gap",
        "A thin shelf of ads, a thick pile of applications",
        "Where U.S. searches for remote and flexible work start, and how that shelf compares with applications.",
        "The looking and the hiring are both measurable. They do not describe the same volume.",
        '''
<div class="takeaways"><h2>In short</h2><ul>
<li>Searches still start on the large boards, then LinkedIn, Google, and employer sites.</li>
<li>Remote postings are roughly a tenth of ads, or less, and about a third of applications.</li>
<li>Insurance, law, math, and software mention remote or hybrid work far more often than retail, driving, or construction.</li>
<li>An unnamed remote offer that asks for a fee matches a pattern in Federal Trade Commission reports.</li>
</ul></div>
<h2>Where the looking starts</h2>
<p>iHire’s 2025 survey of 1,421 U.S. job seekers asked which resources they use. People could choose more than one. General job boards were 78.5%, LinkedIn 54.9%, niche boards 53.8%, company websites 45.0%, and search engines 41.6%. Networking was 32.7%, social media 15.7%, associations 15.4%, job fairs 12.7%, Craigslist 8.3%, and generative tools 6.9%. The prose summary of that survey rounded the board figure differently. The chart figure used here is 78.5%.</p>
<p>HireClix asked 1,000 adults in 2025 where a search starts. Indeed was 56%, LinkedIn 52% (up from 40% in 2023), Google 41%, and corporate career sites 40%. Fifty-seven percent said reviews on Glassdoor or Indeed affect the decision to apply. One survey asks about every channel. The other asks about the first stop. Both can be right.</p>
<p>On the employer side of the iHire survey, 529 respondents named referrals at 71.3%, the career page at 49.5%, LinkedIn at 46.1%, and social at 43.5%.</p>
<h2>The shelf, by occupation</h2>
<p>A secondary compilation of Indeed’s remote tracker, through 31 August 2026, put remote or hybrid mentions at 39.7% of insurance postings, 32.9% of legal, 32.4% of mathematical, 30.8% of software, 25.2% of marketing, and 20.8% of human resources. Construction was 3.9%, retail 1.9%, and driving 1.2%. Robert Half’s second-quarter 2026 professional tracker, from the same secondary source, was 87% on site, 10% hybrid, and 3% fully remote, for professional titles only.</p>
<p>Huntr’s 2025 file of roughly 599,000 tracked applications is a self-selected set, not a national placement rate. Response rates in that file were about 4.5% on Indeed, 3.1% on LinkedIn, 2.8% on ZipRecruiter, and 11.3% on Google Jobs.</p>
<h2>What the crowded ads have stated</h2>
<p>Entry-level remote titles in the FlexJobs database from 1 January to 1 May 2026 were led by customer service, administration, and sales. Named customer-service ads reviewed in autumn 2026, including Concentrix, TTEC, and Firstsource, clustered around $15 to $17 an hour, with an assigned shift, a high-school diploma, and prior customer-service experience. Some required a wired connection rather than a phone hotspot. Those ads expire. They show the shape of the shelf. They are not openings from Weekline.</p>
<p>In the iHire survey, 60.5% said a hiring timeline would make them more likely to apply, and 57.1% said a salary range would. An unnamed employer was an instant turnoff for 50.9%, and missing pay was an instant turnoff for 60.7%. Ghosting was the most common frustration, at 59.0%. Fake or already-filled postings were 39.3% in the findings chart. Finding remote work was named as a challenge by 24.0%.</p>
<h2>The fraud pattern in the public reports</h2>
<p>The Federal Trade Commission’s 10 March 2025 release said reports of job and employment-agency scams tripled from 2020 to 2024, and reported losses rose from $90 million to $501 million. A September 2025 FTC note put 2024 job-scam reports above 105,000 and losses above $513 million. Task scams were about 20,000 reports in the first half of 2024, against about 5,000 in all of 2023. The patterns in FTC consumer guidance are an unexpected text or chat, a remote title with no duties, any fee, a check the person is told to deposit and partly send back, and pay for liking or rating things followed by a demand to deposit money. Reports go to ReportFraud.ftc.gov.</p>
<p class="src-note">iHire, State of Online Recruiting 2025, chart figures. HireClix, 2025 Candidate Experience Survey. Indeed Hiring Lab. Business Insider, 19 October 2025. FlexJobs, entry-level remote guide, updated 28 May 2026. FTC press release, 10 March 2025, and FTC business blog, September 2025. Occupation shares for 31 August 2026 are a secondary compilation.</p>
''',
        "gap.html",
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
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Notes</p><h1>More on the three words</h1>
<p class="lede">Longer notes on where the work happens, how it is delivered, and when the hours fall.</p></div></div>
<section class="band"><div class="wrap">
<div class="filters" role="group" aria-label="Filter notes">
<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>
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
        "Weekline is a reader's companion for remote, online, and independent work in the United States.",
        '''<div class="page-head"><div class="wrap"><p class="kicker">About</p><h1>A companion, not a job board.</h1>
<p class="lede">Weekline explains what remote, online, and independent work actually involve, in plain language, before a reader says yes to any of them.</p></div></div>
<section class="band"><div class="wrap split">
<div>
<h2>What a reader can learn here</h2>
<p>Remote is the place. Online is how the work travels. Flexible is the schedule. Independent is who you answer to. The pages keep those apart using everyday situations, then point to the public count behind a figure when one is used.</p>
<p>Weekline is an independent publisher. It is not an employer, a staffing agency, or a job board. It does not list openings and it does not take applications. Reading a page does not sign anyone up for work.</p>
</div>
<div>
<div class="col"><h3>Who this is for</h3><p>Someone trying remote, online, or independent work for the first time, or anyone who wants a plain answer before taking an offer that sounds too easy.</p></div>
<div class="col" style="margin-top:1.25rem"><h3>The limit</h3><p>The pages do not choose a week for a reader, and they do not replace the Department of Labor, the Internal Revenue Service, a state labor office, or the Federal Trade Commission.</p></div>
</div>
</div></section>
<section class="band"><div class="wrap">
<p class="notice">Weekline publishes general information for reading. It has no application form. A question about a particular job belongs with the employer who offers it.</p>
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
        "privacy.html",
        f"Privacy · {BRAND}",
        "What the Weekline site does and does not collect.",
        f'''<div class="page-head"><div class="wrap"><p class="kicker">Privacy</p><h1>Privacy</h1>
<p class="lede">How a visit to this record is handled. Updated {REVIEWED}.</p></div></div>
<section><div class="wrap article">
<h2>What the site is for</h2>
<p>Weekline publishes a public record. It does not ask readers to create an account, upload a résumé, or submit an application.</p>
<h2>What the site does not collect</h2>
<p>There is no application form and no mailing list. Pages do not ask for a Social Security number, a date of birth, or payment details.</p>
<h2>Fonts</h2>
<p>Pages load Newsreader and Public Sans from Google Fonts. A visit can send the usual technical request, including an IP address, to that service. A browser setting that blocks third-party fonts leaves the words of the record in the fallback typefaces.</p>
<h2>Local features</h2>
<p>The note filter, the term search, and the mobile menu run in the browser. They do not send what a reader types to Weekline.</p>
<h2>Links</h2>
<p>Notes link to public agencies and to reporting on those figures. Those sites have their own practices. A link is a citation.</p>
</div></section>''',
        "about.html",
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

    stale = [p for p in ROOT.glob("*.html") if p.name not in WRITTEN]
    for path in stale:
        path.unlink()
    print("rendered", len(WRITTEN), "pages; removed", len(stale))


if __name__ == "__main__":
    build()
