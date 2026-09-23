# Dependency updates

## Scope and timing

Routine dependency updates normally happen after a new `fcitx5-macos` release, in preparation for the following release.

When asked to perform a routine dependency update, update the top-level Git submodules for every dependency declared anywhere in `scripts/dependencies.py`. Treat all platform lists and dependency relationships in that file as one combined dependency set. Do not update unrelated submodules unless another rule in this file explicitly includes them.

## Version selection

Unless listed as an exception below, update each dependency to its newest stable tagged release. Do not select a prerelease, release candidate, beta, alpha, development snapshot, or an untagged branch commit as the latest stable release.

Update these closely related community-maintained dependencies to the latest commit on their upstream `master` branch instead of a release tag:

- `anthy-cmake`
- `cskk`
- `libmozc`
- `librime`
- Every top-level `librime-*` submodule except `librime-qjs`; this currently includes `librime-lua`, `librime-octagram`, and `librime-predict`
- `m17n-cmake`

Do not update these dependencies:

- `glog`
- `kyotocabinet`
- `libintl`
- `lua`
- `curl`

Update `openssl` to the newest stable `3.x.x` release. Do not move it to a release from another major version or to a prerelease.

## Version files

Some dependency versions are pinned in root-level dotfiles whose names end in `-version`, such as `.boost-version` and `.glib-version`. Update these version pins according to the same version-selection rules whenever their dependencies are part of the update. Do not update `.emscripten-version` during a dependency update.

## Patches and replacement files

Files under `patches/` are not all applied in the same way. Before validating or changing one, inspect the corresponding dependency script under `scripts/` and follow the exact application method used there. In particular, some files are applied with `git apply`, while others are copied over a file in the dependency source tree or installed as build inputs. Do not infer the application method from the filename extension.

After moving a submodule to its selected revision, validate every patch or replacement file used by that dependency against the updated, otherwise-clean source tree.

For a patch applied with `git apply`:

- Check whether the existing patch applies to the updated submodule, using `git apply --check` with the same working directory and patch path used by the build script.
- If the existing patch applies successfully, leave the patch file unchanged.
- If it does not apply, update the patch so that it preserves the existing intended change and applies cleanly to the new revision. Do not drop a patch merely because upstream code changed; first determine whether its behavior is still required.

For files applied by copying or by another mechanism, reproduce the mechanism used by the script and update the file only as needed to preserve its intended effect with the new dependency revision.

## Read-only upstream mirrors

The following submodules use `fcitx-contrib` read-only mirrors because their authoritative upstream repositories are hosted outside GitHub:

| Submodule | Authoritative upstream | fcitx-contrib mirror |
| --- | --- | --- |
| `default-icon-theme` | `https://gitlab.freedesktop.org/xdg/default-icon-theme.git` | `https://github.com/fcitx-contrib/default-icon-theme` |
| `iso-codes` | `https://salsa.debian.org/iso-codes-team/iso-codes` | `https://github.com/fcitx-contrib/iso-codes` |
| `libchewing` | `https://codeberg.org/chewing/libchewing` | `https://github.com/fcitx-contrib/libchewing` |
| `xkeyboard-config` | `https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config` | `https://github.com/fcitx-contrib/xkeyboard-config` |
| `m17n-db` | `https://git.savannah.nongnu.org/git/m17n/m17n-db` | `https://github.com/fcitx-contrib/m17n-db` |
| `m17n-lib` | `https://git.savannah.nongnu.org/git/m17n/m17n-lib` | `https://github.com/fcitx-contrib/m17n-lib` |

As part of every routine dependency update, fetch each authoritative upstream's default branch and tags, then push the updated default-branch commits and all new tags to the corresponding `fcitx-contrib` mirror. Treat the authoritative repository, not the possibly stale mirror, as the source of truth when deciding whether a new tag exists. Complete the mirror push before making any submodule point at a newly mirrored commit or tag. Use fast-forward updates and do not rewrite or delete mirror branches or tags without explicit user authorization.

If a new stable tag is available, update the corresponding dependency to that release under the normal version-selection, patch-validation, and verification rules in this file. The specialized `m17n-cmake` pull-request and pause procedure below takes precedence for `m17n-db` and `m17n-lib`.

Report the synchronized default-branch commit and all newly pushed tags for each mirror. If a mirror is already current, report that no push was needed.

## GLib update procedure

GLib has two distinct source revisions. Do not confuse them:

- The top-level `glib` gitlink in this repository must point to the exact commit tagged by GNOME as `<version>`. It must never point to the tip of an `fcitx-<version>` or `wasm-vips-<version>` branch.
- `.glib-version` must contain the same `<version>`. For a `js` build only, `scripts/glib.py` uses this file to fetch and check out `fcitx-<version>` from `https://github.com/fcitx-contrib/glib`.

