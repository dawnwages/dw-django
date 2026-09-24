"""
Talks, panels and podcasts for the Talks and Podcasts page, loaded with
`python manage.py load_talks`. After loading, edit them in the Wagtail admin.

Recent engagements (2025-2026) were checked against the event's own schedule
or the recording; the rest come from the previous version of the page.
Dates with precision "year" or "month" only need to be right to that level.
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
        "links": [("details", "https://pretalx.com/pyconde-pydata-2026/talk/QBJRBJ/", "Session")],
    },
    # --- 2025 ---------------------------------------------------------------
    {
        "kind": "keynote",
        "title": "Keynote",
        "event": "PyCon India 2025",
        "location": "Bengaluru, India",
        "date": D(2025, 9, 12),
        "date_precision": "month",
        "links": [("details", "https://in.pycon.org/blog/2025/keynote-announcement-dawn-wages.html", "Announcement")],
    },
    {
        "kind": "keynote",
        "title": "The Fellowship of the Stack: Scientific Discovery in Python",
        "event": "EuroSciPy 2025",
        "date": D(2025, 8, 1),
        "date_precision": "year",
        "description": (
            "A narrative take on the evolution of scientific experimentation in Python, the challenges "
            "ahead, and how we can find refuge with each other in the Python community."
        ),
        "links": [("details", "https://dawnwages.info/euroscipy-2025-keynote/", "Keynote page")],
    },
    # --- Earlier talks --------------------------------------------------------
    {
        "kind": "talk",
        "title": "Success Through a Thousand Emails",
        "event": "FOSS Backstage 2024",
        "date": D(2024, 1, 1),
        "date_precision": "year",
        "description": (
            "The most successful fundraising campaigns come from services rendered, shared identity or "
            "urgency, and are driven by thousands of small actions and follow-ups."
        ),
        "links": [
            ("details", "https://program.foss-backstage.de/fossback24/talk/PWXM7V/", "Session"),
            ("watch", "https://youtu.be/UTKcPBKCQEc", ""),
        ],
    },
    {
        "kind": "talk",
        "title": "Navigating Django's Future: Djangonaut Space",
        "event": "DjangoCon US 2023",
        "date": D(2023, 10, 1),
        "date_precision": "year",
        "with_people": "with Rachell Calhoun",
        "description": (
            "A voyage through Djangonaut Space, the Django community's 8-week group mentoring program "
            "for aspiring contributors."
        ),
        "links": [
            ("details", "https://2023.djangocon.us/talks/navigating-djangos-future-djangonaut-space/", "Session"),
            ("watch", "https://youtu.be/UTKcPBKCQEc", ""),
        ],
    },
    {
        "kind": "keynote",
        "title": "A New Adventure Is Born: How Open Source Dinos Unite",
        "event": "DjangoCon Europe 2023",
        "date": D(2023, 5, 1),
        "date_precision": "year",
        "description": (
            "Inspired by The Land Before Time: how persona thinking applies to open source "
            "participants, and how different approaches make communities sustainable."
        ),
        "links": [("watch", "https://youtu.be/dnv9uQVuOl8", "")],
    },
    {
        "kind": "podcast",
        "title": "Dawn Wages on being an ethical open source engineer",
        "event": "Open Source Stories",
        "date": D(2022, 1, 1),
        "date_precision": "year",
        "description": (
            "Ethical open source engineering, practicing anti-racism in open source, psychological "
            "safety and the next generation of contributors."
        ),
        "links": [
            ("listen", "https://archive.storycorps.org/interviews/dawn-wages-on-being-an-ethical-open-source-engineer/", ""),
            ("details", "https://www.opensourcestories.org/stories/2022/dawn-wages/", "Story"),
        ],
    },
    {
        "kind": "talk",
        "title": "Gatsby + Wagtail",
        "event": "Inclusive Product Week 2021",
        "location": "San Jose, CA",
        "date": D(2021, 1, 1),
        "date_precision": "year",
        "description": (
            "Could a GatsbyJS front end with a headless Wagtail back end be a quick, well-designed "
            "option for small clients and personal projects?"
        ),
        "links": [
            ("watch", "https://app.hopin.com/events/inclusive-product-week/sessions/2855352b-be20-40dd-bd9a-8964eb913b1f", ""),
            ("slides", "https://www.slideshare.net/DawnWages/final-gatsby-wagtail-inclusive-product-week", ""),
        ],
    },
    {
        "kind": "talk",
        "title": "Gatsby + Wagtail",
        "event": "PyCon Australia 2020",
        "date": D(2020, 1, 1),
        "date_precision": "year",
        "links": [("watch", "https://www.youtube.com/watch?v=S6ntmaq3hIw", "")],
    },
    {
        "kind": "talk",
        "title": "Open Source Dinosaur Classification: A New Adventure Is Born",
        "event": "Wagtail Space 2018",
        "location": "Philadelphia, PA",
        "date": D(2018, 1, 1),
        "date_precision": "year",
        "description": (
            "How different open source \"dinosaurs\" can learn Wagtail, borrowing the archetypes of "
            "The Land Before Time."
        ),
        "links": [("watch", "https://www.youtube.com/watch?v=C-tXt5fLj_s", "")],
    },
    # --- Podcasts without a confirmed date ------------------------------------
    {
        "kind": "podcast",
        "title": "Episode 12: Dawn Wages",
        "event": "Sad Python Girls Club",
        "description": (
            "The evolution of Django and DjangoCon and shaping codes of conduct. \"It's people who are "
            "the solution to all of the world's woes, and code is but a tool.\""
        ),
        "links": [("listen", "https://anchor.fm/sad-python-girls-club/episodes/Episode-12---Dawn-Wages-e1sbv28", "")],
    },
    {
        "kind": "podcast",
        "title": "Recurring host",
        "event": "Sad Python Girls Club",
        "links": [("listen", "https://bit.ly/SPyGC", "")],
    },
    {
        "kind": "podcast",
        "title": "The Road to Django with Dawn Wages",
        "event": "The Django Girls Podcast",
        "description": "The first Django Girls Podcast episode: my journey to Django, starting with Django Girls, and At The Root.",
        "links": [("listen", "https://anchor.fm/djangogirls/episodes/the-road-to-Django-with-Dawn-Wages-e1ctg68", "")],
    },
    {
        "kind": "podcast",
        "title": "Wagtail, React, Gatsby",
        "event": "Django Chat",
        "with_people": "with Carlton Gibson and William Vincent",
        "description": (
            "My journey to consulting, being a \"community taught\" engineer, React and Gatsby, and the "
            "Antiracist Ethical Source License."
        ),
        "links": [
            ("listen", "https://djangochat.com/episodes/wagtail-react-gatsby-dawn-wages-RaD8k37m", ""),
            ("transcript", "https://djangochat.com/episodes/wagtail-react-gatsby-dawn-wages-RaD8k37m/transcript", ""),
        ],
    },
    {
        "kind": "podcast",
        "title": "At The Root: Decolonizing Tech",
        "event": "#CauseAScene",
        "with_people": "with Kim Crayton",
        "description": "Kim Crayton's final guest: Black Girl Magic, colonialism and capitalism in tech, and who leads the movement.",
        "links": [
            ("listen", "https://hashtagcauseascene.com/podcast/dawn-wages/", ""),
        ],
    },
    {
        "kind": "interview",
        "title": "PATHS Interview, Season 2",
        "event": "LGBT Tech",
        "links": [
            ("watch", "https://www.youtube.com/watch?v=tX9SkxSOTr8", ""),
            ("details", "https://www.lgbttech.org/paths", "About PATHS"),
        ],
    },
]
