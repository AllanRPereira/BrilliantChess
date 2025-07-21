export const DADOS_ANALISADOS_MOCK = {
  id: 1,
  nome: 'Teste de Análise: Gambito da Dama',
  pgn: '1. d4 d5 2. c4 dxc4 3. e3?? b5!',
  
  // ADICIONE ESTA LINHA:
  fenInicial: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',

  analyzedMoves: [
    { san: 'd4', evalAfter: 35, classification: 'best' },
    { san: 'd5', evalAfter: 32, classification: 'best' },
    { san: 'e3??', evalAfter: -150, classification: 'blunder' },
    { san: 'b5!', evalAfter: -160, classification: 'best' },
  ]
};