"""Fetch public GitHub evidence and render a self-contained profile dashboard.

GITHUB_TOKEN is required for GraphQL. No third-party libraries are needed.
Run with --offline to regenerate from the checked-in snapshot.
"""
import argparse
from collections import Counter
from datetime import datetime, date, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
USER = 'sabekunnaher-17'
START = date(2025, 10, 25)
TZ = timezone(timedelta(hours=6))
COLORS = ['#53f7ad', '#73ddd0', '#b3f27b', '#54c790', '#b1edcf', '#68c5a4', '#d1f5df']


def api(path, payload=None):
    headers = {'User-Agent': 'antora-profile', 'Accept': 'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    req = urllib.request.Request('https://api.github.com' + path, headers=headers,
                                 data=json.dumps(payload).encode() if payload else None)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def collect():
    today = datetime.now(TZ).date()
    user = api('/users/' + USER)
    repos, page = [], 1
    while True:
        batch = api(f'/users/{USER}/repos?per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    evidence = []
    for repo in repos:
        evidence.append({k: repo[k] for k in ('name', 'html_url', 'language', 'fork', 'description', 'homepage')})
        evidence[-1]['languages'] = api(f'/repos/{USER}/{repo["name"]}/languages')
        evidence[-1]['head'] = api(f'/repos/{USER}/{repo["name"]}/commits/{repo["default_branch"]}')['sha']
    # GitHub limits contributionsCollection to one year per query.
    collections, cursor = [], START
    while cursor <= today:
        end = min(today, cursor + timedelta(days=364))
        query = '''query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){
          contributionsCollection(from:$from,to:$to){startedAt endedAt
          totalCommitContributions totalIssueContributions totalPullRequestContributions
          totalPullRequestReviewContributions totalRepositoryContributions restrictedContributionsCount
          contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'''
        data = api('/graphql', {'query': query, 'variables': {'login': USER,
            'from': f'{cursor}T00:00:00+06:00', 'to': f'{end}T23:59:59+06:00'}})
        if data.get('errors'):
            raise RuntimeError(data['errors'])
        collections.append(data['data']['user']['contributionsCollection'])
        cursor = end + timedelta(days=1)
    return {'source': 'GitHub REST v3 and GraphQL v4', 'retrieved_at': datetime.now(TZ).isoformat(),
            'start': str(START), 'end': str(today),
            'user': {k: user[k] for k in ('login', 'name', 'public_repos', 'followers', 'following', 'bio', 'blog')},
            'repositories': evidence, 'collections': collections}


def text(x, y, value, size=16, color='#adcbbb', weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'


def rect(x, y, w, h, fill='#10231c', rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'


def svg(name, height, body, title, description):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><linearGradient id="accent"><stop stop-color="#53f7ad"/><stop offset="1" stop-color="#73ddd0"/></linearGradient></defs>
<style>text{{font-family:Consolas,monospace}} .pulse{{animation:pulse 4s ease-in-out infinite}} .orbit{{transform-origin:802px 154px;animation:orbit 24s linear infinite}} .draw{{animation:draw 2s ease-out 1}} .rain{{animation:rain 12s linear infinite}} .packet{{animation:packet 10s ease-in-out infinite}} @keyframes rain{{from{{transform:translateY(-90px)}}to{{transform:translateY(150px)}}}} @keyframes packet{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(110px)}}}} @keyframes orbit{{to{{transform:rotate(360deg)}}}} @keyframes pulse{{50%{{opacity:.35}}}} @keyframes draw{{from{{opacity:.25}}to{{opacity:1}}}} @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{rect(0,0,960,height,'#081510',18)}{ambient(height)}{body}</svg>'''
    (ROOT / 'assets' / name).write_text(content, encoding='utf-8')


def ambient(height):
    """Decorative code streams and circuit traces, never fabricated telemetry."""
    result = '<g opacity=".12" stroke="#3c8a64" fill="none">'
    for x in range(24,960,48):
        result += f'<path d="M{x} 0V{height}"/>'
    for y in range(24,height,48):
        result += f'<path d="M0 {y}H960"/>'
    result += '</g><g opacity=".07" class="rain">'
    for i in range(11):
        for j in range(5):
            result += text(28+i*82,20+j*40,('0101','1010','0011')[(i+j)%3],12,'#53f7ad')
    return result+'</g>'


def repository_banner(filename, title, subtitle, label):
    body = text(36,38,'ANTORA / '+label,13,'#53f7ad',600)
    body += text(36,104,title,34,'#edfff5',700)
    body += text(36,142,subtitle,15,'#adcbbb')
    body += text(36,204,'> explore the source_',14,'#53f7ad')
    body += '<path d="M655 191H735L765 160H908M735 191L765 222H908" fill="none" stroke="#285c43" stroke-width="2"/>'
    body += '<g class="packet"><rect x="777" y="156" width="12" height="8" rx="2" fill="#53f7ad"/></g>'
    body += '<g class="pulse"><circle cx="908" cy="222" r="5" fill="#73ddd0"/></g>'
    svg(filename,250,body,title+' — animated repository banner','Decorative moving circuit packets and code rain. '+subtitle)


def render(data):
    (ROOT / 'assets').mkdir(exist_ok=True)
    days = {}
    for collection in data['collections']:
        for week in collection['contributionCalendar']['weeks']:
            for day in week['contributionDays']:
                if data['start'] <= day['date'] <= data['end']:
                    days[day['date']] = day['contributionCount']
    first, last = date.fromisoformat(data['start']), date.fromisoformat(data['end'])
    expected = [(first + timedelta(days=i)).isoformat() for i in range((last-first).days+1)]
    if sorted(days) != expected:
        raise ValueError('Contribution calendar is incomplete; refusing to replace verified assets')
    total = sum(days.values())
    active = sum(v > 0 for v in days.values())
    sums = {key: sum(c[key] for c in data['collections']) for key in (
        'totalCommitContributions', 'totalIssueContributions', 'totalPullRequestContributions',
        'totalPullRequestReviewContributions', 'totalRepositoryContributions')}
    hero = text(40,40,'ANTORA / FULL-STACK DEVELOPMENT',13,'#53f7ad',600)
    hero += text(40,106,'Sabekunnaher Antora',42,'#edfff5',700)
    hero += text(42,149,'Full-stack development / Testing / Research',18,'#b4d5c3')
    hero += text(42,190,'Secure applications. Tested workflows. Useful data.',17)
    hero += rect(40,219,552,39,'#153625',8) + text(56,245,'C# / ASP.NET Core / EF Core / SQL Server / Java',15,'#53f7ad')
    hero += text(42,295,'AIUB  /  DHAKA, BANGLADESH',13)
    for r in (55,85,115):
        hero += f'<circle cx="802" cy="154" r="{r}" fill="none" stroke="#285c43" stroke-width="1"/>'
    hero += '<path d="M690 154H914M802 42V266" stroke="#285c43"/>'
    hero += '<circle class="pulse" cx="802" cy="154" r="42" fill="#17472d"/>'
    hero += text(771,168,'SA',36,'#53f7ad',700)
    hero += '<g class="orbit"><circle cx="887" cy="154" r="7" fill="#73ddd0"/></g>'
    svg('header.svg',326,hero,'Sabekunnaher Antora — full-stack development','CSE student at AIUB. Full-stack development, software testing and research. ASP.NET Core, EF Core, SQL Server and Java.')

    focus = text(30,37,'PROFILE / ENGINEERING WITH PURPOSE',13,'#53f7ad',600)
    cards = [
        ('BUILD','Full-stack applications','ASP.NET Core + SQL Server','Web, desktop and graphics'),
        ('VERIFY','Software quality','Unit / integration / E2E','Secure, tested workflows'),
        ('COLLABORATE','Research + leadership','Four-member thesis team','Planning, analysis, review')]
    for i,(label,heading,line1,line2) in enumerate(cards):
        x = 24+i*312
        focus += rect(x,61,288,137)
        focus += text(x+17,89,label,12,COLORS[i],600)
        focus += text(x+17,121,heading,16,'#edfff5',600)
        focus += text(x+17,153,line1,13)
        focus += text(x+17,177,line2,13)
    svg('profile-focus.svg',222,focus,'Engineering, quality and collaboration',
        'Full-stack applications; unit, integration and end-to-end testing; research and thesis-team leadership, as described in the CV.')

    stats = text(30,37,'PUBLIC / GITHUB AT A GLANCE',13,'#53f7ad',600)
    stats += text(665,37,'PUBLIC DATA / '+data['end'],13)
    values = [(data['user']['public_repos'],'Public repositories'),(data['user']['followers'],'Followers'),
              (data['user']['following'],'Following'),(total,'Contributions in period')]
    for i,(value,label) in enumerate(values):
        x = 24 + i*235
        stats += rect(x,60,220,117) + text(x+19,114,value,36,'#edfff5',700) + text(x+19,148,label,12)
    svg('overview.svg',201,stats,'GitHub public account overview',str(values))

    chart = text(30,37,'ACTIVITY / INCLUDES DECORATIVE CALENDAR ART',13,'#53f7ad',600)
    chart += text(30,73,f'{total} contributions  /  {active} active days',26,'#edfff5',600)
    chart += text(30,101,'Includes backdated artwork cells; not a historical daily coding streak.',13)
    # Sunday-aligned columns; outside-period cells stay blank, zero days are dark.
    offset = (first.weekday()+1) % 7
    ncols = (len(days)+offset+6)//7
    cell = min(16, 858/ncols)
    last_month = None
    for i,(d,count) in enumerate(sorted(days.items())):
        dt = date.fromisoformat(d)
        col,row = divmod(i+offset,7)
        x,y = 65+col*cell,143+row*22
        if dt.month != last_month:
            if dt.day == 1 or (i == 0 and (dt.replace(day=28)-dt).days > 3):
                chart += text(x,130,dt.strftime('%b'),11)
            last_month = dt.month
        color = '#143b29' if not count else ['#23784a','#32aa69','#53d994','#8bffba'][min(3,(count-1)//3)]
        chart += f'<rect x="{x:.1f}" y="{y}" width="{cell-3:.1f}" height="17" rx="3" fill="{color}"><title>{d}: {count} contributions</title></rect>'
    chart += text(25,178,'Mon',11) + text(25,222,'Wed',11) + text(25,266,'Fri',11)
    chart += text(30,325,f'{first:%d %b %Y} — {last:%d %b %Y} / Dark green = zero; brighter = GitHub-counted activity.',12)
    labels = [('Commits','totalCommitContributions'),('Pull requests','totalPullRequestContributions'),
              ('Issues','totalIssueContributions'),('Reviews','totalPullRequestReviewContributions'),('Repositories','totalRepositoryContributions')]
    for i,(label,key) in enumerate(labels):
        x=30+i*182
        chart += rect(x,349,170,75) + text(x+14,380,sums[key],23,'#edfff5',600) + text(x+14,405,label,13)
    svg('activity.svg',447,chart,'Actual contribution activity',f'{data["start"]} to {data["end"]}: {total} contributions, {active} active days. '+str(sums))

    repos = [r for r in data['repositories'] if not r['fork']]
    primary = Counter(r['language'] for r in repos if r['language'])
    languages = Counter()
    for r in repos:
        languages.update(r['languages'])
    language_body = text(30,37,'CODE / LANGUAGE SIGNALS',13,'#53f7ad',600)
    language_body += text(30,75,'Primary language per repo',20,'#edfff5',600)
    language_body += text(510,75,'Distribution by code bytes',20,'#edfff5',600)
    language_body += text(30,101,'Non-fork public repos with a detected language',11)
    language_body += text(510,101,'Linguist bytes · not proficiency or time spent',11)
    for side,items,denom in [(30,primary.most_common(),sum(primary.values())),(510,languages.most_common(),sum(languages.values()))]:
        for i,(lang,value) in enumerate(items):
            y=139+i*37
            label = f'{value} repo' + ('s' if value!=1 else '') if side==30 else f'{100*value/denom:.1f}%'
            language_body += text(side,y,lang,14,'#d9f5e5') + text(side+326,y,label,13)
            language_body += rect(side,y+8,405,6,'#163627',3)
            language_body += f'<g class="draw">{rect(side,y+8,max(1,405*value/denom),6,COLORS[i%len(COLORS)],3)}</g>'
    h=145+max(len(primary),len(languages))*37
    svg('languages.svg',h,language_body,'Repository language analysis',str(dict(primary))+'; bytes: '+str(dict(languages)))
    stack = text(30,37,'TOOLKIT / FROM INTERFACE TO DELIVERY',13,'#53f7ad',600)
    groups=[('APPLICATION ENGINEERING','C# · ASP.NET Core · EF Core · Identity'),
            ('WEB INTERFACES','React · TypeScript · Razor · HTML · CSS'),
            ('DATA & STORAGE','SQL Server · MySQL · relational data'),
            ('DESKTOP & GRAPHICS','Java Swing · C++ · OpenGL / GLUT'),
            ('RESEARCH ANALYSIS','Python · pandas · SciPy · scikit-learn'),
            ('QUALITY & DELIVERY','Unit / integration · Playwright · CI')]
    for i,(label,tools) in enumerate(groups):
        x,y=24+(i%2)*470,60+(i//2)*90
        stack += rect(x,y,452,75) + text(x+16,y+26,label,12,COLORS[i],600) + text(x+16,y+53,tools,13,'#d9f5e5')
    svg('stack.svg',343,stack,'Core toolkit from the CV and public projects','; '.join(t for _,t in groups))
    repository_banner('projectflow-banner.svg','PROJECTFLOW',
                      'C# / ASP.NET Core MVC / Web API / EF Core / SQL Server','FEATURED ENGINEERING')
    repository_banner('organization.svg','HOSPITAL APPOINTMENTS',
                      'PHP / MySQL / JavaScript / HTML / CSS','ORGANIZATION COLLABORATION')
    # Human-readable, fully usable fallback for image or animation failures.
    fallback = f'<!-- snapshot:start -->\nPublic repositories: **{data["user"]["public_repos"]}** · Followers: **{data["user"]["followers"]}** · Following: **{data["user"]["following"]}**\n\nContribution period: **{data["start"]} → {data["end"]}**, inclusive. **{total} contributions** across **{active} active days**.\n\nCommits: **{sums["totalCommitContributions"]}** · Pull requests: **{sums["totalPullRequestContributions"]}** · Issues: **{sums["totalIssueContributions"]}** · Reviews: **{sums["totalPullRequestReviewContributions"]}** · Repository contributions: **{sums["totalRepositoryContributions"]}**.\n<!-- snapshot:end -->'
    readme = ROOT / 'README.md'
    import re
    readme.write_text(re.sub(r'<!-- snapshot:start -->.*?<!-- snapshot:end -->',lambda _:fallback,readme.read_text(encoding='utf8'),flags=re.S),encoding='utf8')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--offline',action='store_true')
    args=parser.parse_args()
    path=ROOT/'data'/'github.json'
    data=json.loads(path.read_text()) if args.offline else collect()
    render(data)
    if not args.offline:
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    print('Rendered verified profile for '+data['start']+' through '+data['end'])
