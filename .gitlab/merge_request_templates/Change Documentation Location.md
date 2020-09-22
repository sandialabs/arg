## What does this MR do?

Briefly describe what this MR is about

## Related issues

Mention the issue(s) this MR closes or is related to

## Moving docs to a new location?

- [ ] Make sure the old link is not removed and has its contents replaced with
      a link to the new location.
- [ ] Make sure internal links pointing to the document in question are not broken.
- [ ] Search and replace any links referring to old docs
- [ ] Make sure to add [`redirect_from`](https://docs.gitlab.com/ce/development/documentation/index.html#redirections-for-pages-with-disqus-comments)
      to the new document if there are any Disqus comments on the old document thread.
- [ ] Update the link in `features.yml` (if applicable)
- [ ] Ping one of the technical writers for review.

/label ~documentation