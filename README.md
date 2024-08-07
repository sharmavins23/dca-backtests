# Dollar-Cost-Averaging Backtests

I've never played around with investing backtests, and as I was getting into
some investing principles, I felt it would be interesting to compare and
contrast a variety of investing strategies (month-to-month, for long-term
investing only!) with each other.

The sample scenario is simple: An investor receives $3,000 monthly and can
either invest in a particular (ETF) stock or hold it in a more liquid money
market fund (using historical federal reserve board data for interest rates). At
the end of the several-year run, which strategy gains the most net worth?

Gains are aggregated and tested on a variety of differing strategies. All prices
for buying and selling shares are based on the market's adjusted close value.

## Can I make one?

Sure! The structure is designed to spit out a graph for each individual strategy
added to the `strategies` folder. As such, simply add a strategy to the
`strategies` folder with the requisite format (see the other strategies for
examples).

Simply running `python main.py` will execute your strategy and compare it
alongside the others.

## Financial breakdown

A more comprehensive breakdown on the financial side of things is in the
`findocs.md` file.

# License TL;DR

This project is distributed under the MIT license. This is a paraphrasing of a
[short summary](https://tldrlegal.com/license/mit-license).

This license is a short, permissive software license. Basically, you can do
whatever you want with this software, as long as you include the original
copyright and license notice in any copy of this software/source.

## What you CAN do:

- You may commercially use this project in any way, and profit off it or the
  code included in any way;
- You may modify or make changes to this project in any way;
- You may distribute this project, the compiled code, or its source in any way;
- You may incorporate this work into something that has a more restrictive
  license in any way;
- And you may use the work for private use.

## What you CANNOT do:

- You may not hold me (the author) liable for anything that happens to this code
  as well as anything that this code accomplishes. The work is provided as-is.

## What you MUST do:

- You must include the copyright notice in all copies or substantial uses of the
  work;
- You must include the license notice in all copies or substantial uses of the
  work.

If you're feeling generous, give credit to me somewhere in your projects.
