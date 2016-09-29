# meetingbot

meetingbot sends a reminder a day before and on the day of the Rust Community
Team meeting (Wednesday 4PM UTC). The reminder contains a link to the proposed
meeting agenda and the previous meeting minutes.

This is achieved using the following:
- [cathulhu][1] - github client written in Rust.
- [bottymcbottyface][2] - a collection of irc bot(s) written in Rust.
- `git` - to pull a copy of the [team][3] repo which hosts the meeting minutes.
- GNU `date` - to perform date arithmetic.
- A shell script to parse the input from cathulhu and git.
- A crontab entry

At the time of writing meetingbot is running on @booyaa's raspberry pi at home.

# setup

## requirements

- A GitHub Personal Access Token (public repo access). You can get one [here][4].

You'll need the minimum versions of these tools to run meetingbot.

- rustc 1.11.0 (9b21dcd6a 2016-08-15)
- cargo 0.12.0-nightly (6b98d1f 2016-07-04)
- git version 2.1.4
- date (GNU coreutils) 8.23
- cathulhu 0.1.1
- mouthpiece (bottymcbottyface v0.1.2)

n.b. rust and friends installed using rustup 0.6.3 (a0e2132 2016-08-28).
n.b. `date` must be the GNU version. The script is reliant on the `--date` flag
for date arithmetic. MacOS/OSX won't work because they implement BSD's version.

## installation
```
git clone https://github.com/rust-community/meetingbot.git
cd meetingbot
cargo install cathulhu
cargo install --example mouthpiece bottymcbottyface
```

## crontab

Add the following two lines to your crontab (amend values to match your own
environment)

```
# runs 4pm on tuesdays and wednesday (also needs the following env for now)
CATHULHU_GH_PAT=your_personal_access_token
0 16 *   *   2,3   /path/to/meetingbot/doit.sh
```

# requests/bugs/feedback

please raise an [issue][5].

# background

> < carols10cents> booyaa: can you make an irc bot for rust-community that, 1 day and 1 hr before each community meeting, posts a link to the meeting agenda and previous meeting's logs?

# license

Apache2 as per Rust Community [team][3] repository.

[1]:https://github.com/booyaa/cathulhu
[2]:https://github.com/booyaa/bottymcbottyface
[3]:https://github.com/rust-community/team
[4]:https://github.com/settings/tokens
[5]:https://github.com/rust-community/meetingbot/issues/new
