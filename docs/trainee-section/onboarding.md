# Onboarding

> Disclaimer: this is a work in progress, so there might be missing content. If you have questions, ask your Head for help.

This page is dedicated for new members of the Ampera Electrical FSAE team that are part of the Driverless subteam.

Here you're going to find the material you should study during your training process. You don't need to master the contents linked here, but it's important you get a good grasp of the basics, and as such the resources here are at the introductory level.

The sections are ordered in the recommended order of study and divided in weeks, and the whole course spans 9 to 10 weeks.

You're going to be formally introduced to this material by your Head, very likely during a shift.

---

## Week 1

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

The first half of that class is basically about Vim. You can use it if you want, though know that you might have to spend a significant amount of time getting used to it and con#figuring it to attend your needs. If you have that time and will, go for it.

The second half happens on VsCode and talks about language servers, type checking, how to navigate to quickly navigate between references in your code etc. This part is more important, so if you want to skip the part about Vim, that's ok.

Besides VsCode, other very feature complete IDEs are [Zed](https://zed.dev/), the [Jetbrains IDEs](https://www.jetbrains.com/ides/#choose-your-ide), and a bunch of others. Feel free to test them and chose whichever you prefer. Most folks in Driverless end up chosing VsCode for its ease of use.

---

## Week 2

### Gitting Good

If you're going to work on any halfway serious project (especially a software one), even one built solely by you, you'll use Git. My guess is that in software development, Git is the most used tool of all.

Git is a version control tool that gives a team a bunch of benefits while developing a project, such as:

- Knowing what changes were made to the project, when, by whom, and why.
- Going back to a known previous version if the project moved forward in an undesirable way.
- Letting several people collaborate on the same project artifact, asynchronously, with no need for an internet connection while making changes.
- Working on more than one version of the project at the same time, easily switching between them or merging the changes from each into a single version.
- Syncing the changes made by each member of the project without having to keep sending zips by email.

And plenty of others that will become obvious along the guide and your learning process with the tool.

#### Resources

Most important information of all: Read the Git manual! The manual includes everything mentioned in this guide plus basically everything else you might want to know about Git.

The manual is available on its official page. Alternatively, on Linux and MacOS, you can open it in your terminal with `git --help` or `man git`, if you have the `man` package installed (I recommend it).

The manual is the source of truth, but there are plenty of other resources that are more friendly and you should use to learn the tool. For now, let's continue on in the Missing Semester course, with the [class on version control and git](https://missing.csail.mit.edu/2026/version-control/).

There is also an [in-house guide](https://github.com/amperaufsc/git-guide/) -- created for a live git workshop -- that you can have a read on. A part of this guide here was insipired on it.

Besides those, here are some other resources you can use to practice version control with git:

- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials/)
- [Learn Git Branching](https://learngitbranching.js.org/)
- [Oh My Git! (interactive game)](https://ohmygit.org/)

### Managing projects on GitHub

GitHub is basically a cloud storage for git projects. It makes collaboration by multiple people on the same project a much easier task by offering a bunch of tools we can use to organize the work.

#### Issues

An issue is a unit of work registered on GitHub: something to be built, fixed or figured out. In Driverless, we type issues as follows:

- **Epic:** a big chunk of work that can span multiple weeks. Epics are not worked on directly, they're broken down into tasks.
- **Task:** a piece of work that can be done in a single week, since we work in weekly sprints. If a task doesn't fit in a week, that's a sign it should be subdivided into smaller tasks (or that it's actually an epic in disguise).
- **Bug:** something that's broken and needs fixing.

If you've already had some contact with the Open Source world, you're going to notice the way we type our issues is a bit different than what you usually see in other public repositories. The reason we divide them this way is because our project works in yearly seasons, with a well established timeplan, and so dividing up work by size works better for us.

Normally, projects that are community contributed don't have the luxury of coordinating everyone involved with timely meetings and scheduled shifts, so they rely more on different issue types and other metadata.

Issues also use **labels**, most of them referring to the modules of the team's projects. For example, `perception` for issues related to the perception module, or `actuator` for issues related to the steering or brake actuators. Use them! They make it much easier to find who should look at what.

To make documenting easier, issues have **templates** for different purposes. Pick the right one and fill it in, future you (and your teammates) will thank you.

Every issue should also have an **assignee**: whoever is responsible for getting it done. Unassigned issues tend to sit around forever because everyone assumes someone else has it.

The workflow goes like this:

1. Create an issue as a **sub-issue of an epic**. Orphan tasks make it hard to see the bigger picture.
2. Create a branch for that issue **from `main`**. GitHub can also create the branch for you straight from the issue page, which handles the linking too.
3. Work on it, committing as you go (conventional commits, remember?).
4. Open a pull request when you're done (or as draft when it's ready for eyes).

Epics should be created by the Head of the area, as they define most of the long plan work of the team. Talk to you Head if you have any difficulties classifying issues and organize them.

#### Pull Requests

The pull request is how your work gets from your branch into `main`. Everything you learned about opening PRs in the Git guide applies here, plus a few team rules:

- `main` is **protected**, which means nobody can push to it directly. The only way in is through a pull request.
- Every PR needs **at least one approval from another team member** before it can be merged into `main`. Yes, even if you're sure it's fine. Especially if you're sure it's fine.
- PRs also have **templates**. Fill them in! The goal is to properly document the proposed solution: what was done, why it was done that way, and how to check that it works. A PR with an empty description is a PR nobody wants to review.
- **Link the PR to its issue.** Writing `Closes #123` in the PR description connects the two and automatically closes the issue when the PR is merged.
- **Assign the PR** to yourself (the author), and request a review from a teammate.
- Not done yet but want early feedback? Open a **draft PR**. It signals that the work is in progress and isn't ready to be merged, but lets others take a look and comment along the way. When it's ready, mark it as ready for review.
- **Clean up after yourself.** Once your PR is merged, delete the branch. GitHub offers a button for that right after the merge, and it keeps the branch list from turning into a graveyard.

#### The Projects tab

The Projects tab is where we track and plan our work. It has different views, each with its own purpose.

##### Board view

This is the one you'll use the most. It only shows **task** type issues, and it's used both to plan the sprint and to track its progress while it's happening.

The board is divided into 5 columns:

- **Backlog:** tasks that exist but aren't planned for this sprint.
- **Ready:** the sprint backlog. These are the tasks we committed to for the current week.
- **In progress:** someone is working on it right now.
- **In review:** there's an open PR waiting for approval.
- **Done:** merged and finished.

The sprint planning starts at the weekly meeting and is refined during the first shift after it, usually on the same day. That's when tasks get moved to Ready, sized properly (or split) and assigned.

##### Sprint view

A roadmap view that shows which issues are part of each iteration (sprint). Useful for getting the big picture of what was done, and what's planned, week by week.

##### Epic view

Also a roadmap view, but for epics. Epics are not assigned to iterations, since they span multiple weeks. Instead, they have a **start date** and a **target date**, so you can see at a glance how the larger pieces of work line up over time.

#### What about unfinished tasks?

Tasks that don't make it to Done by the end of the sprint are **not carried over** automatically. They stay open, which makes them visibly late so the team can prioritize them in the next planning. If a task keeps showing up as late, that's usually a sign it's too big and should be split.

---

## Week 3

Alrighty. With linux, a text editor/IDE and git, we have almost the whole development environment setup. The only thing we're missing now is a programming language. 

### Python

Coming soon.

<!--
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
