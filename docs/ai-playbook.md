# My AI Playbook

## When I reach for AI first

I use AI early when I need a checklist from a clear brief, a first draft of routine CI or Docker configuration, help narrowing a reproducible error, or a second set of eyes on a small diff. It is most useful when I can give it the relevant files, define what must not change, and verify the answer with a command or direct inspection.

## When I do not reach for AI first

I pause before using AI when the task includes secrets, personal data, unclear ownership, production access, or a high-impact change I do not yet understand. I also work through core learning exercises myself first; otherwise, I may get a plausible answer without learning how it works. If requirements conflict, I resolve the scope before asking for code.

## My non-negotiables

- Never paste credentials, tokens, `.env` contents, production logs, or real customer/personal data.
- Never merge a change I cannot explain line by line.
- Keep prompts and changes inside the agreed scope.
- Review the diff, run relevant tests, and check runtime claims against reality.
- Say when a check could not be completed; never turn a proposed command into claimed evidence.

## My review rules

I start with the actual file and surrounding context, then inspect the AI diff for unnecessary scope, silent behavior changes, broad permissions, and secret exposure. I run a focused check, the full test command, and any relevant endpoint or container check. I grade review findings as useful, noise, or wrong (and security findings as valid, false positive, or noise), recording the reason. I reject suggestions that conflict with requirements even when they sound like general best practice.

## What I am still figuring out

I am still learning when a small project benefits enough from fully locked dependencies, how teams should retain AI-review evidence without creating paperwork, and which security checks should be required before a demo becomes a deployed service.

## Decision Card

| Situation | My rule |
|---|---|
| New feature | Write acceptance criteria and scope first; ask AI only after I know what success means. |
| Code review | Ask for concrete, file-backed comments, then grade and verify each one. |
| Debugging | Reproduce first, share the minimum safe context, and test the proposed cause. |
| Infrastructure | Treat generated config as executable code; inspect defaults, users, permissions, inputs, and failure behavior. |
| Never paste | Secrets, tokens, `.env` values, production logs, or real personal/customer data. |
| One rule | If I cannot explain and verify it, I do not submit it. |
