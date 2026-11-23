set positional-arguments

default:
    @just --list

# Show each active product skill and its source directory.
skills:
    @python3 scripts/product_skills.py list

# Verify the active relative links against their providers' Git trees.
skills-check:
    @python3 scripts/product_skills.py check

# Initialize the pinned product submodules on a fresh checkout.
skills-init:
    @python3 scripts/product_skills.py init

# List upstream skill paths that can be enabled.
skills-available package:
    @python3 scripts/product_skills.py available "$1"

# Expose a skill using its provider-relative directory.
skill-enable package path:
    @python3 scripts/product_skills.py enable "$1" "$2"

# Remove one managed link using its enabled skill name.
skill-disable package name:
    @python3 scripts/product_skills.py disable "$1" "$2"

# Fetch one provider's configured branch and check the active links before updating.
skills-update package:
    @python3 scripts/product_skills.py update "$1"
