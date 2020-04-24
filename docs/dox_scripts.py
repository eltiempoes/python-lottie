import os
import argparse
from importlib.machinery import SourceFileLoader

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doxpath = os.path.join(root, "docs", "dox")
doxfile = os.path.join(doxpath, "scripts.dox")
scriptpath = os.path.join(root, "bin")

os.makedirs(doxpath, exist_ok=True)


scripts = []

for scriptfilename in os.listdir(scriptpath):
    if scriptfilename.endswith(".py"):
        module = SourceFileLoader(
            os.path.splitext(scriptfilename)[0],
            os.path.join(scriptpath, scriptfilename)
        ).load_module()
        if hasattr(module, "parser"):
            scripts.append(module)


class DoxyHelpFormatter(argparse.HelpFormatter):
    class _Section(argparse.HelpFormatter._Section):
        def format_help(self):
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])

            # return nothing if the section was empty
            if not item_help:
                return ''

            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                heading = r"""
\subsubsection script_{name}_{id} {heading}

""".format(
                    name=script.__name__,
                    id=self.heading.lower().replace(" ", "_"),
                    heading=self.heading
)
            else:
                heading = ''

            # join the section-initial newline, the heading and the help
            return join(['\n', heading, item_help, '\n'])

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.sectioned = False

    def start_section(self, heading):
        self.sectioned = True
        return super().start_section(heading)

    def _indent(self):
        pass

    def _dedent(self):
        pass

    def _format_usage(self, usage, actions, groups, prefix):
        return r"""
\subsection script_{name}_usage Usage

\code{{.unparsed}}
{usage}
\endcode

\subsection script_{name}_options Options

""".format(
            name=script.__name__,
            usage=super()._format_usage(usage, actions, groups, "").strip(),
)

    def _metavar_formatter(self, action, default_metavar, doxyfy=False):
        wrapper = super()._metavar_formatter(action, default_metavar)

        if action.metavar is not None:
            result = action.metavar
        else:
            result = default_metavar

        if doxyfy:
            result = "@em @<%s@>" % result.lower()
        else:
            result = "<%s>" % result.lower()

        def format(tuple_size):
            return (result, ) * tuple_size
        return format

    def _format_args(self, action, default_metavar, doxyfy=False):
        get_metavar = self._metavar_formatter(action, default_metavar, doxyfy)
        if action.nargs is None:
            result = '%s' % get_metavar(1)
        elif action.nargs == argparse.OPTIONAL:
            result = '[%s]' % get_metavar(1)
        elif action.nargs == argparse.ZERO_OR_MORE:
            result = '[%s [%s ...]]' % get_metavar(2)
        elif action.nargs == argparse.ONE_OR_MORE:
            result = '%s [%s ...]' % get_metavar(2)
        elif action.nargs == argparse.REMAINDER:
            result = '...'
        elif action.nargs == argparse.PARSER:
            result = '%s ...' % get_metavar(1)
        else:
            formats = ['%s' for _ in range(action.nargs)]
            result = ' '.join(formats) % get_metavar(action.nargs)
        return result

    def _format_action_invocation(self, action, doxyfy=False):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default, doxyfy)(1)
            return metavar
        else:
            os = ", ".join(
                ("@p " if doxyfy else "") + option_string.replace("--", "\\--")
                for option_string in action.option_strings
            )
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default, doxyfy)

            os += " " + args_string

            if action.default is not None and action.default is not argparse.SUPPRESS:
                os += " =%s%s" % (
                    "@c " if doxyfy else "",
                    action.default
                )

            return os

    def _format_action(self, action):
        out = "@par "

        out += self._format_action_invocation(action, True) + "\n@parblock\n"

        if action.help:
            out += self._expand_help(action) + "\n\n"

        if action.choices:
            out += "@b Choices:\n"
            for c in action.choices:
                out += "@li @c %s\n" % c
            out += "\n"

        #for subaction in self._iter_indented_subactions(action):
            #parts.append(self._format_action(subaction))

        return out + "@endparblock \n\n"

    def add_text(self, text):
        if self.sectioned:
            return super().add_text(text)


with open(doxfile, "w") as outf:
    outf.write(r"""
/**
\page scripts Scripts
\brief Script files

|Script|Description|
|---|---|
""")

    for script in scripts:
        outf.write("| \\subpage script_%s | %s |\n" % (
            script.__name__,
            script.parser.description.strip().splitlines()[0]
        ))

    outf.write("\n\n")

    for script in scripts:
        parser = script.parser
        parser.prog = os.path.basename(script.__file__)
        parser.formatter_class = DoxyHelpFormatter
        outf.write(r"""
\page script_{name} {name}.py

\section script_{name}_brief {name}.py

{brief}

{help}
        """.format(
            name=script.__name__,
            brief=parser.description,
            help=parser.format_help(),
        ))

        outf.write("\n")

    outf.write("\n*/")
