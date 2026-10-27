class ImporterError(Exception):
    """Error esperado y presentable al usuario."""


class MarkdownParseError(ImporterError):
    pass


class ConfigurationError(ImporterError):
    pass


class TrelloAPIError(ImporterError):
    pass
