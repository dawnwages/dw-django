---
title: Human-in-the-Loop Isn't Enough
slug: human-in-the-loop-isnt-enough
date: 2026-10-17
tags: AI, Agents, Domain-Driven Design
excerpt: Human-in-the-loop keeps AI systems safe, but it doesn't let the people closest to the work teach them anything. What I found when I went looking for prior art, and what I'm building instead.
---

The thing I care about most at Wildflower Software is building stuff that holds up in the real world. A demo is easy. What I want is a system that's still useful six months in, after prices have moved, a vendor's gotten worse, some new product took off, and the one person who knew about all of it never once logged into the dashboard.

I just put up a post on the Wildflower site called [Human-in-the-Wild](https://wildflowersoftware.com/blog/human-in-the-wild/). It's about a recommendation engine I'm building for a flower shop, where the owner can text what she's seeing and the system actually changes what it knows. When I sat down to write it I went looking for prior art. I figured there'd be a pile of writing on people keeping the knowledge inside their AI systems current, day to day. I didn't find much.

What I found, over and over, was human-in-the-loop. I've built a lot of it, and I don't think it's enough.

## The loop stops bad outputs and forgets why

In practice human-in-the-loop usually means the agent decides something and a person approves or rejects it before it happens. Every agent system I ship has an approval gate, enforced in code, and I'm not taking those out.

But think about what happens to what the person knows. Say the owner rejects an order because that vendor's roses have been opening too fast. The gate catches it and the order doesn't go out. Then her reason just disappears. Tomorrow the system suggests the same vendor and she has to reject it again. It's safer, sure. It hasn't learned anything.

The person ends up as a reviewer, reacting to whatever the system came up with, one thing at a time, with no way to change what it knows. Give that a few weeks and you get approval fatigue. People start clicking yes to get through the queue, and all the knowledge that made their review worth having stays in their head.

If you want a system to keep working once it's out in the world, the people who see the world changing need a way to tell it. When they notice, in their own words, without waiting to be asked.

## What's already out there

I didn't think I'd invented anything, so I went through the stuff that's closest. Every one of these does part of it.

Expert systems were the first real attempt. Back in the 80s, knowledge engineers would interview experts and hand-code their rules. Ed Feigenbaum called the problem that sank a lot of those projects the knowledge acquisition bottleneck. Getting knowledge out of people's heads was slow and expensive, and the rules went stale as soon as anything changed. Same problem I have, forty years earlier. Their fix was more interviews.

Domain-driven design gets closer. Eric Evans's book from 2003 talks about knowledge crunching, where developers and domain experts work through a problem together until the model matches how the experts think, agreeing on a shared language while they're at it. It's still the best thing I've read on modeling what experts know. It also kind of assumes the expert is in the room while you design and then goes back to their real job.

Active learning flips who asks. The model finds the examples it's least sure about and asks a person to label them. Handy, but the model picks the questions, and what it gets back is a label. You can't label your way to "this vendor's been slipping since August."

Interactive machine learning and machine teaching are the closest research I found. Saleema Amershi and her coauthors wrote *Power to the People* in 2014 about putting users in tight loops with the models they're shaping, and Patrice Simard's machine teaching work at Microsoft in 2017 treated the person teaching the model as part of the system. I love both. They're aimed at people building classifiers, though, and the person I'm building for is a florist on her phone.

RLHF uses human feedback too, just at a totally different scale. Millions of comparisons make a model better in general. None of them will tell your system the peonies came in early this year.

Knowledge editing, stuff like ROME and MEMIT, lets researchers go in and change specific facts in a model's weights. Cool work. It's a research tool, and there's no idea of scope or expiration in it.

Agent memory is the most practical neighbor right now. MemGPT (Letta now) and the memory features in most assistants let agents remember things between conversations. Most of that memory gets inferred from chat, though. Nobody confirms it, it isn't scoped to one part of the system, and it doesn't expire.

RAG knowledge bases are what most teams reach for. Chunk the wiki and the SOPs, embed them, retrieve. That's fine for "what's our refund policy." It can only hold what someone already wrote down, and most of the good stuff never gets written down.

Drift monitoring catches the world changing out from under a model, but only statistically, after enough bad predictions pile up. The person doing the work usually noticed weeks before.

So, lots of pieces. I couldn't find anything about the expert, on their own time, steadily improving what a live system knows.

## What Human-in-the-Wild adds

Human-in-the-Wild keeps the approval gate and adds a second channel going the other way. The expert doesn't wait for the system to ask. When they notice something, they send a sentence wherever they already talk. An agent turns it into a structured field signal, reads it back to make sure it got it right, and from then on the system uses it, with their words attached.

The flower shop is where I built it first, so my examples are flowers, but it isn't really about flowers. It could just as easily be a dispatcher who knows a road floods every spring, a buyer who can tell a supplier's about to go under, or a nurse manager who knows which shifts never fill.

A lot of how I built it came straight out of DDD.

I keep her exact words on every signal. The agent translates "opening too fast" into something the engine can use, but the original sentence stays with it, and that's what she sees when a recommendation cites it. She reads her own language in the ordering email, not mine. That's Evans's ubiquitous language, pretty much literally.

Each signal goes into one bounded context (vendors, quality, demand, seasonality or distribution) so a note about a vendor doesn't mess with seasonality and a note about demand doesn't touch quality scores. Words get to mean slightly different things in each one, which is fine. "Early" in seasonality is about the calendar. "Early" in distribution is about a truck.

Once she confirms a signal it doesn't change. If she changes her mind she just sends a new one. It looks roughly like this:

```python
@dataclass(frozen=True)
class FieldSignal:
    context: Literal["vendor", "quality", "demand", "seasonality", "distribution"]
    subject: str          # "garden roses", a vendor, a product
    her_words: str        # exactly what she sent
    effect: str           # what it changes, in the engine's terms
    observed_on: date
    review_by: date       # this week's market shouldn't steer next spring
```

`review_by` is the field I'd have skipped if I were building a normal knowledge base, and it ended up mattering the most. What people know goes stale. Flowers are extreme because the whole business runs on a calendar, but it happens everywhere. What a sales lead knows about a customer this quarter won't hold next year.

The read-back is the DDD conversation, shrunk way down. In DDD the model gets better because developers keep checking their understanding with the expert. Here the agent does a tiny version every time, basically "here's what I think you meant, right?" If it's off, she rewords it. It's cheap enough to happen every day, and that's what makes it work.

## If you're building one of these

A few things I'd tell myself at the start.

- Figure out who the expert actually is. It's almost never whoever owns the project. In a small business it's the owner. In a bigger company it's usually someone who's been on the floor for years and never gets invited to architecture reviews.
- Go to them. The florist texts. A dispatcher's probably in Slack. A field tech might send a voice memo. If sharing what they know means opening a dashboard, they won't.
- Keep their words, not just your version. Your structured interpretation will be wrong sometimes, and the original sentence is how you'll catch it.
- Sort out your bounded contexts before you write a single prompt. Decide what kinds of knowledge exist and what each one's allowed to change, and enforce that in code. Prompts are a bad place for it.
- Put an expiration on everything. Some of it's good for a week, some for a season, some for basically forever. Decide on purpose.
- Show people their knowledge getting used. When a recommendation cites her signal she trusts it more, and she catches mistakes faster.
- Treat the log as your actual knowledge base. Six months of confirmed, dated, scoped signals in the expert's own voice beats any wiki you could talk them into writing.

## Where I've landed

Naming this took longer than building the first version. Every name I tried and dropped had the same problem. It sounded like a one-time thing. Capture, extraction, onboarding. Those are projects with an end date, and the real world doesn't stop.

I think that's a big part of why so little has been written about it. We've treated knowledge as something you load in at build time, and people as a safety check on what comes out. We need both, and neither one keeps a system healthy after it ships. The people closest to the work see things change first, and most of what we build gives them nowhere to put that except a reject button.

The parts are all already here. DDD for modeling what experts know, machine teaching for treating them like teachers, agent memory for keeping things around, approval gates for safety. Agents just make it cheap enough to wire them together and keep them running, from a phone, between deliveries.

That's what I mean when I say I want to build systems that flourish. I want them to keep getting better because the people who know the work can keep teaching them.

If you've seen somebody do this well, or you're trying it yourself, I'd love to hear about it.
