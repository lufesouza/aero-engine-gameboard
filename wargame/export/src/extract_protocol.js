// Pulls the round protocol constants (ORDER_FIELDS, TEAMS, schemas, CURRENT, OBJECTIVES) out of wargame/dashgame/workflows/exco_round.js without running it.
//   node extract_protocol.js <exco_round.js> <out.json>
const fs = require('fs')
const src = fs.readFileSync(process.argv[2], 'utf8')
const start = src.indexOf('const ORDER_FIELDS = ')
const stop = src.indexOf('const A = args || {}')
let body = src.slice(start, stop)
const objStart = src.indexOf('const OBJECTIVES = {')
const fn = new Function(body + '\nconst OBJ_PLACEHOLDER = 0\n' + 'return {ORDER_FIELDS, TEAMS, FRAME, testSchema, decideSchema, GUIDE, REVIEW, VETO}')
const x = fn()
// CURRENT and OBJECTIVES are defined after `const A`; extract their blocks separately
function grab(name, endMarker) {
  const i = src.indexOf('const ' + name + ' = ')
  const j = src.indexOf(endMarker, i)
  return new Function(src.slice(i, j) + '\nreturn ' + name)()
}
const CURRENT = grab('CURRENT', '\n\n')
let OBJECTIVES = (() => { const i = src.indexOf('const OBJECTIVES = {'); const j = src.indexOf('const objNote', i); return new Function(src.slice(i, j) + '\nreturn OBJECTIVES')() })()
const out = { ORDER_FIELDS: x.ORDER_FIELDS, TEAMS: x.TEAMS, schemas: { frame: x.FRAME, test: Object.fromEntries(Object.keys(x.ORDER_FIELDS).map(s => [s, x.testSchema(s)])), decide: Object.fromEntries(Object.keys(x.ORDER_FIELDS).map(s => [s, x.decideSchema(s)])), guidance: x.GUIDE, review: x.REVIEW, veto: x.VETO }, CURRENT, OBJECTIVES }
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1))
console.log('teams', Object.keys(out.TEAMS), 'current', Object.keys(CURRENT), 'objectives', Object.keys(OBJECTIVES))
