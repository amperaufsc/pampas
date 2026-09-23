# Onboarding

> Disclaimer: this is a work in progress, so there might be missing content. If you have questions, ask your Head for help.

This page is dedicated for new members of the Ampera Electrical FSAE team that are part of the Driverless subteam.

Here you're going to find the material you should study during your training process. You don't need to master the contents linked here, but it's important you get a good grasp of the basics, and as such the resources here are at the introductory level.

The sections are ordered in the recommended order of study and divided in weeks, and the whole course spans 9 to 10 weeks.

You're going to be formally introduced to this material by your Head, very likely during a shift.

---

## Week 1 — Linux & Dev Environment

In the first week of your training, you're going to learn how to setup a Linux environment and how to interact with a terminal. This is fundamental knowledge for Driverless because our systems run on Linux, and often we have to work with only the terminal without the help of guided user interfaces (GUIs), the graphical windows that you're used to see in your computer.

The goal of this week is for you to have a functional Linux environment and become comfortable with the terminal.

### Setup Linux

There are many ways we can setup a Linux environment: installing to disk, using a virtual machine, spinning up a container or even accessing remotely a machine that runs Linux. This list is not exhaustive.

If you're a long time Windows user and not ready to do a full migration over to Linux, you can start with something called Windows Subsystem for Linux (WSL). It's basically a virtual machine that runs Linux and exposes a terminal window for you to interact with it.

Just follow the installation instructions provided by the official docs:

