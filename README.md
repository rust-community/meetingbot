# meetingbot v1.0.1

meetingbot is a reminder robot for the Rust Community Team IRC channel on the
Mozilla network.

It currently sends reminders (an hour before) for:

- Mondays 4pm UTC check the Friends of the Forest thread on URLO
- Tuesday 4:30pm UTC for the content team meeting on Tuesday (alternating weeks to main meeting).
- Wednesday 4pm UTC for the main meeting on Wednesday.
- Wednesday 4pm UTC for the events team meeting on Tuesday (alternating weeks to main meeting).
- Thursday 4pm UTC for the switchboard team meeting on Tuesday (alternating weeks to main meeting).

This is achieved using the following:

- [hashpipe][1] - a pipe based irc client written in Rust
- A job/task script that determines what logic to carry out for the type of reminder we wish to send
- A crontab entry

At the time of writing meetingbot is running on @booyaa's raspberry pi at home.

## Adding a new reminder

- Add your message (these variables prefixed with `MSG_`)
- Add your schedule, if you're not famililar with the crontab format, use [crontab.guru](https://crontab.guru).

If you need more exotic schedules i.e. alternating weeks you can use something
similar to what's being used by the community team and its sub-teams:

```shell
[ $(( `date +\%W` \%2 )) -eq 0 ] && ...reminder script
```

This would trigger the script on week numbers divisible by 2 with no remainder.

## Contributing

### Requirements

You'll need the minimum versions of these tools to run meetingbot.

- rustc 1.11.0 (9b21dcd6a 2016-08-15)
- cargo 0.12.0-nightly (6b98d1f 2016-07-04)
- hashpipe v0.1.2

n.b. rust and friends were installed using rustup 0.6.3 (a0e2132 2016-08-28).

### Installation

```shell
git clone https://github.com/rust-community/meetingbot.git
cd meetingbot
cargo install hashpipe
```

### Setup

- crontab -e # edit crontab
- read in meetingbot.crontab
- amend the following variables, to match your own tokens and file locations

amend the path to the `meetingbot` directory in the crontab jobs

## Requests/Bugs/Feedback

please raise an [issue][3].

## Background

> < carols10cents> booyaa: can you make an irc bot for rust-community that, 1 day and 1 hr before each community meeting, posts a link to the meeting agenda and previous meeting's logs?

## License

Apache2 as per Rust Community [team][2] repository.

[1]:https://github.com/LinuxMercedes/hashpipe
[2]:https://github.com/rust-community/team
[3]]:https://github.com/rust-community/meetingbot/issues/new
