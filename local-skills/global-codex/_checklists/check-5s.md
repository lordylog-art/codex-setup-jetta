# CHECK 5s

Run this in 5 seconds before doing anything.

1. **Is it simple?** → If yes, resolve directly. No skill, no long prompt.
2. **Needs large context?** → If no, don't load it. Only impacted files.
3. **Is it critical?** → If yes, upgrade to full review + checklists.
4. **Can it be broken smaller?** → If yes, break it. Do the smallest slice first.
5. **Needs a plan?** → If no, skip straight to code/patch.
6. **Is a patch enough?** → If yes, return only the changed snippet. No full file.
7. **Does review need to be full?** → If no, use quick checklist instead of full review.

> If 1=yes and 2,3,5=no: resolve locally without spending tokens.
