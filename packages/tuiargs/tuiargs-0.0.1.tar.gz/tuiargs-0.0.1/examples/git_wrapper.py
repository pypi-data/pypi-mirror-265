import tuiargs



################################################################################
## Menu layout
################################################################################

menu_structure = \
[
  {
    "type"        : "menu",
    "label"       : "Clone",
    "description" : """\
                    Clones a repository into a newly created directory, creates
                    remote-tracking branches for each branch in the cloned
                    repository (visible using git branch --remotes), and creates
                    and checks out an initial branch that is forked from the
                    cloned repository’s currently active branch.

                    After the clone, a plain git fetch without arguments will
                    update all the remote-tracking branches, and a git pull
                    without arguments will in addition merge the remote master
                    branch into the current master branch, if any (this is
                    untrue when "--single-branch" is given; see below).

                    This default configuration is achieved by creating
                    references to the remote branch heads under
                    refs/remotes/origin and by initializing remote.origin.url
                    and remote.origin.fetch configuration variables.
                    """,
    "trigger"     : "commit",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Local",
        "description" : """\
                        When the repository to clone from is on a local machine,
                        this flag bypasses the normal "Git aware" transport
                        mechanism and clones the repository by making a copy of
                        HEAD and everything under objects and refs directories.
                        The files under .git/objects/ directory are hardlinked
                        to save space when possible.

                        If the repository is specified as a local path (e.g.,
                        /path/to/repo), this is the default, and --local is
                        essentially a no-op. If the repository is specified as a
                        URL, then this flag is ignored (and we never use the
                        local optimizations). Specifying --no-local will
                        override the default when /path/to/repo is given, using
                        the regular Git transport instead.

                        If the repository’s $GIT_DIR/objects has symbolic links
                        or is a symbolic link, the clone will fail. This is a
                        security measure to prevent the unintentional copying of
                        files by dereferencing the symbolic links.

                        NOTE: this operation can race with concurrent
                        modification to the source repository, similar to
                        running cp -r src dst while modifying src.
                        """,
        "trigger"     : "--local",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Show progress",
        "description" : """\
                        Progress status is reported on the standard error stream
                        by default when it is attached to a terminal, unless
                        --quiet is specified. This flag forces progress status
                        even if the standard error stream is not directed to a
                        terminal.
                        """,
        "trigger"     : "--progress",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Reference repository",
        "description" : """\
                        If the reference repository is on the local machine,
                        automatically setup .git/objects/info/alternates to
                        obtain objects from the reference repository. Using an
                        already existing repository as an alternate will require
                        fewer objects to be copied from the repository being
                        cloned, reducing network and local storage costs. When
                        using the --reference-if-able, a non existing directory
                        is skipped with a warning instead of aborting the clone.
                        """,
        "trigger"     : "--reference",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Set the commit message",
        "description" : """\
                        Use the given <msg> as the commit message. If
                        multiple -, options are given, their values are
                        concatenated as separate paragraphs.
                        """,
        "trigger"     : "--message",
        "value"       : "",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : "",
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Commit",
    "description" : """\
                   Create a new commit containing the current contents of the
                   index and the given log message describing the changes. The
                   new commit is a direct child of HEAD, usually the tip of the
                   current branch, and the branch is updated to point to it
                    """,
    "trigger"     : "commit",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Stage all modified and deleted files",
        "description" : """\
                        Tell the command to automatically stage files that have
                        been modified and deleted, but new files you have not
                        told Git about are not affected.
                        """,
        "trigger"     : "--all",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Override the commit author",
        "description" : """\
                        Specify an explicit author using the standard A U Thor
                        <author@example.com> format. Otherwise <author> is
                        assumed to be a pattern and is used to search for an
                        existing commit by that author (i.e. rev-list --all -i
                        --author=<author>); the commit author is then copied
                        from the first such commit found.
                        """,
        "trigger"     : "--author",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Set the commit message",
        "description" : """\
                        Use the given <msg> as the commit message. If
                        multiple -, options are given, their values are
                        concatenated as separate paragraphs.
                        """,
        "trigger"     : "--message",
        "value"       : "",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : "",
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Diff",
    "description" : """\
                    Show changes between the working tree and the index or a
                    tree, changes between the index and a tree, changes between
                    two trees, changes resulting from a merge, changes between
                    two blob objects, or changes between two files on disk.
                    """,
    "trigger"     : "diff",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Indent heuristic",
        "description" : """\
                        Enable the heuristic that shifts diff hunk boundaries to
                        make patches easier to read.  This is the default.
                        """,
        "trigger"     : "--indent-heuristic",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Diff algorithm",
        "description" : """\
                        Choose a diff algorithm. The variants are as follows:

                        myers: The basic greedy diff algorithm.  Currently, this
                        is the default.

                        minimal: Spend extra time to make sure the smallest
                        possible diff is produced.

                        patience: Use "patience diff" algorithm when generating
                        patches.

                        histogram: This algorithm extends the patience algorithm
                        to "support low-occurrence common elements".
                        """,
        "trigger"     : "--diff-algorithm",
        "value"       : "myers",
      },
      {
        "type"        : "menu",
        "label"       : "Compare workdir to staging area",
        "description" : """\
                        This form is to view the changes you made relative to
                        the index (staging area for the next commit). In other
                        words, the differences are what you could tell Git to
                        further add to the index but you still haven’t. You can
                        stage these changes by using git-add(1).
                        """,
        "trigger"     : "",
        "value"       : [
          {
            "type"        : "positional argument",
            "label"       : "Path",
            "description" : """\
                            (Optional) If specified, the diff will only take the
                            provided path in consideration.
                            """,
            "trigger"     : "--",
            "value"       : "",
          },
          {
            "type"        : "endpoint",
            "label"       : "Run!",
            "description" : "",
            "trigger"     : "",
            "value"       : None,
           },
        ],
      },
      {
        "type"        : "menu",
        "label"       : "Compare staged changes to commit",
        "description" : """\
                        This form is to view the changes you staged for the next
                        commit relative to the named <commit>. Typically you
                        would want comparison with the latest commit, so if you
                        do not give <commit>, it defaults to HEAD. If HEAD does
                        not exist (e.g. unborn branches) and <commit> is not
                        given, it shows all staged changes.  --staged is a
                        synonym of --cached.
                        """,
        "trigger"     : "--cached",
        "value"       : [
          {
            "type"        : "positional argument",
            "label"       : "Commit",
            "description" : """\
                            Commit to compare to.
                            """,
            "trigger"     : "",
            "value"       : "HEAD",
          },
          {
            "type"        : "positional argument",
            "label"       : "Path",
            "description" : """\
                            (Optional) If specified, the diff will only take the
                            provided path in consideration.
                            """,
            "trigger"     : "--",
            "value"       : "",
          },
          {
            "type"        : "endpoint",
            "label"       : "Run!",
            "description" : "",
            "trigger"     : "",
            "value"       : None,
           },
        ],
      },
      {
        "type"        : "menu",
        "label"       : "Compare two folders on the filesystem",
        "description" : """\
                        This form is to compare the given two paths on the
                        filesystem.
                        """,
        "trigger"     : "--no-index",
        "value"       : [
          {
            "type"        : "positional argument",
            "label"       : "Path #1",
            "description" : """\
                            Path to the first folder to compare
                            """,
            "trigger"     : "--",
            "value"       : "",
          },
          {
            "type"        : "positional argument",
            "label"       : "Path #2",
            "description" : """\
                            Path to the second folder to compare
                            """,
            "trigger"     : "",
            "value"       : "",
          },
          {
            "type"        : "endpoint",
            "label"       : "Run!",
            "description" : "",
            "trigger"     : "",
            "value"       : None,
           },
        ],
      },
    ],
  },
]



################################################################################
## Auxiliary functions
################################################################################

log_messages = []

def log_print(x):
    global log_messages
    log_messages.append(x)



################################################################################
## Main()
################################################################################

tui = tuiargs.Build(
      menu_structure,
      dbg_print = log_print
)

exception = None

try:
    args = tui.run()
except Exception as e:
    exception = e

for x in log_messages:
    print("LOG: " + str(x))
print("")

if exception:
    raise exception

cmd = f"git {' '.join(args)}"
print(f"Running the following command: {cmd}")

# Here is where we would run the actual command:
#
# os.system(cmd)

