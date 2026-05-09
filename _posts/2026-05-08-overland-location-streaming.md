---
title: "Streaming my location data with Overland"
date: "2026-05-08"
categories:
  - engineering
  - writing
tags:
  - overland
  - telemetry
  - location
  - systems
  - "c++"
layout: post
author: Pramod Kotipalli
description:
  WIP tour of using Overland for iOS with
  overland.trycopilot.ai and the C++ systems behind the live
  location viewer.
---

How does a phone's continuous trail of location updates
become a useful personal memory system?

This is the question I have been exploring with Overland. A
phone is already a very good sensor package: it has GPS,
network access, a clock, battery management, and a user who
usually remembers to carry it. What I wanted was not another
map application, but a simple way to turn that stream of
facts into something durable, queryable, and visible from a
browser.

**WIP note:** Overland is an active build. This post
describes the current prototype I am using to collect my own
location stream, view it on the web, and test some systems
ideas behind high-speed telemetry collection.

If you want to try the current prototype, open
[overland.trycopilot.ai](https://overland.trycopilot.ai/).
Install
[Overland for iOS](https://apps.apple.com/us/app/overland-gps-tracker/id1292426766),
copy the Receiver endpoint URL shown in the web app, paste
it into the iOS app, and start sending updates into your own
track.

The iOS app I use here is
[Overland GPS Tracker](https://apps.apple.com/us/app/overland-gps-tracker/id1292426766),
written by [Aaron Parecki](https://aaronparecki.com/). My
work in this post is the receiver, storage, and web viewer
at `overland.trycopilot.ai`. The upstream source code is
available in
[aaronpk/Overland-iOS](https://github.com/aaronpk/Overland-iOS).

{% comment %} TODO(overland-screenshot): Add screenshot of
the overland.trycopilot.ai setup card showing the Receiver
endpoint. {% include _post_image.html
  src="TODO"
  text="TODO: Overland setup card showing the Receiver endpoint URL." %} {% endcomment %}

I am intentionally keeping the personal data in this post
high-level. The point here is not where I went on any
particular day. The point is the shape of the system: a
mobile device produces small measurements over time, and a
web service turns those measurements into a live personal
record.

## Background

In the past, I have written about remembrance agents,
wearable computers, and human-computer interaction systems
that run continuously in the background. Those systems are
interesting to me because they are not tools you use for one
moment and then put away. They change the boundary between
what a person remembers and what a computer can quietly
preserve.

Location is a natural part of that story. Where I was is
often useful context for what I was doing, who I was
meeting, or what kind of day I was having. In other words,
location is not just a point on a map. It is metadata for
life.

By telemetry, I mean the process of collecting small
measurements from a system over time. In this case, the
system is not a server or a robot. The system is my own
movement through the world, sampled by my phone and sent to
a web service I control.

This is where Overland comes in. Overland for iOS is the
upstream mobile GPS logger that already knows how to collect
location updates and send them to a receiver endpoint.
`overland.trycopilot.ai` is my server-side receiver, storage
layer, and browser for that stream.

## Overview of the data flow

{% comment %} TODO(overland-screenshot): Add screenshot of
the live overland.trycopilot.ai dashboard.
{% include _post_image.html
  src="TODO"
  text="TODO: Live Overland dashboard showing setup, history, and recent samples." %} {% endcomment %}

At a high level, the system is straightforward:

1. Overland for iOS batches location updates on the phone.
2. The phone sends those updates to
   `overland.trycopilot.ai`.
3. The web service validates the request and appends each
   sample to storage.
4. The browser loads history for a selected user and track.
5. A live stream can tail new samples as they arrive.

The public hostname is routed to `overland-service`, and the
service is built from this target in the `cs` monorepo:

```text
//cs/apps/web/trycopilot.ai/overland:main
```

The service exposes three important surfaces:

```text
POST /api/overland/?user_uuid=...
GET /api/overland/stream/
GET /*
```

The first route ingests samples. The second route streams
new samples to the browser. The final catch-all route
renders the web UI: setup instructions, history, the map,
recent samples, filters, and live controls.

This division is useful because it keeps the system easy to
reason about. One route writes the stream. One route tails
the stream. One route explains and visualizes the stream.

## Ingestion

The ingestion endpoint accepts `application/json`. The most
important payload is the GeoJSON-style shape sent by
Overland for iOS. It contains a `locations` array, where
each entry is a `Feature` with point geometry and timestamp
properties.

For example, the structure of the incoming data is roughly:

```text
locations[]
  geometry.coordinates[0]  longitude
  geometry.coordinates[1]  latitude
  properties.timestamp
  properties.altitude
```

Before writing anything, the service performs the basic
checks that make the stream trustworthy:

- The content type must be JSON.
- The batch must contain at least one location.
- The geometry must describe a point.
- The timestamp must include timezone information.
- Latitude must be within `[-90, 90]`.
- Longitude must be within `[-180, 180]`.
- Altitude can be omitted and will default to zero.

These checks are deliberately simple. They are not trying to
infer meaning from the trip or decide whether a point is
interesting. They only decide whether the data is shaped
well enough to enter the append-only record.

After validation, the service appends each sample into the
`overland_updates` collection. The response includes a
record UUID, the user UUID, the number of samples accepted,
and a track path that can be opened in the web UI.

## The record format

The core record is small:

```text
UserPosition
  user_uuid
  timestamp.unix_micros
  position.latitude
  position.longitude
  position.altitude
```

`user_uuid` and `timestamp.unix_micros` are indexed. This is
the main design choice in the data model. Most of the useful
questions about a personal location stream are questions
about identity and time:

- What are the newest samples for this user?
- What did the selected track look like in this time window?
- Which users have recent samples?
- Where should the live stream resume?

In other words, the model is small because the access
pattern is clear. The service does not need to solve every
future geospatial query to be useful. It needs to reliably
write points and quickly recover points by user and time.

This also keeps the hot path understandable. A location
update is validated, serialized, and appended. The database
record becomes the durable fact. Later views can interpret
that fact in different ways.

## The live stream

The live viewer uses server-sent events:

```text
GET /api/overland/stream/
```

When the browser opens the stream, the service resolves the
user, parses cursor parameters, and begins tailing newer
records. The cursor is made from `cursor_unix_micros` and
`cursor_record_uuid`. The timestamp orders the stream, and
the record UUID breaks ties when multiple points have the
same timestamp.

Each emitted event contains the record UUID and the
serialized sample. The browser can then update the recent
samples table, map state, and live status without reloading
the page.

There are a few small mechanisms that matter here:

- Server-sent events keep the browser integration simple.
- Retry hints tell the browser how quickly to reconnect.
- Heartbeats make quiet periods visible to the connection.
- Record UUID dedupe protects against overlap between
  polling windows.
- Bounded fetch limits keep each tail query small.

This is not a fully general realtime database. It is a
practical tail over an indexed append-only collection. That
tradeoff is intentional. For a personal telemetry stream, I
care more about a system I can understand and operate than a
system that sounds more sophisticated than it needs to be.

## The browser

{% comment %} TODO(overland-screenshot): Add screenshot of
the overland.trycopilot.ai map, history, and live-stream
view. {% include _post_image.html
  src="TODO"
  text="TODO: Overland map and history view with live-stream controls." %} {% endcomment %}

The web page has two jobs. First, it should help me set up
the phone. Second, once samples exist, it should let me
understand the track.

The setup card shows the Receiver endpoint URL for Overland
for iOS. It also shows a device id field. The important
value is the receiver URL tied to the resolved user.

Once data exists, the page becomes a small location
workbench. It shows my Overland history, renders the
selected track on a map, lists recent samples, and lets me
filter by time. The live switch lets the page follow the
tail of the stream while keeping the selected track visible.

This is the part that makes the system feel less like a log
file. A log file preserves facts, but a browser can turn
those facts back into a human-readable memory aid.

## Why this architecture works for telemetry

The important design idea is that telemetry should be boring
on the write path.

For example, a phone may send points while moving through
bad network conditions. It may send small batches. It may
retry. The server should not need a complicated transaction
for each point. It should validate the payload, append the
facts, and return enough information for the client and UI
to continue.

Append-only writes are a good fit because location samples
are events. Replacing the latest position would throw away
history. Updating a giant aggregate on every request would
make ingestion more fragile. Keeping each point as a small
record makes the system easier to inspect, replay, and
stream.

The indexed fields are similarly conservative. Indexing the
user and timestamp gives the service the main ordering it
needs without turning the first version into a large
geospatial database project. The map view can be useful even
when the backend is still just storing a typed stream of
points.

The live stream follows the same pattern. It does not
require every client to subscribe to an elaborate pub/sub
system. It can ask for records newer than a cursor, emit
what it finds, remember record UUIDs it has already sent,
and try again. This is not the only way to build realtime
telemetry, but it is a very good first shape because its
failure modes are visible.

## The surrounding trycopilot.ai system

Overland is also useful as a test case for the larger
trycopilot.ai service fleet. It reuses the same kind of
infrastructure as the other apps:

- `cs/net/http` provides requests, responses, routing, and
  server-sent event helpers.
- The database service provides the typed client and query
  model.
- The proto layer gives Overland compact C++ data structs
  that serialize to JSON and declare indexed fields.
- The common website layer provides navigation, domain
  resolution, auth redirects, health checks, load endpoints,
  and shared page rendering.
- Docker Compose and the routing table connect
  `overland.trycopilot.ai` to `overland-service`.
- Remote logging records events such as rejected ingest,
  successful ingest, stream opens, and page renders.

This matters because Overland is not just a script sitting
next to a database. It is a small production-shaped service.
That makes it a better experiment. If the pattern works for
location, the same shape can be adapted for other telemetry
streams.

## Limitations and next steps

The WIP caveat is real. This is not yet a polished
general-purpose location platform. I do not want to imply
that it has solved every privacy, retention, battery, auth,
or large-scale geospatial query problem.

What it does have is the core loop I wanted:

1. A phone samples my movement.
2. The service receives a small typed payload.
3. The database stores append-only records.
4. The browser renders history and can tail new samples.

That loop is already useful. It gives me a personal location
memory system and a concrete place to test high-speed
telemetry ideas in a real web app.

For me, the next interesting work is not to make the system
look bigger than it is. It is to keep tightening the parts
that matter: better setup, clearer failure modes, stronger
privacy controls, and more robust ways to summarize long
tracks without losing the original stream.
