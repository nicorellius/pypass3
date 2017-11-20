# PyPass3
PyPass3 is a Python Flask web application offering dice roll optional, mostly-random word, number, and mixed character password and passphrase generator.

It also provides secure storage for your online secrets. Using [Argon2](https://github.com/P-H-C/phc-winner-argon2) for master password hashing and and AES encryption, Pypass3 stores all data encrypted in the database, in transit, and at rest.

@nicorellius | [nicorellius@gmail.com]()
 
## What does it do?
 
Make robust secrets with random characters, words, or numbers, using [Random.org's](https://www.random.org) system for mostly random strings and numbers.

Choose number of dice and how many times to roll to create passphrases of common words. Number of rolls determines how many words in your passphrase. Number of dice determine which [EFF word list](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) to use: long or short. Defaults to 5 dice and 5 rolls for words type.

Mixed and numbers type don't use dice, but instead use length. Defaults to 20. Longer passwords are better.
