# yq Recipes

## Read value

```bash
yq eval '.path.to.value' file.yml
```

## Set value in place

```bash
yq eval --inplace '.path.to.value = "new"' file.yml
```

## Append to array

```bash
yq eval --inplace '.items += ["new-item"]' file.yml
```

## Delete field

```bash
yq eval --inplace 'del(.obsolete.field)' file.yml
```

## Multi-file patterns

Merge overlays deterministically:

```bash
yq eval-all --inplace 'select(fileIndex == 0) * select(fileIndex == 1)' base.yml overlay.yml
```

## Verification routine

1. Query before edit.
2. Edit in place.
3. Query after edit.
4. Run domain validator (for example `kubectl apply --dry-run=client -f` where appropriate).

## Pitfalls

- Path typos silently creating wrong branches.
- Treating scalars and arrays interchangeably.
- Overwriting rather than merging nested maps.
