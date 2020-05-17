---
layout: posts/post
author: Pramod Kotipalli
title:  Remembrance Agent
description: Java-based implementations of a remembrance agent, a continuously
  running automated information retrieval system, based on work by Bradley
  Rhodes of MIT Media Lab (1997). Available as a standalone, no-dependency
  Java/Gradle project and as a desktop graphical user interface (GUI) featuring 
  integrations with Google Cloud Speech APIs, Gmail, Google Drive, and 
  locally-stored plain text (.txt) or Markdown (.md) files. Open-source and 
  freely-available under the MIT License. Under active development.
tags:
    - note-taking
    - remembrance-agent
    - google-drive-api
    - gmail-api
    - symbiotic-artificial-intelligence
    - java
    - java-swing
    - desktop
    - gui
    - google-cloud-speech-api
subcategories:
    - design
    - engineering
    - research
image: /static/images/2019-07-29-remembrance-agent/remembrance-agent-logo.png
redirect_from: "/portfolio/ra/"
default_image_fullwidth: True
downloads:
    - name: 💻 GitHub (Remembrance Agent Java Gradle project)
      url: https://github.com/remembrance-agent/remembrance-agent.git
    - name: 💻 GitHub (Remembrance Agent Desktop GUI)
      url: https://github.com/remembrance-agent/remembrance-agent-desktop.git
    - name: 💻 macOS .dmg desktop application (v1.0.1)
      url: https://github.com/remembrance-agent/remembrance-agent-desktop/releases/download/v1.0.1/ra-desktop-v1.0.1-macos-dmg.zip
    - name: 💻 Windows .exe desktop application (v1.0.1)
      url: https://github.com/remembrance-agent/remembrance-agent-desktop/releases/download/v1.0.1/ra-desktop-v1.0.1-windows-exe.zip
---

# Remembrance Agents

The concept of a Remembrance Agent (RA) was first outlined by [Rhodes][rhodes-1997]{:target="_blank"} in 1997 as a system that would automatically present contextually-relevant notes, documents, and contacts.

In 1997, it became more evident that the perfect memory of computers could augment the evolutionarily-honed intuition of humans. Computers began to take more and more of a role in note-taking, planning, and managing contacts. However, all this information was typically not indexed in a way is useful to people; documents would need to be rememembered by file name and needed to be scanned through file structures when required. Rhodes sought to bridge this gap by conceptualizing and developing a wearable RA.

Rhodes focused their work on wearable RAs, systems that could live with you and help you live a more productive and information-rich life.

![]({{ page.image }})

# A Desktop RA

In this project, I implemented Rhodes' RA for use on any desktop computer.

As I do not wear head-worn displays consistently<sup>[Sep. 2019 correction: I do wear Glass consistently now]</sup>, I developed an RA features as it would be useful to me when I typically do use my computer, sitting at a desk working on emails or notes for class. I required integration with Google Drive and Gmail as it was where I took and saved most of my notes.

I didn't want to develop an API in the middle to minimize the risk of data breaches and unneeded complexity. Instead, I implemented a local-disk caching method that downloaded plain-text emails and documents that would then be indexed and stored locally. As an additional feature, I implemented a keylogger whose keystrokes would be recorded to a local file for later processing and use (this keylogger only logs keystrokes while the RA is active).

## Usage

Usage is streamlined for non-technical users. No knowledge of programming of editing of config files is required. A simple GUI presents all the features and settings you'd need to use:

![](/static/images/2019-07-29-remembrance-agent/client-with-suggestion.png)

As you type, [every five seconds][ra-query-period]{:target="_blank"} the prior 60 characters of your keyboard buffer are sent to the RA. Suggestions are presented as clickable buttons. To the left of each suggestion is the relevance score of that document [accounting for contextual factors][ra-engine-github]{:target="_blank"} like date and subject of a document (these factors can be re-weighted in the code as done by Rhodes). 