Consequently, native builds start from the pristine GNOME tag and apply `patches/glib.patch`, while JavaScript builds switch to the fcitx-maintained branch and do not apply that patch.

### Build the fcitx GLib branch

For a selected new GLib version `<version>`:

1. Fetch the `<version>` tag from `https://github.com/GNOME/glib` and verify that it resolves to a commit.
2. Fetch `wasm-vips-<version>` from `https://github.com/kleisauke/glib`.
3. Create a new local `fcitx-<version>` branch whose initial commit is exactly the GNOME `<version>` tag commit. Do not base it on an older fcitx branch and do not base it on the tip of kleisauke's branch.
4. Inspect `git log --reverse <version>..kleisauke/wasm-vips-<version>`. From that new-version branch, cherry-pick the commits with the following subjects, individually and in exactly this order:

   1. `Do not build tools`
   2. `Disable NLS`
   3. “Emscripten doesn't implement `pthread_getname_np()`”
   4. `Network libs are not available on Emscripten`
   5. `Ensure separate checks are also done for Emscripten`
   6. `Use vsnpintf/snprintf/printf from musl libc`
   7. `Add support for WebAssembly`
   8. `Fix function pointer cast issues`

5. Never cherry-pick either of these kleisauke commits, even if they apply cleanly and even if they appear between commits in the required list:

   - `Remove GRegex pre-emptively`
   - `Emscripten doesn't always define __GCC_HAVE_SYNC_COMPARE_AND_SWAP_4`

   `Remove GRegex pre-emptively` is not suitable here because consumers in this project may require GRegex. Its presence on an fcitx branch is an error.

6. Do not automatically cherry-pick any other new kleisauke commit that is not in the required list. Report the additional commit and ask the user whether it should be included.
7. From the immediately preceding `fcitx-<old-version>` branch, cherry-pick or recreate these fcitx-maintained commits on top of the retained kleisauke commits, in exactly this order:

   1. `Disable atomic for single thread build`
   2. `Fix function pointer type touched by skk`

8. If a required commit subject is missing or appears more than once, compare its diff with the immediately preceding matching `wasm-vips-<old-version>` and `fcitx-<old-version>` branches. Do not substitute a similarly named commit without checking its diff and intent.
9. Verify the final series with `git log --reverse --format=%s <version>..fcitx-<version>`. It must contain the eight retained kleisauke commits followed by the two fcitx-maintained commits. It must not contain either forbidden commit.
10. Push `fcitx-<version>` to `https://github.com/fcitx-contrib/glib` and verify the remote tip. The GLib branch work is not complete until the remote branch exists at the verified commit. Do not force-push over an existing branch unless the user explicitly authorizes it.

Never use a range cherry-pick from an older `fcitx-*` branch. The corresponding new-version kleisauke branch may contain non-trivial adaptations that are absent from the older commits.

### Update this repository

After the fcitx branch is ready and pushed:

1. Check out the GNOME `<version>` tag commit in the `glib` submodule in detached-HEAD state. Do not leave the submodule at `fcitx-<version>`.
2. Set `.glib-version` to `<version>`.
3. Against the clean GNOME tag checkout, run `git -C glib apply --check ../patches/glib.patch`. If it succeeds, leave `patches/glib.patch` byte-for-byte unchanged. If it fails, update the patch according to the patch rules above and repeat the check.
4. Confirm that the top-level gitlink resolves to the GNOME tag commit and that it differs from the remote `fcitx-<version>` tip.
5. Stage `.glib-version`, the `glib` gitlink, and `patches/glib.patch` only if the patch actually changed.

After pushing, report the GNOME tag and commit used for the top-level gitlink, the pushed fcitx branch and final commit, the eight retained kleisauke commits, the two explicitly omitted commits, and the two fcitx-maintained commits. Include the remote branch URL and disclose every conflict resolution or adaptation.

## m17n-cmake update procedure

`m17n-cmake` and the `fcitx-contrib` mirrors used by its two nested submodules are maintained by the fcitx project. Treat the nested submodules as follows:

| Submodule | Authoritative upstream | fcitx-contrib mirror |
| --- | --- | --- |
| `m17n-db` | `https://git.savannah.nongnu.org/git/m17n/m17n-db` | `https://github.com/fcitx-contrib/m17n-db` |
| `m17n-lib` | `https://git.savannah.nongnu.org/git/m17n/m17n-lib` | `https://github.com/fcitx-contrib/m17n-lib` |

### Ordering and mandatory pause

Handle all `m17n-cmake` maintenance before updating any other dependency in this repository. This includes checking and synchronizing both nested submodule mirrors, processing any new nested-submodule release tags, and checking the glibc release asset described below.

