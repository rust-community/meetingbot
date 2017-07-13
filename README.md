# meetingbot v1.0.0

meetingbot is a reminder robot for the Rust Community Team irc channel.

It currently sends reminders for:

- Mondays 4PM UTC check the Friends of the Forest thread on URLO
- Tuesdays and Wednesday 4PM and 10PM UTC for the weekly meeting on Wednesday.

This is achieved using the following:
- [cathulhu][1] - github client written in Rust.
- [hashpipe][2] - a pipe based irc client written in Rust
- GNU `date` - to perform date arithmetic.
- A job/task script that determines what logic to carry out for the type of reminder we wish to send
- A crontab entry

At the time of writing meetingbot is running on @booyaa's raspberry pi at home.

# setup

## requirements

- A GitHub Personal Access Token (public repo access). You can get one [here][4].

You'll need the minimum versions of these tools to run meetingbot.

- rustc 1.11.0 (9b21dcd6a 2016-08-15)
- cargo 0.12.0-nightly (6b98d1f 2016-07-04)
- date (GNU coreutils) 8.23
- cathulhu 0.1.1
- hashpipe v0.1.2

n.b. rust and friends were installed using rustup 0.6.3 (a0e2132 2016-08-28).

n.b. `date` must be the GNU version. The script is reliant on the `--date` flag
for date arithmetic. MacOS/OSX won't work because they implement BSD's version.

## installation

```
git clone https://github.com/rust-community/meetingbot.git
cd meetingbot
cargo install cathulhu
cargo install hashpipe
```

## setup

crontab -e
read in meetingbot.crontab
amend the following variables, to match your own tokens and file locations

- `CATHULHU_GIT_REPO` - this should be a sub-directory in your meetingbot installation.
- `CATHULHU_CARGO_BIN` - where cathulhu and mouthpiece were installed.


amend the path to the `meetingbot` directory in the crontab jobs

# requests/bugs/feedback

please raise an [issue][5].

# background

> < carols10cents> booyaa: can you make an irc bot for rust-community that, 1 day and 1 hr before each community meeting, posts a link to the meeting agenda and previous meeting's logs?

# license

Apache2 as per Rust Community [team][3] repository.

[1]:https://github.com/booyaa/cathulhu
[2]:https://github.com/LinuxMercedes/hashpipe
[3]:https://github.com/rust-community/team
[4]:https://github.com/settings/tokens
[5]:https://github.com/rust-community/meetingbot/issues/new
