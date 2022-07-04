#!/usr/bin/env python3

# Imports
import re
import sys
import argparse

# Custom
try:
    import slackTools.slackTools as core
except:
    import slackTools as core

# Negates execution from importing slack_tools as a library
if __name__ == "__main__":

    # Parse Input Arguments
    parser = argparse.ArgumentParser(
        description="Link your program's progress to Slack!"
    )
    parser.add_argument('title', nargs='?',  type=str, default=None, help='Number of training samples (ex: 1000)')
    parser.add_argument('-m ', '--messageOnly', action='store_true', default='store_false', help='Send a singular message')
    parser.add_argument('-s ', '--strip', action='store_true', default='store_false', help='Surpress notification messages (ex: init and destruction of slackTools)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Surpress echo of stdin to Slack')
    parser.add_argument('-e', '-r', '--regex_events', nargs='+', help='Parse stdin for a specific event using a regex (ex: keyword END or accuracy >80 percent with acc=[8-9]\d|\d{3,} )')
    parser.add_argument('-n', '--notify_users', nargs='+', help='[Optional] Specify users to mention in slack when an event occurs. If unspecified or empty, will use default from slack.key')
    parser.add_argument('-k', '--slackKey', help='[Optional] Filepath for slack.key (slack webhooks, bot tokens and etc')
    args = parser.parse_args()

    # Tweak config
    args.strip = True if args.messageOnly else args.strip

    # Load SSH key
    if args.slackKey:
        print("Initializing with slackKey at", args.slackKey)
        try:
            slack = core.SlackTools_bot(filePath_slackKeys=args.slackKey, strip=args.strip)
        except:
            slack = core.SlackTools_webhook(filePath_slackKeys=args.slackKey, strip=args.strip)
    else:
        print("Initializing with default slackKey")
        try:
            slack = core.SlackTools_bot(strip=args.strip)
        except:
            slack = core.SlackTools_webhook(strip=args.strip)

    # Check for regex_events
    if args.regex_events:
        print("Will check for regex events(", args.regex_events, ")")

        # Check for users
        if not args.notify_users:
            args.notify_users = slack.keys['NOTIFY_ON_EVENT']
        print("Will notify users (", args.notify_users, ") on event")

        # Create notification string
        args.notify_str=""
        for user in args.notify_users:
            args.notify_str += slack.keys['USERS'][user]
        print(args.notify_str)

    # Print title
    print("-- START stdin pipe --\n")
    if args.title:
        print(f'{args.title}') 
        slack.sendMessage(args.title) 

    # Print stdin
    if not args.messageOnly and sys.stdin.isatty():
        for line in sys.stdin:
            if 'q' == line.rstrip():
                break

            # Echo to terminal
            print(f'{line}') 

            # Echo to Slack
            if not args.quiet:
                slack.sendMessage(line) 
            
            if args.regex_events:
                for regex in args.regex_events:
                    if re.search(regex, line):
                        print("Event! " + str(args.notify_users) + " Regex \"" + regex + "\" was triggered")
                        slack.sendMessage("Event! " + args.notify_str + " Regex \"" + regex + "\" was triggered: ") # Send to slack
                        slack.sendMessage(line) # Send to slack

    print("-- END stdin pipe --\n")