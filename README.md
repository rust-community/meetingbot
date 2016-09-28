# meetingbot

meetingbot sends a reminder a day before and on the day of the Rust Community
Team meeting (Wednesday 4PM UTC). The reminder contains a link to the proposed
meeting agenda and the previous meeting minutes.

This is achieved using the following:
- [cathulhu][1] - github client written in Rust.
- [bottymcbottyface][2] - a collection of irc bot(s) written in Rust.
- git - to pull a copy of the [team][3] repo which hosts the meeting minutes.
- A shell script to parse the input from cathulhu and git.
- A crontab entry

At the time of writing meetingbot is running on @booyaa's raspberry pi at home.

# setup

## requirements

- A recent version of git and Rust and friends (rustc, cargo etc).
- A GitHub Personal Access Token (public repo access). You can get one [here][4].

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
[1]:https://github.com/booyaa/cathulhu
[2]:https://github.com/booyaa/bottymcbottyface
[3]:https://github.com/rust-community/team
[4]:https://github.com/settings/tokens
[5]:https://github.com/rust-community/meetingbot/issues/new
