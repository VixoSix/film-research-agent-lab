class SourceRetrievalError(Exception):
    """Base error for source retrieval failures."""


class InvalidRetrievalInputError(SourceRetrievalError):
    """The retrieval request is invalid."""


class MissingCredentialsError(SourceRetrievalError):
    """The provider API key is missing or blank."""


class ProviderError(SourceRetrievalError):
    """The provider request failed."""

    def __init__(self, message: str, *, category: str = "provider"):
        super().__init__(message)
        self.category = category


class MalformedProviderResponseError(SourceRetrievalError):
    """The provider response does not match the expected envelope."""
