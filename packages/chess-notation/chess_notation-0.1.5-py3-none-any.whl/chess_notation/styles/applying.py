from pydantic import BaseModel
from .styles import Check, Mate, Castle, PawnCapture, PieceCapture
from .classify import is_castle, is_check, is_mate, is_pawn_capture, is_piece_capture
from .map import castle, check, mate, pawn_capture, piece_capture, CapturedPiece

class KingEffects(BaseModel):
  check: Check = 'NONE'
  mate: Mate = 'NONE'

class Motions(BaseModel):
  castle: Castle = 'O-O'
  pawn_capture: PawnCapture = 'dxe4'
  piece_capture: PieceCapture = 'Nxe4'

class Styles(KingEffects, Motions):
  ...

def apply_motions(san: str, motions: Motions, captured_piece: CapturedPiece = None) -> str:
  if is_pawn_capture(san):
    return pawn_capture(san, motions.pawn_capture, captured_piece)
  elif is_piece_capture(san):
    return piece_capture(san, motions.piece_capture, captured_piece)
  elif is_castle(san):
    return castle(san, motions.castle)
  else:
    return san
  
def apply_effects(san: str, effects: KingEffects) -> str:
  if is_check(san):
    return check(san, effects.check)
  elif is_mate(san):
    return mate(san, effects.mate)
  else:
    return san
  
def apply(san: str, styles: Styles, captured_piece: CapturedPiece = None) -> str:
  return apply_effects(apply_motions(san, styles, captured_piece), styles)