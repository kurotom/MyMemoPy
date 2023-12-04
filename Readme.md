# MyMemory: API technical specifications

## Get

Searches MyMemory for matches against a segment.

Call example:

> https://api.mymemory.translated.net/get?q=Hello World!&langpair=en|it


|     |     |     |     |
| --- | --- | --- | --- |
| \*\*Parameter\*\* | \*\*Description\*\* | \*\*Type\*\* | \*\*Example value\*\* |
| q   | The sentence you want to translate. Use UTF-8. \*\*Max 500 bytes\*\* | Mandatory | Hello World! |
| langpair | Source and language pair, separated by the \| symbol. Use ISO standard names or RFC3066 | Mandatory | en\|it |
| mt  | Enables Machine Translation in results. You can turn it off if you want just human segments | Optional | 1 (default), 0 |
| key | Authenticates the request; matches from your private TM are returned too. \*\*Get your key \[here\](keygen.php) or use the keygen API\*\* | Optional |     |
| onlyprivate | If your request is authenticated, returns only matches from your private TM | Optional | 0 (default), 1 |
| ip  | The IP of the end user generating the request. \*\*Recommended for CAT tools and high volume usage\*\* Originating IP is always overridden by \_X-Forwarded-For\_ header, if the latter is set | Optional | 93.81.217.71 |
| de  | A valid email where we can reach you in case of troubles. \*\*Recommended for CAT tools and high volume usage\*\* | Optional | user@yourdomain.com |
| user | Authenticates the request; matches from your private TM are returned too | Optional, but needs the key parameter. Kept for backward compatibility only: now the \*\*key\*\* parameter alone is sufficient |     |

## Keygen

Generates the key associated with a username.

Call example:

**https://api.mymemory.translated.net/keygen?user=username&pass=password**

Parameter description:

|     |     |     |     |
| --- | --- | --- | --- |
| **Parameter** | **Description** | **Type** | **Example value** |
| user | The username whose key we want to generate | Mandatory |     |
| pass | The password associated with the username | Mandatory |     |




# MyMemory: API usage limits

## Get

Searches MyMemory for matches against a segment.

MyMemory tracks it usage in words. This means that it doesn't matter how many requests you submit to consult the archive, but the weight of each request.

> **Free, anonymous usage is limited to <u>5000 chars/day</u>.**

> **Provide a valid email ('de' parameter), where we can reach you in case of troubles, and enjoy <u>50000 chars/day</u>.**

Are you a CAT tool maker? Get whitelisted! Write us and get 150000 chars/day!*

If you are interested in even larger volumes, have a look at our RapidAPI plans!

Don't forget to check out carefully our Terms of Service, also.

* Note for developers:
Please bear in mind that we are eager to include in whitelisting program only estabilished projects of interest (have a look at "Most popular CAT tools" under CAT section, to get an idea of required market share).
Personal projects or "in development" stuff, projects that just use the "get" endpoint without contributing to MyMemory using the "set" endpoint, never qualify for the whitelisting.
Requests failing in complying with such minimum directive will be disregarded.


## Keygen

Generates the key associated with a username.

To prevent abuse, we keep track of call rate and enforce limits when necessary.


## Set

Contributes a translation unit (segment and translation) in some language pair to MyMemory.

This is never limited.