- WSL2 install guide (Windows users): [Microsoft docs](https://learn.microsoft.com/en-us/windows/wsl/install)

Now, if you want a native Linux experience, we recommend you actually install a Linux operating system in your hard drive. There's a catch though. Windows is an operating system that is provided uniquely by Microsoft and that has only a single "flavour" per version. That is, you don't have a choice of a different Windows 11 other than what Microsoft provides (legally).

Linux is different. Linux has many distributions: versions that are configured differently, have different looks and tools, are installed in different ways and are provided by different people/organizations.

It's not in the scope of this guide to describe each Linux _distro_ (short for distribution), we'll point you to this tutorial for that:

- Linux Journey Tutorial: [Getting started](https://labex.io/linuxjourney/courses/getting-started)

It doesn't really matter which distro you chose, but if you're an absolute beginner we recommend either the latest Long Term Support (LTS) version of Ubuntu or Linux Mint. It's usual for people in Driverless to work with Ubuntu, both because it's the most popular disto in the world (I think), and because it comes pretty much pre-configured for you.

If you have enough space in your hard drive, or have a second one that is installed but not really being used, you can install Ubuntu alongside Windows. There is an infinite number of tutorials on the internet on how to install Ubuntu, but we prefer to point you to the official docs:

- Ubuntu install guide: [Canonical docs](https://ubuntu.com/tutorials/install-ubuntu-desktop)

Make sure that you have a working Linux environment before you proceed to the next section.

### Trainee in the Shell

Ok, now it's time to open the terminal and look like a hacker.

On Ubuntu, we can use the application launcher search function by pressing the SUPER button on the keyboard (aka the Windows button) and typing "terminal". Alternatively, you can aura farm by using a shortcut: `ctrl + alt + t`.

That's as far as I'm going. I'll leave the rest to a much more professional guide on the terminal and shell:

- MIT Missing Semester — [Course Overview + Introduction to Shell](https://missing.csail.mit.edu/2026/course-shell/)

- MIT Missing Semester — [Command-line Environment](https://missing.csail.mit.edu/2026/command-line-environment/)

These links are from [The Missing Semester of Your CS Education (2026)](https://missing.csail.mit.edu/), an excellent guide by the MIT on computer science stuff you should learn, but that is not usually taught in university. Now we know not all trainees of Driverless are in the computer science course, you may be in any kind of engineering, maybe even mathematics or physics. Regardless, the material presented there is very useful for any STEM student, not limited to whether you're going to work with code or not.

There is a video and a written material. I recommend watching the video then reading the text. If you're confident you already know what you're watching, still watch the video but skip the parts you're familiar with. There are some less common things being shown and taught that even a long time Linux user might not know or remember.

Mind you there is a list of exercises after the text, at the bottom of each of those pages. They are not mandatory, but we recommend you read through them and try to solve some. 

Try to do it with only the information you got from the class. If you're having a hard time, use `man` or `tldr` to see the documentation of the command you're using. If it's still too hard, search up some examples. As a final resource, ask an AI for tips. Avoid going straight for the answer without having tried at least 10 different ways. It might not be enough, but is through that process, repetition, that you start learning what you're doing.

Ah, and of course, if there's a colleague nearby, ask away! Don't be shy :)

### Choosing an editor

In Driverless, there's a very high chance you'll need to interact with code -- or at least some kind of config file in your Linux machine -- and you'll want to use some kind of text editor for that; and I'm not talking about formatted text editors like Word and Google Docs.

It's common for programmers to use IDEs (Integrated Development Environments), that are basically text editors with a bunch of nice extras that help you write code. The most well known of them is [VsCode](https://code.visualstudio.com/).

There is a class about that in the MIT course:

- MIT Missing Semester — [Development Environment and Tools](https://missing.csail.mit.edu/2026/development-environment/)

The first half of that class is basically about Vim. You can use it if you want, though know that you might have to spend a significant amount of time getting used to it and configuring it to attend your needs. If you have that time and will, go for it.

The second half happens on VsCode and talks about language servers, type checking, how to navigate to quickly navigate between references in your code etc. This part is more important, so if you want to skip the part about Vim, that's ok.

Besides VsCode, other very feature complete IDEs are [Zed](https://zed.dev/), the [Jetbrains IDEs](https://www.jetbrains.com/ides/#choose-your-ide), and a bunch of others. Feel free to test them and chose whichever you prefer. Most folks in Driverless end up chosing VsCode for its ease of use.

---

## Week 2 — Git & GitHub

Coming soon.

<!--**Resources:**

- [Pro Git Book — Chapters 1-3](https://git-scm.com/book/en/v2)
- [Atlassian Git Tutorials — Branching & Merging](https://www.atlassian.com/git/tutorials/using-branches)
- [Oh My Git! (interactive game)](https://ohmygit.org/)

**Focus on:** commits, branching, merge vs. rebase, resolving conflicts hands-on. Skip: submodules, advanced history rewriting.

**Team workflow:**

- [ ] TODO: link to our branching strategy / PR conventions
- [ ] TODO: link to our GitHub repo structure and issue board

**Checkpoint exercise:** TODO — give them a repo pre-built to produce a merge conflict, have them resolve it and open a PR.-->

---

<!--## Week 3 — Language Refresher (C++/Python for Robotics)

Coming soon.

**Resources:**

- TODO: link based on team's primary language
- If C++: [LearnCpp — pointers/memory sections](https://www.learncpp.com/), CMake basics guide
- If Python: virtual environments (`venv`/`conda`), packaging basics

**Focus on:** what's different from intro CS courses — build systems, memory management (C++) or environment management (Python). Skip basic syntax they already know.

**Checkpoint exercise:** TODO

---

## Week 4 — Driverless Overview & System Architecture

_No external resources here — this is entirely team-specific._

- Full pipeline walkthrough: perception → SLAM → path planning → control → actuation
- Our sensor suite (cameras, LiDAR, IMU, encoders, GPS)
- Competition rules relevant to driverless (FSG/FS-AI — link rulebook)
- Past competition footage/logs

**TODO:** slides or recorded walkthrough link, sensor datasheet links, rulebook link.

---

## Week 5 — Intro to ROS2

**Resources:**

- [ROS2 Official Tutorials — Beginner: CLI Tools](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools.html)
- [ROS2 Official Tutorials — Beginner: Client Libraries](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries.html) (publisher/subscriber, services)

**Focus on:** nodes, topics, services, launch files, parameters. Skip: actions and lifecycle nodes for now (cover later if relevant).

**Team setup:**

- [ ] TODO: link to our ROS2 workspace setup / repo

**Checkpoint exercise:** TODO — write a simple pub/sub node pair.

---

## Week 6 — ROS2 Deep Dive + Simulation

**Resources:**

- [ROS2 TF2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [Gazebo / our sim environment docs] — TODO link
- [RViz2 user guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

**Focus on:** TF2 (transforms) — budget extra time here, it trips everyone up. `ros2 bag` for logging/replay.

**Checkpoint exercise:** TODO — visualize a TF tree or replay a bag file in RViz.

---

## Week 7 — Perception Basics

**Resources:**

- TODO: camera/LiDAR calibration intro links
- TODO: cone detection approach overview (link to our method: classical CV vs. learned)

**Focus on:** what our stack actually uses — don't survey the whole field.

**Checkpoint exercise:** TODO

---

## Week 8 — Planning & Control Basics

**Resources:**

- TODO: path planning intro (matched to our approach — occupancy grid / spline-based / etc.)
- TODO: PID intuition resource

**Focus on:** how planning/control consume perception output — the interfaces matter more than the theory depth at this stage.

**Checkpoint exercise:** TODO

---

## Week 9 — Integration Project

Small end-to-end challenge combining prior weeks, e.g.: subscribe to simulated cone detections, publish a simple path.

- [ ] TODO: define the capstone task
- [ ] TODO: pair each freshman with a subteam mentor for next steps after onboarding

**Final shift:** short presentations/demos.

---

## Maintainer Notes

_(Remove this section before publishing, or keep as an internal wiki note)_

- Replace all TODOs with team-specific links before first use.
- Resources should be re-checked yearly (docs versions, dead links).
- Consider tracking completion of checkpoint exercises per person via the wiki or a shared board.-->
