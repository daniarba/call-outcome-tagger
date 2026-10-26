"""call-outcome-tagger: tag call transcripts with an outcome."""
from .models import Call, Outcome
from .tagger import tag

__all__ = ["Call", "Outcome", "tag"]
__version__ = "1.0.0"
