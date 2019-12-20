
import re

RE_COMMENT = re.compile(r'^/\*.*\*/$')
RE_SECTION_START = re.compile(r'^(?P<section>.*) {$')


class VyOSConfigError(Exception):
    pass


class VyOSConfigSetting:
    """
    Base class for settings from VyOS configuration

    Implements the 'path' method to construct full setting name
    """

    def __init__(self, parent=None):
        self.parent = parent

    @property
    def path(self):
        path = []
        parent = self.parent
        while parent is not None:
            if parent.name is not None:
                path.append(parent.name)
            parent = parent.parent
        path.reverse()
        return ' '.join(path)


class VyOSConfigFlag(VyOSConfigSetting):
    """
    A configuration flag without value
    """

    def __init__(self, parent, flag):
        super().__init__(parent)
        self.flag = flag.strip()

    def __repr__(self):
        return ' '.join([self.path, self.flag])


class VyOSConfigItem(VyOSConfigSetting):
    """
    Configuration item with value
    """

    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key.strip()
        self.value = value

    def __repr__(self):
        return ' '.join([self.path, self.key, self.value])


class VyOSConfigSection(VyOSConfigSetting):
    """
    Configuration section in VyOS configuration
    """

    def __init__(self, name=None, parent=None):
        super().__init__(parent)
        self.name = name.rstrip(' {').strip() if name is not None else None
        self.items = []
        self.__iter_index__ = None
        if self.parent is not None:
            self.parent.items.append(self)

    def __repr__(self):
        return self.name if self.name is not None else ''

    def __iter__(self):
        return self

    def __next__(self):
        if self.items:
            if self.__iter_index__ is None:
                self.__iter_index__ = 0

            try:
                item = self.items[self.__iter_index__]
                if isinstance(item, VyOSConfigSection):
                    try:
                        return next(item)
                    except StopIteration:
                        self.__iter_index__ += 1
                        return next(self)
                else:
                    self.__iter_index__ += 1
                    return item
            except IndexError:
                self.__iter_index__ = None
                raise StopIteration
        else:
            # Silly cases in 'protocols' section
            if self.__iter_index__ is None:
                self.__iter_index__ = 0
                return '{} {}'.format(self.path, self.name)
            else:
                raise StopIteration


class VyOSConfig:
    """
    Parser for VyOS configuration
    """
    def __init__(self):
        self.lines = []
        self.__config__ = None
        self.__comment_lines__ = None

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__config__)

    def load(self, fd):
        self.lines = []
        self.__config__ = VyOSConfigSection()
        self.__comment_lines__ = []
        config_lines = []
        try:
            for line in [line.rstrip() for line in fd.readlines()]:
                self.lines.append(line)
                if line == '' or RE_COMMENT.match(line):
                    self.__comment_lines__.append(line)
                else:
                    config_lines.append(line)
        except Exception as e:
            raise VyOSConfigError('Error reading {}: {}'.format(fd, e))

        section = self.__config__
        for line in config_lines:
            m = RE_SECTION_START.match(line)
            if m:
                section = VyOSConfigSection(m.groupdict()['section'], section)
                if section.parent is None:
                    self.__config__.items.append(section)
            elif line.endswith('}'):
                section = section.parent
            else:
                try:
                    key, value = line.split(None, 1)
                    section.items.append(VyOSConfigItem(section, key, value))
                except ValueError:
                    section.items.append(VyOSConfigFlag(section, line))
                except Exception as e:
                    raise VyOSConfigError('Error parsing line {}: {}'.format(line, e))