If this work creates a pull request in `fcitx-contrib/m17n-cmake`, finish the required branch push and any required `prebuild` workflow dispatch, report the pull request to the user, and stop the entire dependency-update task. Do not merge the pull request and do not continue with GLib or any other dependency while waiting. Resume only after the user explicitly says that the pull request has been merged.

After the user confirms the merge, switch the local `m17n-cmake` submodule to `master`, pull the updated `origin/master` with a fast-forward-only pull, and update its nested submodule worktrees to the commits recorded by the merged `master`. Verify that the expected pull-request changes are present, then update this repository's `m17n-cmake` gitlink to that `master` commit and continue with the remaining dependencies. If no `m17n-cmake` pull request was needed, continue without pausing.

For each nested repository, fetch the authoritative upstream's current commit history and tags and push the upstream default branch commits and all new upstream tags to the corresponding `fcitx-contrib` mirror. Complete this mirror synchronization before updating a gitlink in `m17n-cmake`, so every referenced commit is already available from the URL recorded in `m17n-cmake/.gitmodules`. Do not rewrite or delete existing mirror branches or tags unless the user explicitly authorizes it.

When either authoritative upstream publishes a new tagged release:

1. Synchronize that repository's commits and tags to its `fcitx-contrib` mirror.
2. Create a new `dev` branch in `fcitx-contrib/m17n-cmake` from the current `master` branch.
3. On `dev`, update each affected nested submodule gitlink to the selected release tag commit from its fcitx-contrib mirror. If both upstream projects have new releases, update both in the same branch when appropriate.
4. Validate any affected patch according to the patch rules above. In particular, `m17n-lib` uses `m17n-cmake/patches/m17n-lib.patch` through `git apply` in both the build script and CI.
5. Commit and push `dev`, then create a pull request from `dev` to `master` in `fcitx-contrib/m17n-cmake`. Do not update the `m17n-cmake` gitlink in this prebuilder repository to an unmerged PR commit unless the user explicitly requests it.
6. If the pull request updates `m17n-db`, manually dispatch the `prebuild` workflow (`.github/workflows/prebuild.yml`) on the PR's `dev` branch. Monitor the dispatched run and include its result and URL in the report.

Report the upstream and mirror commit IDs, every synchronized tag, the `m17n-cmake` `dev` commit, and the pull request URL. For an `m17n-db` update, also report the `prebuild` workflow run URL and final status. Disclose any non-fast-forward condition, tag mismatch, patch adaptation, or workflow failure instead of silently forcing or bypassing it.

### glibc release assets

During an `m17n-cmake` update, compare the version in `m17n-cmake/.glibc-version` with the newest stable glibc release. If a newer version exists, prepare the GitHub release asset before changing `.glibc-version`, because `.github/workflows/prebuild.yml` downloads that asset using the version file.

1. Download the matching `glibc-<new-version>.tar.xz` source archive from `https://ftp.gnu.org/gnu/glibc/`. Use the exact upstream `.xz` archive without repacking or modifying it, and verify that the download completed successfully and is a valid xz archive.
2. In `fcitx-contrib/m17n-cmake`, create a GitHub release whose tag and release title are both `glibc-<new-version>`, targeting the current `master` commit. Upload `glibc-<new-version>.tar.xz` as a release asset. Do not move or overwrite an existing release or tag without explicit user authorization.
3. Verify that the asset is accessible at the URL shape used by the workflow: `https://github.com/fcitx-contrib/m17n-cmake/releases/download/glibc-<new-version>/glibc-<new-version>.tar.xz`.
4. Create or update the `dev` pull-request branch and change `.glibc-version` to `<new-version>`. This change may be included in the same pull request as nested `m17n-db` or `m17n-lib` updates; it does not require a separate pull request.

Report the old and new glibc versions, the authoritative download URL, the GitHub release URL and target commit, the uploaded asset name, and the pull request containing the `.glibc-version` change.

## Change boundaries

Limit changes to the relevant top-level submodule gitlinks, applicable root-level version files, and patch or replacement files that actually require adjustment. Preserve unrelated working-tree changes, and do not reformat or otherwise modify dependency source trees as part of a version-only update.

## Staging for review

Before reporting completion or a mandatory pause, stage every file and top-level submodule gitlink changed in this repository as part of the dependency-update task so the user can review the complete result with `git diff --cached`. Use explicit paths when staging. Do not use a broad command such as `git add -A`, and do not stage unrelated pre-existing modifications or untracked files. Check both `git status --short` and the staged diff before reporting, and clearly distinguish staged task changes from any unrelated changes that remain unstaged.
