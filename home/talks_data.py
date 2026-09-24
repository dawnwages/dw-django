"""
Talks, panels and podcasts for the Talks and Podcasts page, loaded with
`python manage.py load_talks`. After loading, edit them in the Wagtail admin.

Every video link was checked against the video itself (title and channel via
YouTube oEmbed) or an official schedule, pyvideo.org or DjangoTV page.
Dates with precision "year" or "month" only need to be right to that level.
Links are (kind, url, label); an empty label shows the link kind.
"""
import datetime

D = datetime.date

TALKS = [
    # --- 2026 ---------------------------------------------------------------
    {
        "kind": "keynote",
        "title": "Boldly Go, Building Worlds: Is there Room for me on the Bridge?",
        "event": "DjangoCon US 2026",
        "location": "Chicago, IL",
        "date": D(2026, 8, 24),
        "date_precision": "day",
        "description": (
            "The opening keynote. Drawing on Star Trek and Octavia Butler, a look at how people "
            "from the margins build inclusive communities and make room for others in tech leadership."
        ),
        "links": [("details", "https://2026.djangocon.us/talks/keynote-monday/", "Session")],
        "featured": True,
    },
    {
        "kind": "talk",
        "title": "How Many Spoons Does Your Environment Cost?",
        "event": "EuroPython 2026",
        "location": "Kraków, Poland",
        "date": D(2026, 7, 16),
        "date_precision": "day",
        "description": (
            "Spoon theory for Python environments: why they are so draining to keep working, "
            "and why it's the ecosystem, not you."
        ),
        "links": [
            ("details", "https://ep2026.europython.eu/session/how-many-spoons-does-your-environment-cost-broken-demos-human-element", "Session"),
            ("watch", "https://www.youtube.com/watch?v=ShBUTixLn88", "Preview"),
        ],
    },
    {
        "kind": "interview",
        "title": "Numerically Speaking LIVE (host)",
        "event": "Anaconda",
        "date": D(2026, 7, 11),
        "date_precision": "month",
        "description": "Anaconda's livestream on the Python data ecosystem, with guests from conda, HoloViz and beyond.",
        "links": [
            ("watch", "https://www.youtube.com/watch?v=LS5qdjtH8Tg", "Locked, Loaded, Reproducible"),
            ("watch", "https://www.youtube.com/watch?v=8fpoRJreR5Q", "AI & package discovery"),
            ("watch", "https://www.youtube.com/watch?v=UI-E3We_50M", "HoloViz & LumenAI"),
            ("watch", "https://www.youtube.com/watch?v=uAamIxbatcA", "Conda roadmap"),
        ],
    },
    {
        "kind": "interview",
        "title": "Road to PyCon Togo 26: Meeting a Python Icon",
        "event": "Python Software Community Togo",
        "date": D(2026, 6, 27),
        "date_precision": "day",
        "description": "A livestream conversation about the Python ecosystem, local-first AI and building diverse communities.",
        "links": [("watch", "https://www.youtube.com/watch?v=IEnL6fCmmXY", "")],
    },
    {
        "kind": "keynote",
        "title": "Stop Being a Generalist: The Small Model Revolution",
        "event": "PyCon Italia 2026",
        "location": "Bologna, Italy",
        "date": D(2026, 5, 29),
        "date_precision": "day",
        "links": [("details", "https://2026.pycon.it/en", "Conference")],
    },
    {
        "kind": "talk",
        "title": "How many spoons does your environment cost: Feat. demos breaking and the human element of your broken env",
        "event": "PyCon US 2026",
        "location": "Long Beach, CA",
        "date": D(2026, 5, 15),
        "date_precision": "day",
        "links": [("details", "https://us.pycon.org/2026/schedule/presentation/119/", "Session")],
    },
    {
        "kind": "panel",
        "title": "Fostering better collaboration between the scientific Python community and core Python development",
        "event": "PyCon US 2026",
        "location": "Long Beach, CA",
        "date": D(2026, 5, 15),
        "date_precision": "day",
        "with_people": "with Jonathan Dekhtiar and Michael Droettboom",
        "links": [("details", "https://us.pycon.org/2026/schedule/presentation/123/", "Session")],
    },
    {
        "kind": "interview",
        "title": "Python, AI, and What Comes After the Demo",
        "event": "PyCon US 2026",
        "date": D(2026, 5, 15),
        "date_precision": "month",
        "with_people": "with Paul Everitt",
        "description": "A conversation about Python, AI, developer communities and where the ecosystem is heading next.",
        "links": [("watch", "https://www.youtube.com/watch?v=gQGMU1QdCAA", "")],
    },
    {
        "kind": "fireside",
        "title": "PyLadies Fireside Chat",
        "event": "PyCon DE & PyData 2026",
        "location": "Darmstadt, Germany",
        "date": D(2026, 4, 15),
        "date_precision": "day",
        "with_people": "with Tereza Iofciu and Jessica Greene",
        "description": "What it means to build with Python while AI reshapes the craft of software development.",
        "links": [
            ("watch", "https://www.youtube.com/watch?v=aMebGZmkgnI", ""),
            ("details", "https://pretalx.com/pyconde-pydata-2026/talk/QBJRBJ/", "Session"),
        ],
    },
    {
        "kind": "interview",
        "title": "Upgrade Wagtail CMS with Dawn Wages",
        "event": "Wagtail livestream",
        "date": D(2026, 2, 21),
        "date_precision": "day",
        "with_people": "with Meagen Voss",
        "description": "Upgrading a Wagtail site live on stream.",
        "links": [("watch", "https://www.youtube.com/watch?v=ZFnvh-XJhIs", "")],
    },
    # --- 2025 ---------------------------------------------------------------
    {
        "kind": "podcast",
        "title": "Dawn Wages and Loren Crary on funding the PSF",
        "event": "Sustain, Episode 276",
        "date": D(2025, 12, 12),
        "date_precision": "day",
        "with_people": "with Richard Littauer and Loren Crary",
        "description": "How the Python Software Foundation is funded and governed, including the decision to turn down an NSF grant.",
        "links": [
            ("listen", "https://podcast.sustainoss.org/276", ""),
            ("watch", "https://www.youtube.com/watch?v=4gxglJ2LR8Q", ""),
        ],
    },
    {
        "kind": "talk",
        "title": "The Lifecycle of a Jupyter Environment",
        "event": "PyData Boston 2025 · PyData Global 2025",
        "date": D(2025, 12, 8),
        "date_precision": "month",
        "description": "How a notebook project's environment has to change as it grows from exploration toward production.",
        "links": [
            ("watch", "https://www.youtube.com/watch?v=s9zwyyMJnqM", "PyData Boston"),
            ("watch", "https://www.youtube.com/watch?v=kHYNyYnSShU", "PyData Global"),
        ],
    },
    {
        "kind": "keynote",
        "title": "Keynote",
        "event": "PyCon India 2025",
        "location": "Bengaluru, India",
        "date": D(2025, 9, 13),
        "date_precision": "day",
        "links": [("details", "https://in.pycon.org/blog/2025/keynote-announcement-dawn-wages.html", "Announcement")],
    },
    {
        "kind": "panel",
        "title": "Two Decades of Django: The Past, Present and Future",
        "event": "DjangoCon US 2025",
        "location": "Chicago, IL",
        "date": D(2025, 9, 10),
        "date_precision": "day",
        "with_people": "with Velda Kiara, Tim Schilling, Natalia Bidart, Rachell Calhoun, Peter Grandstaff and Jeff Triplett",
        "description": "Django at 20: its history, governance and what comes next.",
        "links": [("watch", "https://www.youtube.com/watch?v=uYN7cpxhuhE", "")],
    },
    {
        "kind": "talk",
        "title": "Community Update: Python Software Foundation",
        "event": "DjangoCon US 2025",
        "location": "Chicago, IL",
        "date": D(2025, 9, 9),
        "date_precision": "day",
        "description": "What the PSF is working on, how to get involved, and plans for 2026.",
        "links": [("watch", "https://www.youtube.com/watch?v=RT1yd-sMs3Y", "")],
    },
    {
        "kind": "keynote",
        "title": "The Fellowship of the Stack: Scientific Discovery in Python",
        "event": "EuroSciPy 2025",
        "location": "Kraków, Poland",
        "date": D(2025, 8, 21),
        "date_precision": "day",
        "description": (
            "Transformed from humble beginnings into a catalyst for breakthrough science—decoding cosmic "
            "mysteries, healing human diseases, predicting planetary futures—our hero joins millions of "
            "computational explorers pushing the boundaries of human understanding. Every scientific "
            "revolution starts with a single spark of code. What epic will you write? In this keynote "
            "we'll take a narrative approach to the evolution of scientific experimentation, the daunting "
            "challenges that await and how we as the protagonists can find refuge with each other in the "
            "Python ecosystem."
        ),
        "links": [
            ("slides", "https://dawnwages.info/documents/116/EuroSciPy_Keynote_Fellowship_of_the_stack.pdf", ""),
            ("details", "https://euroscipy.org/talks/VCLRCU/", "Session"),
            ("details", "https://dawnwages.info/euroscipy-2025-keynote/", "Keynote page"),
        ],
    },
    {
        "kind": "talk",
        "title": "Lightning talk",
        "event": "PyTexas 2025",
        "date": D(2025, 4, 13),
        "date_precision": "day",
        "links": [("watch", "https://www.youtube.com/watch?v=HunjqprrbpQ", "Lightning talks, day 2")],
    },
    {
        "kind": "podcast",
        "title": "Why Python developers just use Postgres",
        "event": "Talking Postgres, Episode 25",
        "date": D(2025, 3, 14),
        "date_precision": "day",
        "with_people": "with Claire Giordano",
        "description": "Why Django developers lean on Postgres, plus Djangonaut Space and open source culture.",
        "links": [
            ("listen", "https://talkingpostgres.com/episodes/why-python-developers-just-use-postgres-with-dawn-wages", ""),
            ("watch", "https://www.youtube.com/watch?v=leir3xJ4Klo", ""),
            ("transcript", "https://talkingpostgres.com/episodes/why-python-developers-just-use-postgres-with-dawn-wages/transcript", ""),
        ],
    },
    # --- 2024 ---------------------------------------------------------------
    {
        "kind": "podcast",
        "title": "Season 2 co-host",
        "event": "Sad Python Girls Club",
        "date": D(2024, 1, 12),
        "date_precision": "year",
        "with_people": "with Luciana Abud",
        "links": [
            ("listen", "https://creators.spotify.com/pod/profile/sad-python-girls-club/episodes/S2-Episode-1---New-Year--New-Season-e2eb1ft", "New Year, New Season!"),
            ("listen", "https://creators.spotify.com/pod/profile/sad-python-girls-club/episodes/S2-Episode-4---Charlie-Marsh-on-Astral-tools-e2moldc", "Charlie Marsh on Astral tools"),
            ("listen", "https://bit.ly/SPyGC", "All episodes"),
        ],
    },
    {
        "kind": "talk",
        "title": "3D Files with Wagtail",
        "event": "Wagtail Space US 2024",
        "location": "Philadelphia, PA",
        "date": D(2024, 7, 1),
        "date_precision": "year",
        "with_people": "with Mira Gibson",
        "description": "A case study of working with 3D and XR files in a Wagtail project.",
        "links": [("watch", "https://www.youtube.com/watch?v=ccBrb50xRCM", "")],
    },
    {
        "kind": "talk",
        "title": "Supercharging your Python Development Environment",
        "event": "DjangoCon Europe 2024",
        "location": "Vigo, Spain",
        "date": D(2024, 6, 5),
        "date_precision": "month",
        "description": "Reproducible Python development environments with VS Code and dev containers, for Django projects.",
        "links": [("watch", "https://www.youtube.com/watch?v=gCUJW70gRog", "")],
    },
    {
        "kind": "talk",
        "title": "Success Through a Thousand Emails: Fundraising and Outreach",
        "event": "FOSS Backstage 2024",
        "location": "Berlin, Germany",
        "date": D(2024, 3, 5),
        "date_precision": "day",
        "description": (
            "All of the most successful fundraising campaigns come from three categories: services "
            "rendered, shared identity, or urgency; and are driven by thousands of small actions and "
            "follow up to create opportunities, clarity and collaboration. Getting the right people to "
            "care is a behemoth task. Large corporations that are expected to write a check and fill the "
            "gap of a worthwhile initiative don't show up like we expect; why does money never seem to "
            "flow to the right place at the right time?\n\n"
            "Through this presentation I'll discuss ways grassroots campaigns strike a chord with their "
            "audience to get over the fundraising finish line, with some common gotchas:\n"
            "• The audience you thought would care, doesn't.\n"
            "• Who has the bank account?\n"
            "• How much is a handshake worth?\n"
            "• Getting Western donations to African initiatives.\n"
            "• Reduce the \"I'm going to get yelled at\" factor when asking corporations for contributions.\n"
            "• Creating the next wave of financially and fiscally aware in Open Source."
        ),
        "links": [
            ("watch", "https://www.youtube.com/watch?v=YuPXZZKry4Y", ""),
            ("details", "https://program.foss-backstage.de/fossback24/talk/PWXM7V/", "Session"),
        ],
    },
    # --- 2023 ---------------------------------------------------------------
    {
        "kind": "talk",
        "title": "Navigating Django's Future: Djangonaut Space",
        "event": "DjangoCon US 2023",
        "location": "Durham, NC",
        "date": D(2023, 10, 17),
        "date_precision": "day",
        "with_people": "with Rachell Calhoun",
        "description": (
            "Embark on a voyage through Djangonaut Space, a one-of-a-kind mentorship initiative within the "
            "Django community. With a focus on collaborative learning, sustainability, and long-term "
            "growth, we invite aspiring Djangonauts to join our 8-week group mentoring program. Here, "
            "participants work at their own pace in a structured learning environment, setting the stage "
            "for future contributions and potential leadership roles within the Django community.\n\n"
            "The mission is crystal clear: to nurture Django's next generation of leaders, boost community "
            "sustainability, and create a more diverse and inclusive contributor base.\n\n"
            "But does this program truly deliver on its promises? Can its unique approach effectively "
            "achieve its ambitious goals? Is it the transformative experience it professes to be? In "
            "short, will these Djangonauts reach the stars?\n\n"
            "With the conclusion of our Pilot Program, we invite you to join us in reflecting on its "
            "inception, achievements, and its potential impact on the broader Django universe going "
            "forward. Don't miss this opportunity to be part of the discussion and our mission to shape "
            "the future of Django together."
        ),
        "links": [
            ("watch", "https://youtu.be/UTKcPBKCQEc", ""),
            ("details", "https://2023.djangocon.us/talks/navigating-djangos-future-djangonaut-space/", "Session"),
        ],
    },
    {
        "kind": "keynote",
        "title": "A New Adventure Is Born: How Open Source Dinos Unite",
        "event": "DjangoCon Europe 2023",
        "location": "Edinburgh, UK",
        "date": D(2023, 5, 30),
        "date_precision": "day",
        "description": (
            "A coding brontosaurus teams up with other Open Source dinosaurs and unite as a community to "
            "advance their project. From The Apprentice-Rex to the Ptero-Python-Party-o-Dactyl, this rag "
            "tag group of friends' unique approaches work together to make our journeys better and our "
            "communities sustainable. This keynote, inspired by the playful characters of the classic "
            "children's film A Land Before Time (1988) brings a fun approach to how persona marketing "
            "applies to the participants in Open Source. We compare project ecosystems, talk friction "
            "reducing activities tending to your community, and how iterative product and developer "
            "experience design through empathy is essential to project adoption."
        ),
        "links": [
            ("watch", "https://youtu.be/dnv9uQVuOl8", ""),
            ("watch", "https://youtu.be/Zc0W3L1tIZM", "Lightning talks"),
        ],
    },
    {
        "kind": "podcast",
        "title": "Dawn Wages of PSF on organizing communities, ethical licenses, and more",
        "event": "Sustain, Episode 169",
        "date": D(2023, 4, 21),
        "date_precision": "day",
        "with_people": "with Richard Littauer",
        "description": "PSF membership, ethical source licensing and running communities.",
        "links": [
            ("listen", "https://podcast.sustainoss.org/169", ""),
            ("watch", "https://www.youtube.com/watch?v=nKQCJ5m95rU", ""),
        ],
    },
    {
        "kind": "talk",
        "title": "Supercharge your Python Development Environment with VS Code + Dev Container",
        "event": "PyCon US 2023",
        "location": "Salt Lake City, UT",
        "date": D(2023, 4, 21),
        "date_precision": "month",
        "description": "Building reproducible Python development environments with VS Code and dev containers.",
        "links": [("watch", "https://www.youtube.com/watch?v=WYlC8jE8itI", "")],
    },
    {
        "kind": "interview",
        "title": "Python Pulse (host)",
        "event": "Visual Studio Code livestream",
        "date": D(2023, 1, 13),
        "date_precision": "year",
        "description": (
            "A monthly livestream I hosted from 2023 to 2025 on Python in VS Code, with guests "
            "from the Python, data science and developer tools communities."
        ),
        "links": [
            ("watch", "https://www.youtube.com/watch?v=U6B-0f3gTyo", "Supercharge your DX"),
            ("watch", "https://www.youtube.com/watch?v=lxheR6p1u0A", "Meet the Python for VS Code team"),
            ("details", "https://devblogs.microsoft.com/python/announcing-python-pulse/", "About the show"),
            ("details", "https://github.com/dawnwages/python-pulse-stream", "Show notes"),
        ],
    },
    # --- 2022 ---------------------------------------------------------------
    {
        "kind": "podcast",
        "title": "Episode 12: Dawn Wages",
        "event": "Sad Python Girls Club",
        "date": D(2022, 12, 16),
        "date_precision": "day",
        "with_people": "hosted by Kim-Adeline and Luciana",
        "description": (
            "Having a blast with the Sad Python Girls Club as the Python Community Product Manager at "
            "Microsoft, PSF director, DjangoCon organizer and Wagtail CMS core team member. \"I feel like "
            "it's people, who are the solution to all of the world's woes, and code is but a tool.\" We "
            "talk about the evolution of Django and DjangoCon, shaping codes of conduct while being "
            "mindful of ethical questions, and a few thoughts and avenues on how to make communities "
            "more welcoming."
        ),
        "links": [("listen", "https://creators.spotify.com/pod/profile/sad-python-girls-club/episodes/S1-Episode-12---Dawn-Wages-e1sbv28", "")],
    },
    {
        "kind": "panel",
        "title": "The State of Django (moderator)",
        "event": "DjangoCon US 2022",
        "location": "San Diego, CA",
        "date": D(2022, 10, 19),
        "date_precision": "day",
        "with_people": "with Andrew Godwin, Carlton Gibson, Jeff Triplett, Mariusz Felisiak, Rachell Calhoun and Will Vincent",
        "description": "The state of the Django codebase and community, including newcomers and diversity.",
        "links": [("watch", "https://www.youtube.com/watch?v=IumYtz0G5v0", "")],
    },
    {
        "kind": "interview",
        "title": "Managing Yourself Effectively While Working Remotely",
        "event": "Remote Work Decoded, #1",
        "date": D(2022, 9, 22),
        "date_precision": "day",
        "description": "Async remote work, productivity tools and contributing to open source.",
        "links": [("watch", "https://www.youtube.com/watch?v=rNMqx4hJbYI", "")],
    },
    {
        "kind": "interview",
        "title": "PATHS Interview, Season 2, Episode 3",
        "event": "LGBT Tech",
        "date": D(2022, 6, 28),
        "date_precision": "day",
        "description": (
            "Identity; coming out and finding my labels; finding my love for tech; my experience as a "
            "queer woman of color in tech; anti-racist coding and why an anti-racist license matters; "
            "barriers for LGBTQ+ people entering tech; and advice for LGBTQ+ people interested in STEAM."
        ),
        "links": [
            ("watch", "https://www.youtube.com/watch?v=tX9SkxSOTr8", ""),
            ("details", "https://www.lgbttech.org/paths", "About PATHS"),
        ],
    },
    {
        "kind": "podcast",
        "title": "Dawn Wages on being an ethical open source engineer",
        "event": "Open Source Stories",
        "date": D(2022, 5, 16),
        "date_precision": "day",
        "with_people": "with julia ferraioli",
        "description": (
            "Ethical open source engineering, farm-to-table open source, practicing anti-racism in open "
            "source, fostering innovation through psychological safety, the next generation of open "
            "source contributors, and responsible open source development."
        ),
        "links": [
            ("watch", "https://www.youtube.com/watch?v=LJwEMfAfULk", ""),
            ("listen", "https://archive.storycorps.org/interviews/dawn-wages-on-being-an-ethical-open-source-engineer/", ""),
            ("transcript", "https://www.opensourcestories.org/stories/2022/dawn-wages/", ""),
        ],
    },
    {
        "kind": "podcast",
        "title": "The Road to Django with Dawn Wages",
        "event": "The Django Girls Podcast",
        "date": D(2022, 1, 13),
        "date_precision": "day",
        "with_people": "with Aisha Bello and Leona So",
        "description": (
            "Had a wonderful time on the first Django Girls Podcast episode with Aisha and Leona about my "
            "journey to Django, starting with Django Girls. I also got a chance to talk about new "
            "initiatives with At The Root."
        ),
        "links": [
            ("listen", "https://creators.spotify.com/pod/profile/djangogirls/episodes/the-road-to-Django-with-Dawn-Wages-e1ctg68", ""),
            ("details", "https://attheroot.dev/", "At The Root"),
        ],
    },
    # --- 2021 ---------------------------------------------------------------
    {
        "kind": "podcast",
        "title": "At The Root: Decolonizing Tech",
        "event": "#CauseAScene",
        "date": D(2021, 2, 17),
        "date_precision": "day",
        "with_people": "with Kim Crayton",
        "description": (
            "I had the absolute privilege of being Kim Crayton's final guest on her podcast #CauseAScene. "
            "We waxed philosophical about whether or not we use Black Girl Magic, whether colonialism and "
            "capitalism are inextricably linked to tech, who leads the movement and why the answer is US!"
        ),
        "links": [
            ("listen", "https://hashtagcauseascene.com/podcast/dawn-wages/", ""),
            ("transcript", "https://hashtagcauseascene.com/podcast/dawn-wages/", ""),
        ],
    },
    {
        "kind": "podcast",
        "title": "Wagtail, React, & Gatsby",
        "event": "Django Chat",
        "date": D(2021, 2, 3),
        "date_precision": "day",
        "with_people": "with Carlton Gibson and William Vincent",
        "description": (
            "Super fun episode with Carlton Gibson and William Vincent where I discuss my journey to "
            "consulting, being a \"community taught\" engineer, my work in React and Gatsby, and the "
            "Antiracist Ethical Source License."
        ),
        "links": [
            ("listen", "https://djangochat.com/episodes/wagtail-react-gatsby-dawn-wages-RaD8k37m", ""),
            ("watch", "https://www.youtube.com/watch?v=ZtRU-Xa91ns", ""),
            ("transcript", "https://djangochat.com/episodes/wagtail-react-gatsby-dawn-wages-RaD8k37m/transcript", ""),
        ],
    },
    {
        "kind": "talk",
        "title": "Gatsby + Wagtail",
        "event": "Inclusive Product Week 2021",
        "location": "San Jose, CA",
        "date": D(2021, 5, 20),
        "date_precision": "day",
        "description": (
            "Exploring if a GatsbyJS progressive web app generator frontend with a headless Wagtail "
            "backend could be a solution for small-sized clients and personal projects when I want to "
            "\"whip something up\" quickly without sacrificing design, performance/hosting costs, user or "
            "site editor experience (can I have it all?). Gatsby is an open source framework based on "
            "React. Wagtail is a Django CMS with lots of cool features for content creators, and \"plays "
            "nicely with everything else in your tech stack\" because it's built on and easily integrates "
            "with all uses of Python.\n\n"
            "I am a JavaScript and Python consultant and used this stack to host a project near to my "
            "heart: At The Root: The AntiRacist Ethical Source License. In this talk I dive into a little "
            "code, a lot of cool features, and some important ways Open Source Engineers can contribute "
            "to the accessibility and accountability of their communities.\n\n"
            "Learn about: static site generators, progressive web apps, Python for the web, React, "
            "content management systems, ethical licenses for open code, GraphQL and \"headless\" backends."
        ),
        "links": [
            ("details", "https://www.inclusiveproductweek.org/speakers/#DawnWages", "Speaker page"),
            ("watch", "https://app.hopin.com/events/inclusive-product-week/sessions/2855352b-be20-40dd-bd9a-8964eb913b1f", ""),
            ("slides", "https://www.slideshare.net/DawnWages/final-gatsby-wagtail-inclusive-product-week", ""),
        ],
    },
    # --- 2020 and earlier -----------------------------------------------------
    {
        "kind": "talk",
        "title": "At The Root: Wagtail + Gatsby + GitPod",
        "event": "PyCon Australia 2020 (online)",
        "date": D(2020, 9, 5),
        "date_precision": "day",
        "description": (
            "The developer-experience version of my Gatsby + Wagtail talk: a GatsbyJS front end with a "
            "headless Wagtail back end, built for At The Root."
        ),
        "links":[("watch", "https://www.youtube.com/watch?v=S6ntmaq3hIw", "")],
    },
    {
        "kind": "talk",
        "title": "Gatsby + Wagtail + Netlify (with a little GitPod)",
        "event": "Wagtail Space US 2020 (online)",
        "date": D(2020, 8, 10),
        "date_precision": "month",
        "description": "A headless Wagtail back end with a Gatsby front end, deployed on Netlify.",
        "links": [("watch", "https://youtu.be/FP907CJsSBk", "")],
    },
    {
        "kind": "talk",
        "title": "Lightning talk",
        "event": "DjangoCon US 2019",
        "location": "San Diego, CA",
        "date": D(2019, 9, 23),
        "date_precision": "day",
        "links": [("watch", "https://www.youtube.com/watch?v=b5jS4mLR1N0&t=1576s", "")],
    },
    {
        "kind": "talk",
        "title": "Learning Wagtail",
        "event": "Wagtail Space US 2018",
        "location": "Philadelphia, PA",
        "date": D(2018, 6, 21),
        "date_precision": "day",
        "description": (
            "Open Source Dinosaur Classification: A New Adventure Is Born. This talk has taken a few forms "
            "over the years. Its first form began as an introduction to how different \"dinosaurs\" can "
            "learn Wagtail. Borrowing from the fun and playful characters in A Land Before Time (1988), it "
            "looks at the archetypes and \"personalities\" of people who participate in the Open Source "
            "community and how they seek to interact at large.\n\n"
            "This talk is for projects that would like to grow from dozens of users to hundreds, a handful "
            "of contributors to dozens, and provide friction-reducing methods for learning and sharing in "
            "Open Source. We look at the ecosystems of React / ECMAScript PWA communities, Wagtail and "
            "other Python projects, and Ruby on Rails comparatively, and how they reduce the friction for "
            "adoption and contribution through starter tutorials, fun incentive programs, intuitive "
            "documentation, assistive tools, and partnerships. A healthy community is empathetic, "
            "welcoming and diverse. Have fun with the Apprentice-Rex, the Fail-Fast-adon and other "
            "dinosaur friends, as we learn how they navigate new engineering projects on the way to seek "
            "the oasis known as the Great Valley."
        ),
        "links": [("watch", "https://www.youtube.com/watch?v=C-tXt5fLj_s", "")],
    },
]