The core algorithm used to determine the similarity between two documents is TFiDF, or [Term-Frequency Inverse Document Frequency][tfidf-github]{:target="_blank"}: documents are weighted by both the frequency of a word in a document and the frequency of the word in the larger corpus of documents (i.e. a "document database" in this project's parlance).

Upon clicking the first button (my meeting notes with Professor Abowd at Georgia Tech), the RA client will open the corresponding Google Doc in Chrome:

![](/static/images/2019-07-29-remembrance-agent/chrome-opened-suggestion.png)


## Integrations

I use Gmail and Google Docs for communicating with everyone and for taking notes on everything, respectively. For this desktop RA, I needed integrations with Gmail and Google Drive that did not rely on a third-party API developed by me or others: I wanted a self-contained RA solution that could be deployed in a single-click with minimal dependence on the internet.

As such, a target Google Drive folder ID can be specified in the GUI of the RA client:

![](/static/images/2019-07-29-remembrance-agent/client-menu-open.png)

In addition, a maximum number of Gmail emails to index can be specified. All authentication is taken care of automatically by the Gmail and Google Drive API client libraries.

## Caching

Querying Google's Gmail and Drive APIs upon every restart would be computationally, network-wise, and time-wise extremely expensive. As such, upon requesting that the caches are invalidated, emails and documents are downloaded from Google and stored as plain text documents on disk. Reading from disk upon restarts is much faster than reading from online. Metadata about each file is also stored in a special `~metadata.json` file in the specified cache directory. I opted that this directory (and the one containing the `keylogger.log`) be synced to Google Drive through Google's Backup and Sync utility.

## Performance considerations

When architecting and implementing the library package `remembrance-agent`, I wanted to ensure that it would be memory and CPU efficent so it could be run on hardware like Google Glass. On such a small wearable platform, CPU clock speeds are measured in the hundreds of megahertz and RAM sizes are measured in the low single-digit gigabytes. Further, over-heating is a constant concern on such platforms.  

As such, used performance analysis tools like 

## Installation & Running

Usage and installation should be easy. As such, I made the process as simple as possible without use of a proper installer agent (the project is not ready for such formalities). In three steps:

1. Clone the project repository from Github
2. Build the project locally
3. Run the command `ra` from any terminal

Further instructions can be found on the [GitHub README][readme].


## Architecture

I closely followed the algorithms and data structures outlined in Rhodes' paper.

I separated the Remembrance Agent backend functionality from the presentation functionality. This resulted in two repositories:
1. [`remembrance-agent`][ra-repo]: This is a pure-Java (version 7) package with no dependencies that implements the "engine" of the RA. It provides an easy-to-use [interface][ra-interface] for setting up and querying an RA. It comes with a few standard databases implemented, including one that will index a choosen directory of your local disk.
2. [`remembrance-agent-desktop`][ra-desktop]: This package uses the `remembrance-agent` package as a dependency. It provides a Java Swing-based GUI for the RA. It implements a Google Drive- and Gmail-based document database as well as usage of our keystrokes or speech as input to the RA.

[rhodes-1997]:http://alumni.media.mit.edu/~rhodes/Papers/wear-ra-personaltech/
[ra-query-period]:https://github.com/remembrance-agent/remembrance-agent/blob/v1.2.1/src/main/java/io/p13i/ra/RemembranceAgentClient.java#L332-L337
[ra-engine-github]:https://github.com/remembrance-agent/remembrance-agent/blob/v1.2.1/src/main/java/io/p13i/ra/engine/RemembranceAgentSuggestionCalculator.java
[tfidf-github]:https://github.com/remembrance-agent/remembrance-agent/blob/v1.2.1/src/main/java/io/p13i/ra/utils/TFIDFCalculator.java
[readme]:https://github.com/remembrance-agent/remembrance-agent/blob/master/README.md
[ra-repo]:https://github.com/remembrance-agent/remembrance-agent
[ra-interface]:https://github.com/remembrance-agent/remembrance-agent/blob/f061e14770e2aa8c0e79dcefb654b9d28c6325e3/src/main/java/io/p13i/ra/engine/IRemembranceAgentEngine.java#L17-L38
[ra-desktop]:https://github.com/remembrance-agent/remembrance-agent-desktop